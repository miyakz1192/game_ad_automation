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

画面のキャプチャなど
=======================

game ad automationで必要な画面のキャプチャだけど、scrcpyではヘビーすぎる。
https://github.com/Genymobile/scrcpy/issues/684

adbコマンドによる操作が案内されているし、scrcpyにはmp4で録画するオプションはあるけど、
キャプチャー自体は存在しない。

画面のタップ
=======================

scrcpyコマンド単体で座標などを指定してタップすることは出来ないらしい。
githubをサラッと探してみたが希望するプロジェクトは存在せず。

scrcpyをverboseで起動してみて適当に画面操作してみると、以下のような感じ出ててくれ、
なんとなく、出来そうな感触をつかめる::

  a@scrcpy:~/scrcpy$ scrcpy --tcpip=192.168.110.178:39445 --verbosity=verbose
  scrcpy 1.24 <https://github.com/Genymobile/scrcpy>
  INFO: Connecting to 192.168.110.178:39445...
  INFO: Connected to 192.168.110.178:39445
  DEBUG: Device serial: 192.168.110.178:39445
  DEBUG: Using server: /usr/local/share/scrcpy/scrcpy-server
  /usr/local/share/scrcpy/scrcpy-server: 1 file pushed, 0 skipped. 170.9 MB/s (41159 bytes in 0.000s)
  [server] INFO: Device: OPPO CPH2099 (Android 11)
  [server] DEBUG: Using encoder: 'OMX.qcom.video.encoder.avc'
  DEBUG: Server connected
  DEBUG: Starting controller thread
  DEBUG: Starting receiver thread
  [server] ERROR: Encoding error: android.media.MediaCodec$CodecException: Error 0xfffffc0e
  [server] INFO: Retrying with -m1920...
  [server] DEBUG: Using encoder: 'OMX.qcom.video.encoder.avc'
  INFO: Renderer: opengl
  INFO: OpenGL version: 3.1 Mesa 21.2.6
  INFO: Trilinear filtering enabled
  DEBUG: Using icon: /usr/local/share/icons/hicolor/256x256/apps/scrcpy.png
  INFO: Initial texture: 1080x2400
  DEBUG: Starting demuxer thread
  INFO: New texture: 864x1920
  VERBOSE: input: touch [id=mouse] down position=228,1878 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] up   position=228,1878 pressure=0 buttons=000000
  VERBOSE: input: touch [id=mouse] down position=293,1170 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] up   position=293,1170 pressure=0 buttons=000000
  VERBOSE: input: touch [id=mouse] down position=222,1878 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] up   position=222,1878 pressure=0 buttons=000000
  VERBOSE: input: touch [id=mouse] down position=374,1306 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=374,1303 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=374,1300 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1288 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1280 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1265 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1244 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1214 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1182 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1143 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1087 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=377,1028 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=374,957 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=371,897 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=371,841 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=368,782 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=368,737 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=365,702 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=362,681 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] move position=359,672 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] up   position=359,672 pressure=0 buttons=000000
  ^CDEBUG: Server disconnected
  DEBUG: Server terminated
  DEBUG: User requested to quit
  DEBUG: quit...
  DEBUG: End of frames
  DEBUG: Receiver stopped
  a@scrcpy:~/scrcpy$ 

ソースの解析
================

まず、上記を出しているのはこのあたり::

    152 void
    153 sc_control_msg_log(const struct sc_control_msg *msg) {
    154 #define LOG_CMSG(fmt, ...) LOGV("input: " fmt, ## __VA_ARGS__)
    155     switch (msg->type) {
    156         case SC_CONTROL_MSG_TYPE_INJECT_KEYCODE:
    157             LOG_CMSG("key %-4s code=%d repeat=%" PRIu32 " meta=%06lx",
    158                      KEYEVENT_ACTION_LABEL(msg->inject_keycode.action),
    159                      (int) msg->inject_keycode.keycode,
    160                      msg->inject_keycode.repeat,
    161                      (long) msg->inject_keycode.metastate);
    162             break;
    163         case SC_CONTROL_MSG_TYPE_INJECT_TEXT:
    164             LOG_CMSG("text \"%s\"", msg->inject_text.text);
    165             break;
    166         case SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT: {
    167             int action = msg->inject_touch_event.action
    168                        & AMOTION_EVENT_ACTION_MASK;
    169             uint64_t id = msg->inject_touch_event.pointer_id;
    170             if (id == POINTER_ID_MOUSE || id == POINTER_ID_VIRTUAL_FINGER) {
    171                 // string pointer id
    172                 LOG_CMSG("touch [id=%s] %-4s position=%" PRIi32 ",%" PRIi32
    173                              " pressure=%g buttons=%06lx",
    174                          id == POINTER_ID_MOUSE ? "mouse" : "vfinger",
    175                          MOTIONEVENT_ACTION_LABEL(action),
    176                          msg->inject_touch_event.position.point.x,
    177                          msg->inject_touch_event.position.point.y,
    178                          msg->inject_touch_event.pressure,
    179                          (long) msg->inject_touch_event.buttons);
  

さらにこの辺。::

    125 static void
    126 sc_mouse_processor_process_touch(struct sc_mouse_processor *mp,
    127                                  const struct sc_touch_event *event) {
    128     struct sc_mouse_inject *mi = DOWNCAST(mp);
    129 
    130     struct sc_control_msg msg = {
    131         .type = SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT,
    132         .inject_touch_event = {
    133             .action = convert_touch_action(event->action),
    134             .pointer_id = event->pointer_id,
    135             .position = event->position,
    136             .pressure = event->pressure,
    137             .buttons = 0,
    138         },
    139     };
    140 
    141     if (!sc_controller_push_msg(mi->controller, &msg)) {
    142         LOGW("Could not request 'inject touch event'");
    143     }
    144 }

ここ。::

    146 void
    147 sc_mouse_inject_init(struct sc_mouse_inject *mi,
    148                      struct sc_controller *controller) {
    149     mi->controller = controller;
    150 
    151     static const struct sc_mouse_processor_ops ops = {
    152         .process_mouse_motion = sc_mouse_processor_process_mouse_motion,
    153         .process_mouse_click = sc_mouse_processor_process_mouse_click,
    154         .process_mouse_scroll = sc_mouse_processor_process_mouse_scroll,
    155         .process_touch = sc_mouse_processor_process_touch,
    156     };
    157 
    158     mi->mouse_processor.ops = &ops;
    159 
    160     mi->mouse_processor.relative_mode = false;
    161 }

んで、ここ::

   590 static void
    591 sc_input_manager_process_touch(struct sc_input_manager *im,
    592                                const SDL_TouchFingerEvent *event) {
    593     if (!im->mp->ops->process_touch) {
    594         // The mouse processor does not support touch events
    595         return;
    596     }
    597 
    598     int dw;
    599     int dh;
    600     SDL_GL_GetDrawableSize(im->screen->window, &dw, &dh);
    601 
    602     // SDL touch event coordinates are normalized in the range [0; 1]
    603     int32_t x = event->x * dw;
    604     int32_t y = event->y * dh;
    605 
    606     struct sc_touch_event evt = {
    607         .position = {
    608             .screen_size = im->screen->frame_size,
    609             .point =
    610                 sc_screen_convert_drawable_to_frame_coords(im->screen, x, y),
    611         },
    612         .action = sc_touch_action_from_sdl(event->type),
    613         .pointer_id = event->fingerId,
    614         .pressure = event->pressure,
    615     };
    616 
    617     im->mp->ops->process_touch(im->mp, &evt);
    618 }

以下で呼び出し::

    787 void
    788 sc_input_manager_handle_event(struct sc_input_manager *im, SDL_Event *event) {
    789     bool control = im->controller;

以下から呼び出し::

    818 void
    819 sc_screen_handle_event(struct sc_screen *screen, SDL_Event *event) {
    820     bool relative_mode = sc_screen_is_relative_mode(screen);

最終的には以下。::

    152 static enum scrcpy_exit_code
    153 event_loop(struct scrcpy *s) {
    154     SDL_Event event;
    155     while (SDL_WaitEvent(&event)) {
    156         switch (event.type) {
    157             case EVENT_STREAM_STOPPED:
    158                 LOGW("Device disconnected");
    159                 return SCRCPY_EXIT_DISCONNECTED;
    160             case SDL_QUIT:
    161                 LOGD("User requested to quit");
    162                 return SCRCPY_EXIT_SUCCESS;
    163             default:
    164                 sc_screen_handle_event(&s->screen, &event);
    165                 break;
    166         }
    167     }
    168     return SCRCPY_EXIT_FAILURE;
    169 }

ここで、SDL_Eventの型がわかれば、自由自在に改造ができそうだ。


http://utsukemononi.gozaru.jp/gc/sdl/page006.html

これって、linux標準のイベントフレームワークっぽい。

ここを、event_loopをやめて、sc_screen_handle_event単体を呼び出すようにする。
引数としてどの座標でイベントを発生させるというのを指定して、単にそれで終了してしまう。
こういった改造をすればよいかと思われる。











