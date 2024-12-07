from typing import List
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

time_format = "%H:%M:%S"


class CO2Analizer:
    def __init__(self, date) -> None:
        self.logger = logging.getLogger('CO2Analizer')
        self.date = date 
        self.__CO2Data = []
        self.__CO2CleanedData = []
        self.isBroken = False

        self.startPos = { 'time': None, 'co2': -100 } # { time: .., co2: .. }
        self.endPos   = { 'time': None, 'co2': -100 } # ..

    def push_back(self, newData):
        self.__CO2Data.append(newData)

    def getData(self) -> List[object]:
        return self.__CO2Data


    # brute-force from 7:50 ~ 17:10
    def startCalculate(self):
        self.logger.info(f"start calculate max rate of data on {self.date}")
        
        print( self.__CO2Data[0]['time'] )

        if len(self.__CO2Data) == 0:
            self.isBroken = True
            self.logger.warning(f"length of data are not acceptable on {self.date}")
            return
        elif int(self.__CO2Data[0]['time'].split(':')[0]) > 8:
            self.isBroken = True
            self.logger.warning(f"Begining of time are not acceptable on {self.date}")
            return
        
        self.__getStartPos()

        if self.startPos['time'] is None:
            self.isBroken = True
            self.logger.warning(f"Begining of co2/time are not acceptable on {self.date}")
            return

        self.endPos = self.startPos
        self.__cleanData()
        self.__getEndPos()


    
    def __cleanData(self):
        startTime = datetime.strptime(self.startPos['time'], time_format).time() 
        curMin = self.startPos['co2']
        self.__CO2CleanedData.append(self.startPos)

        for curPos in self.__CO2Data:
            curTime = datetime.strptime(curPos['time'], time_format).time()  
            if curTime > startTime and curPos['co2'] < curMin:
                curMin = curPos['co2']
                self.__CO2CleanedData.append(curPos) 



    def __getStartPos(self):
        
        for data in self.__CO2Data:
            hour = data['time'].split(':')[0]
            minute = data['time'].split(':')[1]
            co2 = data['co2']
            if  co2 > self.startPos['co2']:                
                self.startPos = data 
            if int(hour) >= 8 and int(minute) > 30:
                break
    

    def __getEndPos(self):

        startTime = datetime.strptime(self.startPos['time'], time_format).time()
         
        for data in self.__CO2Data:
            curTime = datetime.strptime(data['time'], time_format).time()  
            if curTime > startTime and data['co2'] < self.endPos['co2']:
                self.endPos = data 
        return
                

    def drawPlot(self):
        if self.startPos['time'] is None or self.endPos['time'] is None:
            self.logger.warning(f"start/end position broken on {self.date}")
            return

        startTime = datetime.strptime(self.startPos['time'], time_format)
        endTime = datetime.strptime(self.endPos['time'], time_format)



        times2 = [ datetime.strptime(i['time'], time_format) for i in self.__CO2Data]
        co2Values2 = [ i['co2'] for i in self.__CO2Data ]
        plt.plot(times2, co2Values2, marker='o', linestyle='None', color='r')


        times = [startTime, endTime]
        co2Values = [self.startPos['co2'], self.endPos['co2']]
        plt.plot(times, co2Values, marker='o', linestyle='-', color='b')



        plt.title('CO2 Levels Over Time')
        plt.xlabel('Time')
        plt.ylabel('CO2 Concentration')

        plt.ylim(200, 700)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        start_limit = datetime.strptime("07:00:00", time_format)
        end_limit = datetime.strptime("18:00:00", time_format)
        plt.xlim(start_limit, end_limit)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        return
