from machine import I2C
from machine import Pin
from machine import RTC
import binascii

class RTC_DS3231:
    """ 外付RTC制御 I2C addressは 104 (0x68) """
    # 1. PicoからRTCに時刻を書き込む  (パソコンの時刻をRTCに書き込むことを想定している)
    # 2. RTCからPicoに時刻を書き込む  (Picoの時刻をRTCに書き込むことを想定している)

    def __init__(self, i2c):
        self.rtcPico = RTC()

        self.address = 0x68
        self.register = 0x00
        self.bus= i2c   # I2C0を使用

        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.weekday = 0

        self.week  = ["Mon","Tues","Wed","Thur","Fri","Sat","SUN"]   # Pythonに合わせるため、月曜スタートに定義した

    def decimal2num(self, b):
        return ((b & 0xf) + 10 * (b >> 4))

    def num2decimal(self, d):
        return ((d % 10) | (d // 10) << 4)
    
    def read(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.register),7)
        
        a = t[0]&0x7F  # sec   DS3221のデータフォーマットは秒から始まり年に続く
        b = t[1]&0x7F  # min
        c = t[2]&0x3F  # hour
        d = t[3]&0x07  # week
        e = t[4]&0x3F  # day
        f = t[5]&0x1F  # month
        g = t[6]       # year
 
        self.year    = int(self.decimal2num(g)) + 2000
        self.month   = int(self.decimal2num(f))
        self.day     = int(self.decimal2num(e))
        self.weekday = int(self.decimal2num(d))
        self.hour    = int(self.decimal2num(c))
        self.min     = int(self.decimal2num(b))
        self.sec     = int(self.decimal2num(a))

        # print("DS3231: 20%x/%02x/%02x %02x:%02x:%02x %s" % (t[6],t[5],t[4],t[2],t[1],t[0], self.week[t[3]-1]))

    def write(self):
        num_year = self.num2decimal(self.year-2000)
        num_month = self.num2decimal(self.month)
        num_day = self.num2decimal(self.day)
        num_weekday = self.num2decimal(self.weekday)
        num_hour = self.num2decimal(self.hour)
        num_min = self.num2decimal(self.min)
        num_sec = self.num2decimal(self.sec)
        
        self.NowTime = num_sec.to_bytes(1, "big") + num_min.to_bytes(1, "big") + num_hour.to_bytes(1, "big") + num_weekday.to_bytes(1, "big") + num_day.to_bytes(1, "big") + num_month.to_bytes(1, "big") + num_year.to_bytes(1, "big")
        self.bus.writeto_mem(int(self.address),int(self.register),self.NowTime)

    def print_time_of_ExtRTC(self):
        self.read()
        print("Date/Time (Ext RTC):  [%2d/%2d/%2d %2d:%2d:%2d (%d)]"
              % (self.year, self.month, self.day,
                 self.hour, self.min, self.sec, self.weekday))

    def print_time_of_PicoRTC(self):
        YrP, MnP, DyP, WdP, hrP, miP, seP, _ = self.rtcPico.datetime()   # '_' = subseconds, non-use
        print("Date/Time (Pico RTC): [%2d/%2d/%2d %2d:%2d:%2d]" % (YrP, MnP, DyP, hrP, miP, seP))

    def set_time_from_ExtRTC_to_Pico(self):
        """ 外付RTCからPico内蔵RTCに時刻を書き込む """
        self.read()
        self.rtcPico.datetime((self.year, self.month, self.day, self.weekday, self.hour, self.min, self.sec, 0))

    def set_time_from_PicoRTC_to_Ext(self):
        """ Pico内蔵RTCから外付RTCに時刻を書き込む """
        self.year, self.month, self.day, self.weekday, self.hour, self.min, self.sec, _ = self.rtcPico.datetime()   # '_' = subseconds, non-use
        self.write()


if __name__ == "__main__":
    i2c = I2C(1,scl=Pin(3),sda=Pin(2))
    rtcExt = RTC_DS3231(i2c)
    
    print("Detected I2C address: " + str(rtcExt.bus.scan()))

    # 外付RTCからPico内蔵RTCに時刻を書き込む
#    rtcExt.set_time_from_ExtRTC_to_Pico()

    # Pico内蔵RTCから外付RTCに時刻を書き込む
    rtcExt.set_time_from_PicoRTC_to_Ext()

    # 表示
    rtcExt.print_time_of_ExtRTC()
    rtcExt.print_time_of_PicoRTC()

