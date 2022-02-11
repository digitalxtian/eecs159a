import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
gpioInput = 7
GPIO.setup(gpioInput, GPIO.IN)
import PySimpleGUI as sg
import json

class WaterData:

        def __init__(self):
                self.total_gallons = 0
                self.total_time = 0
                self.gallons_min = 0
                self.minutes = 0
                self.constant = 0.10
                self.time_new = 0
                self.rate_count = 0
                self.total_count = 0

        def read_total_gallons(self):
                print(self.total_gallons)

        def read_total_time(self):
                print(self.total_time)

        def read_gallon_min(self):
                print(self.gallon_min)

if __name__ == '__main__':

        h2o = WaterData()

        while True:
                try:
                        h2o.time_new = time.time() + 10
                        h2o.rate_count = 0
                        while time.time() <= h2o.time_new:
                                if GPIO.input(gpioInput)!=0:
                                        h2o.rate_count += 1
                                        h2o.total_count += 1
                                try:
                                        print(GPIO.input(gpioInput), end='')
                                except KeyboardInterrupt:
                                        break
                                        
                                        
                        h2o.minutes += 1
                except KeyboardInterrupt:
                        break

        print("\nTotal Time: " + str(h2o.minutes))
        print("\nLiters / min ", round(h2o.rate_count * h2o.constant,4))
        print("\nTotal liters ", round(h2o.total_count * h2o.constant,4))
        print("\nTime (min & clock) ", "\t", time.asctime(time.localtime()),"\n")
        GPIO.cleanup()
        print("Done") 

        data_set = {"liters_used": round(h2o.rate_count * h2o.constant,4), "total_liters": round(h2o.total_count * h2o.constant,4)}
        json_dump = json.dumps(data_set)
        with open('data.json', 'w') as f:
                json.dump(data_set, f)
        f.close


        layout = [[sg.Text("Current temprature       ", key='temp', justification='left')],
                [sg.Text("Last Time Used           ", key='last', justification='left')],
                [sg.Text("Schedule Your Next Shower", key='time', justification='center')],
                [sg.Input(key='INPUT')],
                [sg.Button('OK')],
                [sg.Text(size=(40, 1), key='OUTPUT')]]

        window = sg.Window('The Screen', layout)

        while True:
                event, values = window.read(timeout=100)
                if event == sg.WINDOW_CLOSED:
                  break

                f = open("data.json")
                data = json.load(f)

                window["temp"].update("liters_used       "+str(data["liters_used"]))
                window["last"].update("total_liters           "+str(data["total_liters"])+":00")
                # if values['INPUT'] != "":
                if event == 'OK':
                        window['OUTPUT'].update('You have set showertime to be ' + values['INPUT'] + ":00 !")

                window.refresh()

                data["scheduled"] = values['INPUT']
                # We can also change the current temp and last time used here
                """
                if change is True:
                        data["temperature"] = new temp
                        data["last_used"] = new time
                """

                with open("data.json", "w") as j:
                        json.dump(data, j)

                f.close()

        window.close()
