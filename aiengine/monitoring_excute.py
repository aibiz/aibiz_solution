import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitoring_code  import *
class Target():

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def get_path(self, monitoring_path, sensor_num, input_path, output_path):
        self.watchDir = f"{monitoring_path}"
        self.input = f"{input_path}"
        self.output = f"{output_path}"
        self.sensornum = int(f"{sensor_num}")

    def run(self):
        event_handler = Handler()
        event_handler.get_data(self.input, self.output,  self.sensornum)
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):

    def get_data(self,input, output, sensor_num ):
        self.input_file_path = input
        self.output_path = output
        self.sensor_num = sensor_num

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        input_path = event.src_path
        print(input_path)

        test_anomaly(self.sensor_num, input_path, self.input_file_path, self.output_path)



"******Excution method******"
# w = Target()
# w.get_path('monitoring',2 , "train_data/recipe1", "monitoring_anomalies")
# w.run()