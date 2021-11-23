import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
input = 7
GPIO.setup(input, GPIO.IN)

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
                h2o.time_new = time.time() + 10
                h2o.rate_count = 0
                while time.time() <= h2o.time_new:
                        if GPIO.input(input)!=0:
                                h2o.rate_count += 1
                                h2o.total_count += 1
                        try:
                                print(GPIO.input(input), end='')
                        except KeyboardInterrupt:
                                print("\nExiting gracefully")
                                print("\nTotal Gallons: " + str(h2o.total_gallons))
                                print("\nTotal Time: " + str(h2o.total_time))
                                print("\nGallons per minute: " + str(h2o.gallons_min))
                                GPIO.cleanup()
                                sys.exit()
                h2o.minutes += 1
                print("\nLiters / min ", round(h2o.rate_count * h2o.constant,4))
                print("\nTotal liters ", round(h2o.total_count * h2o.constant,4))
                print("\nTime (min & clock) ", h2o.minutes, "\t", time.asctime(time.localtime()),"\n")

        GPIO.cleanup()
        print("Done")

                              
