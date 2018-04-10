import time
from w1thermsensor import W1ThermSensor

sensor_address =  '28-0317620a2cff'  #address of sensor at slsc

class ds18b20(object):
    def __init__(self):
        self.sensor = W1ThermSensor()

    def getTempC(self):
        return self.sensor.get_temperature()

    def test(self):
        t = self.getTemp()
        'Self test of the object'
        print('\n*** Test ds18b20 ***\n')
        print('Temp C: %.2f F' %self.getTempC())

if __name__=="__main__":
    t=ds18b20()
    t.test()
