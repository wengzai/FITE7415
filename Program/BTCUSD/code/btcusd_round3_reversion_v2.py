from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest
from AlgoAPI.AlgoAPIUtil import getHistoricalBar
from datetime import datetime
import pandas as pd


class AlgoEvent:
    def __init__(self):
        self.symbol = "BTCUSD"
        self.rsi_period = 2
        self.rsi_entry_threshold = 20
        self.sma_period = 20
        self.pullback_pct = 0.01
        self.atr_period = 14
        self.stop_atr_multiple = 1.5
        self.take_profit_atr_multiple = 2.5
        self.max_hold_days = 7
        self.risk_per_trade = 0.01
        self.initial_capital = 10000.0
        self.min_volume = 0.01
        self.volume_step = 0.01
        self.last_bar_day = None
        self.has_position = False

    def start(self, mEvt):
        self.evt = AlgoAPI_Backtest.AlgoEvtHandler(self, mEvt)
        self.evt.start()

    def on_marketdatafeed(self, md, ab):
        if getattr(md, "instrument", None) != self.symbol:
            return

        bar_time = self._extract_time(md)
        if bar_time is None:
            return

        bar_day = bar_time.strftime("%Y-%m-%d")
        if bar_day == self.last_bar_day:
            return
        self.last_bar_day = bar_day

        if self.has_position:
            return

        count = self.sma_period + self.atr_period + 60
        bars = getHistoricalBar(
            {"instrument": self.symbol},
            count,
            "D",
            bar_day,
        )
        if not bars or len(bars) < count // 2:
            return

        df = pd.DataFrame(list(bars.values()))
        if df.empty or "t" not in df or "c" not in df or "h" not in df or "l" not in df:
            return

        df["t"] = pd.to_datetime(df["t"])
        df = df.sort_values("t").reset_index(drop=True)

        close = pd.to_numeric(df["c"], errors="coerce")
        high = pd.to_numeric(df["h"], errors="coerce")
        low = pd.to_numeric(df["l"], errors="coerce")
        if close.isna().any() or high.isna().any() or low.isna().any():
            return

        sma20 = close.rolling(self.sma_period).mean()
        rsi2 = self._rsi(close, self.rsi_period)
        atr = self._atr(high, low, close, self.atr_period)

        if pd.isna(sma20.iloc[-1]) or pd.isna(rsi2.iloc[-1]) or pd.isna(atr.iloc[-1]):
            return

        latest_close = float(close.iloc[-1])
        latest_sma20 = float(sma20.iloc[-1])
        latest_rsi2 = float(rsi2.iloc[-1])
        latest_atr = float(atr.iloc[-1])

        pullback_level = latest_sma20 * (1.0 - self.pullback_pct)
        if latest_close > pullback_level:
            return
        if latest_rsi2 > self.rsi_entry_threshold:
            return

        stop_loss = latest_close - self.stop_atr_multiple * latest_atr
        take_profit = latest_close + self.take_profit_atr_multiple * latest_atr
        if stop_loss >= latest_close or take_profit <= latest_close:
            return

        volume = self._calc_volume(latest_close, stop_loss)
        if volume < self.min_volume:
            return

        order = AlgoAPIUtil.OrderObject(
            instrument=self.symbol,
            openclose="open",
            buysell=1,
            ordertype=0,
            volume=volume,
            stopLossLevel=round(stop_loss, 2),
            takeProfitLevel=round(take_profit, 2),
            holdtime=self.max_hold_days * 24 * 60 * 60,
        )
        self.evt.sendOrder(order)

    def on_openPositionfeed(self, op, oo, uo):
        try:
            self.has_position = len(op) > 0
        except Exception:
            self.has_position = False

    def on_orderfeed(self, of):
        pass

    def on_dailyPLfeed(self, pl):
        pass

    def on_bulkdatafeed(self, isSync, bd, ab):
        pass

    def _atr(self, high, low, close, period):
        prev_close = close.shift(1)
        tr = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        return tr.rolling(period).mean()

    def _rsi(self, close, period):
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / avg_loss.replace(0, pd.NA)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(100)

    def _calc_volume(self, entry_price, stop_loss):
        risk_amount = self.initial_capital * self.risk_per_trade
        stop_distance = max(entry_price - stop_loss, 0.01)
        raw_volume = risk_amount / stop_distance
        stepped_volume = int(raw_volume / self.volume_step) * self.volume_step
        return round(max(stepped_volume, self.min_volume), 2)

    def _extract_time(self, md):
        for attr in ["timestamp", "datetime", "dateTime", "t", "time"]:
            value = getattr(md, attr, None)
            if value is None:
                continue
            try:
                return pd.to_datetime(value).to_pydatetime()
            except Exception:
                continue
        return datetime.utcnow()
