import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class maSignal():

    def __init__(self):
        self.author = 'ChannelCMT'

    def maEnvironment(self, am, paraDict):
        envPeriod = paraDict["envPeriod"]

        envMa = ta.MA(am.close, envPeriod)
        envDirection = 1 if am.close[-1]>envMa[-1] else -1
        return envDirection, envMa

    def maCross(self,am,paraDict):
        fastPeriod = paraDict["fastPeriod"]
        slowPeriod = paraDict["slowPeriod"]

        sma = ta.MA(am.close, fastPeriod)
        lma = ta.MA(am.close, slowPeriod)
        goldenCross = sma[-1]>lma[-1] and sma[-2]<=lma[-2]
        deathCross = sma[-1]<lma[-1] and sma[-2]>=lma[-2]

        maCrossSignal = 0
        if goldenCross:
            maCrossSignal = 1
        elif deathCross:
            maCrossSignal = -1
        else:
            maCrossSignal = 0
        return maCrossSignal, sma, lma
    
        