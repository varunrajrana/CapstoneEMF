import time
import board
import adafruit_dht
import csv
import logging
from datetime import datetime

#python3 main.py > /dev/null 2>&1 &
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
logger = logging.getLogger()

def newDay(file_log_handler):
    logger.removeHandler(file_log_handler)
    file_log_handler = logging.FileHandler(r"/home/pi/Data/"+start_today+r".csv")
    logger.addHandler(file_log_handler)
    logger.info("Time, Temperature, Humidity")

def getMeaurement():
    temperature_c = str(dhtDevice.temperature)
    humidity = str(dhtDevice.humidity)
    return temperature_c, humidity

def fileSetup(end_today):
    logger.setLevel(logging.INFO)
    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    file_log_handler = logging.FileHandler(r"/home/pi/Data/"+end_today+r".csv")
    logger.addHandler(file_log_handler)
    logger.info("Time, Temperature, Humidity")
    return file_log_handler

if __name__ == "__main__":

    today = datetime.today()
    end_today = today.strftime('%Y%m%d')

    file_log_handler = fileSetup(end_today)

    while True:
        try:
            today = datetime.today()
            start_today = today.strftime('%Y%m%d')

            # New csv file generated if new day
            if start_today != end_today: newDay(file_log_handler)

            # Get measurements
            temp,humidity = getMeaurement()

            logger.info(today.strftime('%H:%M:%S')+", "+temp+", "+humidity)

            end_today=start_today

        except RuntimeError as error:
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
    
        time.sleep(5.0)