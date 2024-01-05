# AmpMonitor

Raspberry Pi Pico, 電流・電圧計測センサ(INA226)＋大型シャント抵抗, EEPROM(24FC1025), 外付RTC(DS3221)を組み合わせた電圧電流モニタです。

## 各ファイルの概要

### main.py

スイッチをオンにすると、センサから電流計測して結果を時刻情報と共にEEPROMへ書き込みます。スイッチがオフになるまで繰り返します。

### E2P_24FC1025.py

EEPROMを制御します。
初期化(FFhで全埋め)・計測データの読込と書込を行います。
Picoに繋がっているEEPROMの計測データを、パソコンのThonnyなどでテキスト形式で取り込み、エクセルなどで確認できます。

### ExtRTC.py

外付けのRTC DS3221を制御します。
外付けのRTCの時刻情報をPicoへ取り込んだり、Picoの時刻情報を外付けのRTCに書き込んだりできます。

### INA226.py

Texas Instruments製の電圧・電流センサ INA226を制御します。
シャント抵抗の電圧値とバスの電圧値を取り込みます。シャント抵抗の電圧値を所定の定数をかけることで電流値を求めています。
テスト用のコードはマイナス値を処理していません。

### setting_VMVL.py

Picoの各ピンへの機能割当を一覧管理するファイルです。
この電圧電流計測用のソフトではあまり使っていません。
他の計測ソフトで2つのPico間で送受信するときに使っています。

## Pico単独で計測する準備

バッテリーをPicoに繋げただけのシンプルな構成で計測したいと考えています。

- 外付RTCは、Pico単独で動作させた時の現在時刻取得用です。
- Pico Display Packは計測状態のモニタ用です。

### Pico Display Pack

[Pico Display Pack](https://shop.pimoroni.com/products/pico-display-pack?variant=32368664215635)を使っています。
（が、現在はLEDだけ使っています。そのため、Pico Displayの代わりに、LEDを1個つければ充分です。）

Pimoroni製uf2が必要です。
次のエラーが発生したときは、Pimoroni製uf2でなく、他の（RaspberryPi純正など）uf2が書き込まれている可能性があります。

- ImportError: no module named "'picographics'"

### その他

Picoの電流もモニタするために、INA228もつけています。
また、RoLa通信モジュールも載せられるようにブレッドボードの配線を施してます。
