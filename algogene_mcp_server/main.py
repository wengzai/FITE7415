from typing import Annotated, List, Dict, Any
import asyncio, sys, requests, logging, argparse
from mcp.server.fastmcp import FastMCP


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)



mcp = FastMCP(
    name="algogene_tools",
    instructions="""
    This server provides secure access to ALGOGENE functionality following MCP best practices.

    AVAILABLE TOOLS:
    
    Contract Specification:
    - get_instruments: Get all available instruments available on ALGOGENE
    - get_instrument_meta: Get contract specification of a financial instrument
    - search_instrument: Search related financial instruments based on matched keywords of symbol or description
    - list_econs_series: List out all available economic time series
    - search_econs_series: Search related economic time series based on matched keywords of titles, geo and freq
    - get_econs_series_meta: Get meta data or specification of an economic time series

    Real-time Data:
    - get_realtime_prices: Get current price for trading symbol(s)
    - get_realtime_price_24hrchange: Get the recent 24 hours market price change
    - get_realtime_exchange_rate: Get current exchange rate between 2 currencies
    - get_realtime_news: Get latest news for a specified language/source/categroy
    - get_realtime_weather: Get latest weather info for a specified region
    - get_realtime_econs_calendar: Get the upcoming economic calendar info such as holiday, statistics release, president speech, etc
    - get_realtime_econs_stat: Get the most recent released economic statistics

    Historical Data:
    - get_history_price: Get historical market price
    - get_history_news: Get historical news
    - get_history_weather: Get historical weather
    - get_history_corp_announcement: Get company's corporate announcement history
    - get_history_econs_calendar: Get economic calendar history, such as holiday, statistics release, president speech, etc
    - get_history_econs_stat: Get historical released economic statistics
    - strategy_market_perf: Get performance statistics for a market index 

    Trading Account Current Status:
    - get_session: Get session token that will be used to access account and order related resources
    - list_accounts: List out all your trading accounts with latest balance on ALGOGENE.
    - get_positions: Get outstanding positions of a trading account
    - get_balance: Get current balance of a trading account
    - get_opened_trades: Get opened trades of a trading account
    - get_pending_trades: Get pending trades (or limit orders) of a trading account
    - set_account_config: Trading connection setup with your personal broker/exchange account on ALGOGENE.

    Trading Account History: 
    - strategy_trade: Get transaction history of a trading account
    - strategy_bal: Get daily history of account balance of a trading account
    - strategy_pos: Get daily history of position of a trading account
    - strategy_pl: Get daily history of cumulative profit/loss of a trading account
    - strategy_cashflow: Get history of cash flow (eg. deposit, withdrawal, dividend payment, etc) of a trading account
    - strategy_stats: Get performance statistics history and trading setting of a trading account
    - stratey_logs: Get system logs for running backtest or live algo script

    Order Placecment and Management: 
    - open_order: Place an order on a trading account
    - query_order: Query an order's details of a trading account
    - update_pending_order: Update trading parameters of a pending order
    - update_opened_order: Update trading parameters of an outstanding/opened order
    - cancel_orders: cancel a list of unfilled limit/stop orders
    - close_orders: close a list of outstanding orders

    Strategy Development:
    - backtest_run: Submit a strategy script to run on ALGOGENE cloud platform
    - backtest_cancel: Cancel a running backtest task
    - get_task_status: Query the current status of a task on ALGOGENE (eg. backtest) 

    Other Trading Apps available on (https://algogene.com/marketplace#app): 
    - app_predict_sentiment: Give a sentiment score for a given text (eg. news, blog posts, financial reports)
    - app_asset_allocation: Calculate an optimal portfolio based on given risk tolerance level.
    - app_portfolio_optimizer: Calculate an optimal portfolio based on dynamic objectives and conditions, such as target return, risk tolerance, group constraints, etc
    - app_portfolio_optimizer_custom: Similar to 'app_portfolio_optimizer' to calculate an optimal portfolio based on given time series data
    - app_fourier_prediction: Estimate the future range (i.e. upper and lower bound) of a financial instrument based on Fourier analysis and transformation. 
    - app_market_classifer: Calculate the bull-bear line and classify the market condition of a given financial instrument
    - app_us_company_filing_hitory: Get the filing history's report URL from US SEC for a given ticker
    - app_us_company_financials: Get company financial data for a given US stock 
    - app_stock_tagger: Identify related stocks for a given news
    - app_index_composite: Get the index constituent data including the composited stocks, current weighting and sensitivity
    - app_pattern_recoginer: Identify key technical pattern for a given financial instrument and time frame
    - app_risk_analysis: Analyze potential market risk for a given portfolio holding
    - app_trading_pair_aligner: Identify the most suitable instrument within the same asset class that can form a trading pair based on a given instrument
    - app_price_simulator: Generate a financial time series based on correlation of another given time series
    - app_capitalflow_hkex_szse: Get capital flow historical data between Hong Kong Stock Exchange (HKEx) and Shenzhen Stock Exchange (SZSE) 
    - app_capitalflow_hkex_sse: Get capital flow historical data between Hong Kong Stock Exchange (HKEx) and Shanghai Stock Exchange (SSE)
    - app_performance_calculator: Calculate investment performance statistics based on given NAV time series
    - app_algo_generator: Generate a backtest script of trading algorithm according to user's trading ideas or description

    """
)



@mcp.tool()
def get_realtime_prices(
    symbols: List[str],
    broker: str = ""
) -> Dict[str, Any]:
    """
    Get the current price for trading symbol(s) on ALGOGENE.
    
    This function fetches real-time price data for any valid trading instrument available on ALGOGENE.
    
    Args:
        symbol: Trading instrument in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC')
            Must be a valid symbol listed on ALGOGENE.
        broker: the data source from a specific broker/exchange (eg. 'alpaca','binance','bybit','bitget','ib','ig','kucoin','oanda','okx'). If broker is an empty string, result will be the latest price regardless of brokers
        
    Returns:
        Dict containing:
        - count (integer): number of record
        - res (dict): Response data containing each symbol
            - for each symbol (dic): Response data containing timestamp, bidPrice, askPrice, bidSize, askSize, bidOrderBook, askOrderBook
            - timestamp (str): time zone in UTC+0 in the format of YYYY-MM-DD HH:MM:SS.FFFFFF
            - bidPrice (float): bid price
            - askPrice (float): ask price
            - bidSize (float): bid size
            - askSize (float): ask size
            - bidOrderBook (list): bid order book cpmtaining a list of (price, size)
            - askOrderBook (list): ask order book cpmtaining a list of (price, size)
        
    Examples:
        result = get_realtime_prices(["BTCUSD","AAPL"])  # Bitcoin and Apple price
        for symbol in result:
            bidPrice = result[symbol]["bidPrice"]
            askPrice = result[symbol]["askPrice"]
            print(f"$(symbol) bid price: ${bidPrice}")
            print(f"$(symbol) ask price: ${askPrice}")
    """
    try:
        from tools import get_realtime_prices as _get_realtime_prices
        return _get_realtime_prices.get_realtime_prices(symbols, broker)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_prices tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_realtime_price_24hrchange(
    symbols: List[str]
) -> Dict[str, Any]:
    """
    Get the recent 24-hour market price change on ALGOGENE.

    This function retrieves the market price changes for specified financial instruments over the last 24 hours. 

    Args:
        symbols (list): a list of up to 10 financial symbols available on ALGOGENE (eg, "BTCUSD","ETHUSD").

    Returns:
        Dict containing:
        - count (int): The total number of instruments returned.
        - res (List[Dict]): Array of objects containing the following details for each instrument:
            - instrument (str): The name of the financial instrument.
            - current_price (float): The current market price.
            - lastday_price (float): The market price recorded 24 hours ago.
            - change (float): The absolute price change over the last 24 hours.
            - change_pct (float): The percentage change over the last 24 hours.

    Examples:
        result = get_realtime_price_24hrchange(, symbols="BTCUSD,XAUUSD")
        print(f"Total instruments: {result['count']}")
        for item in result['res']:
            print(f"{item['instrument']} - Current Price: {item['current_price']}, Change: {item['change']}, Change Percentage: {item['change_pct']}")
    """
    try:
        from tools import get_realtime_price_24hrchange as _get_realtime_price_24hrchange
        return _get_realtime_price_24hrchange.get_realtime_price_24hrchange(symbols)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_price_24hrchange tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"




@mcp.tool()
def get_realtime_exchange_rate(
    cur1: str,
    cur2: str
) -> Dict[str, float]:
    """
    Get the current exchange rate on ALGOGENE.
    
    This function fetches real-time exchange rate data available on ALGOGENE.
    
    Args:
        cur1: the currency exchange from
        cur2: the currency exchange to
        
    Returns:
        Dict containing:
        - res (float): Response data containing the value of exchange rate
        
    Examples:
        result = get_realtime_exchange_rate("EUR","USD")  # exchange rate to convert 1 EUR to USD
        print(f"Exchange rate: ${result['res']}")
    """
    try:
        from tools import get_realtime_exchange_rate as _get_realtime_exchange_rate
        return _get_realtime_exchange_rate.get_realtime_exchange_rate(cur1, cur2)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_exchange_rate tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def get_realtime_news(
    lang: str,
    category: str = "",
    source: str = ""
) -> Dict[str, Any]:
    """
    Get the latest news for specific topic/source on ALGOGENE.
    
    This function fetches latest news data for any news sources available on ALGOGENE.
    
    Args:
        lang: language of News to retrieve, language codes follows [ISO 639-1 codes], available values include ‘af','ar','bg','bn','ca','cs','cy','da','de','el','en','es','et','fa','fi','fr','gu','he','hi','hr','hu','id','it','ja','kn','ko ','lt','lv','mk','ml','mr','ne','nl','no','pa','pl','pt','ro','ru','sk','sl','so','sq','sv','sw','ta','te','th','tl','tr','uk',' ur','vi','zh-cn','zh-tw'
        category (optional): Avaiable values include 'AFRICA', 'AGRICULTURE', 'AMERICAS', 'ART', 'ASIA', 'ASSET_SALES', 'AUSTRALIA', 'AUTO', 'BIOTECH', 'BOND', 'BOOK', 'BOTsWANA', 'BUSINESS', 'BUYBACK', 'CANADA', 'CENTRAL_ASIA', 'CHINA', 'COMMENTARY', 'COMMODITY', 'COMMUNITY', 'COMPANY', 'COMPANY NEWS', 'CONTRACT', 'CULTURE', 'DIPLOMACY', 'DIVIDENDS', 'EARNINGS', 'EAST_ASIA', 'ECONOMY', 'EDUCATION', 'EMERGING_MARKET', 'ENERGY', 'ENTERTAINMENT', 'ENVIRONMENT', 'ETF', 'ETHIOPIA', 'EUROPE', 'EVENT', 'FASHION', 'FDA', 'FEDERAL_RESERVE', 'FINANCE', 'FINANCING', 'FINTECH', 'FOREX', 'FORUM', 'FRANCE', 'FUND', 'FUTURE', 'GENERAL', 'GEOPOLITICS', 'GERMANY', 'GHANA', 'HEALTH', 'HEIDI', 'HISTORY', 'HONG KONG', 'HOT', 'HOUSE', 'INDIA', 'INDONESIA', 'INSIDER_TRADE', 'INTERNET', 'INTERVIEW', 'IPO', 'IRELAND', 'ISRAEL', 'ITALIA', 'JAPAN', 'KENYA', 'KOREA', 'LATIN_AMERICA', 'LATVIA', 'LAW', 'LEGAL', 'LIFESTYLE', 'LOGISTICS', 'M&A', 'MALAYSIA', 'MANAGEMENT', 'MEDIA', 'MIDDLE_EAST', 'MILITARY', 'MONEY', 'MOVIES', 'NAMIBIA', 'NATION', 'NEW_ZEALAND', 'NIGERIA', 'NORTH_KOREA', 'OFFERING', 'OPINION', 'OPTION', 'PAKISTAN', 'PEOPLE', 'PETS', 'PHILIPPINES', 'PICTURES', 'POLITICS', 'POLLS', 'POSTAL', 'PRESS', 'RATING', 'REAL_ESTATE', 'REAL_TIME', 'REGION', 'RESEARCH', 'RETAIL_SALES', 'REVIEW', 'RUMORS', 'RUSSIA', 'SCIENCE', 'SINGAPORE', 'SMALL_CAP', 'SOCIALS', 'SOUTHEAST_ASIA', 'SOUTH_AFRICA', 'SOUTH_ASIA', 'SPEECH', 'SPORT', 'SPORT_BOXING', 'SPORT_GOLF', 'SPORT_RACING', 'SPORT_RUGBY', 'SPORT_SOCCER', 'SPORT_TENNIS', 'STATISITCS', 'STOCK', 'STOCK_SPLIT', 'STORY', 'TAIWAN', 'TANZANIA', 'TECHNOLOGY', 'TELECOMS', 'TOP', 'TOURISM', 'TRAFFIC', 'TRAVEL', 'TURKEY', 'UGANDA', 'UK', 'US', 'USA', 'WEATHER', 'WORLD', 'ZIMBABWE'; Multiple category separated by "," 
        - source (optional): Available values include 'APPLE_DAILY', 'AsahiNews', 'BBC', 'CHINADAILYHK', 'CHOSUM', 'CNN', 'CUP', 'DW_NEWS', 'ENGADGET', 'ETNET', 'FACEBOOK', 'GOOGLE', 'GOV.HK', 'GRASSMEDIACTION', 'HKET', 'HKEX', 'HKFP', 'HORBOURTIMES', 'InsiderInsight', 'JTBC', 'JapanIndustryNews', 'KBS', 'KINLIU', 'KyodoNews', 'LOCALPRESSHK', 'LivedoorNews', 'MADDOG', 'MARKETWATCH', 'MASTER-INSIGHT', 'MINGPAO', 'MSN', 'NDTV', 'NHK', 'NYTIMES', 'NipponNews', 'OILPRICE', 'ORIENTAL_DAILY', 'PMNEWS', 'PeopleDaily', 'REUTERS', 'RFA', 'RTHK', 'SUPERMEDIA', 'SYMEDIALAB', 'SoraNews', 'TRT', 'TheNewsLensHK', 'UDN', 'VOACANTONESE', 'WallStreetJournal', 'YAHOO', 'Yonhap', 'aamacau', 'bastillepost', 'benzinga', 'feedburner', 'feedx', 'heraldcorp', 'hkcnews', 'hkjam', 'inmediahk', 'japaninsides', 'japantimes', 'japantoday', 'koreaherald', 'koreatimes', 'litenews', 'localpresshk', 'mcnews', 'memehk', 'newsonjapan', 'nytimes', 'pentoy', 'philstar', 'polymerhk', 'post852', 'scmp', 'thebridge', 'theinitium', 'thejapannews', 'thestandnews', 'tmhk', 'tokyoreporter', 'voachinese', 'yahoo', 'zakzak', 'zhihu' Mutiple source separated by ","
        
    Returns:
        Dict containing:
        - res (dict): Response data containing 
            - authors (str): the author for the news
            - category (str): the category of the News
            - link (str): the original URL of the News
            - movies (array): the list of embeded videos in the News
            - published (str): the published datetime, timezone in UTC+0
            - source (str): the source of the News
            - text (str): the News content
            - title (str): the news headline
            - top_image (str): an URL for the top image (if any) embeded in the News
        
    Examples:
        result = get_realtime_news(lang="en", source="BBC")  # english news from BBC
        news = result['res']
        title = news["title"]
        text = news["text"]
        print(f"news: ${title}")
    """
    try:
        from tools import get_realtime_news as _get_realtime_news
        return _get_realtime_news.get_realtime_news(lang, category, source)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_news tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_realtime_weather(
    city: str
) -> Dict[str, Any]:
    """
    Get the latest weather info for specific city.
    
    This function fetches latest weather data for specified city from on ALGOGENE.
    
    Args:
        city: any city name in the world, including but not limited to 'Baghdad', 'Bangkok', 'Beijing', 'Berlin', 'Bloemfontein', 'Boston', 'Brasilia', 'Cairo', 'Cape Town', 'Chengdu', 'Chicago', 'Chongqing', 'Columbia', 'Hanoi', 'Havana', 'Hong Kong', 'Jakarta', 'Kinshasa', 'London', 'Los Angeles', 'Madrid', 'Malaysia', 'Manila', 'Moscow', 'New Delhi', 'New York City', 'Osaka', 'Ottawa', 'Paris', 'Perth', 'Phnom Penh', 'Pretoria', 'Pyongyang', 'Rabat', 'Reykjavik', 'Rome', 'San Diego', 'Seoul', 'Shanghai', 'Singapore', 'Sudan', 'Taipei', 'Tokyo', 'Toronto', 'Ulaanbaatar', 'Washington', 'Xinjiang', etc

    Returns:
        Dict containing:
        - res (dict): Response data containing 
            - city (str): city name
            - country (str): the country of the city
            - coord_lat (float): latitude of the city's geographic coordinate
            - coord_lon (float): longitude of the city's geographic coordinate
            - surnise (str): sunrise time in format of YYYY-MM-DD HH:MM:SS.FFFFFF
            - sunset (str): estimated sunset time in format of YYYY-MM-DD HH:MM:SS.FFFFFF
            - visibility (float): the visibility, unit in miles, None for missing value
            - pressure (float): the atmosheric pressure of the city at the recorded time, unit in Dynes per squre centimetre
            - temperature_min (float): the minimum temperature of the city on the recorded date, unit in Fahrenheit (F)
            - temperature_max (float): the maximum temperature of the city on the recorded date, unit in Fahrenheit (F)
            - temperature (float): the temperature of the city at the recorded time, unit in Fahrenheit (F)
            - humidity (float): the humidity of the city at the recorded time, unit in percentage (%)
            - wind_speed (float): the wind speed of the city at the recorded time, unit in mile per hour (mph)
            - wind_degree (float): the wind degree of the city at the recorded time, value range from 0 to 360 degree
            - weather (str): high level classification of the city's weather, value include 'Clear', 'Clouds', 'Haze', 'Mist', 'Rain', etc
            - weather_desc (str): detailed description of the city's weather, value include 'broken clouds', 'clear sky', 'few clouds', 'haze', 'light rain', 'mist', 'moderate rain', 'overcast clouds', 'scattered clouds', etc
            - clouds (float): the density of cloud of the city, value ranging from 0 to 100

    Examples:
        result = get_realtime_weather(city="Shanghai")  # weather in Shanhai
        res = result['res']
        temperature = res["temperature"]
        humidity = res["humidity"]
        print(f"temperature: ${temperature}")
    """
    try:
        from tools import get_realtime_weather as _get_realtime_weather
        return _get_realtime_weather.get_realtime_weather(city)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_weather tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def get_realtime_econs_calendar(
    count: int
) -> Dict[str, Any]:
    """
    Get the latest economic calendar data on ALGOGENE.

    This function retrieves upcoming economic events, including statistics releases, speeches, holidays, and other relevant occurrences that may impact the financial markets.

    Args:
        count (int): The number of results to return (default is 10, optional).

    Returns:
        Dict containing:
        - res (List[Dict]): Array of objects containing details about each economic event:
            - timestamp (str): The scheduled time of the calendar event.
            - eventid (str): Unique identifier for the event.
            - currency (str): The impacted currency or country related to the event.
            - impact (str): The expected economic impact level (e.g., Low, Medium, High).
            - nevent (str): A description of the calendar event.
            - actual (str): The actual figure (if available).
            - forecast (str): The forecast figure for the event.
            - previous (str): The previous figure recorded for the event.
            - unit (str): The unit of measurement for the figures (if applicable).

    Examples:
        result = get_realtime_econs_calendar(count=10)
        print(f"Number of events: {len(result['res'])}")
        for event in result['res']:
            print(f"{event['timestamp']} - {event['nevent']} (Impact: {event['impact']})")
    """
    try:
        from tools import get_realtime_econs_calendar as _get_realtime_econs_calendar
        return _get_realtime_econs_calendar.get_realtime_econs_calendar(count)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_econs_calendar tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def get_realtime_econs_stat() -> Dict[str, Any]:
    """
    Get the latest economic statistics data on ALGOGENE.

    This function retrieves the most recent economic statistics, including various measurements and metrics that can influence market dynamics.

    Args: None

    Returns:
        Dict containing:
        - series_id (str): The unique identifier for the economic statistics series.
        - title (str): A description of the economic statistics.
        - src (str): The original source of the statistics.
        - geo (str): The city or country applicable to the statistics (if available).
        - tag (List[str]): Categories or tags associated with the economic statistics.
        - freq (str): The release frequency of the statistics (e.g., monthly, quarterly).
        - units (str): The units of the observation value.
        - seasonal_adj (str): Identifier for seasonal adjustment (if applicable).
        - notes (str): Additional remarks or details about the data.
        - popularity (float): Popularity rating of the economic statistics.
        - obs_date (str): The observation date for the statistic.
        - obs_val (float): The observed value of the statistic.

    Examples:
        result = get_realtime_econs_stat()
        print(f"Statistic: {result['title']} - Value: {result['obs_val']} {result['units']}")
    """
    try:
        from tools import get_realtime_econs_stat as _get_realtime_econs_stat
        return _get_realtime_econs_stat.get_realtime_econs_stat()
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_econs_stat tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def get_instruments() -> Dict[str, Any]:
    """
    Get the list of available financial instruments on ALGOGENE.

    This function retrieves all currently supported financial instruments by ALGOGENE, providing users with the instruments they can trade or analyze.

    Args: None

    Returns:
        Dict containing:
        - count (int): The total number of financial instruments returned.
        - res (List[str]): A list of all available financial instruments sorted in alphabetical order.

    Examples:
        result = get_list_instrument()
        print(f"Total instruments available: {result['count']}")
        for instrument in result['res']:
            print(instrument)  # Prints each available financial instrument
    """
    try:
        from tools import get_instruments as _get_instruments
        return _get_instruments.get_instruments()
    except Exception as e:
        logger.error(f"Unexpected error in get_instruments tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_instrument_meta(
    instrument: str
) -> Dict[str, Any]:
    """
    Get the metadata of a specified financial instrument on ALGOGENE.

    This function retrieves the contract specification details for a particular financial instrument, including information about its market, product type, and other relevant properties.

    Args:
        instrument (str): The name of the financial instrument from the list of available instruments.

    Returns:
        Dict containing:
        - res (Dict): A JSON object with the financial contract specification, including:
            - contractSize (int): The number of shares per lot.
            - market (str): The corresponding asset market (e.g., 'COM', 'CRYTO', 'ENERGY', 'EQ', 'FX', 'IR', 'METAL').
            - producttype (str): The type of product (e.g., 'SPOT', 'FUT', 'OPT').
            - settleCurrency (str): The currency used for settlement.
            - description (str): A description of the financial instrument.

    Examples:
        result = get_meta_instrument(instrument="BTCUSD")
        print(f"Contract Size: {result['res']['contractSize']}")
        print(f"Description: {result['res']['description']}")
    """
    try:
        from tools import get_instrument_meta as _get_instrument_meta
        return _get_instrument_meta.get_instrument_meta(instrument)
    except Exception as e:
        logger.error(f"Unexpected error in get_instrument_meta tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def search_instrument(
    symbols: str = "",
    desc: str = ""
) -> Dict[str, Any]:
    """
    Search Financial Instruments

    This function allows users to search for financial instruments based on keywords found in their symbols or descriptions. Users can specify multiple keywords for a more refined search.

    Args:
        desc (string): Optional. A comma-separated list of keywords to search within instrument descriptions.
        symbols (string): Optional. A comma-separated list of keywords to search within instrument symbols.

    Returns:
        Dict containing:
        - count (integer): The number of search results returned.
        - res (array): A list of matched financial instruments, each represented as an object containing:
            - asset (string): The asset class of the instrument.
            - instrument (string): The name of the instrument.
            - desc (string): A description of the instrument.

    Examples:
        # Example 1: Search for Financial Instruments by Description
        result = search_instrument(
            desc="gold,silver"
        )
        print(f"Number of Results: {result['count']}")
        for instrument in result['res']:
            print(f"Asset: {instrument['asset']}, Instrument: {instrument['instrument']}, Description: {instrument['desc']}")

        # Example 2: Search for Financial Instruments by Symbols
        result = search_instrument(
            symbols="xau,xag"
        )
        print(f"Number of Results: {result['count']}")
        for instrument in result['res']:
            print(f"Asset: {instrument['asset']}, Instrument: {instrument['instrument']}, Description: {instrument['desc']}")

        # Example 3: Search Using Both Description and Symbols
        result = search_instrument(
            desc="equity",
            symbols="lux"
        )
        print(f"Number of Results: {result['count']}")
        for instrument in result['res']:
            print(f"Asset: {instrument['asset']}, Instrument: {instrument['instrument']}, Description: {instrument['desc']}")

        # Example 4: Search with No Keywords Provided
        result = search_instrument(
            api_key="123456",
            user="demo1"
        )
        print(f"Number of Results: {result['count']} - No keywords provided.")
    """
    try:
        from tools import search_instrument as _search_instrument
        return _search_instrument.search_instrument(symbols, desc)
    except Exception as e:
        logger.error(f"Unexpected error in search_instrument tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



def search_econs_series(
    titles: str,
    freq: str = "",
    geo: str = ""
) -> Dict[str, Any]:
    """
    Search Economic Series

    This function allows users to search for economic time series data based on specified parameters including titles, geographical location, and frequency. The data returned provides insights into various economic indicators.

    Args:
        titles (string): Required. A comma-separated list of keywords to search for in economic time series titles.
        geo (string): Optional. A geographical location to filter the economic series by city or country.
        freq (string): Optional. Data frequency to filter the economic series (e.g., annual, monthly).

    Returns:
        Dict containing:
        - count (integer): The number of matched economic series.
        - res (array[object]): A list of matched economic series, each containing:
            - series_id (string): The unique identifier for the economic series.
            - title (string): The description of the economic series.
            - freq (string): The frequency of the economic release.
            - units (string): The unit of measurement for the statistics value.
            - seasonal (string): Identifier for any seasonal adjustments.
            - src (string): The original source of the data.
            - geo (string): The applicable city/country for the economic statistics.
            - tag (array[string]): Categories associated with the series.
            - obs_start (string): The earliest date of observation.

    Examples:
        # Example 1: Search for Economic Series by Title, Geographic Location, and Frequency
        result = search_econs_series(
            titles="gdp",
            geo="usa",
            freq="annual"
        )
        print(f"Number of Results: {result['count']}")
        for series in result['res']:
            print(f"Title: {series['title']}, Series ID: {series['series_id']}, Frequency: {series['freq']}")

        # Example 2: Search for Economic Series by Title Only
        result = search_econs_series(
            titles="inflation"
        )
        print(f"Number of Results: {result['count']}")
        for series in result['res']:
            print(f"Title: {series['title']}, Series ID: {series['series_id']}, Units: {series['units']}")

        # Example 3: Search for Economic Series without Geographical Filter
        result = search_econs_series(
            titles="employment",
            freq="monthly"
        )
        print(f"Number of Results: {result['count']}")
        for series in result['res']:
            print(f"Title: {series['title']}, Frequency: {series['freq']}, Start Date: {series['obs_start']}")

        # Example 4: Search Without Any Optional Parameters
        result = search_econs_series(
            titles="trade"
        )
        print(f"Number of Results: {result['count']} - No additional filtering.")
    """
    try:
        from tools import search_econs_series as _search_econs_series
        return _search_econs_series.search_econs_series(titles, freq, geo)
    except Exception as e:
        logger.error(f"Unexpected error in search_econs_series tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def list_econs_series() -> Dict[str, Any]:
    """
    Get the list of available economic series IDs on ALGOGENE.

    This function retrieves all economic series IDs currently available on ALGOGENE, allowing users to access a wide range of economic data. Due to the large volume of data, only a subset of available series IDs is presented in examples.

    Args: None

    Returns:
        Dict containing:
        - count (int): The total number of available economic series IDs.
        - res (List[str]): An array containing the available economic series IDs.

    Examples:
        result = get_list_econs_series()
        print(f"Total economic series available: {result['count']}")
        print("Available series IDs:")
        for series_id in result['res']:
            print(series_id)  # Prints each available economic series ID
    """
    try:
        from tools import list_econs_series as _list_econs_series
        return _list_econs_series.list_econs_series()
    except Exception as e:
        logger.error(f"Unexpected error in list_econs_series tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_econs_series_meta(
    series_id: str
) -> Dict[str, Any]:
    """
    Get the metadata of a specified economic series on ALGOGENE.

    This function retrieves detailed metadata for a particular economic series, including descriptions, frequency of release, and other relevant attributes associated with the series.

    Args:
        series_id (str): The ID of the economic series for which metadata is requested, obtained from the /list_econs_series endpoint.

    Returns:
        Dict containing:
        - res (Dict): A JSON object containing the metadata of the economic series:
            - series_id (str): The unique identifier for the economic series.
            - title (str): A description of the economic series.
            - freq (str): The frequency of the economic release (e.g., annual, quarterly).
            - units (str): The units of the statistics value (e.g., Thousands of Chained 2012 U.S. Dollars).
            - seasonal (str): Identifier for any seasonal adjustment applied to the series.
            - src (str): The original source of the economic data.
            - geo (str): The applicable geographical area of the economic statistics.
            - tag (List[str]): Categories associated with the series.
            - obs_start (str): The earliest observation date for the series.

    Examples:
        result = get_meta_econs_series(user="yyy", api_key="xxx", series_id="REALGDPSERV56041")
        print(f"Series Title: {result['res']['title']}")
        print(f"Observation Start Date: {result['res']['obs_start']}")
    """
    try:
        from tools import get_econs_series_meta as _get_econs_series_meta
        return _get_econs_series_meta.get_econs_series_meta(series_id)
    except Exception as e:
        logger.error(f"Unexpected error in get_econs_series_meta tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_history_price(
    instrument: str,
    interval: str,
    count: int,
    timestamp: str,
    chain_dated: int = 0,
    expiry: str = "",
    right: str = "", 
    strike: float = 0
) -> Dict[str, Any]:
    """
    Get historical price and volume data for financial instruments on ALGOGENE.

    This function retrieves historical data, including price and volume, for specified financial instruments, allowing users to analyze past market performance.

    Args:
        instrument (str): The name of the financial instrument obtained from the /list_instrument endpoint.
        count (int): The number of records to return (minimum: 1, maximum: 1000; default is 1).
        interval (str): The candlestick interval for the data. Available values include 'T', 'S', 'S5', 'S10', 'S15', 'S30', 'M','M2','M5','M10','M15','M30','H','H2','H3','H4','H6','H12','D'
        timestamp (str): Retrieve data with timestamps less than this specified value (format: "YYYY-MM-DD HH:MM:SS", GMT+0).
        chain_dated (int, optional): For future-related instruments, specify the combined future chain history (1-4 for different expiry contracts).
        expiry (str, optional): Expiry date in format yyyymmdd, applicable for FUT/OPT contracts.
        right (str, optional): The type of exercise right for OPT contracts ('C' for call, 'P' for put).
        strike (float, optional): The strike price for OPT contracts.

    Returns:
        Dict containing:
        - count (int): The number of records returned.
        - res (List[Dict]): A list of JSON objects for candlestick data, sorted by ascending timestamp, each containing:
            - t (str): Timestamp at bar closing (format: "YYYY-MM-DD HH:MM:SS").
            - o (float): Open price for the candle bar.
            - h (float): Highest price for the candle bar.
            - l (float): Lowest price for the candle bar.
            - c (float): Closing price for the candle bar.
            - b (float): Closing bid price for the candle bar.
            - a (float): Closing ask price for the candle bar.
            - m (float): Closing mid price for the candle bar.
            - v (int): Transaction volume for the candle bar.
            - expiry (str): Expiry date for FUT/OPT contracts (if applicable).
            - right (str): Option exercise right for OPT contracts (if applicable).
            - strike (float): Strike price for OPT contracts (if applicable).

    Examples:
        result = get_history_price(
            count=3,
            interval="D",
            timestamp="2018-10-30 00:00:00",
            instrument="ZARJPY"
        )
        print(f"Total records: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['t']} - Open: {record['o']}, Close: {record['c']}, Volume: {record['v']}")
    """
    try:
        from tools import get_history_price as _get_history_price
        return _get_history_price.get_history_price(instrument=instrument, interval=interval, count=count, timestamp=timestamp, chain_dated=chain_dated, expiry=expiry, right=right, strike=strike)
    except Exception as e:
        logger.error(f"Unexpected error in get_history_price tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_history_news(
    lang: str,
    count: int,
    starttime: str,
    endtime: str,
    category: str = "",
    source: str = ""
) -> Dict[str, Any]:
    """
    Get historical news articles from ALGOGENE.

    This function retrieves historical news articles based on specified filters, allowing users to access relevant news stories within a specified timeframe.

    Args:
        user (str): Your user ID generated by ALGOGENE at system registration.
        api_key (str): Your API key for authentication.
        count (int): The number of news articles to return (maximum: 100).
        starttime (str): Retrieve news published after this timestamp (format: "yyyy-mm-dd hh:mm:ss").
        endtime (str): Retrieve news published before this timestamp (format: "yyyy-mm-dd hh:mm:ss").
        lang (str): Language code for the news articles (ISO 639-1). available values include ‘af','ar','bg','bn','ca','cs','cy','da','de','el','en','es','et','fa','fi','fr','gu','he','hi','hr','hu','id','it','ja','kn','ko ','lt','lv','mk','ml','mr','ne','nl','no','pa','pl','pt','ro','ru','sk','sl','so','sq','sv','sw','ta','te','th','tl','tr','uk',' ur','vi','zh-cn','zh-tw'
        category (str): Comma-separated categories to filter results (e.g., 'WORLD,USA'). Avaiable values include 'AFRICA', 'AGRICULTURE', 'AMERICAS', 'ART', 'ASIA', 'ASSET_SALES', 'AUSTRALIA', 'AUTO', 'BIOTECH', 'BOND', 'BOOK', 'BOTsWANA', 'BUSINESS', 'BUYBACK', 'CANADA', 'CENTRAL_ASIA', 'CHINA', 'COMMENTARY', 'COMMODITY', 'COMMUNITY', 'COMPANY', 'COMPANY NEWS', 'CONTRACT', 'CULTURE', 'DIPLOMACY', 'DIVIDENDS', 'EARNINGS', 'EAST_ASIA', 'ECONOMY', 'EDUCATION', 'EMERGING_MARKET', 'ENERGY', 'ENTERTAINMENT', 'ENVIRONMENT', 'ETF', 'ETHIOPIA', 'EUROPE', 'EVENT', 'FASHION', 'FDA', 'FEDERAL_RESERVE', 'FINANCE', 'FINANCING', 'FINTECH', 'FOREX', 'FORUM', 'FRANCE', 'FUND', 'FUTURE', 'GENERAL', 'GEOPOLITICS', 'GERMANY', 'GHANA', 'HEALTH', 'HEIDI', 'HISTORY', 'HONG KONG', 'HOT', 'HOUSE', 'INDIA', 'INDONESIA', 'INSIDER_TRADE', 'INTERNET', 'INTERVIEW', 'IPO', 'IRELAND', 'ISRAEL', 'ITALIA', 'JAPAN', 'KENYA', 'KOREA', 'LATIN_AMERICA', 'LATVIA', 'LAW', 'LEGAL', 'LIFESTYLE', 'LOGISTICS', 'M&A', 'MALAYSIA', 'MANAGEMENT', 'MEDIA', 'MIDDLE_EAST', 'MILITARY', 'MONEY', 'MOVIES', 'NAMIBIA', 'NATION', 'NEW_ZEALAND', 'NIGERIA', 'NORTH_KOREA', 'OFFERING', 'OPINION', 'OPTION', 'PAKISTAN', 'PEOPLE', 'PETS', 'PHILIPPINES', 'PICTURES', 'POLITICS', 'POLLS', 'POSTAL', 'PRESS', 'RATING', 'REAL_ESTATE', 'REAL_TIME', 'REGION', 'RESEARCH', 'RETAIL_SALES', 'REVIEW', 'RUMORS', 'RUSSIA', 'SCIENCE', 'SINGAPORE', 'SMALL_CAP', 'SOCIALS', 'SOUTHEAST_ASIA', 'SOUTH_AFRICA', 'SOUTH_ASIA', 'SPEECH', 'SPORT', 'SPORT_BOXING', 'SPORT_GOLF', 'SPORT_RACING', 'SPORT_RUGBY', 'SPORT_SOCCER', 'SPORT_TENNIS', 'STATISITCS', 'STOCK', 'STOCK_SPLIT', 'STORY', 'TAIWAN', 'TANZANIA', 'TECHNOLOGY', 'TELECOMS', 'TOP', 'TOURISM', 'TRAFFIC', 'TRAVEL', 'TURKEY', 'UGANDA', 'UK', 'US', 'USA', 'WEATHER', 'WORLD', 'ZIMBABWE'; 
        source (str): Comma-separated news sources to filter results (e.g., 'BBC,CNN'). Available values include 'APPLE_DAILY', 'AsahiNews', 'BBC', 'CHINADAILYHK', 'CHOSUM', 'CNN', 'CUP', 'DW_NEWS', 'ENGADGET', 'ETNET', 'FACEBOOK', 'GOOGLE', 'GOV.HK', 'GRASSMEDIACTION', 'HKET', 'HKEX', 'HKFP', 'HORBOURTIMES', 'InsiderInsight', 'JTBC', 'JapanIndustryNews', 'KBS', 'KINLIU', 'KyodoNews', 'LOCALPRESSHK', 'LivedoorNews', 'MADDOG', 'MARKETWATCH', 'MASTER-INSIGHT', 'MINGPAO', 'MSN', 'NDTV', 'NHK', 'NYTIMES', 'NipponNews', 'OILPRICE', 'ORIENTAL_DAILY', 'PMNEWS', 'PeopleDaily', 'REUTERS', 'RFA', 'RTHK', 'SUPERMEDIA', 'SYMEDIALAB', 'SoraNews', 'TRT', 'TheNewsLensHK', 'UDN', 'VOACANTONESE', 'WallStreetJournal', 'YAHOO', 'Yonhap', 'aamacau', 'bastillepost', 'benzinga', 'feedburner', 'feedx', 'heraldcorp', 'hkcnews', 'hkjam', 'inmediahk', 'japaninsides', 'japantimes', 'japantoday', 'koreaherald', 'koreatimes', 'litenews', 'localpresshk', 'mcnews', 'memehk', 'newsonjapan', 'nytimes', 'pentoy', 'philstar', 'polymerhk', 'post852', 'scmp', 'thebridge', 'theinitium', 'thejapannews', 'thestandnews', 'tmhk', 'tokyoreporter', 'voachinese', 'yahoo', 'zakzak', 'zhihu' 

    Returns:
        Dict containing:
        - count (int): The number of articles returned.
        - res (List[Dict]): A list of news articles sorted by published time, each containing:
            - published (str): Published time in GMT+0.
            - authors (List[str]): List of authors for the article.
            - title (str): Title of the article.
            - source (str): Publisher of the article.
            - text (str): Content of the article.
            - category (str): Category of the article.
            - link (str): URL link to the article.
            - top_image (str): URL link to the main image in the article.
            - movies (List[str]): List of video links embedded in the article.

    Examples:
        result = get_history_news(
            count=2,
            starttime="2019-12-13 00:00:00",
            endtime="2019-12-13 23:59:59",
            lang="en"
        )
        print(f"Total articles retrieved: {result['count']}")
        for article in result['res']:
            print(f"Title: {article['title']} - Published: {article['published']} - Source: {article['source']}")
    """
    try:
        from tools import get_history_news as _get_history_news
        return _get_history_news.get_history_news(lang, count, starttime, endtime, category, source)
    except Exception as e:
        logger.error(f"Unexpected error in get_history_news tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_history_weather(
    city: str,
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    """
    Get historical weather information for a specified city.

    This function retrieves detailed weather data for a given city within a specified time range, allowing users to analyze past weather conditions.

    Args:
        city (str): The name of the city for which historical weather is needed. eg. 'Baghdad', 'Bangkok', 'Beijing', 'Berlin', 'Bloemfontein', 'Boston', 'Brasilia', 'Cairo', 'Cape Town', 'Chengdu', 'Chicago', 'Chongqing', 'Columbia', 'Hanoi', 'Havana', 'Hong Kong', 'Jakarta', 'Kinshasa', 'London', 'Los Angeles', 'Madrid', 'Malaysia', 'Manila', 'Moscow', 'New Delhi', 'New York City', 'Osaka', 'Ottawa', 'Paris', 'Perth', 'Phnom Penh', 'Pretoria', 'Pyongyang', 'Rabat', 'Reykjavik', 'Rome', 'San Diego', 'Seoul', 'Shanghai', 'Singapore', 'Sudan', 'Taipei', 'Tokyo', 'Toronto', 'Ulaanbaatar', 'Washington', 'Xinjiang', etc
        starttime (str): Retrieve weather data recorded after this timestamp (format: "yyyy-mm-dd hh:mm:ss").
        endtime (str): Retrieve weather data recorded before this timestamp (format: "yyyy-mm-dd hh:mm:ss").

    Returns:
        Dict containing:
        - count (int): The number of weather records returned.
        - res (List[Dict]): A list of weather records for the specified city, each containing:
            - timestamp (str): The recorded timestamp of the weather event (in UTC).
            - city (str): The city/region of the weather event.
            - country (str): The country/region code.
            - coord_lat (float): Geographical latitude of the recorded location.
            - coord_lon (float): Geographical longitude of the recorded location.
            - sunrise (str): Sunrise time for that date.
            - sunset (str): Sunset time for that date.
            - visibility (float | None): Visibility in miles or None for missing values.
            - pressure (float): Atmospheric pressure in Dynes per square centimeter.
            - temperature_min (float): Minimum temperature during the day in Fahrenheit.
            - temperature_max (float): Maximum temperature during the day in Fahrenheit.
            - temperature (float): Temperature at the captured time in Fahrenheit.
            - humidity (int): Humidity percentage (%).
            - wind_speed (float): Wind speed in miles per hour (mph).
            - wind_degree (int): Wind direction in degrees (0-360).
            - weather (str): High-level classification of weather (e.g., 'Clear', 'Clouds').
            - weather_desc (str): Detailed weather description (e.g., 'clear sky', 'light rain').
            - clouds (int): Cloud density percentage (0-100).

    Examples:
        result = get_history_weather(
            city="Hong Kong",
            starttime="2020-06-24 00:00:00",
            endtime="2020-06-24 23:59:59"
        )
        print(f"Total records retrieved: {result['count']}")
        for record in result['res']:
            print(f"Timestamp: {record['timestamp']} - Weather: {record['weather_desc']} - Temperature: {record['temperature']}°F")
    """
    try:
        from tools import get_history_weather as _get_history_weather
        return _get_history_weather.get_history_weather(city, starttime, endtime)
    except Exception as e:
        logger.error(f"Unexpected error in get_history_weather tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_history_corp_announcement(
    symbol: str,
    starttime: str,
    endtime: str,
    event: str = ""
) -> Dict[str, Any]:
    """
    Get historical corporate announcements for listed stocks.

    This function retrieves corporate event data, such as dividends and splits, for specified stocks over a defined date range.

    Args:
        symbol (str): The stock symbol for which corporate events are needed (must be a valid instrument from /list_instrument).
        starttime (str): Apply filter for starting date of announcement (format: 'YYYY-MM-DD').
        endtime (str): Apply filter for ending date of announcement (format: 'YYYY-MM-DD').
        event (str, optional): Filter by event type ('dividends', 'splits'); omit to return all corporate events.

    Returns:
        Dict containing:
        - count (int): The number of corporate announcements returned.
        - res (List[Dict]): A list of corporate events, each containing:
            - announce_date (str): The date the corporate action was announced.
            - event (str): The type of corporate action ('dividends', 'splits').
            - ex_date (str): The ex-dividend date for eligibility.
            - payable_date (str, optional): The date for dividend payment (only present for 'dividends').
            - is_special (str, optional): Indicates if it is a special dividend ('T' or 'F', only present for 'dividends').
            - dividend_amt (float, optional): The amount of dividend (only present for 'dividends').
            - splits (float, optional): The share split ratio (only present for 'splits').

    Examples:
        result = get_history_corp_announcement(
            symbol="AAPL",
            event="dividends",
            starttime="2019-01-01",
            endtime="2019-12-31"
        )
        print(f"Total corporate announcements retrieved: {result['count']}")
        for announcement in result['res']:
            print(f"Announcement Date: {announcement['announce_date']} - Event: {announcement['event']} - Dividend Amount: ${announcement.get('dividend_amt', 0)}")
    """
    try:
        from tools import get_history_corp_announcement as _get_history_corp_announcement
        return _get_history_corp_announcement.get_history_corp_announcement(symbol, starttime, endtime, event)
    except Exception as e:
        logger.error(f"Unexpected error in get_history_corp_announcement tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def get_history_econs_calendar(
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    """
    Get historical economic calendar data.

    This function retrieves historical economic calendar events, such as statistics release times, holidays, and speeches, over a specified date range.

    Args:
        starttime (str): Retrieve events recorded after this timestamp (format: 'YYYY-MM-DD').
        endtime (str): Retrieve events recorded before this timestamp (format: 'YYYY-MM-DD').

    Returns:
        Dict containing:
        - count (int): The number of events returned.
        - res (List[Dict]): A list of economic events, each containing:
            - timestamp (str): The captured timestamp of the event (in UTC).
            - eventid (str): Unique identifier of the calendar event.
            - currency (str): The impacted currency/country related to the event.
            - impact (str): The estimated impact of the calendar event (e.g., 'Low Impact Expected').
            - nevent (str): Description of the calendar event.
            - actual (str): Actual figure of the calendar event.
            - forecast (str): Forecast figure for the calendar event.
            - previous (str): Previous figure for the calendar event.
            - unit (str): The unit of the reported figures.

    Examples:
        result = get_history_econs_calendar(
            starttime="2025-12-01",
            endtime="2025-12-31"
        )
        print(f"Total economic events retrieved: {result['count']}")
        for event in result['res']:
            print(f"Timestamp: {event['timestamp']} - Event: {event['nevent']} - Actual: {event['actual']}")
    """
    try:
        from tools import get_history_econs_calendar as _get_history_econs_calendar
        return _get_history_econs_calendar.get_history_econs_calendar(starttime, endtime)
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_econs_calendar tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_history_econs_stat(
    series_id: str,
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    """
    Get historical observations of a specified economic series.

    This function retrieves historical economic data based on a specific economic series ID, allowing users to analyze trends over a defined date range.

    Args:
        series_id (str): The economic series ID for which to retrieve historical observations (must be valid from /list_econs_series).
        starttime (str): Retrieve data recorded after this timestamp (format: 'YYYY-MM-DD').
        endtime (str): Retrieve data recorded before this timestamp (format: 'YYYY-MM-DD').

    Returns:
        Dict containing:
        - count (int): Total number of observations returned.
        - res (List[Dict]): A list of observations, each containing:
            - date (str): Observation date of the economic series.
            - value (str): Observation value of the economic series.
            - series_id (str): The specified economic series ID used for the request.

    Examples:
        result = get_history_econs_stat(
            series_id="YOUN639TRADN",
            starttime="2020-01-01",
            endtime="2020-05-31"
        )
        print(f"Total observations retrieved: {result['count']}")
        for observation in result['res']:
            print(f"Date: {observation['date']} - Value: {observation['value']}")
    """
    try:
        from tools import get_history_econs_stat as _get_history_econs_stat
        return _get_history_econs_stat.get_history_econs_stat(series_id, starttime, endtime)
    except Exception as e:
        logger.error(f"Unexpected error in get_history_econs_stat tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_session() -> Dict[str, Any]:
    """
    Create or refresh a session token for trade actions.

    This function generates a temporary session token required for performing subsequent trading operations. The token is valid for one hour. Once expired, a new token must be obtained.

    Args: None

    Returns:
        Dict containing:
        - res (Dict): 
            - token (str): The generated session token string.
            - expired_utc (str): The expiry datetime of the token (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).

    Examples:
        result = get_session()
        print(f"Token: {result['res']['token']}")
        print(f"Token expires at: {result['res']['expired_utc']}")
    """
    try:
        from tools import get_session as _get_session
        return _get_session.get_session()
    except Exception as e:
        logger.error(f"Unexpected error in get_session tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def list_accounts(
    runmode: str,
    token: str
) -> Dict[str, Any]:
    """
    List all available trading accounts with latest balances.

    This function retrieves a list of all trading accounts associated with the user, along with their latest balances and trading statuses.

    Args:
        runmode (str): The strategy run mode, which can be either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.

    Returns:
        Dict containing:
        - count (int): Total number of accounts returned.
        - res (List[Dict]): A list of accounts, each containing:
            - accountid (str): Unique ID of the trading account.
            - runmode (str): Type of account, either 'livetest' or 'livetrade'.
            - NAV (float): Net Asset Value of the account.
            - availableBalance (float): The remaining balance that is available for trading.
            - marginUsed (float): Capital currently in use.
            - realizedPL (float): Cumulative realized profit/loss.
            - unrealizedPL (float): Outstanding unrealized profit/loss.
            - lastUpdatedTime (str): Last updated time (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
            - isTrading (bool): Indicates whether an algorithm is currently running on this account.

    Examples:
        result = get_accounts(
            runmode="livetest",
            token="123456"
        )
        print(f"Total accounts retrieved: {result['count']}")
        for account in result['res']:
            print(f"Account ID: {account['accountid']} - NAV: {account['NAV']} - Available Balance: {account['availableBalance']}")
    """
    try:
        from tools import list_accounts as _list_accounts
        return _list_accounts.list_accounts(runmode, token)
    except Exception as e:
        logger.error(f"Unexpected error in list_accounts tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_positions(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    """
    Retrieve outstanding positions for a specified trading account.

    This function retrieves the current outstanding inventory and positions for a specified account, showing all symbols with non-zero positions.

    Args:
        accountid (str): The ALGOGENE account ID for which to retrieve positions.
        runmode (str): The run mode or account type, which can be either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.

    Returns:
        Dict containing:
        - count (int): Total number of symbols that have non-zero positions.
        - res (Dict): 
            - symbol (str): Unique identifier of the symbol (e.g., 'EURUSD').
                - LastTradeTime (str): Last transaction time (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
                - MarketValue (float): Current market value of the position.
                - Position (float): Net position in shares.
                - netVolume (float): Net volume in lots.

    Examples:
        result = get_positions(
            runmode="livetest",
            accountid="1000",
            token="123456"
        )
        print(f"Total symbols with positions: {result['count']}")
        for symbol, position in result['res'].items():
            print(f"Symbol: {symbol} - Position: {position['Position']} - Market Value: {position['MarketValue']}")
    """
    try:
        from tools import get_positions as _get_positions
        return _get_positions.get_positions(runmode, accountid, token)
    except Exception as e:
        logger.error(f"Unexpected error in get_positions tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_balance(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    """
    Retrieve the latest account balance of a specified trading account.

    This function provides the current financial status of a specified trading account, including net asset value, available balance, and profit/loss information.

    Args:
        accountid (str): The ALGOGENE account ID for which to retrieve the balance.
        runmode (str): The run mode or account type, which can be either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.

    Returns:
        Dict containing:
        - NAV (float): Net Asset Value of the account.
        - available_Balance (float): Remaining balance that is available for trading.
        - margin_Used (float): Capital currently in use.
        - realized_PL (float): Cumulative realized profit/loss.
        - timestamp (str): Last updated time (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
        - unrealized_PL (float): Outstanding unrealized profit/loss.
        - BaseCurrency (str): The base currency of the account.

    Examples:
        result = get_balance(
            accountid="1000",
            runmode="livetest",
            token="123456"
        )
        print(f"Net Asset Value: {result['NAV']}")
        print(f"Available Balance: {result['available_Balance']}")
        print(f"Base Currency: {result['BaseCurrency']}")
    """
    try:
        from tools import get_balance as _get_positions
        return _get_positions.get_balance(runmode, accountid, token)
    except Exception as e:
        logger.error(f"Unexpected error in get_balance tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_opened_trades(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    """
    Retrieve all outstanding open trades for a specified account.

    This function fetches all open trades associated with a specified trading account, providing details on each trade, including direction, instrument, and profit/loss.

    Args:
        accountid (str): The ALGOGENE account ID for which to retrieve open trades.
        runmode (str): Execution mode or account type, which can be either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.

    Returns:
        Dict containing:
        - count (int): Total number of outstanding trades.
        - res (List[Dict]): A list of trades, each containing:
            - timestamp (str): Transaction time (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
            - broker (str): The transacted broker/dealer.
            - buysell (int): Buy/sell direction (1 for buy order, -1 for sell order).
            - instrument (str): The transacted instrument.
            - symbol (str): The transacted symbol (varies for different product types).
            - openclose (str): Status of the trade ('open' or 'close').
            - holdtime (int): Time holding this trade (in seconds, 0 if unspecified).
            - volume (float): Transacted volume in lots.
            - market (str): Security market of the instrument.
            - order_Ref (str): User-customized order reference.
            - price (float): Transacted price.
            - product_type (str): Product type of the instrument.
            - right (str): Option exercise right (if applicable).
            - expiry (str): Contract expiry date (if applicable, format: 'YYYYMMDD').
            - strike (str): Option strike price (if applicable).
            - trade_ID (str): ALGOGENE transaction ID.
            - unrealizedPL (float): Outstanding unrealized profit/loss of this trade.
            - takeProfitLevel (float): Specified take profit level (0 if not specified).
            - stopLossLevel (float): Specified stop loss level (0 if not specified).
            - channel (str): The channel through which this trade was executed ('api', 'web', 'manual').

    Examples:
        result = get_opened_trades(
            accountid="1000",
            runmode="livetest",
            token="123456"
        )
        print(f"Total outstanding trades: {result['count']}")
        for trade in result['res']:
            print(f"Trade ID: {trade['trade_ID']} - Instrument: {trade['instrument']} - Unrealized P/L: {trade['unrealizedPL']}")
    """
    try:
        from tools import get_opened_trades as _get_opened_trades
        return _get_opened_trades.get_opened_trades(runmode, accountid, token)
    except Exception as e:
        logger.error(f"Unexpected error in get_opened_trades tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_pending_trades(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    """
    Retrieve submitted limit orders that are pending to fill.

    This function fetches all limit orders for a specified account that have been submitted but have not yet been executed.

    Args:
        accountid (str): The ALGOGENE account ID for which to retrieve pending trades.
        runmode (str): Execution mode or account type, which can be either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.

    Returns:
        Dict containing:
        - count (int): Total number of limit orders in the pending queue.
        - res (List[Dict]): A list of pending orders, each containing:
            - timestamp (str): Creation timestamp of this limit order (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
            - broker (str): The transacted broker/dealer.
            - buysell (int): Buy/sell direction (1 for buy, -1 for sell).
            - channel (str): Execution channel ('api', 'web', 'manual').
            - instrument (str): The instrument name.
            - symbol (str): The transacted symbol (varies for different product types).
            - expiry (str): Contract expiry date (for FUT/OPT products).
            - right (str): Option exercise right (if applicable).
            - strike (float): Option strike price (if applicable).
            - openclose (str): Indicates if the order is open or close.
            - market (str): The security market of the instrument.
            - product_type (str): Product type of the instrument.
            - price (float): Specified limit price to execute the order.
            - volume (float): Specified volume in lots.
            - trade_ID (str): ALGOGENE transaction ID.
            - holdtime (float): Specified holding time after the limit order is filled (in seconds).
            - stopLossLevel (float): Specified stop loss level after the order is filled.
            - takeProfitLevel (float): Specified take profit level after the order is filled.
            - timeinforce (float): Time before canceling the limit order (in seconds).
            - order_Ref (str): Your specified order reference.

    Examples:
        result = get_pending_trades(
            accountid="1000",
            runmode="livetest",
            token="123456"
        )
        print(f"Total pending trades: {result['count']}")
        for order in result['res']:
            print(f"Order Ref: {order['order_Ref']} - Instrument: {order['instrument']} - Price: {order['price']}")
    """
    try:
        from tools import get_pending_trades as _get_pending_trades
        return _get_pending_trades.get_pending_trades(runmode, accountid, token)
    except Exception as e:
        logger.error(f"Unexpected error in get_pending_trades tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def set_account_config(
    runmode: str,
    accountid: str,
    broker_name: str,
    broker_api: str = "",
    broker_account: str = "",
    broker_user: str = "",
    broker_pwd: str = "",
    broker_server: str = "",
    broker_passphrase: str = ""
) -> Dict[str, Any]:
    """
    Update broker connection settings for your ALGOGENE trading account.

    This function allows you to programmatically update the broker connection settings of your ALGOGENE account. These settings can also be configured manually via the ALGOGENE portal under /settings.

    Args:
        runmode (str): Execution mode or account type, either 'livetest' or 'livetrade'.
        accountid (str): The ALGOGENE account ID to update.
        broker_name (str): The broker to connect. Supported brokers include: 
            "alpaca", "binance", "bitget", "bybit", "whalefin", "coinex", 
            "bingx", "bitrue", "ig", "okx", "kucoin", "bitmart", 
            "tigerbrokers", "hyperliquid", "aftx", "exness", 
            "tickmill", "fpmarkets", "icmarkets", "roboforex", 
            "pepperstone", "gomarkets", "xmglobal".
        broker_api (str, optional): The API key generated from your broker.
        broker_account (str, optional): Your broker account ID.
        broker_user (str, optional): Your broker account's username.
        broker_pwd (str, optional): Your broker account's password.
        broker_server (str, optional): Your broker's specific server.
        broker_passphrase (str, optional): The passphrase generated from your broker.

    Returns:
        Dict containing:
        - res (str): Success message indicating the update status.

    ### Required Parameters for Different Brokers
    - For **AFTX**, **Exness**, **Tickmill**, **FPMarkets**, **ICMarkets**, **RoboForex**, **Pepperstone**, **GoMarkets**, **XMGlobal**:
        - `broker_user`, `broker_pwd`, `broker_server` are required.

    - For **OANDA** and **IG**:
        - `broker_api`, `broker_account`, `broker_user`, `broker_pwd` are required.

    - For **Alpaca**, **Binance**, **Bitget**, **Bybit**, **Whalefin**, **Coinex**, **BingX**, **Bitrue**:
        - `broker_api`, `broker_pwd` are required.

    - For **OKX**, **Kucoin**, **Bitmart**:
        - `broker_api`, `broker_pwd`, `broker_passphrase` are required.

    - For **Tigerbrokers** and **Hyperliquid**:
        - `broker_api`, `broker_account`, `broker_pwd` are required.

    Examples:
    1. **Updating connection for Alpaca**:
        ```
        result = set_account_config(
            runmode = "livetrade",
            accountid = "1234",
            broker_name = "alpaca",
            broker_api = "alpaca_api_key",
            broker_pwd = "alpaca_api_secret"
        )
        print(f"result: {result['res']}")
        ```
       
    2. **Updating connection for IG**:
        ```
        result = set_account_config(
            runmode = "livetrade",
            accountid = "4321",
            broker_name = "ig",
            broker_api = "ig_api_key",
            broker_account = "ig_account",
            broker_user = "ig_user",
            broker_pwd = "ig_password"
        )
        print(f"result: {result['res']}")
        ```
       
    3. **Updating connection for OANDA**:
        ```
        result = set_account_config(
            runmode = "livetrade",
            accountid = "5678",
            broker_name = "oanda",
            broker_api = "oanda_api_key",
            broker_account = "oanda_account"
        )
        print(f"result: {result['res']}")
        ```

    Responses will vary based on the broker and the optional parameters provided. All responses will contain a message indicating the outcome of the update operation.
    """
    try:
        from tools import set_account_config as _set_account_config
        return _set_account_config.set_account_config(runmode, accountid, broker_name, broker_api, broker_account, broker_user, broker_pwd, broker_server, broker_passphrase)
    except Exception as e:
        logger.error(f"Unexpected error in set_account_config tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def query_order(
    runmode: str,
    accountid: str,
    token: str,
    tradeID: str
) -> Dict[str, Any]:
    """
    Query the trade details of an outstanding or pending order.

    This function retrieves information about a specific trade based on the provided trade ID, allowing users to check the status and details of their orders.

    Args:
        accountid (str): The ALGOGENE account ID for which to query the order.
        runmode (str): Execution mode or account type, either 'livetest' or 'livetrade'.
        token (str): The session token obtained via the /session endpoint.
        tradeID (str): The trade ID obtained from the /open_order endpoint.

    Returns:
        Dict containing:
        - status (str): Current status of the order ('PENDING', 'FILLED', 'PARTIAL_FILLED').
        - err_msg (str): Error message if any errors occurred during the request.
        - tradeID (str): The trade ID being queried.
        - orderRef (str): Your specified order reference (if applicable).
        - buysell (int): Buy/sell direction (1 for buy, -1 for sell).
        - price (float): The executed price or limit price of a pending order.
        - volume (float): The executed volume (in lots) or intended trading volume for pending orders.
        - timestamp (str): Creation timestamp of the order (format: 'YYYY-MM-DD hh:mm:ss.ffffff', in UTC).
        - takeProfitLevel (float): Specified take profit level; 0 if not specified.
        - stopLossLevel (float): Specified stop loss level; 0 if not specified.
        - holdtime (float): Specified holding time after the order is filled (in seconds); 0 if not specified.
        - trailingstop (float): Specified trailing stop percentage; 0 if not specified.
        - timeinforce (float): Amount of time before canceling the limit order (in seconds); 0 if not specified.
        - instrument (str): The instrument name.
        - symbol (str): The transacted symbol; varies for different product types.
        - expiry (str): Expiry date for FUT/OPT products; empty for non FUT/OPT.
        - right (str): Option exercise right for OPT products ('C' for call, 'P' for put); empty for non-OPT.
        - strike (float): Option strike price for OPT products; 0 for non-OPT.

    Examples:
    1. **Querying a filled order**:
        ```
        result = query_order(
            runmode = "livetrade",
            accountid = "5678",
            token = "your_session_token",
            tradeID = "1234567890"
        )
        print(f"result: {result}")# Expected response with order details
        ```

    2. **Querying a pending order**:
        ```
        result = query_order(
            runmode = "livetrade",
            accountid = "5678",
            token = "your_session_token",
            tradeID = "0987654321"
        )
        print(f"result: {result}") # Expected response with order details including status 'PENDING'
        ```

    Responses will include the current order status, execution details, and additional parameters as specified, allowing users to make informed trading decisions based on their outstanding or filled orders.
    """
    try:
        from tools import query_order as _query_order
        return _query_order.query_order(runmode, accountid, token, tradeID)
    except Exception as e:
        logger.error(f"Unexpected error in query_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def open_order(
    runmode: str,
    accountid: str,
    token: str,
    instrument: str,
    buysell: int,
    volume: float,
    ordertype: str,
    price: float = 0,
    timeinforce: int = 0,
    takeProfitLevel: float = 0,
    stopLossLevel: float = 0,
    holdtime: int = 0,
    orderRef: str = "",
    callback: str = "",
    expiry: str = "",
    right: str = "",
    strike: float = 0
) -> Dict[str, Any]:
    """
    Open Order API

    This endpoint allows users to open a trading order on the ALGOGENE platform. Users must provide necessary authentication and order information to successfully create an order.

    Args:
        token (string): Required. The token obtained via the /session endpoint for authentication.
        runmode (string): Required. The execution mode or account type, which can be either 'livetest' or 'livetrade'.
        accountid (string): Required. Your ALGOGENE account ID.
        instrument (string): Required. The name of the trading instrument (e.g., "EURUSD").
        expiry (string): Optional. For futures/options products, specify the contract expiry date.
        right (string): Optional. For options products, specify the option exercise right, 'C' for call and 'P' for put.
        strike (string): Optional. For options products, specify the option strike price.
        buysell (string): Required. Indicates the buy/sell direction; value can be either 'BUY' or 'SELL'.
        volume (number): Required. The intended trading volume in the number of lots (e.g., 0.01).
        ordertype (string): Required. The type of order; options include 'MKT' for market order, 'LMT' for limit order, or 'STOP' for stop order.
        price (number): Optional. Specify the limit/stop price; only applicable to limit/stop orders.
        timeinforce (integer): Optional. For limit/stop orders, specify the maximum number of seconds to wait before auto-cancelling the order if not filled.
        takeProfitLevel (number): Optional. Specify the take profit level if this order has been opened.
        stopLossLevel (number): Optional. Specify the stop loss level if this order has been opened.
        holdtime (integer): Optional. Specify the holding time (in seconds) if this order has been opened.
        orderRef (string): Optional. Your reference/message attached to this order; ignore if not specified.
        callback (string): Optional. Your publicly accessible callback URL for receiving asynchronous messages; ignore if not specified.

    Returns:
        Dict containing:
        - status (string): The current status of the order (e.g., "PENDING_TO_FILL").
        - timestamp_utc (string): The system update time in the format 'YYYY-MM-DD hh:mm:ss.ffffff', time zone in UTC.
        - tradeID (string): The system-generated transaction ID for tracking the order status.

    Examples:
        # Example 1: Opening a Market Order
        result = open_order(
            runmode = "livetrade",
            accountid = "1001",
            token = "123456",
            instrument = "EURUSD",
            buysell = "BUY",
            volume = 0.01,
            ordertype = "MKT",
            stopLossLevel = 147.00,
            orderRef = "my_order_abcd1234"
        )
        print(f"result: {result}")

        # Possible response:
        # {
        #   "status": "PENDING_TO_FILL",
        #   "timestamp_utc": "2020-09-06 06:46:22.504000",
        #   "tradeID": "12345678"
        # }

        # Example 2: Opening a Limit Order with Take Profit and Stop Loss
        result = open_order(
            runmode = "livetrade",
            accountid = "1001",
            token = "123456",
            instrument = "AAPL",
            buysell = "SELL",
            volume = 1,
            ordertype = "LMT",
            price = 145.00,
            takeProfitLevel = 140.00,
            stopLossLevel = 147.00
        )
        print(f"result: {result}")

        # Possible response:
        # {
        #   "status": "PENDING_TO_FILL",
        #   "timestamp_utc": "2020-09-06 06:46:22.504000",
        #   "tradeID": "12345679"
        # }
    """
    try:
        from tools import open_order as _open_order
        return _open_order.open_order(runmode, accountid, token, instrument, buysell, volume, ordertype, price, timeinforce, takeProfitLevel, stopLossLevel, holdtime, orderRef, callback, expiry, right, strike)
    except Exception as e:
        logger.error(f"Unexpected error in open_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def update_pending_order(
    runmode: str,
    accountid: str,
    token: str,
    tradeID: str,
    price: float = 0,
    timeinforce: int = 0,
    takeProfitLevel: float = 0,
    stopLossLevel: float = 0,
    holdtime: int = 0,
    orderRef: str = "",
    callback: str = ""
) -> Dict[str, Any]:
    """
    Update Pending Order

    This function updates the trading parameters of an unfilled limit or stop order on the ALGOGENE platform. By providing the necessary information, users can modify various aspects of their pending orders.

    Args:
        runmode (string): Required. The execution mode or account type, which can be either 'livetest' or 'livetrade'.
        accountid (string): Required. Your ALGOGENE account ID.
        token (string): Required. The token obtained via the /session endpoint for authorization.
        tradeID (string): Required. The ALGOGENE trade ID that can be obtained from the /pending_trades endpoint.
        orderRef (string): Optional. A new reference for the order; skip this parameter if no update is required.
        callback (string): Optional. A new callback URL for receiving asynchronous messages; skip this parameter if no update is required.
        price (number): Optional. A new limit price; skip this parameter if no update is required.
        takeProfitLevel (number): Optional. A new take profit level after the limit order has been filled; skip if not needed.
        stopLossLevel (number): Optional. A new stop loss level after the limit order has been filled; skip if not needed.
        holdtime (integer): Optional. A new holding time (number of seconds) after the limit order has been filled; skip if not needed.
        timeinforce (integer): Optional. A new time-in-force value for the limit order; skip if not needed.

    Returns:
        Dict containing:
        - status (string): The current status of the operation (e.g., "SUCCESS").
        - res (string): A message indicating the result of the update request.

    Examples:
        # Example 1: Update Price and Reference of a Pending Order
        result = update_pending_order(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            tradeID="403",
            price=1.1,
            orderRef="my new reference"
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for pending order update!"
        # }

        # Example 2: Update Stop Loss and Hold Time of a Pending Order
        result = update_pending_order(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            tradeID="403",
            stopLossLevel=1.05,
            holdtime=3600
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for pending order update!"
        # }

        # Example 3: Update Callback URL of a Pending Order
        result = update_pending_order(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            tradeID="403",
            callback="https://example.com/callback"
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for pending order update!"
        # }
    """
    try:
        from tools import update_pending_order as _update_pending_order
        return _update_pending_order.update_pending_order(runmode, accountid, token, tradeID, price, timeinforce, takeProfitLevel, stopLossLevel, holdtime, orderRef, callback)
    except Exception as e:
        logger.error(f"Unexpected error in update_pending_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def update_opened_order(
    runmode: str,
    accountid: str,
    token: str,
    tradeID: str,
    takeProfitLevel: float = 0,
    stopLossLevel: float = 0,
    holdtime: int = 0,
    orderRef: str = "",
    callback: str = ""
) -> Dict[str, Any]:
    """
    Update Opened Order

    This function updates the trading parameters of an outstanding or opened order on the ALGOGENE platform. Users can modify aspects such as take profit, stop loss levels, and references for their active orders.

    Args:
        runmode (string): Required. The execution mode or account type, either 'livetest' or 'livetrade'.
        accountid (string): Required. Your ALGOGENE account ID.
        token (string): Required. The token obtained via the /session endpoint for authorization.
        tradeID (string): Required. The ALGOGENE trade ID that can be obtained from the /opened_trades endpoint.
        callback (string): Optional. A new callback URL for receiving asynchronous messages; skip this parameter if no update is required.
        orderRef (string): Optional. A new reference for the order; skip this parameter if no update is required.
        takeProfitLevel (number): Optional. A new take profit level; skip this parameter if no update is required.
        stopLossLevel (number): Optional. A new stop loss level; skip this parameter if no update is required.
        holdtime (number): Optional. A new holding time in seconds; skip this parameter if no update is required.

    Returns:
        Dict containing:
        - status (string): The current status of the operation (e.g., "SUCCESS").
        - res (string): A message indicating the result of the update request.

    Examples:
        # Example 1: Update Take Profit Level and Reference of an Opened Order
        result = update_opened_order(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeID="366",
            takeProfitLevel=0.9,
            orderRef="my new reference"
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for order update!"
        # }

        # Example 2: Update Stop Loss Level and Hold Time of an Opened Order
        result = update_opened_order(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeID="366",
            stopLossLevel=0.85,
            holdtime=300  # Set hold time to 5 minutes
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for order update!"
        # }

        # Example 3: Update Callback URL of an Opened Order
        result = update_opened_order(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeID="366",
            callback="https://example.com/callback"  # Update to a new callback URL
        )
        print(f"Update Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for order update!"
        # }
    """
    try:
        from tools import update_opened_order as _update_opened_order
        return _update_opened_order.update_opened_order(runmode, accountid, token, tradeID, takeProfitLevel, stopLossLevel, holdtime, orderRef, callback)
    except Exception as e:
        logger.error(f"Unexpected error in update_opened_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"





@mcp.tool()
def cancel_orders(
    runmode: str,
    accountid: str,
    token: str,
    tradeIDs: str
) -> Dict[str, Any]:
    """
    Cancel Orders

    This function cancels a set of unfilled limit orders on the ALGOGENE platform. Users can specify multiple trade IDs to cancel their pending orders efficiently.

    Args:
        runmode (string): Required. The execution mode or account type, either 'livetest' or 'livetrade'.
        accountid (string): Required. Your ALGOGENE account ID.
        token (string): Required. The token obtained via the /session endpoint for authorization.
        tradeIDs (string): Required. A comma-separated list of ALGOGENE trade IDs corresponding to the unfilled limit or stop orders you want to cancel.

    Returns:
        Dict containing:
        - status (string): The current status of the operation (e.g., "SUCCESS").
        - res (string): A message indicating the result of the cancellation request.

    Examples:
        # Example 1: Cancel Multiple Orders
        result = cancel_orders(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeIDs="192,193,194"
        )
        print(f"Cancellation Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for BULK_CANCEL"
        # }

        # Example 2: Cancel a Single Order (as part of multiple orders)
        result = cancel_orders(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeIDs="195"
        )
        print(f"Cancellation Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for BULK_CANCEL"
        # }

        # Example 3: Cancel All Pending Orders (if they are known)
        result = cancel_orders(
            runmode="livetrade",
            accountid="1002",
            token="123456",
            tradeIDs="196,197,198,199,200"  # Cancelling several at once
        )
        print(f"Cancellation Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted for BULK_CANCEL"
        # }
    """
    try:
        from tools import cancel_orders as _cancel_orders
        return _cancel_orders.cancel_orders(runmode, accountid, token, tradeIDs)
    except Exception as e:
        logger.error(f"Unexpected error in cancel_orders tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def close_orders(
    runmode: str,
    accountid: str,
    token: str,
    tradeIDs: str = "",
    orderRef: str = ""
) -> Dict[str, Any]:
    """
    Close Orders

    This function closes a set of outstanding orders on the ALGOGENE platform. Users can specify multiple trade IDs or an order reference to close their trades efficiently.

    Args:
        runmode (string): Required. The execution mode or account type, either 'livetest' or 'livetrade'.
        accountid (string): Required. Your ALGOGENE account ID.
        token (string): Required. The token obtained via the /session endpoint for authorization.
        tradeIDs (string): Optional. A comma-separated list of ALGOGENE trade IDs corresponding to the orders you want to close; either this or orderRef must be provided.
        orderRef (string): Optional. A user-defined reference for the orders to close; either this or tradeIDs must be provided.

    Returns:
        Dict containing:
        - status (string): The current status of the operation (e.g., "SUCCESS").
        - res (string): A message indicating the result of the close order request.

    Examples:
        # Example 1: Close Multiple Orders Using Trade IDs
        result = close_orders(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            tradeIDs="192,193,194,195"
        )
        print(f"Close Order Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted close order request for '1234567890'"
        # }

        # Example 2: Close Orders Using Order Reference
        result = close_orders(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            orderRef="my_order_ref"  # Close all trades with this reference
        )
        print(f"Close Order Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted close order request for '1234567890'"
        # }

        # Example 3: Close Orders Using Both Trade IDs and Order Reference (though only one is required)
        result = close_orders(
            runmode="livetrade",
            accountid="1001",
            token="123456",
            tradeIDs="196,197,198",
            orderRef="optional_order_ref"  # This is optional and ignored if tradeIDs are provided
        )
        print(f"Close Order Status: {result['status']}, Message: {result['res']}")
        # Expected response:
        # {
        #   "status": "SUCCESS",
        #   "res": "Submitted close order request for '1234567890'"
        # }
    """
    try:
        from tools import close_orders as _close_orders
        return _close_orders.close_orders(runmode, accountid, token, tradeIDs, orderRef)
    except Exception as e:
        logger.error(f"Unexpected error in close_orders tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def backtest_run(
    code: str,
    settings: object
) -> Dict[str, Any]:
    """
    Run a backtest strategy on the ALGOGENE platform.

    This function submits a backtest script along with the necessary configuration settings to run a backtest for a specified trading strategy.

    Args:
    - settings (object): Configuration settings for the strategy, which includes:
      - strategyName (string): Name of your trading strategy.
      - subscribeList (array): List of instruments that your strategy will trade on.
      - StartDate (string): Backtest start date in the format of YYYY-MM.
      - EndDate (string): Backtest end date in the format of YYYY-MM.
      - InitialCapital (number): Initial capital amount (must be >= 0).
      - BaseCurrency (string): Base currency of your strategy.
      - risk_free (number): Risk-free rate (e.g., input 0.01 for 1%).
      - Leverage (number): Account leverage (must be >= 0).
      - allowShortSell (boolean): Set to true if your strategy allows short selling.
      - dataset (integer): Data granularity for backtesting (0 for tick data; 1 for 1-min data; 5 for 5-min data; 60 for 1-hour data; 1440 for 1-day data).
      - isPositionBaseEnv (boolean): Set to true for position netting environment; false for order based environment.
      - isNewsFeedOn (boolean): Set to true to enable news event stream.
      - isEconstatFeedon (boolean): Set to true to enable economics data stream.
      - isWeatherFeedOn (boolean): Set to true to enable weather data stream.

    - code (string): Your backtest script written in the appropriate programming language.

    Returns:
    Dict containing:
    - status (bool): Returns true if the backtest script has been submitted successfully.
    - task_id (string): The task ID that can be used to monitor the running status on the platform.

    Examples:
    1. Run a grid trading strategy backtest:
       result = backtest_run(
           settings={
               "strategyName": "grid trading",
               "subscribeList": ["XAUUSD"],
               "StartDate": "2025-01",
               "EndDate": "2025-12",
               "InitialCapital": 10000,
               "BaseCurrency": "USD",
               "risk_free": 0,
               "Leverage": 1,
               "allowShortSell": True,
               "dataset": 1440,
               "isPositionBaseEnv": False,
               "isNewsFeedOn": False,
               "isEconstatFeedon": False,
               "isWeatherFeedOn": False
           },
           code="from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest\nfrom datetime import datetime, timedelta\nimport numpy as np\nimport pandas as pd\nimport pandas_ta as ta\n\nclass AlgoEvent:\n    def __init__(self):\n        self.timer = datetime(1970,1,1)\n        self.grid_setup_time = datetime(1970,1,1)\n        self.grid_size_pct = 0.01\n        self.grid_num = 5\n        self.tp_pct = 0.01\n        self.sl_pct = 0.01\n        self.numObs = 30\n        self.is_runningGrid = False\n        self.trade_size = 0.1\n\n    # Additional methods omitted for brevity\n    ...\n"
       )
       print(f"Backtest submitted successfully, Task ID: {result['task_id']}")
    """
    try:
        from tools import backtest_run as _backtest_run
        return _backtest_run.backtest_run(code, settings)
    except Exception as e:
        logger.error(f"Unexpected error in backtest_run tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def backtest_cancel(
    task_id: str
) -> Dict[str, Any]:
    """
    Cancel a running backtest task on the ALGOGENE platform.

    This function cancels a backtest that is currently running based on the given task ID.

    Args:
    - task_id: the task ID obtained from the /run_backtest endpoint

    Returns:
    Dict containing:
    - status (boolean): Returns true if the backtest script has been submitted to the system for cancellation
    - res (string): System message indicating the result, e.g., 'canceled' for successfully canceled the backtest

    Examples:
    result = backtest_cancel(task_id="1771596582631443")
    if result['status']:
        print("Backtest task canceled:", result['res'])
    else:
        print("Failed to cancel backtest task.")
    """
    try:
        from tools import backtest_cancel as _backtest_cancel
        return _backtest_cancel.backtest_cancel(task_id)
    except Exception as e:
        logger.error(f"Unexpected error in backtest_cancel tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def get_task_status(
    task: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Get the status of a system task on the ALGOGENE platform.

    This function queries the status of a specific task, such as a backtest.

    Args:
    api_key: your API key
    task: the related task category (e.g., 'backtest')
    task_id: the task ID obtained from the /run_backtest endpoint
    user: your user ID generated by ALGOGENE at system registration

    Returns:
    Dict containing:
    - status (boolean): Returns true for a successful API call
    - res (list of strings): The current status of the given task

    Examples:
    result = get_task_status(task="backtest", task_id="1771596582631443")
    if result['status']:
        print("Task status:", result['res'])
    else:
        print("Failed to retrieve task status.")
    """
    try:
        from tools import get_task_status as _get_task_status
        return _get_task_status.get_task_status(task, task_id)
    except Exception as e:
        logger.error(f"Unexpected error in get_task_status tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_trade(
    runmode: str,
    runtime_id: str,
    acdate: str,
    orderRef: str = ""
) -> Dict[str, Any]:
    """
    History of Transactions

    This function retrieves the complete transaction history of a particular trading strategy on the ALGOGENE platform. Users can filter the results based on specific parameters such as date and order reference.

    Args:
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.
        acdate (string): Optional. The accounting date to retrieve transaction details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.
        orderRef (string): Optional. A user-defined order reference to filter the transactions; can be left empty for all transactions.

    Returns:
        Dict containing:
        - count (integer): The number of transactions returned in the result.
        - res (list): A list of JSON objects representing the transaction details, sorted in ascending time.

    Examples:
        # Example 1: Get Transaction History for a Specific Date
        result = history_of_transactions(
            runtime_id="1000",
            runmode="livetest",
            acdate="2020-09-14"
        )
        print(f"Transaction Count: {result['count']}")
        for transaction in result['res']:
            print(f"Trade ID: {transaction['trade_ID']}, Price: {transaction['price']}, Volume: {transaction['volume']}")

        # Example 2: Get Complete Transaction History Without Date Filtering
        result = history_of_transactions(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Transaction Count: {result['count']}")
        for transaction in result['res']:
            print(f"Trade ID: {transaction['trade_ID']}, Timestamp: {transaction['timestamp']}")

        # Example 3: Get Transaction History with Order Reference
        result = history_of_transactions(
            runtime_id="1000",
            runmode="livetrade",
            orderRef="my new reference"  # Filter by user-defined order reference
        )
        print(f"Transaction Count: {result['count']}")
        for transaction in result['res']:
            if transaction['order_ref'] == "my new reference":
                print(f"Trade ID: {transaction['trade_ID']}, Price: {transaction['price']}")
    """
    try:
        from tools import strategy_trade as _strategy_trade
        return _strategy_trade.strategy_trade(runmode, runtime_id, acdate, orderRef)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_trade tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_bal(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    """
    History of Daily Account Balance

    This function retrieves the history of account balance and margin usage for a particular trading strategy on the ALGOGENE platform. Users can request balance details for specific dates or the full history.

    Args:
        acdate (string): Required. The accounting date to retrieve details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.

    Returns:
        Dict containing:
        - count (integer): The number of records returned in the result.
        - res (list): A list of JSON objects representing account balance details sorted in ascending order by date.

    Examples:
        # Example 1: Get Account Balance History for a Specific Date
        result = history_of_daily_account_balance(
            acdate="2020-09-14",
            runtime_id="1000",
            runmode="livetest"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, NAV: {record['NAV']}, Available Balance: {record['available_Balance']}")

        # Example 2: Get Full Account Balance History without Date Filtering
        result = history_of_daily_account_balance(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, NAV: {record['NAV']}")

        # Example 3: Get Account Balance History for a Specific Date with Non-existing Date
        result = history_of_daily_account_balance(
            acdate="2022-01-01",  # Assuming no records exist for this date
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}, No records returned for the specified date.")
    """
    try:
        from tools import strategy_bal as _strategy_bal
        return _strategy_bal.strategy_bal(runmode, runtime_id, acdate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_bal tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_pos(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    """
    History of Daily Outstanding Inventory

    This function retrieves the daily history of positions for a particular trading strategy on the ALGOGENE platform. Users can request inventory details for specific dates or the full history.

    Args:
        acdate (string): Required. The accounting date to retrieve details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.

    Returns:
        Dict containing:
        - count (integer): The number of records returned in the result.
        - res (list): A list of JSON objects representing the outstanding inventory details sorted in ascending order by date.

    Examples:
        # Example 1: Get Inventory History for a Specific Date
        result = history_of_daily_outstanding_inventory(
            acdate="2020-09-14",
            runtime_id="1000",
            runmode="livetest"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, HKXHKD Inventory: {record['HKXHKD']}")

        # Example 2: Get Full Inventory History without Date Filtering
        result = history_of_daily_outstanding_inventory(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, HKXHKD Inventory: {record['HKXHKD']}")

        # Example 3: Get Inventory History for a Future Date (e.g., no records exist)
        result = history_of_daily_outstanding_inventory(
            acdate="2023-01-01",  # Assuming no records exist for this date
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}, No records returned for the specified date.")
    """
    try:
        from tools import strategy_pos as _strategy_pos
        return _strategy_pos.strategy_pos(runmode, runtime_id, acdate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_pos tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_pl(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    """
    History of Daily Cumulative P/L

    This function retrieves the history of daily cumulative profit/loss (P/L) for a specific trading strategy on the ALGOGENE platform. Users can request P/L details for specific accounting dates or retrieve the full history.

    Args:
        acdate (string): Required. The accounting date to retrieve details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.

    Returns:
        Dict containing:
        - count (integer): The number of records returned in the result.
        - res (list): A list of JSON objects containing cumulative P/L details sorted in ascending order by date.

    Examples:
        # Example 1: Get Cumulative P/L History for a Specific Date
        result = history_of_daily_cumulative_pl(
            acdate="2020-09-14",
            runtime_id="1000",
            runmode="livetest"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, Total P/L: {record['TotalPL']}")

        # Example 2: Get Full Cumulative P/L History without Date Filtering
        result = history_of_daily_cumulative_pl(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}")
        for record in result['res']:
            print(f"Date: {record['Acdate']}, HKXHKD P/L: {record['HKXHKD']}, Total P/L: {record['TotalPL']}")

        # Example 3: Get Cumulative P/L History for a Non-existent Date
        result = history_of_daily_cumulative_pl(
            acdate="2023-01-01",  # Assuming no records exist for this date
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Record Count: {result['count']}, No records returned for the specified date.")
    """
    try:
        from tools import strategy_pl as _strategy_pl
        return _strategy_pl.strategy_pl(runmode, runtime_id, acdate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_pl tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_cashflow(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    """
    History of Account Cashflow

    This function retrieves the history of cashflow events (such as deposits, withdrawals, dividend payments, etc.) for a particular account or trading strategy on the ALGOGENE platform. Users can request cashflow details for specific accounting dates or retrieve the full history.

    Args:
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.
        acdate (string): Optional. The accounting date to retrieve details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.

    Returns:
        Dict containing:
        - count (integer): The number of cashflow events returned in the result.
        - res (list): A list of JSON objects representing the cashflow events, including date, amount, and event type.

    Examples:
        # Example 1: Get Cashflow History for a Specific Date
        result = history_of_account_cashflow(
            runtime_id="1000",
            runmode="livetest",
            acdate="2020-09-14"
        )
        print(f"Cashflow Event Count: {result['count']}")
        for cashflow in result['res']:
            print(f"Date: {cashflow['Acdate']}, Amount: {cashflow['Cash_flow']}, Event: {cashflow['Event']}")

        # Example 2: Get Full Cashflow History Without Date Filtering
        result = history_of_account_cashflow(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Cashflow Event Count: {result['count']}")
        for cashflow in result['res']:
            print(f"Date: {cashflow['Acdate']}, Amount: {cashflow['Cash_flow']}, Event: {cashflow['Event']}")

        # Example 3: Get Cashflow History for a Date with No Events
        result = history_of_account_cashflow(
            runtime_id="1000",
            runmode="livetrade",
            acdate="2023-01-01"  # Assuming no records exist for this date
        )
        print(f"Cashflow Event Count: {result['count']}, No cashflow events returned for the specified date.")
    """
    try:
        from tools import strategy_cashflow as _strategy_cashflow
        return _strategy_cashflow.strategy_cashflow(runmode, runtime_id, acdate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_cashflow tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_stats(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    """
    Settings & Performance Statistics

    This function retrieves the settings and performance statistics of a specific trading strategy on the ALGOGENE platform. Users can request details based on a specific accounting date or fetch the entire history.

    Args:
        acdate (string): Required. The accounting date for which to retrieve the details, formatted as "YYYY-MM-DD"; omitted or empty will return the full history.
        runmode (string): Required. The strategy run mode, which can be either 'backtest', 'livetest', or 'livetrade'.
        runtime_id (string): Required. The backtest strategy runtime ID or account ID for livetest/livetrade.

    Returns:
        Dict containing:
        - settings (object): A JSON object containing the initial settings of the strategy.
        - performance (object): A JSON object containing the performance statistics of the strategy.

    Examples:
        # Example 1: Get Settings and Performance Statistics for a Specific Date
        result = get_strategy_stats(
            acdate="2020-09-14",
            runtime_id="1000",
            runmode="livetest"
        )
        print(f"Strategy Name: {result['settings']['strategyName']}")
        print(f"Total PnL: {result['performance']['TotalPnL']}")
        print(f"Annual Sharpe Ratio: {result['performance']['AnnualSharpe']}")

        # Example 2: Get Full Settings and Performance Statistics without Date Filtering
        result = get_strategy_stats(
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"Base Currency: {result['settings']['BaseCurrency']}")
        print(f"Number of Trades: {result['performance']['TradeCnt']}")

        # Example 3: Get Settings and Performance for a Date with No Data Available
        result = get_strategy_stats(
            acdate="2023-01-01",  # Assuming no records exist for this date
            runtime_id="1000",
            runmode="livetrade"
        )
        print(f"No statistics available for the specified date: {result['settings']}, {result['performance']}")
    """
    try:
        from tools import strategy_stats as _strategy_stats
        return _strategy_stats.strategy_stats(runmode, runtime_id, acdate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_stats tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def strategy_logs(
    runmode: str,
    runtime_id: str
) -> Dict[str, Any]:
    """
    Get the system logs for your algo strategy on ALGOGENE.

    vim
    This function queries the system logs for your algorithmic strategy, whether it is a backtest or a live running script.

    Args:
    runtime_id: The backtest strategy runtime ID, or livetest/livetrade account ID (string, required)
    runmode: The strategy run mode, which can either be 'backtest', 'livetest', or 'livetrade' (string, required)

    Returns:
    Dict containing:
    - res (string): The full system log messages. For performance reasons, only the most recent 2000 log messages are returned.

    Examples:
    result = get_system_logs(runtime_id="20260225_123450_240000", runmode="backtest")
    print(f"System logs:\n{result['res']}")

    result = get_system_logs(runtime_id="1000", runmode="livetest")
    print(f"System logs:\n{result['res']}")

    result = get_system_logs(runtime_id="1003", runmode="livetrade")
    print(f"System logs:\n{result['res']}")
    """
    try:
        from tools import strategy_logs as _strategy_logs
        return _strategy_logs.strategy_logs(runmode, runtime_id)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_logs tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

@mcp.tool()
def strategy_market_perf(
    symbol: str,
    startDate: str,
    endDate: str
) -> Dict[str, Any]:
    """
    Market Index Performance

    This function evaluates a simple buy-and-hold strategy for a specified financial instrument over a defined period on the ALGOGENE platform. Users can request performance statistics based on specific start and end dates.

    Args:
        startDate (string): Required. The starting date for performance evaluation, formatted as "YYYY-MM-DD".
        endDate (string): Required. The end date for performance evaluation, formatted as "YYYY-MM-DD".
        symbol (string): Required. The market index name or underlying symbol name defined in /list_all_instrument.

    Returns:
        Dict containing:
        - res (object): A JSON object of market performance statistics.

    Examples:
        # Example 1: Evaluate Performance for a Specific Market Index
        result = strategy_market_perf(
            startDate="2020-01-01",
            endDate="2020-12-31",
            symbol="S&P500"
        )
        print(f"Total PnL: {result['res']['TotalPnL']}")
        print(f"Annual Sharpe Ratio: {result['res']['AnnualSharpe']}")
        print(f"Win Rate: {result['res']['WinRate']}")

        # Example 2: Evaluate Performance for a Different Market Index
        result = strategy_market_perf(
            startDate="2021-06-01",
            endDate="2021-12-31",
            symbol="NASDAQ"
        )
        print(f"Annual Sortino Ratio: {result['res']['AnnualSortino']}")
        print(f"Average Daily Return: {result['res']['MeanDailyReturn']}")

        # Example 3: Query Performance for a Date Range with No Trading Activity
        result = strategy_market_perf(
            startDate="2023-01-01",
            endDate="2023-01-31",
            symbol="FTSE100"
        )
        print(f"No trading activity found. Data: {result['res']}")
    """
    try:
        from tools import strategy_market_perf as _strategy_market_perf
        return _strategy_market_perf.strategy_market_perf(symbol, startDate, endDate)
    except Exception as e:
        logger.error(f"Unexpected error in strategy_market_perf tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def app_predict_sentiment(
    sentences: List[str],
) -> Dict[str, Any]:
    """
    Predict Sentiment of Sentences

    This function evaluates the sentiment of provided sentences or paragraphs and returns sentiment scores indicating positive, negative, or neutral sentiments.

    Args:
        sentences (array): Required. An array of sentences or paragraphs for sentiment analysis.
        user (string): Required. Your user ID generated by ALGOGENE at system registration.
        api_key (string): Required. Your API key for authentication.

    Returns:
        Dict containing:
        - status (boolean): Indicates the success of the request; true if successful.
        - res (array): An array of sentiment scores for each sentence, where each score is represented as:
            - Positive score
            - Negative score
            - Neutral score

    Examples:
        # Example 1: Analyze Sentiment of Multiple Sentences
        result = app_predict_sentiment(
            sentences=[
                "Hong Kong's leader has said the financial hub will not uphold sanctions with 'no legal basis'.",
                "Mordashov, a billionaire steel magnate, is among several wealthy Russians sanctioned."
            ]
        )
        print(f"Status: {result['status']}")
        print("Sentiment Scores:")
        for score in result['res']:
            print(f"Positive: {score[0]}, Negative: {score[1]}, Neutral: {score[2]}")

        # Example 2: Analyze Sentiment of Longer Text
        result = app_predict_sentiment(
            sentences=[
                "The economy is recovering slowly from the impacts of the pandemic, and consumer confidence is on the rise."
            ]
        )
        print(f"Status: {result['status']}")
        print(f"Sentiment Scores: {result['res']}")

        # Example 3: Send an Empty Array
        result = app_predict_sentiment(
            sentences=[]
        )
        print(f"Status: {result['status']}")  # Expecting the status to be true
        print("Sentiment Scores: No sentences provided.")
    """
    try:
        from tools import app_predict_sentiment as _app_predict_sentiment
        return _app_predict_sentiment.app_predict_sentiment(sentences)
    except Exception as e:
        logger.error(f"Unexpected error in app_predict_sentiment tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_asset_allocation(
    StartDate: str,
    EndDate: str,
    symbols: list[str],
    risk_tolerance: float,
    allowShortSell: bool
) -> Dict[str, Any]:
    """
    Allocate an optimal portfolio based on risk analysis.

    This function analyzes the risk profile of chosen financial instruments and generates the optimal portfolio allocation over a specified date range.

    Args:
        start_date: The start date of the analysis horizon in 'yyyy-mm-dd' format (must be less than today's date).
        end_date: The end date of the analysis horizon in 'yyyy-mm-dd' format (must be less than today's date).
        symbols: A list of financial instruments (e.g., stocks) to be included in the portfolio.
        risk_tolerance: The maximum risk tolerance level (in %) as a positive number.
        allow_short_sell: Boolean indicating whether short selling is allowed for the portfolio.

    Returns:
    Dict containing:
    - status (boolean): Indicates whether the allocation was successful.
    - res (object): Contains the results of the analysis including:
      - port_risk (float): Estimated portfolio risk or volatility of the optimal allocation.
      - port_return (float): Estimated annual return of the optimal allocation.
      - weights (object): The optimal asset allocation weights; total must sum to 1 (negative weight indicates short selling).

    # Example 1: Successful Portfolio Allocation:
    result = app_asset_allocation("2020-01-01", "2020-12-31", ["AAPL", "GOOG", "MSFT", "TSLA"], 0.3, False)
    print(f"Allocation successful: {result['status']}")
    print(f"Estimated Portfolio Return: {result['res']['port_return']}")
    print(f"Estimated Portfolio Risk: {result['res']['port_risk']}")
    print(f"Optimal Weights: {result['res']['weights']}")

    # Example 2: Portfolio Allocation with Short Selling Allowed:
    result = app_asset_allocation("2021-01-01", "2021-12-31", ["AMZN", "NFLX", "FB"], 0.25, True)
    print(f"Allocation successful: {result['status']}")
    print(f"Estimated Portfolio Return: {result['res']['port_return']}")
    print(f"Estimated Portfolio Risk: {result['res']['port_risk']}")
    print(f"Optimal Weights: {result['res']['weights']}")

    # Example 3: Invalid Dates:
    result = app_asset_allocation("2022-01-01", "2022-01-01", ["AAPL", "TSLA"], 0.2, False)
    # This will return an error since start and end dates must be in the past, and the same date is not valid.
    print(f"Allocation successful: {result['status']}")
    print(f"Error Status: {result['res']['status']}")
    """
    try:
        from tools import app_asset_allocation as _app_asset_allocation
        return _app_asset_allocation.app_asset_allocation(StartDate, EndDate, symbols, risk_tolerance, allowShortSell)
    except Exception as e:
        logger.error(f"Unexpected error in app_asset_allocation tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_fourier_prediction(
    instrument: str,
    numForc: int,
    timestamp: str
) -> Dict[str, Any]:
    """
    Forecast future price movement using Fourier analysis on a specified financial instrument.

    This function estimates the range of future price movements using Fourier transformation based on the provided parameters.

    Args:
        instrument: the target financial instrument (e.g., "AAPL" for Apple Inc.)
        numForc: the number of forecast periods in days (integer)
        timestamp: (optional) the forecast date in 'YYYY-MM-DD' format. If omitted, the current date will be used.

    Returns:
    Dict containing:
    - status (bool): Indicates success of the request
    - res (object): Forecast range
      - lower (float): Lower bound of the forecasted price series
      - upper (float): Upper bound of the forecasted price series

    Examples:
    result = app_fourier_prediction("AAPL", 30, "2022-11-30") 
    print(f"Forecasted price range for AAPL: ${result['res']['lower']} to ${result['res']['upper']}")

    result = app_fourier_prediction("GOOGL", 15)  
    print(f"Forecasted price range for GOOGL: ${result['res']['lower']} to ${result['res']['upper']}")
    """
    try:
        from tools import app_fourier_prediction as _app_fourier_prediction
        return _app_fourier_prediction.app_fourier_prediction(instrument, numForc, timestamp)
    except Exception as e:
        logger.error(f"Unexpected error in app_fourier_prediction tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_market_classifer(
    instrument: str,
    timestamp: str = ""
) -> Dict[str, Any]:
    """
    Estimate the market state (bull or bear) for a specified financial instrument using a Support Vector Machine approach.

    This function determines whether the current market price is above or below the bull-bear line and provides relevant metrics.

    Args:
    instrument: the financial instrument name (e.g., "AAPL" for Apple Inc.)
    timestamp: (optional) the time-in-point estimation in 'YYYY-MM-DD' format. If omitted, the current day will be used.

    Returns:
    Dict containing:
    - status (bool): Indicates the success of the request
    - res (object): Classification results
      - state (string): The market state, either "bull" or "bear"
      - BullBearLine (float): The current bull-bear line of the underlying instrument
      - distance_pct (float): The percentage distance between the current market price and the Bull-Bear Line

    Examples:
    result = app_market_classifer("HKXHKD", "2023-01-20") 
    print(f"Market state for HKXHKD: {result['res']['state']}, Bull-Bear Line: {result['res']['BullBearLine']}, Distance: {result['res']['distance_pct']}%")

    result = app_market_classifer("AAPL")  
    print(f"Market state for AAPL: {result['res']['state']}, Bull-Bear Line: {result['res']['BullBearLine']}, Distance: {result['res']['distance_pct']}%")
    """
    try:
        from tools import app_market_classifer as _app_market_classifer
        return _app_market_classifer.app_market_classifer(instrument, timestamp)
    except Exception as e:
        logger.error(f"Unexpected error in app_market_classifer tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_us_company_filing_hitory(
    ticker: str
) -> Dict[str, Any]:
    """
    Get the filing history for a specified US stock symbol from the SEC.

    This function retrieves the latest and historical SEC filing records for a given corporate document from the U.S. Securities and Exchange Commission since 1994.

    Args:
    ticker: the US stock symbol (e.g., "AAPL" for Apple Inc.)

    Returns:
    Dict containing:
    - status (bool): success status returning true if successful
    - res (list): A list of filing records, where each record is an object containing:
      - filingDate (str): The date the filing was made, in format 'YYYY-MM-DD'.
      - reportDate (str): The date of the reporting period, in format 'YYYY-MM-DD'.
      - report (str): The URL link to the official filing report on the SEC.

    Examples:
    result = app_us_company_filing_hitory("AAPL") # retrieves filing history for Apple Inc.
    if result['status']:
        for filing in result['res']:
            print(f"Filing Date: {filing['filingDate']}, Report Date: {filing['reportDate']}, Report Link: {filing['report']}")
    """
    try:
        from tools import app_us_company_filing_hitory as _app_us_company_filing_hitory
        return _app_us_company_filing_hitory.app_us_company_filing_hitory(ticker)
    except Exception as e:
        logger.error(f"Unexpected error in app_us_company_filing_hitory tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_us_company_financials(
    ticker: str,
    reportDate: str,
    item: str = ""
) -> Dict[str, Any]:
    """
    Get financial data for a specified company based on its ticker symbol and report date.

    This function fetches parsed financial data from the annual reports (10-K) published on the U.S. Securities and Exchange Commission. 

    Args:
    - ticker (str): The US stock symbol for the company (e.g., "AAPL" for Apple Inc.).
    - reportDate (str): The date of the report in 'YYYY-MM-DD' format (e.g., "2020-09-26").
    - item (str, optional): Specific financial item from the report (e.g., "StatementsOfIncome"). If omitted, all financial data will be fetched.

    Returns:
    Dict containing:
    - status (bool): Success status of the request.
    - res (object): Financial data containing various items such as Earnings Per Share, Revenue, etc. Each item will have:
      - decimals (int): Decimal places for figure rounding.
      - unit (str): Currency unit (e.g., "usd").
      - startDate (str): Reporting start date in 'YYYY-MM-DD' format.
      - endDate (str): Reporting end date in 'YYYY-MM-DD' format.
      - value (float): The financial figure reported.

    Examples:
    1. Fetch all financial data for Apple on the specified date:
       result = app_us_company_financials("AAPL", "2020-09-26")
       print(result["status"])  # Check if the request was successful
       print(result["res"])      # Access the financial data

    2. Fetch specific financial item (Statements Of Income) for Apple:
       result = app_us_company_financials("AAPL", "2020-09-26", item="StatementsOfIncome")
       if result["status"]:
           income_data = result["res"]["EarningsPerShareBasic"]
           print(f"Earnings Per Share (Basic): {income_data['items'][0]['value']} {income_data['items'][0]['unit']}")
    """
    try:
        from tools import app_us_company_financials as _app_us_company_financials
        return _app_us_company_financials.app_us_company_financials(ticker, reportDate, item)
    except Exception as e:
        logger.error(f"Unexpected error in app_us_company_financials tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_stock_tagger(
    news: str,
    maxItem: int = 5
) -> Dict[str, Any]:
    """
    Tag stocks related to a news article using the Stock Tagging API.

    This function utilizes a natural language processing model to identify and tag stock symbols mentioned within a given news article. It supports both English and Chinese news.

    Args:
    - news (str): The input news article that contains stock mentions.
    - maxItem (int, optional): The maximum number of related stock symbols to return. The default value is 5.

    Returns:
    Dict containing:
    - status (bool): Indicates success of the operation.
    - res (object): A list of identified stock symbols with their corresponding prediction scores. Each item in the list will include:
      - symbol (str): The stock symbol identified in the news.
      - score (float): The confidence score for the stock prediction, with higher values indicating greater confidence.

    Examples:
    1. Extract stock symbols from a news article:
       result = app_stock_tagger.predict("Apple’s iPhone sales rebound after supply chain challenges...")
       if result["status"]:
           for stock in result["res"]:
               print(f"Identified Stock: {stock['symbol']}, Confidence Score: {stock['score']}")

    2. Optionally limit the number of symbols returned:
       result = app_stock_tagger.predict("Investment in AI is becoming crucial for tech companies.", maxItem=3)
       if result["status"]:
           print(f"Top 3 Identified Stocks: {[stock['symbol'] for stock in result['res']]}")
    """
    try:
        from tools import app_stock_tagger as _app_stock_tagger
        return _app_stock_tagger.app_stock_tagger(news, maxItem)
    except Exception as e:
        logger.error(f"Unexpected error in app_stock_tagger tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_index_composite(
    index: str
) -> Dict[str, Any]:
    """
    Get the composite data for a specified stock index.

    This function fetches comprehensive index constituent data, including the complete list of composited stocks, their current weighting, and sensitivity. It is essential for investment analysis, portfolio management, and hedging.

    Args:
    index: the stock index name [supported values: 'DOWJONES', 'HSI', 'NASDAQ100', 'SP500']

    Returns:
    Dict containing:
    - status (boolean): success status of the operation
    - res (list): List of dictionaries containing:
      - symbol (string): stock symbol of the constituent
      - weight (float): stock weight contribution to the index
      - sensitivity (float): index point changes due to a 1 dollar change in stock price

    Examples:
    result = get_composite("HSI")
    if result['status']:
        for stock in result['res']:
            print(f"Stock: {stock['symbol']}, Weight: {stock['weight']}, Sensitivity: {stock['sensitivity']}")
    """
    try:
        from tools import app_index_composite as _app_index_composite
        return _app_index_composite.app_index_composite(index)
    except Exception as e:
        logger.error(f"Unexpected error in app_index_composite tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_portfolio_optimizer(
    StartDate: str,
    EndDate: str,
    arrSymbol: list[str], 
    objective: int,
    basecur: str,
    total_portfolio_value: float = 1000000,
    risk_free_rate: float = 0,
    target_return: float = 0,
    risk_tolerance: float = 0,
    allowShortSell: bool = False,
    group_cond: object = {}
) -> Dict[str, Any]:
    """
    Optimize investment portfolio based on specified parameters.

    This function helps investors create and manage their investment portfolios by recommending an optimal allocation of investments according to their risk tolerance, investment goals, and other criteria.

    Args:
    allowShortSell: (boolean) Whether short selling is allowed for the portfolio. Default is false.
    risk_tolerance: (float) The maximum risk tolerance level; value should be a positive number.
    target_return: (float) Your desired target return.
    total_portfolio_value: (float) Initial balance of the portfolio.
    risk_free_rate: (float) Risk-free rate.
    basecur: (string) Base currency of the portfolio.
    objective: (integer) Optimization objective. Options are:
      - 0: Minimize volatility
      - 1: Maximize Sharpe ratio
      - 2: Maximize Sortino ratio
      - 3: Minimize tail risk
      - 4: Risk parity diversification
    group_cond: (object, optional) Asset grouping constraints with min/max weights for specific groups.
    arrSymbol: (list) List of financial instruments to be included in the portfolio.
    StartDate: (string) Start date of the analysis horizon (format: yyyy-mm-dd; must be before today).
    EndDate: (string) End date of the analysis horizon (format: yyyy-mm-dd; must be before today).

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed results including:
      - asset_allocate (object): Allocation details for each instrument and remaining cash.
      - asset_correl (object): Pearson correlation matrix of the instruments.
      - asset_project (object): Performance projection based on optimal allocation.
      - asset_single (object): Performance statistics of each instrument.
      - asset_soln (object): Optimal allocation and performance statistics.
      - eff_frontier (object): Efficient frontier line.
      - err_msg (string): Error messages if any.

    # Examples 1 - without group condition :
    result = app_portfolio_optimizer(
        allowShortSell=False,
        risk_tolerance=0.3,
        target_return=0.15,
        total_portfolio_value=1000000,
        risk_free_rate=0.01,
        basecur="USD",
        objective=0,
        StartDate="2023-12-01",
        EndDate="2023-12-31",
        arrSymbol=["EURUSD", "BTCUSD", "XAUUSD"]
    )

    if result['status']:
        print("Optimal Allocation:", result['res']['asset_allocate'])
        print("Performance Projection:", result['res']['asset_project'])

    # Examples 2 - with group condition:
    result = app_portfolio_optimizer(
        allowShortSell=False,
        risk_tolerance=0.3,
        target_return=0.15,
        total_portfolio_value=1000000,
        risk_free_rate=0.01,
        basecur="USD",
        objective=0,
        StartDate="2023-12-01",
        EndDate="2023-12-31",
        arrSymbol=["EURUSD", "BTCUSD", "XAUUSD"],
        group_cond={
            "map": {
                "EURUSD": "Group1",
                "BTCUSD": "Group2",
                "XAUUSD": "Group2"
            },
            "lower": {
                "Group1": 0.1
            },
            "upper": {
                "Group1": 0.5,
                "Group2": 0.5
            }
        }
    )

    if result['status']:
        print("Optimal Allocation:", result['res']['asset_allocate'])
        print("Performance Projection:", result['res']['asset_project'])
    """
    try:
        from tools import app_portfolio_optimizer as _app_portfolio_optimizer
        return _app_portfolio_optimizer.app_portfolio_optimizer(StartDate, EndDate, arrSymbol, objective, basecur, total_portfolio_value, risk_free_rate, target_return, risk_tolerance, allowShortSell, group_cond)
    except Exception as e:
        logger.error(f"Unexpected error in app_portfolio_optimizer tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_portfolio_optimizer_custom(
    StartDate: str,
    EndDate: str,
    arrUserdata: dict, 
    objective: int,
    basecur: str,
    total_portfolio_value: float = 1000000,
    risk_free_rate: float = 0,
    target_return: float = 0,
    risk_tolerance: float = 0,
    allowShortSell: bool = False,
    group_cond: object = {}
) -> Dict[str, Any]:
    """
    Optimize investment portfolio based on specified parameters.

    This function helps investors create and manage their investment portfolios by recommending an optimal allocation of investments according to their risk tolerance, investment goals, and other criteria.

    Args:
    allowShortSell: (boolean) Whether short selling is allowed for the portfolio. Default is false.
    risk_tolerance: (float) The maximum risk tolerance level; value should be a positive number.
    target_return: (float) Your desired target return.
    total_portfolio_value: (float) Initial balance of the portfolio.
    risk_free_rate: (float) Risk-free rate.
    basecur: (string) Base currency of the portfolio.
    objective: (integer) Optimization objective. Options are:
      - 0: Minimize volatility
      - 1: Maximize Sharpe ratio
      - 2: Maximize Sortino ratio
      - 3: Minimize tail risk
      - 4: Risk parity diversification
    group_cond: (object, optional) Asset grouping constraints with min/max weights for specific groups.
    arrUserdata: (object) user provided market prices series to be included in the portfolio. A JSON object where key represent a time seeries name
    StartDate: (string) Start date of the analysis horizon (format: yyyy-mm-dd; must be before today).
    EndDate: (string) End date of the analysis horizon (format: yyyy-mm-dd; must be before today).

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed results including:
      - asset_allocate (object): Allocation details for each instrument and remaining cash.
      - asset_correl (object): Pearson correlation matrix of the instruments.
      - asset_project (object): Performance projection based on optimal allocation.
      - asset_single (object): Performance statistics of each instrument.
      - asset_soln (object): Optimal allocation and performance statistics.
      - eff_frontier (object): Efficient frontier line.
      - err_msg (string): Error messages if any.

    # Examples 1 - with group condition:
    result = app_portfolio_optimizer(
        allowShortSell=False,
        risk_tolerance=0.3,
        target_return=0.15,
        total_portfolio_value=1000000,
        risk_free_rate=0.01,
        basecur="USD",
        objective=0,
        StartDate="2023-12-01",
        EndDate="2023-12-31",
        arrUserdata={
            "XXX": {
                "2025-01-01": 10,
                "2025-01-02": 10.34,
                "2025-01-03": 10.02,
                "2025-01-04": 10.31,
                "2025-01-05": 10.66,
                "2025-01-06": 10.33,
                "2025-01-07": 10.68,
                "2025-01-08": 10.54,
                "2025-01-09": 10.94,
                "2025-01-10": 10.81,
                "2025-01-11": 10.8,
                "2025-01-12": 11.29,
                "2025-01-13": 11.48,
                "2025-01-14": 11.2,
                "2025-01-15": 11.57,
                "2025-01-16": 11.63,
                "2025-01-17": 11.86,
                "2025-01-18": 11.84,
                "2025-01-19": 11.8,
                "2025-01-20": 12.36,
                "2025-01-21": 12.22,
                "2025-01-22": 12.49,
                "2025-01-23": 12.37,
                "2025-01-24": 12.93,
                "2025-01-25": 13.5,
                "2025-01-26": 13.89,
                "2025-01-27": 13.65,
                "2025-01-28": 13.54,
                "2025-01-29": 13.47
            },
            "YYY": {
                "2025-01-01": 20,
                "2025-01-02": 20.49,
                "2025-01-03": 20.87,
                "2025-01-04": 20.47,
                "2025-01-05": 20.88,
                "2025-01-06": 20.63,
                "2025-01-07": 21.03,
                "2025-01-08": 21.44,
                "2025-01-09": 21.71,
                "2025-01-10": 21.61,
                "2025-01-11": 21.94,
                "2025-01-12": 21.84,
                "2025-01-13": 22.34,
                "2025-01-14": 21.96,
                "2025-01-15": 22.38,
                "2025-01-16": 22.52,
                "2025-01-17": 22.26,
                "2025-01-18": 22.14,
                "2025-01-19": 22.56,
                "2025-01-20": 23.01,
                "2025-01-21": 23.07,
                "2025-01-22": 23.35,
                "2025-01-23": 23.41,
                "2025-01-24": 23.1,
                "2025-01-25": 22.85,
                "2025-01-26": 23.33,
                "2025-01-27": 22.98,
                "2025-01-28": 23.19,
                "2025-01-29": 22.82
            }
        },
        group_cond={
            "map": {
                "EURUSD": "Group1",
                "BTCUSD": "Group2",
                "XAUUSD": "Group2"
            },
            "lower": {
                "Group1": 0.1
            },
            "upper": {
                "Group1": 0.5,
                "Group2": 0.5
            }
        }
    )

    if result['status']:
        print("Optimal Allocation:", result['res']['asset_allocate'])
        print("Performance Projection:", result['res']['asset_project'])
    """
    try:
        from tools import app_portfolio_optimizer_custom as _app_portfolio_optimizer_custom
        return _app_portfolio_optimizer_custom.app_portfolio_optimizer_custom(StartDate, EndDate, arrUserdata, objective, basecur, total_portfolio_value, risk_free_rate, target_return, risk_tolerance, allowShortSell, group_cond)
    except Exception as e:
        logger.error(f"Unexpected error in app_portfolio_optimizer_custom tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_pattern_recoginer(
    instrument: str, 
    timestamp: str,
    count: int,
    interval: str
) -> Dict[str, Any]:
    """
    Identify technical analysis patterns for a given financial instrument.

    This function retrieves actionable chart pattern signals, helping traders make informed decisions based on various formations.

    Args:
    instrument: The trading instrument (e.g., "XAUUSD") from available instruments in get_instruments()
    interval: The candlestick interval (e.g., "H" for hourly) from supported intervals.
    count: The number of observations counted backward from the specified timestamp.
    timestamp: The reference time, formatted as "yyyy-mm-dd HH:MM:SS" in GMT+0.

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed indicators for each pattern, including:
      - hs_pattern (integer): Head and Shoulders pattern signal (1 for buy, -1 for sell, 0 for no signal).
      - ihs_pattern (integer): Inverse Head and Shoulders pattern signal.
      - double_top_pattern (integer): Double Top pattern signal.
      - double_bottom_pattern (integer): Double Bottom pattern signal.
      - ascend_triangle_pattern (integer): Ascending Triangle pattern signal.
      - descend_triangle_pattern (integer): Descending Triangle pattern signal.
      - bull_flag (integer): Bull Flag pattern signal.
      - bear_flag (integer): Bear Flag pattern signal.
      - bull_pennant (integer): Bull Pennant pattern signal.
      - bear_pennant (integer): Bear Pennant pattern signal.

    Examples:
    result = app_pattern_recoginer(
        instrument="XAUUSD",
        interval="H",
        count=100,
        timestamp="2024-08-30 00:00:00"
    )

    if result['status']:
        print("Head and Shoulders Pattern Signal:", result['res']['hs_pattern'])
        print("Inverse Head and Shoulders Pattern Signal:", result['res']['ihs_pattern'])
    """
    try:
        from tools import app_pattern_recoginer as _app_pattern_recoginer
        return _app_pattern_recoginer.app_pattern_recoginer(instrument, timestamp, count, interval)
    except Exception as e:
        logger.error(f"Unexpected error in app_pattern_recoginer tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_risk_analysis(
    data: object
) -> Dict[str, Any]:
    """
    Get investment insights and risk analysis for a given portfolio holding.

    This function analyzes your portfolio holdings to provide tailored insights, identifying key news and upcoming economic releases that may impact your assets.

    Args:
    data: A JSON object representing your portfolio holdings, where the instrument is the key and the corresponding market exposure is the value (e.g., {"EURUSD": -500, "0005HK": 400, "XAUUSD": 1}).

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed analysis including:
      - key_economic_release (string): Upcoming economic announcements with high impact on your portfolio.
      - key_news_highlight (string): Recent key news affecting your portfolio.
      - corporate_event (string): Recent corporate events relevant to your stocks.
      - key_financials (string): Recent financial performance insights for your stock portfolio.

    Examples:
    result = app_risk_analysis({
        "data": {
            "EURUSD": -500,
            "0005HK": 400,
            "XAUUSD": 1
        }
    })

    if result['status']:
        print("Key Economic Release:", result['res']['key_economic_release'])
        print("Key News Highlight:", result['res']['key_news_highlight'])
        print("Recent Corporate Events:", result['res']['corporate_event'])
        print("Key Financials:", result['res']['key_financials'])
    """
    try:
        from tools import app_risk_analysis as _app_risk_analysis
        return _app_risk_analysis.app_risk_analysis(data)
    except Exception as e:
        logger.error(f"Unexpected error in app_risk_analysis tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_trading_pair_aligner(
    instrument: object
) -> Dict[str, Any]:
    """
    Find optimal trading pairs for a given instrument.

    This function intelligently analyzes a selected instrument to identify the best compatible trading pair, enhancing your trading strategy and opportunities.

    Args:
    instrument: The trading instrument for which you want to find the best pair (e.g., "BTCUSD"). All available instruments refer to get_instruments()

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Details of the identified trading pair including:
      - pairs (array): An array of the best trading pairs identified.
      - confidence (number): The confidence level of the identified trading pair.

    Examples:
    result = app_trading_pair_aligner("BTCUSD")

    if result['status']:
        print("Best Trading Pairs:", result['res']['pairs'])
        print("Confidence Level:", result['res']['confidence'])
    """
    try:
        from tools import app_trading_pair_aligner as _app_trading_pair_aligner
        return _app_trading_pair_aligner.app_trading_pair_aligner(instrument)
    except Exception as e:
        logger.error(f"Unexpected error in app_trading_pair_aligner tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_price_simulator(
    corr: float,
    data: list[Dict]
) -> Dict[str, Any]:
    """
    Simulate price movements based on specified correlation using the Price Simulator API on ALGOGENE.

    This function generates new time series data by correlating with existing datasets, enabling enhanced backtesting and risk management.

    Args:
    corr: The correlation coefficient with the given time series, a value between -1 and 1.
    data: An array of JSON objects, each containing:
      - t: The timestamp for the closing price.
      - c: The closing price value.

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (array): An array of objects containing:
      - t (string): The timestamp for the original time series.
      - c (number): The original closing price.
      - c_sim (number): The simulated closing price based on the specified correlation.

    Examples:
    result = app_price_simulator(
        corr=0.8,
        data=[
            {"t": "2013-01-01", "c": 100},
            {"t": "2013-01-02", "c": 102},
            {"t": "2013-01-03", "c": 101},
            {"t": "2023-01-01", "c": 150},
            {"t": "2023-01-02", "c": 152}
        ]
    )

    if result['status']:
        for entry in result['res']:
            print(f"Date: {entry['t']}, Original Price: {entry['c']}, Simulated Price: {entry['c_sim']}")
    """
    try:
        from tools import app_price_simulator as _app_price_simulator
        return _app_price_simulator.app_price_simulator(corr, data)
    except Exception as e:
        logger.error(f"Unexpected error in app_price_simulator tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



@mcp.tool()
def app_capitalflow_hkex_szse(
    date: str
) -> Dict[str, Any]:
    """
    Get capital flow data for the Hong Kong and Shenzhen Stock Exchanges through the Stock Connect program.

    This function retrieves detailed capital flow statistics, including total turnover, trade counts, and top trading stocks, enabling you to make informed investment decisions.

    Args:
    date: The date for which to retrieve capital flow data, formatted as 'YYYY-MM-DD'.

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed statistics including:
      - timestamp (string): Data release timestamp.
      - SZSE Northbound (object): Northbound capital flow details with:
        - total_turnover (number): Total turnover amount (RMB).
        - total_trade_count (integer): Total number of trades.
        - etf_turnover (number): ETF turnover amount (RMB).
        - top10 (array): The ten most actively traded stocks.
      - SZSE Southbound (object): Southbound capital flow details with:
        - total_turnover (number): Total turnover amount (HKD).
        - buy_turnover (number): Buy turnover amount.
        - sell_turnover (number): Sell turnover amount.
        - buy_trade_count (integer): Number of buy trades.
        - sell_trade_count (integer): Number of sell trades.
        - total_trade_count (integer): Total number of trades.
        - etf_turnover (number): ETF turnover amount (HKD).
        - top10 (array): The ten most actively traded stocks.

    Examples:
    result = app_capitalflow_hkex_szse(date="2025-12-04")

    if result['status']:
        print("Total Turnover (Northbound):", result['res']['SZSE Northbound']['total_turnover'])
        print("Top Trading Stocks (Northbound):", result['res']['SZSE Northbound']['top10'])
        print("Total Turnover (Southbound):", result['res']['SZSE Southbound']['total_turnover'])
        print("Top Trading Stocks (Southbound):", result['res']['SZSE Southbound']['top10'])
    """
    try:
        from tools import app_capitalflow_hkex_szse as _app_capitalflow_hkex_szse
        return _app_capitalflow_hkex_szse.app_capitalflow_hkex_szse(date)
    except Exception as e:
        logger.error(f"Unexpected error in app_capitalflow_hkex_szse tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_capitalflow_hkex_sse(
    date: str
) -> Dict[str, Any]:
    """
    Get capital flow data for the Hong Kong and Shanghai Stock Exchanges through the Stock Connect program.

    This function retrieves detailed capital flow statistics, including total turnover, trade counts, and top trading stocks, helping you make informed investment decisions.

    Args:
    date: The date for which to retrieve capital flow data, formatted as 'YYYY-MM-DD'.

    Returns:
    Dict containing:
    - status (boolean): Success status of the operation.
    - res (object): Detailed statistics including:
      - timestamp (string): Data release timestamp.
      - SSE Northbound (object): Northbound capital flow details with:
        - total_turnover (number): Total turnover amount (RMB).
        - total_trade_count (integer): Total number of trades.
        - etf_turnover (number): ETF turnover amount (RMB).
        - top10 (array): The ten most actively traded stocks.
      - SSE Southbound (object): Southbound capital flow details with:
        - total_turnover (number): Total turnover amount (HKD).
        - buy_turnover (number): Buy turnover amount.
        - sell_turnover (number): Sell turnover amount.
        - buy_trade_count (integer): Number of buy trades.
        - sell_trade_count (integer): Number of sell trades.
        - total_trade_count (integer): Total number of trades.
        - etf_turnover (number): ETF turnover amount (HKD).
        - top10 (array): The ten most actively traded stocks.

    Examples:
    result = app_capitalflow_hkex_sse(date="2025-12-04")

    if result['status']:
        print("Total Turnover (Northbound):", result['res']['SSE Northbound']['total_turnover'])
        print("Top Trading Stocks (Northbound):", result['res']['SSE Northbound']['top10'])
        print("Total Turnover (Southbound):", result['res']['SSE Southbound']['total_turnover'])
        print("Top Trading Stocks (Southbound):", result['res']['SSE Southbound']['top10'])
    """
    try:
        from tools import app_capitalflow_hkex_sse as _app_capitalflow_hkex_sse
        return _app_capitalflow_hkex_sse.app_capitalflow_hkex_sse(date)
    except Exception as e:
        logger.error(f"Unexpected error in app_capitalflow_hkex_sse tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_performance_calculator(
    arr: list[str],
    benchmark: str = ""
) -> Dict[str, Any]:
    """
    Calculate performance metrics for a strategy's Net Asset Value (NAV) time series.

    This function processes a user's provided time series data of daily NAV, returning a comprehensive overview of performance statistics. This includes metrics such as daily returns, Sharpe ratios, and benchmark comparisons.

    Args:
    - arr (array): An array of daily NAV data points, with each point as a pair of date (string) and NAV (float).
    - benchmark (str, optional): An instrument name for benchmark comparison. If omitted, the analysis will be based solely on the provided NAV.

    Returns:
    Dict containing:
    - status (bool): Indicates whether the request was successful.
    - res (object): Contains performance metrics such as:
      - Acdate (str): The latest accounting date from the provided time series.
      - TradableDay (int): Total number of tradable days.
      - AvgPerDayPL (float): Average profit/loss per day.
      - MeanDailyReturn (float): Mean of daily returns.
      - MeanAnnualReturn (float): Annualized return.
      - MedianDailyReturn (float): Median of daily returns.
      - Q1DailyReturn (float): 25-th percentile of daily returns.
      - Q3DailyReturn (float): 75-th percentile of daily returns.
      - c95_1DVaR (float): 95% 1-day Value-at-Risk.
      - c99_1DVaR (float): 99% 1-day Value-at-Risk.
      - PlainDailyStdDev (float): Standard deviation of daily returns.
      - PlainAnnStdDev (float): Annualized volatility.
      - DownsideDailyStdDev (float): Standard deviation of daily downside returns.
      - WinRate (float): Winning days in percentage.
      - OddRatio (float): Odds ratio.
      - DailySharpe (float): Daily Sharpe ratio.
      - AnnualSharpe (float): Annualized Sharpe ratio.
      - maxDrawdown_amt (float): Maximum drawdown amount.
      - maxDrawdown_pct (float): Maximum drawdown percentage.
      - maxDrawdownDuration (int): Maximum drawdown duration in days.
      - AvgDrawdownDuration (float): Average drawdown duration in days.
      - TotalPnL (float): Total profit and loss.
      - numWinDay (int): Number of winning days.
      - numLossDay (int): Number of losing days.
      - maxConsWinDay (int): Maximum consecutive winning days.
      - maxConsLossDay (int): Maximum consecutive losing days.
      - maxConsWinAmt (float): Maximum consecutive win amount.
      - maxConsLossAmt (float): Maximum consecutive loss amount.
      - AvgConsWin (float): Average consecutive win amount.
      - AvgConsLoss (float): Average consecutive loss amount.
      - Score_Total (float): Total score.
      - alpha (float): Excess alpha from benchmark.
      - beta (float): Beta to benchmark.
      - calmar_ratio (float): Calmar ratio.
      - information_ratio (float): Information ratio.
      - omega_ratio (float): Omega ratio.
      - rolling_return_7d (float): Recent 7-day return.
      - rolling_return_30d (float): Recent 30-day return.
      - rolling_return_90d (float): Recent 90-day return.
      - rolling_return_180d (float): Recent 180-day return.
      - rolling_return_365d (float): Recent 365-day return.
      - tail_ratio (float): Tail ratio.
      - treynor_ratio (float): Treynor ratio.

    Examples:
    1. Calculate performance metrics without a benchmark:
       result = app_performance_calculator([
           ["2026-01-01", 100], 
           ["2026-01-02", 101.4], 
           ["2026-01-03", 103.1],
           ["2026-01-04", 102],
           ["2026-01-05", 102.8],
           ["2026-01-06", 103.3],
           ["2026-01-07", 103.1],
           ["2026-01-08", 103.8],
           ["2026-01-09", 105.5],
           ["2026-01-10", 104.7],
           ["2026-01-11", 106.8],
           ["2026-01-12", 107.1],
           ["2026-01-13", 105.9],
           ["2026-01-14", 106.4],
           ["2026-01-15", 107.3]
       ])
       print(f"Total PnL: ${result['res']['TotalPnL']}, Win Rate: {result['res']['WinRate']*100:.2f}%")

    2. Calculate performance metrics with a benchmark:
       result = app_performance_calculator([
           ["2026-01-01", 100], 
           ["2026-01-02", 101.4], 
           ["2026-01-03", 103.1],
           ["2026-01-04", 102],
           ["2026-01-05", 102.8],
           ["2026-01-06", 103.3],
           ["2026-01-07", 103.1],
           ["2026-01-08", 103.8],
           ["2026-01-09", 105.5],
           ["2026-01-10", 104.7],
           ["2026-01-11", 106.8],
           ["2026-01-12", 107.1],
           ["2026-01-13", 105.9],
           ["2026-01-14", 106.4],
           ["2026-01-15", 107.3]
       ], benchmark="SPXUSD")
       print(f"Alpha: {result['res']['alpha']}, Beta: {result['res']['beta']}")
    """
    try:
        from tools import app_performance_calculator as _app_performance_calculator
        return _app_performance_calculator.app_performance_calculator(arr, benchmark)
    except Exception as e:
        logger.error(f"Unexpected error in app_performance_calculator tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"


@mcp.tool()
def app_algo_generator(
    prompt: str,
    model: str = ""
) -> Dict[str, Any]:
    """
    Generate a trading algorithm script based on user-provided prompts.

    This function transforms a user's trading idea into a fully functional trading strategy script for the ALGOGENE platform. By inputting a description of the desired trading concept, users can receive a detailed script with high accuracy.

    Args:
    - prompt (string): A guideline or description of your trading strategy concept.
    - model (string, optional): Specify the AI model used for generation. The available value is 'algogene'.

    Returns:
    Dict containing:
    - status (bool): Indicates the success of the operation.
    - res (string): The generated backtest script and explanation based on the provided prompt.

    Examples:
    1. Generate a grid trading strategy for XAUUSD:
       result = app_algo_generator("Write a grid trading strategy for XAUUSD:\n 1. set max number of grids to 10 \n 2. grid size set to 5 points away from current bid and ask price.\n 3. take profit and stop loss set to 5 points away from each grid level")
       print(f"AI Response:\n{result['res']}")

    2. Generate a moving average crossover strategy:
       result = app_algo_generator("Create a moving average crossover strategy for trading BTCUSD based on 50-period and 200-period moving averages.")
       print(f"AI Response:\n{result['res']}")
    """
    try:
        from tools import app_algo_generator as _app_algo_generator
        return _app_algo_generator.app_algo_generator(prompt, model)
    except Exception as e:
        logger.error(f"Unexpected error in app_algo_generator tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"



def validate_configuration() -> bool:
    """
    Validate server configuration and dependencies with security checks.
    
    Returns:
        bool: True if configuration is valid and secure, False otherwise
    """
    def _session_token(response):
        if not isinstance(response, dict):
            return ""
        token = response.get("token")
        if token:
            return token
        nested = response.get("res")
        if isinstance(nested, dict):
            return nested.get("token", "")
        return ""

    try:
        import utils
        
        # Validate API credentials security
        status, res = utils.validate_api_credentials()
        if status == 200 and _session_token(res):
            logger.info("Configuration validated successfully")
            return True
        else:
            logger.error("API credentials validation failed")
            return False
    except ImportError as e:
        logger.error(f"Failed to import configuration module: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        return False


def main() -> None:
    """
    Main entry point for the AlgoGene MCP Server.
    
    Handles argument parsing, configuration validation, and server startup
    with proper error handling and exit codes.
    
    Exit Codes:
        0: Successful execution or user interruption
        1: Configuration error or validation failure
        84: Server startup or runtime error
    """
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="AlgoGene MCP Server - Model Context Protocol server for AlgoGene API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            %(prog)s                           # Start with STDIO transport (default)
            %(prog)s --transport streamable-http          # Start with streamable-http transport for testing
            %(prog)s --transport sse --port 8080 --host 0.0.0.0  # Custom SSE configuration
        """
    )
    
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http", "sse"], 
        default="stdio",
        help="Transport method to use (stdio for MCP clients, streamable-http/sse for testing)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="localhost",
        help="Host for HTTP transport (default: localhost)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Configure logging level based on argument
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    
    logger.info(f"Starting AlgoGene MCP Server with {args.transport} transport")
    logger.info(f"Log level set to: {args.log_level}")
    
    
    # Validate configuration before starting server
    if not validate_configuration():
        logger.error("Configuration validation failed. Please check your environment variables.")
        logger.error("Required: user, api_key")
        sys.exit(84)
    
    
    if args.transport in ["streamable-http", "sse"]:
        logger.info(f"HTTP server will start on {args.host}:{args.port}")
        logger.info("HTTP mode is primarily for testing. Use STDIO for MCP clients.")
    else:
        logger.info("STDIO mode: Ready for MCP client connections")
    
    
    try:
        if args.transport == "stdio":
            logger.info("Initializing STDIO transport...")
            mcp.run(transport="stdio")
        else:
            logger.info(f"Initializing {args.transport} transport on {args.host}:{args.port}")
            mcp.run(transport=args.transport, port=args.port, host=args.host)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user (Ctrl+C)")
        sys.exit(0)
    except ImportError as e:
        logger.error(f"Missing required dependencies: {str(e)}")
        logger.error("Please ensure all required packages are installed")
        sys.exit(84)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {args.port} is already in use. Please choose a different port.")
            sys.exit(84)
        else:
            logger.error(f"Network error during server startup: {str(e)}")
            sys.exit(84)
    except Exception as e:
        logger.error(f"Server startup failed with unexpected error: {str(e)}")
        logger.error("This is likely a configuration or environment issue")
        sys.exit(84)


if __name__ == "__main__":
    main()
    #mcp.run(transport="stdio")
    #mcp.run(transport="http", host="0.0.0.0", port=8000)
    
