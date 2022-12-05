================================================
androidゲームの広告を自動操作する
================================================

https://github.com/Genymobile/scrcpy


https://qiita.com/tabbyz/items/5f6cec37e1d525a8e4d5

https://developers.cyberagent.co.jp/blog/archives/29686/

https://qiita.com/ooba1192/items/79c3aae8f48cd663aefd


https://maku77.github.io/android/adb/connect-adb-with-tcpip.html

ADB を TCP/IP 接続に切り替える
ADB 接続を USB 経由ではなく、LAN 接続 (TCP/IP プロトコル）で行うようにする手順です。 Android 端末側の ADB デーモンを TCP/IP モードに切り替えないといけないので、この設定自体は USB 接続された状態で行う必要があります。 一度設定してしまえば、次回からは USB ケーブルは必要なくなります。

Android 端末側の「開発者向けオプション」を有効にして USB 接続する
[設定] > [デバイス情報] に移動して、[ビルド番号] を 7 回タップすると「開発者向けオプション」が有効になります。
（USB 接続された状態で）Android 端末側の ADB デーモンを TCP/IP 接続モードにする
adb tcpip 5555
Android 端末の LAN 内の IP アドレスを確認しておく
adb shell "ip addr | grep inet"
（この時点で USB ケーブルは外して OK）
PC から Android 端末のアドレスとポート番号を指定して TCP/IP で接続
adb connect 192.168.11.6:5555
USB 接続に戻したいときは、adb usb コマンドを実行します。


https://stackoverflow.com/questions/17626691/adb-device-offline-with-adb-wireless
For me the complete steps that worked were :

Settings -> Developer options -> Revoke USB debugging authorizations (clear the list of authorized PCs).

Set USB Debugging OFF.

In Terminal write : adb kill-server

Then : adb start-server

Then : adb connect xx.xx.xx.xx:5555 (the devices ip), it should say unable to connect.

Now turn ON USB debugging again and type the adb connect xx.xx.xx.xx:5555 again.

It should now ask for authorization and you are back online without needing to connect cable to USB, only wifi used.

scrpyが使えるようになるまで
=============================

ubuntu 20.04のscrcpyはtcpipオプションが使えないので、
scrcpyをgit cloneしてくる。次に以下を実施する。

1) scrcpyのインストール
   https://github.com/Genymobile/scrcpy/blob/master/BUILD.md
   を参考にして必須パッケージをインストールする。

以下のコマンドライン::

  # runtime dependencies
  sudo apt install ffmpeg libsdl2-2.0-0 adb libusb-1.0-0
  
  # client build dependencies
  sudo apt install gcc git pkg-config meson ninja-build libsdl2-dev \
                   libavcodec-dev libavdevice-dev libavformat-dev libavutil-dev \
                   libusb-1.0-0-dev
  
  # server build dependencies
  sudo apt install openjdk-11-jdk

ただし、wirelessを使おうと考えると、ubuntu 20.04のadbではscrpyが動作しないため、
最新のadbをインストールする必要がある。

2) scrcpyをインストールする::

  install_release.sh

を実行するのみ。
  
adb
=========

最新版のadbをインストールする。
https://developer.android.com/studio/releases/platform-tools?hl=ja

ここからlinux版のzipをダウンロードして展開する。
以下のコマンドでubuntu 20.04に標準添付されているadbをアンインストールする::

  sudo apt purge adb  

展開したzipのディレクトリにパスを通す（心配なら再起動)

このＵＲＬが一番参考になる。

https://zenn.dev/ik11235/articles/android-wireless-debug

1) OPPO A73の開発者オプションでUSBデバッグをOFFにして、ワイヤレスデバッグをONにする
2) ワイヤレスデバッグをタップして詳細画面に行く
3) ペア設定コードによるデバイスペアの設定をタップして、ポート番号と番号を控える
  　以下のように入力する。ポート番号は3)で得たポート番号::

  $ adb pair 10.113.19.97:41765
  Enter pairing code: XXXXXX
  Successfully paired to 10.113.19.97:41765 [guid=adb-XXXXXXXXXX-XXXXXX]```


4) 次にadb connectコマンドを実行する
   ここのポート番号は2)の画面で得たポート番号::
  
  $adb connect 10.113.19.97:40511

wirelessでscrcpyを使うためには、ubuntu 20.04に標準で入っているadbでは古く(pairコマンドが使えない)、
最新のものを使う必要がある。

scrcpyの起動
===============

以下のようなコマンドにより、PCからスマホを直接操作できる!::

  scrcpy --tcpip=192.168.110.178:40511


