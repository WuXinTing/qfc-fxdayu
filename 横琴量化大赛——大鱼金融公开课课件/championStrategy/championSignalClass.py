import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class championSignal():

    def __init__(self):
        self.author = 'ChannelCMT'

    def cmiEnvironment(self, am, paraDict):
        cmiPeriod = paraDict["cmiPeriod"]
        cmiMaPeriod = paraDict["cmiMaPeriod"]
        cmiThreshold = paraDict["cmiThreshold"]

        roc = am.close[cmiPeriod:]-am.close[:-cmiPeriod]
        hl = ta.MAX(am.high, cmiPeriod)-ta.MIN(am.low, cmiPeriod)
        cmiMa = ta.MA(np.abs(roc[-(cmiMaPeriod+10):]/hl[-(cmiMaPeriod+10):])*100, cmiMaPeriod)
        trendStatus = 1 if cmiMa[-1]>cmiThreshold else 0
        return trendStatus, cmiMa

    def filterLowAtr(self, am, paraDict):
        atrPeriod = paraDict["atrPeriod"]
        lowVolThreshold = paraDict["lowVolThreshold"]

        # 过滤超小波动率
        atr = ta.ATR(am.high, am.low, am.close, atrPeriod)
        filterCanTrade = 1 if atr[-1]>am.close[-1]*lowVolThreshold else 0
        return filterCanTrade

    def breakBandSignal(self, am, paraDict):
        smallAtrTime = paraDict["smallAtrTime"]
        bigAtrTime = paraDict["bigAtrTime"]
        atrPeriod = paraDict["atrPeriod"]

        atr = ta.ATR(am.high, am.low, am.close, atrPeriod)

        # 区分趋势与盘整计算上下轨
        hlcMean = ta.MA((am.high+am.low+am.close)/3, 3)[-1]
        priceDirection = 1 if am.close[-1]> hlcMean else -1
        longMultipler = smallAtrTime if priceDirection==1 else bigAtrTime
        shortMultipler = smallAtrTime if priceDirection==-1 else bigAtrTime
        upperBand = am.close[-1]+longMultipler*atr[-1]
        lowerBand = am.close[-1]-shortMultipler*atr[-1]
        breakUpperBand = am.close[-1]>upperBand and am.close[-2]<upperBand
        breakLowerBand = am.close[-1]<lowerBand and am.close[-2]>lowerBand

        return breakUpperBand, breakLowerBand, upperBand, lowerBand

    def breakTrendBand(self, am, paraDict):
        hlMaPeriod = paraDict["hlMaPeriod"]

        upperBand = ta.MA(am.high, hlMaPeriod)[-1]
        lowerBand = ta.MA(am.low, hlMaPeriod)[-1]
        breakUpperBand = am.close[-1]>upperBand and am.close[-2]<upperBand
        breakLowerBand = am.close[-1]<lowerBand and am.close[-2]>lowerBand
        return breakUpperBand, breakLowerBand, upperBand, lowerBand

    def maExit(self, am, paraDict):
        maPeriod = paraDict['maPeriod']
        # 计算均线出场条件
        exitLongTrendSignal = am.low[-1]<ta.MA(am.close, maPeriod)[-1]
        exitShortTrendSignal = am.high[-1]>ta.MA(am.close, maPeriod)[-1]
        return exitLongTrendSignal, exitShortTrendSignal

    def atrStoploss(self, am, paraDict):
        atrPeriod = paraDict['atrPeriod']
        atr = ta.ATR(am.high, am.low, am.close, atrPeriod)
        return atr