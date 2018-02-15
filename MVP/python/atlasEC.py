import smbus2, time

address = 0x64                   #Atlas EC Probe standard I2C address is 100  decimal.

class atlasEC(object):

# The SMB stuff needs to be abstracted into a seperate class or module.
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
            print("Atlas EC probe value error: " + block)
            return 0.00

    def extractEC(self, block):
        if block[0] == 1:
            block.pop(0)
            return self.extractFloatFromString("".join(map(chr, block)))
        else:
            print("Atlas EC  probe status code error: " + block[0])
            return 0.00

    # -> float
    def getEC(self):
        self.write('R')
        time.sleep(0.6)
        block = self.readBlock(8)
        return self.extractEC(block)

    def test(self):
        'Self test of the object'
        print('*** Test Atlas EC  ***')
        print('EC: %.2f' %self.getEC())

if __name__=="__main__":
    t=atlasEC()
    t.test()
    
