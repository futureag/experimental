import glob

class ds18b20(object):

    

    def __init__(self):

       # The Raspbian kernal drivers create a link for each 1 wire device.  This link
       # contains the 1 wire device id and thus must is different for every 
       # physical sensor.  
       self.rp_kernal_driver_link = "/sys/bus/w1/devices/28-051790c18bff"
    

    def getTemp(self) -> float:
    #TBD - add exception processing.

       lines = []

       with open(self.rp_kernal_driver_link + "/w1_slave") as f:
           lines = f.readlines()

       if len(lines) != 2:
          return False, 0

       if lines[0].find("YES") == -1:
          return False, 0

       d = lines[1].strip().split('=')

       if len(d) != 2:
         return False, 0

       return True, int(d[1])

    def test(self):
        t = self.getTemp()
        'Self test of the object'
        print('*** test temperatur sensor ***')
        print('Sensor Id: %'  %self.rp_kernal_driver_link)

if __name__=="__main__":
    wt = ds18b20()
    wt.test()
