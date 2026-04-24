from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest
from AlgoAPI.AlgoAPIUtil import getHistoricalBar
from datetime import datetime
import pandas as pd


class AlgoEvent:
    def __init__(self):
        self.symbol = "BTCUSD"
        self.breakout_lookback = 20
        self.ema_fast_period = 50
        self.ema_slow_period = 200
        self.atr_period = 14
        self.stop_atr_multiple = 2.0
        self.take_profit_atr_multiple = 4.0
        self.max_hold_days = 15
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

        count = self.ema_slow_period + self.breakout_lookback + self.atr_period + 5
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

        ema_fast = close.ewm(span=self.ema_fast_period, adjust=False).mean()
        ema_slow = close.ewm(span=self.ema_slow_period, adjust=False).mean()
        atr = self._atr(high, low, close, self.atr_period)
        if len(df) < self.breakout_lookback + 2 or pd.isna(atr.iloc[-1]):
            return

        breakout_level = high.iloc[-(self.breakout_lookback + 1):-1].max()
        latest_close = float(close.iloc[-1])
        latest_atr = float(atr.iloc[-1])
        latest_ema_fast = float(ema_fast.iloc[-1])
        latest_ema_slow = float(ema_slow.iloc[-1])

        if latest_close <= breakout_level:
            return
        if latest_ema_fast <= latest_ema_slow:
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