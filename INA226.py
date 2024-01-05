from machine import I2C, Pin

class I2C_INA226(object):
    """Driver for the Power monitor INA226."""

    def __init__(self, i2c_ch, i2c_addr):
        self.i2c_ch = i2c_ch
        self.i2c_addr = i2c_addr

    def read(self, addr, nbytes):
        return self.i2c_ch.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=8)

    def write(self, addr, buf):
        self.i2c_ch.writeto_mem(self.i2c_addr, addr, buf, addrsize=8)
        time.sleep_ms(5)

    def read_Amp(self):
        self.Amp_bytes = self.read(0x01, 2)
        self.Amp_int = int.from_bytes(self.Amp_bytes, 'big')
        self.Amp_mA = 0.0
        self.Amp_mA = self.Amp_int * 8.33
#        print("01 Amp[%s] %4.2f mA" % (self.Amp_bytes.hex(), self.Amp_mA))
        return self.Amp_mA

    def read_Vlt(self):
        self.Vlt_bytes = self.read(0x02, 2)
        self.Vlt_int = int.from_bytes(self.Vlt_bytes, 'big')
        self.Vlt_mV = 0.0
        self.Vlt_mV = self.Vlt_int * 1.25
#        print("02 Vlt[%s] %4.2f mV" % (self.Vlt_bytes.hex(), self.Vlt_mV))
        return self.Vlt_mV

    def read_Pow(self):
#        self.Pow_bytes = self.read(0x08, 3)
#        self.Pow_int = int.from_bytes(self.Pow_bytes, 'big')
        self.Pow_mW = 0.0
#        self.Pow_mW = self.Pow_int * 10
#        print("03 Pow[%s] %4.2f mW" % (self.Pow_bytes.hex(), self.Pow_mW))
        return self.Pow_mW
    
    def get_Amp_Volt_Watt(self):
        self.A = self.read_Amp()
        self.V = self.read_Vlt()
#        self.W = self.read_Pow()
        self.W = self.A * self.V
        return self.A, self.V, self.W

if __name__ == "__main__":
#import I2C_INA226
    import time

#    i2c = I2C(0,scl=Pin(5),sda=Pin(4))   # I2C0, SCL=GP5=Pin7, SDA=GP4=Pin6
    i2c_ch = I2C(1,scl=Pin(3),sda=Pin(2))   # I2C1, SCL=GP3=Pin5, SDA=GP2=Pin4
    
    i2c_INA = I2C_INA226(i2c_ch,i2c_addr=0x4D)
    print("Detected I2C address: " + str(i2c_ch.scan()))


    # シャント抵抗値を指定
#    i2c_INA.write(0x05, [0x0a, 0x00])
    i2c_INA.write(0x05, b'\x00\x00')


    # 個別のデータ読み込みのテスト
    print("00 [%s] Config" % i2c_INA.read(0x00, 2).hex())
    print("01 [%s] Shunt Voltage" % i2c_INA.read(0x01, 2).hex())
    print("02 [%s] Bus Voltage" % i2c_INA.read(0x02, 2).hex())
    print("03 [%s] Power" % i2c_INA.read(0x03, 2).hex())
    print("04 [%s] Current" % i2c_INA.read(0x04, 2).hex())
    print("05 [%s] Calibration" % i2c_INA.read(0x05, 2).hex())
    print("06 [%s] Mask/Enable" % i2c_INA.read(0x06, 2).hex())
    print("07 [%s] Alert Limit" % i2c_INA.read(0x07, 2).hex())
    print("FE [%s] Manufacture ID" % i2c_INA.read(0xFE, 2).hex())
    print("FF [%s] Die ID" % i2c_INA.read(0xFF, 2).hex())



    # 電流・電圧・電力をまとめて読み込むテスト
    while True:
        print("A,V,W = %4.2f[mA], %4.2f[mV], %4.2f[mW]" % (i2c_INA.get_Amp_Volt_Watt()) )
        time.sleep(1)