# VMVIの設定値をこのmoduleで管理する。
from machine import Pin

class setting:
    """ class for device settings """

    def __init__(self):
      
        # Port番号の指定。 (Pin番号ではないことに注意)
        self.numDevice = 2   # デバイスの数 2 (00:VA-Meter, 01:Inky) (10:WSePは保留)
        self.numSelectedDevice = 0 # 初期値
        self.numPort_SelectedDevice = 28   # デバイスを認識するポートの番号 (ポートの状態を表す変数は Status_SelectedDevice)
        self.Port_SelectedDevice = Pin(self.numPort_SelectedDevice, Pin.IN, Pin.PULL_UP)   # IO設定
        # 後で個別化しよう。今は昔の共通bitの作りのまま


        self.List_nameDevice = ['pico display+Pico', 'Inky+PicoW']
        self.List_numPort_LoRa_Tx = [4, 4]
        self.List_numPort_LoRa_Rx = [5, 5]
        self.List_numPort_LoRa_AUX = [9, 9]  # LoRa.py
        self.List_numPort_LoRa_M0 = [10, 10]
        self.List_numPort_LoRa_M1 = [11, 11]

        self.List_numPort_inky_switch_A = [99, 12]
        self.List_numPort_inky_switch_B = [99, 13]
        self.List_numPort_inky_switch_C = [99, 14]
        self.List_numPort_inky_MISO = [99, 16]
        self.List_numPort_inky_SCLK = [99, 18]
        self.List_numPort_inky_MOSI = [99, 19]
        self.List_numPort_inky_DC = [99, 20]
        self.List_numPort_inky_RST = [99, 21]
        self.List_numPort_inky_BUSY = [99, 26]

        self.List_numPort_Diag_LED = [8, 8]
        self.List_numPort_Diag_switch = [27, 27]

        self.set_value()

    def set_value(self):

        self.get_SelectedDevice()
        
        self.nameDevice = self.List_nameDevice[self.Status_SelectedDevice]
        self.numPort_LoRa_Tx = self.List_numPort_LoRa_Tx[self.Status_SelectedDevice]
        self.numPort_LoRa_Rx = self.List_numPort_LoRa_Rx[self.Status_SelectedDevice]
        self.numPort_LoRa_AUX = self.List_numPort_LoRa_AUX[self.Status_SelectedDevice]
        self.numPort_LoRa_M0 = self.List_numPort_LoRa_M0[self.Status_SelectedDevice]
        self.numPort_LoRa_M1 = self.List_numPort_LoRa_M1[self.Status_SelectedDevice]

        self.numPort_inky_switch_A = self.List_numPort_inky_switch_A[self.Status_SelectedDevice]
        self.numPort_inky_switch_B = self.List_numPort_inky_switch_B[self.Status_SelectedDevice]
        self.numPort_inky_switch_C = self.List_numPort_inky_switch_C[self.Status_SelectedDevice]
        self.numPort_inky_MISO = self.List_numPort_inky_MISO[self.Status_SelectedDevice]
        self.numPort_inky_SCLK = self.List_numPort_inky_SCLK[self.Status_SelectedDevice]
        self.numPort_inky_MOSI = self.List_numPort_inky_MOSI[self.Status_SelectedDevice]
        self.numPort_inky_DC = self.List_numPort_inky_DC[self.Status_SelectedDevice]
        self.numPort_inky_RST = self.List_numPort_inky_RST[self.Status_SelectedDevice]
        self.numPort_inky_BUSY = self.List_numPort_inky_BUSY[self.Status_SelectedDevice]

        self.numPort_Diag_LED = self.List_numPort_Diag_LED[self.Status_SelectedDevice]
        self.numPort_Diag_switch = self.List_numPort_Diag_switch[self.Status_SelectedDevice]

    def get_SelectedDevice(self):
        if (self.Port_SelectedDevice.value() == 1):
            self.Status_SelectedDevice = 1
        else:
            self.Status_SelectedDevice = 0
#        self.Status_SelectedDevice = self.Port_SelectedDevice.value()
        return self.Status_SelectedDevice


if __name__ == "__main__":

    print("Test")

    vmvl = setting()
    print("Device name: %s" %vmvl.nameDevice)
    print("Port number of LoRa AUX: %d" % vmvl.numPort_LoRa_AUX)
