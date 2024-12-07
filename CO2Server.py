from CO2Analizer import CO2Analizer
from typing import List
import psycopg2
import psycopg2.extras
from psycopg2 import Error
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class CO2Server:
    def __init__(self) -> None:
        self.logger = logging.getLogger("CO2Server")
        self.conn = None
        self.cursor = None
        self.__initServer()
        self.indoorData = self.__getIndoorData() 

    def __initServer(self):
        DB_PARAMS = {
            'host': 'techsense.panspace.me',
            'database': 'plantgrowth',
            'user': 'WTLab',
            'password': 'WTLab502',
            'cursor_factory': psycopg2.extras.DictCursor
        }
        try:
            self.conn = psycopg2.connect(**DB_PARAMS)
            self.cursor = self.conn.cursor()
            self.logger.info("Database connected successfully")
            return True
        except (Exception, Error) as error:
            self.logger.warning(f"Database connect error: {error}")
            return False
    
    def __getIndoorData(self):
        try:
            query = """
                SELECT timestamp, co2
                FROM sensor_data
                WHERE location = 'indoor'
                AND CAST(timestamp AS DATE) NOT IN (
                    SELECT date
                    FROM calculated_results
                )
                AND timestamp::time BETWEEN '07:20:00' AND '17:20:00'
                ORDER BY timestamp ASC;            
                """

            df = pd.read_sql(query, self.conn)
            print(df)
            return df
        except Exception as e:
            self.logger.warning(f"Query error: {e}")
            return None


    def getGroupOfCO2Data(self) -> List[CO2Analizer]:

        analizers = []

        if self.indoorData is None:
            self.logger.warning("Data is None")
            return []

        curAnalizer = None

        for index, row in self.indoorData.iterrows():
            timestamp = row['timestamp']
            date_str = str(timestamp).split()[0]  # Get YYYY-MM-DD
            time_str = str(timestamp).split()[1]  # Get HH:MM:SS
            co2 = row['co2']

            if curAnalizer is None:
                curAnalizer = CO2Analizer(date_str)  

            elif curAnalizer.date != date_str:
                analizers.append(curAnalizer)
                curAnalizer = CO2Analizer(date_str)

            else:
                curAnalizer.push_back({
                    'time': time_str,
                    'co2': co2
                })

        if not (curAnalizer is None):
            analizers.append(curAnalizer)
                     
        return analizers
