import time
from machine import I2C, Pin, RTC
import binascii

import ConfigTreat
import INA226
import ExtRTC
import E2P_24FC1025
import setting_VMVL

if __name__ == "__main__":

    # Initialize
    from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565  # type:ignore
    from pimoroni import RGBLED  # type:ignore

#    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB565, rotate=0)
#    display.set_backlight(0.8)


    # 接続デバイスの初期設定

    led = RGBLED(6, 7, 8)
    led.set_rgb(0, 0, 255)  # Blue LED On
    
    i2c_ch = I2C(1,scl=Pin(3),sda=Pin(2))   # I2C1, SCL=GP3=Pin5, SDA=GP2=Pin4
    i2c_INA = INA226.I2C_INA226(i2c_ch,i2c_addr=0x4D)
    e2p = E2P_24FC1025.AT24C32N(i2c_ch)
    rtcExt = ExtRTC.RTC_DS3231(i2c_ch)
    rtcPico = RTC()
    vmvl = setting_VMVL.setting()

    Slide_switch_number = vmvl.numPort_Diag_switch
    Slide_switch = Pin(Slide_switch_number, Pin.IN, Pin.PULL_UP)

    print("Detected I2C address: " + str(i2c_ch.scan()))  # debug


    # 時刻の準備 (RTCとPico起動からの経過時間)
    
#    rtcExt.set_time_from_ExtRTC_to_Pico()  # 外付RTCからPico内蔵RTCに時刻を書き込む
    rtcExt.set_time_from_PicoRTC_to_Ext()  # Pico内蔵RTCから外付RTCに時刻を書き込む

    Start_WorkedTime = time.ticks_ms()

    while True:
        if Slide_switch.value() == True:
            led.set_rgb(0, 0, 0)  # LED Off
 
            # 電流・電圧取得 (Byte型)
            Shunt_byte = i2c_INA.read(0x01, 2)
            Volt_byte = i2c_INA.read(0x02, 2)

            # 時刻取得
            year, month, day, _, hour, min, sec, _ = rtcPico.datetime()
            Now_WorkedTime = time.ticks_diff(time.ticks_ms(), Start_WorkedTime) % 0x10000

#            print("[%2d/%2d/%2d %2d:%2d:%2d] [%d] [%s, %s]" % (year, month, day, hour, min, sec, Now_WorkedTime, Shunt_byte.hex(), Volt_byte.hex()))  # debug

            y_byte = rtcExt.num2decimal(year-2000).to_bytes(1, "big")
            m_byte = rtcExt.num2decimal(month).to_bytes(1, "big")
            d_byte = rtcExt.num2decimal(day).to_bytes(1, "big")
            H_byte = rtcExt.num2decimal(hour).to_bytes(1, "big")
            M_byte = rtcExt.num2decimal(min).to_bytes(1, "big")
            S_byte = rtcExt.num2decimal(sec).to_bytes(1, "big")
            
            WT_byte = Now_WorkedTime.to_bytes(2, "big")

            # E2P書込データ作成
            E2P_wtData = y_byte + m_byte + d_byte + H_byte + M_byte + S_byte + WT_byte + Shunt_byte + Volt_byte + ','
            print(binascii.hexlify(E2P_wtData))  # debug
 
            if False == e2p.Write_data(E2P_wtData):
                print("EEPROM might be full.")
                led.set_rgb(255, 0, 0)  # Red LED On
        else:
            led.set_rgb(0, 0, 255)  # Blue LED On

