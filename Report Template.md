\# \[Report Template]



\## Group Info



|   | Student Name | UID |

| - | ------------ | --- |

| 1. |              |     |

| 2. |              |     |

| 3. |              |     |



\## ALGOGENE System Info



| User ID         |     |

| --------------- | --- |

| Backtest ID     |     |

| Strategy Script | \[Example]<br><br>from AlgoAPI import AlgoAPIUtil, AlgoAPI\_Backtest<br><br>class AlgoEvent:<br><br>def \\\_\\\_init\\\_\\\_(self):<br><br>pass<br><br>def start(self, mEvt):<br><br>self.evt = AlgoAPI\_Backtest.AlgoEvtHandler(self, mEvt)<br><br>self.evt.start()<br><br>def on\_bulkdatafeed(self, isSync, bd, ab):<br><br>pass<br><br>def on\_marketdatafeed(self, md, ab):<br><br>pass<br><br>def on\_orderfeed(self, of):<br><br>pass<br><br>def on\_dailyPLfeed(self, pl):<br><br>pass<br><br>def on\_openPositionfeed(self, op, oo, uo):<br><br>pass |



\---



\## Executive Summary (15 points)



High level description of your trading idea. Any trading philosophy/hypothesis behind your strategy? What financial market/instruments your strategy apply to? What kind of data/inputs does your strategy use?



\## Implementation Details (20 points)



What are the exact trading logics? What conditions will trigger trades? How do you derive the trading model/logic? What theories/methodologies have you applied? Any assumptions made?



\## Risk Management (20 points)



What are the risk factors? What is the worst scenario? How do you manage the risks?



\## Capital Management (15 points)



Does your strategy utilize the investment capital? How do you manage the funding liquidity? What is the minimum capital to execute your strategy? Is your strategy scalable? Can your strategy still work if the investment size becomes very large?



\## Backtest Performance (20 points)



Is your PnL consistent over time? Any economic or fundamental reasons behind a good/bad performance period? What key metric do you base to compare/optimize your strategy? Present your results using equity chart, drawdown chart, monthly return breakdown, and so on, would be helpful to visualize the results.



\## Expectations for real trading (10 points)



What market situations would be (un)favorable to your strategy? Can your strategy fully automate for different market scenarios? How frequent does your strategy trade? What is an ideal investment size to execute your strategy? Does your strategy require leverage? Is your assumption realistic (eg. trading cost, leverage, any brokers in the market can support, etc)? Any potential issues for real trading?

