from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest
from AlgoAPI.AlgoAPIUtil import getHistoricalBar
from datetime import datetime
import pandas as pd


class AlgoEvent:
    def __init__(self):
        self.symbol = "XAUUSD"
        self.sma_period = 20
        self.trend_period = 80
        self.std_period = 20
        self.z_entry = -1.0
        self.atr_period = 14
        self.stop_atr_multiple = 1.2
        self.take_profit_atr_multiple = 2.5
        self.max_hold_days = 5
        self.risk_per_trade = 0.005
        self.initial_capital = 10000.0
        self.contract_size = 100.0
        self.min_volume = 0.01
        self.volume_step = 0.01
        self.last_bar_day = None
        self.last_entry_day = None

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

        if self.last_entry_day is not None:
            days_since_entry = (bar_time.date() - self.last_entry_day).days
            if days_since_entry < self.max_hold_days:
                return

        count = max(self.sma_period, self.std_period, self.trend_period) + self.atr_period + 60
        bars = getHistoricalBar({"instrument": self.symbol}, count, "D", bar_day)
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

        sma = close.rolling(self.sma_period).mean()
        std = close.rolling(self.std_period).std()
        atr = self._atr(high, low, close, self.atr_period)
        if pd.isna(sma.iloc[-1]) or pd.isna(std.iloc[-1]) or pd.isna(atr.iloc[-1]):
            return

        latest_close = float(close.iloc[-1])
        latest_sma = float(sma.iloc[-1])
        latest_std = float(std.iloc[-1])
        latest_atr = float(atr.iloc[-1])
        if latest_std <= 0:
            return

        zscore = (latest_close - latest_sma) / latest_std
        if zscore > self.z_entry:
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
        self.last_entry_day = bar_time.date()

    def on_openPositionfeed(self, op, oo, uo):
        pass

    def on_orderfeed(self, of):
        pass

    def on_dailyPLfeed(self, pl):
        pass

    def on_bulkdatafeed(self, isSync, bd, ab):
        pass

    def _atr(self, high, low, close, period):
        prev_close = close.shift(1)
        tr = pd.concat([
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def _calc_volume(self, entry_price, stop_loss):
        risk_amount = self.initial_capital * self.risk_per_trade
        stop_distance = max(entry_price - stop_loss, 0.01)
        risk_per_lot = stop_distance * self.contract_size
        if risk_per_lot <= 0:
            return 0

        raw_volume = risk_amount / risk_per_lot
        max_affordable_volume = self.initial_capital / max(entry_price * self.contract_size, 0.01)
        capped_volume = min(raw_volume, max_affordable_volume)
        stepped_volume = int(capped_volume / self.volume_step) * self.volume_step
        return round(max(stepped_volume, 0), 2)

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
