import smbus2, time

address = 0x63                   #Atlas PH Probe standard I2C address is 99 decimal.
rh_no_hold = 0xf5
previous_temp = 0xe0

class atlasPH(object):
    def __init__(self):
        self.bus = smbus2.SMBus(1)

    def write(self, command):
        self.bus.write_byte(address, ord(command))

    def readBlock(self, numBytes):
        return self.bus.read_i2c_block_data(address, 0, 5)

    # val:str, -> float
    def extractFloatFromString(self, val):
        try:
            return float(val)
        except ValueError:
            print("Atlas PH probe value error: " + block)
            return 0.00

    def extractPH(self, block):
        if block[0] == 1:
            block.pop(0)
            return self.extractFloatFromString("".join(map(chr, block)))
        else:
            print("Atlas PH probe status code error: " + block[0])
            return 0.00

    # -> float
    def getPH(self):
        self.write('R')
        time.sleep(0.9)
        block = self.readBlock(8)
        return self.extractPH(block)

    def test(self):
        'Self test of the object'
        print('*** Test Atlas PH ***')
        print('PH: %.2f' %self.getPH())

if __name__=="__main__":
    t=atlasPH()
    t.test()
    
