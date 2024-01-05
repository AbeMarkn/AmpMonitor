# 対象ハードウェア： I2C EEPROM 24FC1025-I/P (64KB*2, 1MHz対応品)
# データ内容： 時刻6バイトと経過時間2バイトと電圧2バイト・電流値2バイト。データ区切りはカンマ  (6+2+2+2+1=13)
#   13バイト固定長。最初のデータはヘッダ。 64*1024/13 = 5041回分（ヘッダ含む）
# その他： 初期状態はFFhが全て書き込まれた状態とする。

from machine import I2C, Pin
import time

class AT24C32N(object):
    """Driver for the AT24C32N 32K EEPROM."""

    def __init__(self, i2c, i2c_addr=0x50, pages=128, bpp=32):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.pages = pages
        self.bpp = bpp # bytes per page

        self.data_length = 13   # 記録する計測データの長さ
        self.max_num_of_data = 5041   # EEPROMに記録できる最大計測データ数 (タイトルの1行目もデータ数に含む)
        self.d2 = ""

        self.Y_bk = 99
        self.M_bk = 99
        self.D_bk = 99

    def capacity(self):
        """Storage capacity in bytes"""
        return self.pages * self.bpp

    def read(self, addr, nbytes):
        """Read one or more bytes from the EEPROM starting from a specific address"""
        return self.i2c.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=16)

    def write(self, addr, buf):
        """Write one or more bytes to the EEPROM starting from a specific address"""
        offset = addr % self.bpp
        partial = 0
        # partial page write
        if offset > 0:
            partial = self.bpp - offset
            self.i2c.writeto_mem(self.i2c_addr, addr, buf[0:partial], addrsize=16)
            time.sleep_ms(5)
            addr += partial
        # full page write
        for i in range(partial, len(buf), self.bpp):
            self.i2c.writeto_mem(self.i2c_addr, addr+i-partial, buf[i:i+self.bpp], addrsize=16)
            time.sleep_ms(5)
    
    def test(self):
        #    print(self.read(0, 32))
        #    self.write(0, 'hello world')
        #    print(self.read(0, 32))
        #    print(self.read(0,4096))   # OSError: [Errno 110] ETIMEDOUT
        #    print(self.read(0,2048))   # OSError: [Errno 110] ETIMEDOUT
        print(self.read(0,1024))

    def Write_Title(self):   # 1行目(0)はタイトル行
        #              123456789012345678901234567890
        self.write(0, 'RTC   MsStBs,')

    def Search_for_Write_Address(self):
        # 先頭アドレスから指定のデータ長毎に読み込み、FFhを見つけた最初の場所を書き込み開始位置とする。
        i=0
        ret = 0
        for i in range(self.max_num_of_data + 1):
            a = self.read(self.data_length*i, 1)
            if a == b'\xff':
                ret = i
                print("E2P Write address:[%d]" % ret)  # debug
                break
#            else:
#                print("n[%d]" % i)
        if (self.max_num_of_data  <= i):
            print("It shows the bottom. EEPROM is full.")
        return i

    def decimal2num(self, b):
        return ((b & 0xf) + 10 * (b >> 4))

    def calc_Complement_two(self, i):
        ret = 0
        if i & 0x8000 != 0:
            ret = (((~i) & 0xFFFF) + 1) * -1
        else:
            ret = i
        return ret

    def Print_all_data(self):
        i = self.Search_for_Write_Address() - 1   # データの個数 (=書込データアドレス)
        print("Measurement data %d:" % i)
        print("Date, Time, ms, Ampare[mA], Volt[mV]")

        for j in range(i):
            self.rdData = self.read(self.data_length*(j+1), self.data_length)

            self.year    = int(self.decimal2num(self.rdData[0])) + 2000
            self.month   = int(self.decimal2num(self.rdData[1]))
            self.day     = int(self.decimal2num(self.rdData[2]))
            self.hour    = int(self.decimal2num(self.rdData[3]))
            self.min     = int(self.decimal2num(self.rdData[4]))
            self.sec     = int(self.decimal2num(self.rdData[5]))

            self.ms      = int(self.rdData[6]) * 0x100 + int(self.rdData[7])

            self.Amp_uint = int(self.rdData[8]) * 0x100 + int(self.rdData[9])
            self.Amp_int  = self.calc_Complement_two(self.Amp_uint)
            self.Amp_mA = 0.0
            self.Amp_mA = self.Amp_int * 8.33

            self.Vlt_uint = int(self.rdData[10]) * 0x100 + int(self.rdData[11])
            self.Vlt_int  = self.calc_Complement_two(self.Vlt_uint)
            self.Vlt_mV = 0.0
            self.Vlt_mV = self.Vlt_int * 1.25

            dispData = "%4d/%2d/%2d, %02d:%02d:%02d, %d, %+4.2f, %+4.2f" % (self.year, self.month, self.day, self.hour, self.min, self.sec, self.ms, self.Amp_mA, self.Vlt_mV)
#            dispData = self.rdData.hex()
            print(dispData)

    def Write_data(self, wtData):
        i = self.Search_for_Write_Address()
        if (self.max_num_of_data  <= i):
            return False
        else:
            self.write(self.data_length*i, wtData)
            return True

    def Clear_all_data(self):
        self.page_data = b'\xff' * 32
        for i in range(4096):  # 128kByte / 32 = 4096
            self.write(i*32, self.page_data)

if __name__ == "__main__":
#import at24c32n
    i2c = I2C(1,scl=Pin(3),sda=Pin(2))
    e2p = AT24C32N(i2c)
    print("Detected I2C address: " + str(i2c.scan()))   # [87, 95, 104] 0x57, 0x5F, 0x68

#    e2p.Clear_all_data()
#    e2p.Write_Title()
#    print(e2p.read(0, 200))   # バイト列で表示。テキスト以外も確認するため。
#    e2p.Print_all_data()

#    e2p.test()

# 参照サイト
#  https://github.com/mcauser/micropython-tinyrtc-i2c
