import talib

def add_features(df):



    open = df['Open']
    high = df['High']
    low = df['Low']
    close = df['Close']
    volume = df['Volume']

    # patterns
    #df['threeLineStrike'] = talib.CDL3LINESTRIKE(open,high,low,close)
    # df['threeBlackCrow'] = talib.CDL3BLACKCROWS(open,high,low,close)
    # df['eveningStar'] = talib.CDLEVENINGSTAR(open,high,low,close)
    #df['engulfing'] = talib.CDLENGULFING(open,high,low,close)
    # df['dragonflyDoji'] = talib.CDLDRAGONFLYDOJI(open,high,low,close)
    # df['gravestoneDoji'] = talib.CDLGRAVESTONEDOJI(open,high,low,close)
    # df['tasukigap'] = talib.CDLTASUKIGAP(open,high,low,close)
    #df['hammer'] = talib.CDLHAMMER(open,high,low,close)
    # df['darkCloudCover'] = talib.CDLDARKCLOUDCOVER(open,high,low,close)
    #df['piercingLine'] = talib.CDLPIERCING(open,high,low,close)
    #df['doji'] = talib.CDLDOJI(open,high,low,close)
    # df['dojiStar'] = talib.CDLDOJISTAR(open,high,low,close)
    # df['shootingStar'] = talib.CDLSHOOTINGSTAR(open,high,low,close)

    # threeLineStrike = talib.CDL3LINESTRIKE(open,high,low,close)
    # engulfing = talib.CDLENGULFING(open,high,low,close)
    # hammer = talib.CDLHAMMER(open,high,low,close)
    # piercingLine = talib.CDLPIERCING(open,high,low,close)

    # df['pattern'] = threeLineStrike + engulfing + hammer + piercingLine




    # lines
    df['rsi'] = talib.RSI(close, timeperiod=14)
    # df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    # df['cci'] = talib.CCI(high, low, close, timeperiod=14)
    # df['dx'] = talib.DX(high, low, close, timeperiod=14)

    df['ema'] = talib.EMA(df['Close'], timeperiod=14)

    df['MACD'], df['macd_signal'], df['macd_hist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(close, timeperiod=14)
    df['SMA'] = talib.SMA(df['Close'], 14)


    df['adx'] = talib.ADX(high, low, close, timeperiod=14)
    # df['cci'] = talib.CCI(high, low, close, timeperiod=14)
    # df['sar'] = talib.SAR(high, low, acceleration=0.02, maximum=0.2)


    # # overlap studies
    # df['sar'] = talib.SAR(high,low,acceleration=0., maximum=0.)

    # momentum indicators
    # df['adx'] = talib.ADX(high,low,close)
    # df['adxr'] = talib.ADXR(high,low,close)
    df['apo'] = talib.APO(close)
    # df['aroonsc'] = talib.AROONOSC(high,low)
    # df['bop'] = talib.BOP(open,high,low,close)
    # df['cmo'] = talib.CMO(close)
    # df['mfi'] = talib.MFI(high,low,close,volume)
    df['minus_di'] = talib.MINUS_DI(high,low,close)
    # df['minus_dm'] = talib.MINUS_DM(high,low)
    # df['mom'] = talib.MOM(close)
    df['plus_di'] = talib.PLUS_DI(high,low,close)
    # df['plus_dm'] = talib.PLUS_DM(high,low)
    # df['ppo'] = talib.PPO(close)
    # df['roc'] = talib.ROC(close)
    # df['rocr'] = talib.ROCR(close)
    # df['rocr100'] = talib.ROCR100(close)
    # df['trix'] = talib.TRIX(close)
    # df['ultosc'] = talib.ULTOSC(high,low,close)
    # df['willr'] = talib.WILLR(high,low,close)

    # # volume indicators
    # df['ad'] = talib.AD(high, low, close, volume)
    # df['adosc'] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
    # df['obv'] = talib.OBV(close, volume)

    # # cycle indicators
    # df['roc'] = talib.ROC(close)
    # df['ht_dcperiod'] = talib.HT_DCPERIOD(close)
    # df['ht_dcphase'] = talib.HT_DCPHASE(close)
    # df['ht_sine'], _ = talib.HT_SINE(close)
    # df['ht_trendline'] = talib.HT_TRENDLINE(close)
    df['ht_trendmode'] = talib.HT_TRENDMODE(close)


    # patterns = ['threeLineStrike', 'threeBlackCrow', 'eveningStar', 'engulfing', 'dragonflyDoji', 'gravestoneDoji', 'tasukigap', 
    # 'hammer', 'darkCloudCover', 'piercingLine', 'doji', 'dojiStar', 'shootingStar'] 

    patterns = ['pattern']


    # for x in df.index:
    #     for cd in patterns:
    #         if df.loc[x, cd] == 100:
    #             df.loc[x, cd] = 1
    #         if df.loc[x, cd] == -100:
    #             df.loc[x, cd] = 0

    return df