================================================
androidゲームの広告を自動操作する
================================================

画面の操作をするのはscrcpyというOSSが一番よい様子

https://github.com/Genymobile/scrcpy


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

ただし、wirelessデバッグを使おうと考えると、ubuntu 20.04のadbではscrpyが動作しないため、
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

     85 sc_mouse_processor_process_mouse_click(struct sc_mouse_processor *mp,
     86                                     const struct sc_mouse_click_event *event) {
     87     struct sc_mouse_inject *mi = DOWNCAST(mp);
     88 
     89     struct sc_control_msg msg = {
     90         .type = SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT,
     91         .inject_touch_event = {
     92             .action = convert_mouse_action(event->action),
     93             .pointer_id = POINTER_ID_MOUSE,
     94             .position = event->position,
     95             .pressure = event->action == SC_ACTION_DOWN ? 1.f : 0.f,
     96             .buttons = convert_mouse_buttons(event->buttons_state),
     97         },
     98     };
     99 
    100     if (!sc_controller_push_msg(mi->controller, &msg)) {
    101         LOGW("Could not request 'inject mouse click event'");
    102     }
    103 }




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

ここも。::

     58 static void
     59 sc_mouse_processor_process_mouse_motion(struct sc_mouse_processor *mp,
     60                                     const struct sc_mouse_motion_event *event) {
     61     if (!event->buttons_state) {
     62         // Do not send motion events when no click is pressed
     63         return;
     64     }
     65 
     66     struct sc_mouse_inject *mi = DOWNCAST(mp);
     67 
     68     struct sc_control_msg msg = {
     69         .type = SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT,
     70         .inject_touch_event = {
     71             .action = AMOTION_EVENT_ACTION_MOVE,
     72             .pointer_id = POINTER_ID_MOUSE,
     73             .position = event->position,
     74             .pressure = 1.f,
     75             .buttons = convert_mouse_buttons(event->buttons_state),
     76         },
     77     };
     78 
     79     if (!sc_controller_push_msg(mi->controller, &msg)) {
     80         LOGW("Could not request 'inject mouse motion event'");
     81     }
     82 }

マウスボタンに関する本丸はここか::

    620 static void
    621 sc_input_manager_process_mouse_button(struct sc_input_manager *im,
    622                                       const SDL_MouseButtonEvent *event) {
    623     struct sc_controller *controller = im->controller;
    624 
    625     if (event->which == SDL_TOUCH_MOUSEID) {
    626         // simulated from touch events, so it's a duplicate
    627         return;
    628     }




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

https://mesonbuild.com/howtox.html

こんな感じ::


  set arg --tcpip=192.168.110.178:39053 --verbosity=verbose
   gdb --args /usr/local/bin/scrcpy  --tcpip=192.168.110.178:39053 --verbosity=verbose
  
  
  
  Thread 1 "scrcpy" received signal SIGFPE, Arithmetic exception.
  0x000055555556d2f2 in sc_screen_convert_drawable_to_frame_coords (screen=0x55555560a1b8 <scrcpy+280>, x=0, y=0) at ../app/src/screen.c:936
  936     x = (int64_t) (x - screen->rect.x) * w / screen->rect.w;
  (gdb) [server] ERROR: Encoding error: android.media.MediaCodec$CodecException: Error 0xfffffc0e
  [server] INFO: Retrying with -m1920...
  [server] DEBUG: Using encoder: 'OMX.qcom.video.encoder.avc'
  
  a@scrcpy:~/scrcpy$ /usr/local/bin/scrcpy --tcpip=192.168.110.178:39053 --verbosity=verbose
  scrcpy 1.24 <https://github.com/Genymobile/scrcpy>
  INFO: Connecting to 192.168.110.178:39053...
  INFO: Connected to 192.168.110.178:39053
  DEBUG: Device serial: 192.168.110.178:39053
  DEBUG: Using server: /usr/local/share/scrcpy/scrcpy-server
  /usr/local/share/scrcpy/scrcpy-server: 1 file pushed, 0 skipped. 132.7 MB/s (41159 bytes in 0.000s)
  [server] INFO: Device: OPPO CPH2099 (Android 11)
  DEBUG: Server connected
  DEBUG: Starting controller thread
  DEBUG: Starting receiver thread
  [server] DEBUG: Using encoder: 'OMX.qcom.video.encoder.avc'
  INFO: Renderer: opengl
  INFO: OpenGL version: 3.1 Mesa 21.2.6
  INFO: Trilinear filtering enabled
  DEBUG: Using icon: /usr/local/share/icons/hicolor/256x256/apps/scrcpy.png
  INFO: Initial texture: 1080x2400
  DEBUG: Starting demuxer thread
  INFO: [INFO] miyakz mode
  [server] ERROR: Encoding error: android.media.MediaCodec$CodecException: Error 0xfffffc0e
  [server] INFO: Retrying with -m1920...
  [server] DEBUG: Using encoder: 'OMX.qcom.video.encoder.avc'
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz mode CUT EVENT target!!!
  INFO: New texture: 864x1920
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz mode CUT EVENT target!!!
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz mode CUT EVENT target!!!
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  
  
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  INFO: [INFO] miyakz called event_loop
  DEBUG: User requested to quit
  DEBUG: quit...
  DEBUG: End of frames
  DEBUG: Receiver stopped
  [server] DEBUG: Controller stopped
  WARN: Killing the server...
  DEBUG: Server disconnected
  DEBUG: Server terminated
  a@scrcpy:~/scrcpy$ 
  
  INFO: [INFO] miyakz called event_loop
  
  Thread 1 "scrcpy" hit Breakpoint 1, event_loop (s=0x55555560a0a0 <scrcpy>) at ../app/src/scrcpy.c:188
  188	         	    	LOGI("[INFO] miyakz mode CUT EVENT target!!!");
  (gdb) 
  (gdb) l
  183	            case SDL_QUIT:
  184	                LOGD("User requested to quit");
  185	                return SCRCPY_EXIT_SUCCESS;
  186	            default:
  187	         	    if(s->screen.rect.w == 0 || s->screen.rect.h == 0){
  188	         	    	LOGI("[INFO] miyakz mode CUT EVENT target!!!");
  189	         	    }
  190		                sc_screen_handle_event(&s->screen, &event);
  191	                break;
  192	        }
  (gdb) p event
  $1 = {type = 32768, common = {type = 32768, timestamp = 4426}, display = {type = 32768, timestamp = 4426, display = 0, event = 0 '\000', 
      padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', data1 = 0}, window = {type = 32768, timestamp = 4426, windowID = 0, 
      event = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', data1 = 0, data2 = 0}, key = {type = 32768, timestamp = 4426, 
      windowID = 0, state = 0 '\000', repeat = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', keysym = {scancode = SDL_SCANCODE_UNKNOWN, sym = 0, 
        mod = 0, unused = 0}}, edit = {type = 32768, timestamp = 4426, windowID = 0, text = '\000' <repeats 31 times>, start = 0, length = 0}, text = {
      type = 32768, timestamp = 4426, windowID = 0, text = '\000' <repeats 31 times>}, motion = {type = 32768, timestamp = 4426, windowID = 0, 
      which = 0, state = 0, x = 0, y = 0, xrel = 0, yrel = 0}, button = {type = 32768, timestamp = 4426, windowID = 0, which = 0, button = 0 '\000', 
      state = 0 '\000', clicks = 0 '\000', padding1 = 0 '\000', x = 0, y = 0}, wheel = {type = 32768, timestamp = 4426, windowID = 0, which = 0, 
      x = 0, y = 0, direction = 0}, jaxis = {type = 32768, timestamp = 4426, which = 0, axis = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', 
      padding3 = 0 '\000', value = 0, padding4 = 0}, jball = {type = 32768, timestamp = 4426, which = 0, ball = 0 '\000', padding1 = 0 '\000', 
      padding2 = 0 '\000', padding3 = 0 '\000', xrel = 0, yrel = 0}, jhat = {type = 32768, timestamp = 4426, which = 0, hat = 0 '\000', 
      value = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000'}, jbutton = {type = 32768, timestamp = 4426, which = 0, button = 0 '\000', 
      state = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000'}, jdevice = {type = 32768, timestamp = 4426, which = 0}, caxis = {type = 32768, 
      timestamp = 4426, which = 0, axis = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', value = 0, padding4 = 0}, 
    cbutton = {type = 32768, timestamp = 4426, which = 0, button = 0 '\000', state = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000'}, cdevice = {
      type = 32768, timestamp = 4426, which = 0}, adevice = {type = 32768, timestamp = 4426, which = 0, iscapture = 0 '\000', padding1 = 0 '\000', 
      padding2 = 0 '\000', padding3 = 0 '\000'}, sensor = {type = 32768, timestamp = 4426, which = 0, data = {0, 0, 0, 0, 0, 0}}, quit = {
      type = 32768, timestamp = 4426}, user = {type = 32768, timestamp = 4426, windowID = 0, code = 0, data1 = 0x0, data2 = 0x0}, syswm = {
      type = 32768, timestamp = 4426, msg = 0x0}, tfinger = {type = 32768, timestamp = 4426, touchId = 0, fingerId = 0, x = 0, y = 0, dx = 0, dy = 0, 
      pressure = 0}, mgesture = {type = 32768, timestamp = 4426, touchId = 0, dTheta = 0, dDist = 0, x = 0, y = 0, numFingers = 0, padding = 0}, 
    dgesture = {type = 32768, timestamp = 4426, touchId = 0, gestureId = 0, numFingers = 0, error = 0, x = 0, y = 0}, drop = {type = 32768, 
      timestamp = 4426, file = 0x0, windowID = 0}, padding = "\000\200\000\000J\021", '\000' <repeats 49 times>}
  (gdb) 
  
★　以下がMOUSE BOTTUN DOWN時のevent構造体::

  Thread 1 "scrcpy" hit Breakpoint 1, event_loop (s=0x55555560a0a0 <scrcpy>) at ../app/src/scrcpy.c:179
  179	         	LOGI("[INFO] miyakz mode: SOME MOTION DOWN!");
  (gdb) p event
  $1 = {type = 1025, common = {type = 1025, timestamp = 5683}, display = {type = 1025, timestamp = 5683, display = 2, event = 0 '\000', 
      padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', data1 = -16711423}, window = {type = 1025, timestamp = 5683, windowID = 2, 
      event = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', data1 = -16711423, data2 = 132}, key = {type = 1025, 
      timestamp = 5683, windowID = 2, state = 0 '\000', repeat = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', keysym = {scancode = 4278255873, 
        sym = 132, mod = 406, unused = 32767}}, edit = {type = 1025, timestamp = 5683, windowID = 2, 
      text = "\000\000\000\000\001\001\001\377\204\000\000\000\226\001\000\000\377\177\000\000\004\000\000\000\000\000\000\000\265\200\352", <incomplete sequence \367>, start = 32767, length = 4}, text = {type = 1025, timestamp = 5683, windowID = 2, 
      text = "\000\000\000\000\001\001\001\377\204\000\000\000\226\001\000\000\377\177\000\000\004\000\000\000\000\000\000\000\265\200\352", <incomplete sequence \367>}, motion = {type = 1025, timestamp = 5683, windowID = 2, which = 0, state = 4278255873, x = 132, y = 406, xrel = 32767, yrel = 4}, 
    button = {type = 1025, timestamp = 5683, windowID = 2, which = 0, button = 1 '\001', state = 1 '\001', clicks = 1 '\001', padding1 = 255 '\377', 
      x = 132, y = 406}, wheel = {type = 1025, timestamp = 5683, windowID = 2, which = 0, x = -16711423, y = 132, direction = 406}, jaxis = {
      type = 1025, timestamp = 5683, which = 2, axis = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', value = 257, 
      padding4 = 65281}, jball = {type = 1025, timestamp = 5683, which = 2, ball = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', 
      padding3 = 0 '\000', xrel = 257, yrel = -255}, jhat = {type = 1025, timestamp = 5683, which = 2, hat = 0 '\000', value = 0 '\000', 
      padding1 = 0 '\000', padding2 = 0 '\000'}, jbutton = {type = 1025, timestamp = 5683, which = 2, button = 0 '\000', state = 0 '\000', 
      padding1 = 0 '\000', padding2 = 0 '\000'}, jdevice = {type = 1025, timestamp = 5683, which = 2}, caxis = {type = 1025, timestamp = 5683, 
      which = 2, axis = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000', padding3 = 0 '\000', value = 257, padding4 = 65281}, cbutton = {
      type = 1025, timestamp = 5683, which = 2, button = 0 '\000', state = 0 '\000', padding1 = 0 '\000', padding2 = 0 '\000'}, cdevice = {
      type = 1025, timestamp = 5683, which = 2}, adevice = {type = 1025, timestamp = 5683, which = 2, iscapture = 0 '\000', padding1 = 0 '\000', 
      padding2 = 0 '\000', padding3 = 0 '\000'}, sensor = {type = 1025, timestamp = 5683, which = 2, data = {0, -1.71475624e+38, 1.84971397e-43, 
        5.68927177e-43, 4.59163468e-41, 5.60519386e-45}}, quit = {type = 1025, timestamp = 5683}, user = {type = 1025, timestamp = 5683, windowID = 2, 
      code = 0, data1 = 0x84ff010101, data2 = 0x7fff00000196}, syswm = {type = 1025, timestamp = 5683, msg = 0x2}, tfinger = {type = 1025, 
      timestamp = 5683, touchId = 2, fingerId = 571213938945, x = 5.68927177e-43, y = 4.59163468e-41, dx = 5.60519386e-45, dy = 0, 
      pressure = -9.51256214e+33}, mgesture = {type = 1025, timestamp = 5683, touchId = 2, dTheta = -1.71475624e+38, dDist = 1.84971397e-43, 
      x = 5.68927177e-43, y = 4.59163468e-41, numFingers = 4, padding = 0}, dgesture = {type = 1025, timestamp = 5683, touchId = 2, 
      gestureId = 571213938945, numFingers = 406, error = 4.59163468e-41, x = 5.60519386e-45, y = 0}, drop = {type = 1025, timestamp = 5683, 
      file = 0x2 <error: Cannot access memory at address 0x2>, windowID = 4278255873}, 
    padding = "\001\004\000\000\063\026\000\000\002\000\000\000\000\000\000\000\001\001\001\377\204\000\000\000\226\001\000\000\377\177\000\000\004\000\000\000\000\000\000\000\265\200\352\367\377\177\000\000\004\000\000\000\000\000\000"}
  (gdb) 
  

これを見るとわかるように、簡単には擬似イベントデータを自分で作ることは難しそう。特にdisplayの所にいろいろなデータが入っており、display = 2の所は可変になりそうな感じがしてくる。

http://sdl2referencejp.osdn.jp/SDL_MouseMotionEvent.html

SDL_WarpMouseInWindow()を呼ぶとイベントが発生するということでこいつを上手く活用できないものか。
MOUSEMOTIONをDOWNに変換はできた。::

  INFO: New texture: 864x1920
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  VERBOSE: input: touch [id=mouse] down position=0,0 pressure=1 buttons=000000
  INFO: INFO: miyakz MOUSEMOTION!!!->TO DOWN
  ^CDEBUG: Server disconnected
  DEBUG: Server terminated
  [Thread 0x7fffea21d700 (LWP 23320) exited]
  
  Thread 1 "scrcpy" received signal SIGINT, Interrupt.
  0x00007ffff7ea823f in __GI___clock_nanosleep (clock_id=clock_id@entry=0, flags=flags@entry=0, req=req@entry=0x7fffffffe090, 
      rem=rem@entry=0x7fffffffe090) at ../sysdeps/unix/sysv/linux/clock_nanosleep.c:78
  78	../sysdeps/unix/sysv/linux/clock_nanosleep.c: No such file or directory.
  (gdb) quit
  A debugging session is active.
  
  	Inferior 1 [process 23304] will be killed.
  
  Quit anyway? (y or n) y
  a@scrcpy:~/scrcpy$ 

eventloopのところを試験的に以下のように書きなおしてやった。::

  +    SDL_WarpMouseInWindow(s->screen.window, 0, 0);
  +    SDL_WarpMouseInWindow(s->screen.window, 0, 0);
  +    SDL_WarpMouseInWindow(s->screen.window, 0, 0);
       while (SDL_WaitEvent(&event)) {
           switch (event.type) {
               case EVENT_STREAM_STOPPED:
  @@ -161,6 +186,14 @@ event_loop(struct scrcpy *s) {
                   LOGD("User requested to quit");
                   return SCRCPY_EXIT_SUCCESS;
               default:
  +               if(event.type == SDL_MOUSEMOTION){
  +                       LOGI("INFO: miyakz MOUSEMOTION!!!->TO DOWN");
  +                       SDL_WarpMouseInWindow(s->screen.window, 0, 0);
  +                       event.type=SDL_MOUSEBUTTONDOWN;
  +                       event.motion.x=0;
  +                       event.motion.y=0;
  +                       sleep(1);
  +               }
                   sc_screen_handle_event(&s->screen, &event);
                   break;

最初のSDL_WarpMouseInWindowの３行はやっても、if(event.type == SDL_MOUSEMOTION){    のところには行かない。
マウスをウインドウ上で動かしてやって初めて、LOGI("INFO: miyakz MOUSEMOTION!!!->TO DOWN");のところに行った。

ちなみに以下のようにしてもダメ。::

  +    LOGI("INFO: miyakz GO");
  +    SDL_WarpMouseInWindow(s->screen.window, 0, 0);
  +    sleep(1);
  +    LOGI("INFO: miyakz GO");
       while (SDL_WaitEvent(&event)) {

eventを受け付けるためには、一度、SDL_WaitEventを実行しないとダメらしい。
(SDL_WaitEvent実行以前に発行したイベントは虫されるっぽい)

ということは、scrcpyにCLIでx,yにMOUSE DOWNイベントを発行させるには

1) event_loop実行前に1つ新たなスレッドをつくり
2) event_loop実行してSDL_WaitEventした所を狙って(1sec位sleep?)、1)のスレッドでMOUSE DOWNイベントを発行させる 
　やりかたは、MOUSE MOTIONを発行して(1のすれっど )、それをDOWNに変換(event_loop内部。意図的なMOUSE DOWNを発行したかどうかを判定するアトミックなフラグは必要そう)
3)scrcpyを終了

とりあえず、汚いけど（携帯電話にデバッグ受付メッセージが出まくる気がするけど）、
これで一旦動くものは出来る見通し。

画面の取得
============

以下のコマンドでmp4化する。長くは取る必要がないので、
１秒位取ったら、このプロセスをkillする(HUPはだめ)。::

  664  /usr/local/bin/scrcpy  --tcpip=192.168.110.178:39053 --verbosity=verbose --record=/tmp/a.mp4

そうすると、mp4が生成されているので、ffmpegでpngあたりに変換してやる::

  660  ffmpeg -i /tmp/a.mp4  -vcodec png -frames:v 1 /tmp/a.png

jpgだと以下のような::

  a@scrcpy:~/scrcpy$ ffmpeg -i /tmp/a.mp4  -frames:v 1 /tmp/a.jpg


実験(オリジナルスレッドのscrpyでの生成)
===========================================

まず、10secに一回メッセージを表示するスレッドを作ってみる::

  a@scrcpy:~/scrcpy$ grep -rn run_recorder app/src/ -B1 -A10
  app/src/recorder.c-135-static int
  app/src/recorder.c:136:run_recorder(void *data) {
  app/src/recorder.c-137-    struct sc_recorder *recorder = data;
  app/src/recorder.c-138-
  app/src/recorder.c-139-    for (;;) {
  app/src/recorder.c-140-        sc_mutex_lock(&recorder->mutex);
  app/src/recorder.c-141-
  app/src/recorder.c-142-        while (!recorder->stopped && sc_queue_is_empty(&recorder->queue)) {
  app/src/recorder.c-143-            sc_cond_wait(&recorder->queue_cond, &recorder->mutex);
  app/src/recorder.c-144-        }
  app/src/recorder.c-145-
  app/src/recorder.c-146-        // if stopped is set, continue to process the remaining events (to
  --
  app/src/recorder.c-289-    LOGD("Starting recorder thread");
  app/src/recorder.c:290:    ok = sc_thread_create(&recorder->thread, run_recorder, "scrcpy-recorder",
  app/src/recorder.c-291-                          recorder);
  app/src/recorder.c-292-    if (!ok) {
  app/src/recorder.c-293-        LOGE("Could not start recorder thread");
  app/src/recorder.c-294-        goto error_avio_close;
  app/src/recorder.c-295-    }
  app/src/recorder.c-296-
  app/src/recorder.c-297-    LOGI("Recording started to %s file: %s", format_name, recorder->filename);
  app/src/recorder.c-298-
  app/src/recorder.c-299-    return true;
  app/src/recorder.c-300-
  a@scrcpy:~/scrcpy$ 

プロトタイプ定義は以下。::

  bool
  sc_thread_create(sc_thread *thread, sc_thread_fn fn, const char *name,
                   void *userdata);


画面サイズの考察
=======================

INFO: Initial texture: 1080x2400
INFO: New texture: 864x1920

scrcpyの動作としては、最初にInitial textureで画面を取ろうとして、lilyの解像度が以下のため、
エラーが発生して、New textureに補正した模様。::

  miyakz@lily:~$ xdpyinfo | grep dimensions
    dimensions:    1366x768 pixels (361x203 millimeters)
  miyakz@lily:~$ 

※ widthは足りているけど、heightが足りていない。
  
マウスクリックイベントが発生する場合、scrcpyで最初に認識する座標は、
Xwindow上に描画されたゲーム画面の座標になる(1)。

一方で、scrcpy内で認識されているゲームの画像が上記の"New texture"のサイズになるので、(1)から
New texture上の座標系に変換される(2)。

この座標系と実際のスマホの座標系が1:1対応になるようにどこかで変換されるのかな？

game ad automationアプリとしては、(1)と(2)のどちらを取得するべきなんだろう。

初版はscrcpyで画面をmp4として取って、それをffmpegでpng(またはjpgでも何でも良いが)に変換する予定なので、
取れた画像のサイズを確認するべき(なぜならそれをssdでclose画像を検出する対象の画像になるため)
(どうも、scrcpyにはスマホから取得する画面のサイズ通り、1080*2400でxwindow上に表示するようなオプションは無い様子。)

pngにした結果は以下で、(2)のサイズと一致する。::

  a@scrcpy:~/scrcpy$ file /tmp/a.png 
  /tmp/a.png: PNG image data, 864 x 1920, 8-bit/color RGB, non-interlaced
  a@scrcpy:~/scrcpy$ 

と、いうことは、game ad automation(gaa)まわりで、以下のような座標系変換が行われる？

整理すると座標系はざっくり以下の3種あるらしい

A) スマホ本体の本当の座標系(自分のOPPOだと1080 x 2400のそれ)
B) scrcpyが表示するXWindowの座標系
C) scrcpyが内部で管理するスマホ画面の座標系(上記,New textureの864 x 1920)


1) scrcpyを起動させる。
2) pngを取得する。この画像は(C)の座標系
3) gaaがscrcpyを起動して、2)の画像を読み込んでcloseの位置を検出。このcloseの座標X,Yは(C)の座標系。次にMOUSE BOTTON DOWNするためにXwindowの(B)の座標系に変換する必要がある(X' y')
4) その後、scrcpyが(X' Y')を(X Y)に変換して(ややこしいな!)、スマホにクリック信号を送信

理想としては、3)を経由せずに単に2)から4)の呼び出しが可能になれば物事は超シンプルなんだが。
ヒントとしては、sc_input_manager_process_mouse_buttonの以下のコードかなぁ。::

    681     struct sc_mouse_click_event evt = {
    682         .position = {
    683             .screen_size = im->screen->frame_size,
    684             .point = sc_screen_convert_window_to_frame_coords(im->screen,
    685                                                               event->x,
    686                                                               event->y),
    687         },
    688         .action = sc_action_from_sdl_mousebutton_type(event->type),
    689         .button = sc_mouse_button_from_sdl(event->button),
    690         .buttons_state =
    691             sc_mouse_buttons_state_from_sdl(sdl_buttons_state,
    692                                             im->forward_all_clicks),
    693     };
    694 
    695     assert(im->mp->ops->process_mouse_click);
    696     im->mp->ops->process_mouse_click(im->mp, &evt);

L681の構造体のあたりの.pointメンバがB)からC)への変換された後のデータが入っていると思われる。
なので、event_loop関数の時点で、imとかim->mp->ops。。。などが取得できればＯＫな気がする。

できそうなので、event_loopの時点で直接process_mouse_clickを呼び出すようにしてみる。
できた。::

  a@scrcpy:~/scrcpy$ DEBUG: [mdown_input] event=1, data=864,0
  DEBUG: [mdown input] handle SDL MOUSEMOTION
  VERBOSE: input: touch [id=mouse] down position=864,0 pressure=1 buttons=000001

こんな感じで、Xwindow上でゲームのアイコンにマウスカーソルを合わせてMOUSE DOWN/UPした時に表示された
座標(152,192)に対して、pipeから(CLIから)同じ座標を指示して、スマホ上ゲームアイコンを正しくクリックできた!::

  a@scrcpy:~/scrcpy$ DEBUG: [mdown_input] event=1, data=152,192
  DEBUG: [mdown input] handle SDL MOUSEMOTION
  VERBOSE: input: touch [id=mouse] down position=152,192 pressure=1 buttons=000001
  VERBOSE: input: touch [id=mouse] up   position=152,192 pressure=0 buttons=000001

コードは思いっきり汚いが、とりあえず動くコードはできた。
コマンドラインは以下のような感じ。::

  a@scrcpy:~/scrcpy$ scrcpy --tcpip=192.168.110.178:38665 --verbosity=verbose & sleep 10 ; echo "152,192" > mdown_input_pipe

デバッグ出力した際にスマホ画面上に「リモートでバッグ接続されました」的な画面が出て、そのせいでクリックが即座にできないので、
10秒の待を入れている

ただし、その通知画面をタップすると出ないようにも設定出来る様子。なので、GAAを他のデバイスに適用する場合は、
画面の解像度などを含めてカスタマイズする必要があるかもしれない。スマホの世界はいろいろなデバイスがあるので、
非常に奥が深い（というか、めんどくさい）

結果の成果物を乗せておく::

  a@scrcpy:~/scrcpy$ git remote -v
  origin	https://github.com/miyakz1192/scrcpy.git (fetch)
  origin	https://github.com/miyakz1192/scrcpy.git (push)
  a@scrcpy:~/scrcpy$ 
  
  
  commit 00a1f758546e225d7326c31b7efd3bed315edbce (HEAD -> test, origin/test)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Thu Dec 8 16:28:19 2022 +0000
  
      mouse click automation base added

さらなる改善(backlog)
========================

struct scrcpyさえあれば、直接(C)の座標系でマウスクリックイベントを発生させることができたため、
SDL_WarpMouseInWindowによる操作は全く不要だと思われる。
今後はその点をリファクタしたい。が、とりあえず、後回しにしておく。。。

今後について
--------------------

close画像の認識部分、クリック信号を送信する部分が出来たため、
あとはアルゴリズムの構築をしてgameの広告を見る操作を自動化するプログラミングに移りたい。

認識精度について
--------------------

今の所、単純なバッテンは認識するけど、薄い灰色ベースに白のバッテンや、さらに背景が交じり合った上での白バッテンなどは認識できない。
この画像認識部分は改善の余地があり、訓練データのバリエーションや数を増やすコトでなんとかなりそうな気配のため、
別途、data augmentationと学習をすすめることにして、アルゴリズムの実装を行い、まずはとりあえず動作するものを目指す

アルゴリズム
==================

まずは、以下の超単純なやつを作ってみる。

ゲーム画像を取得する。
closeが現れるのを待つ
現れたらそこをクリックする


実は、これだけだとあんまり頭が良くない。

A)広告を見るのを繰り返す。という作業全体ができていない
B)close以外の記号(広告を見ていると時々出現する>>のようなもの）の対応が未
C)closeがほかの背景に薄くオーバーラップした際の認識精度がちょっと不安
D)他の解像度が異なるデバイスへの対応

A)は実は、広告を見るボタンの認識が必要。広告が見れなくなったらグレーになるようなケースが多く。
広告がまだ見れる状態の広告を見るボタンのAI認識が必要。

アルゴリズムとしては、広告が見れる状態のボタンをひたすら押して、広告を流し、closeを見つけたらそれを押す（最初に戻る）という
ことを繰り返せば良い気がする。そして、広告が見れるボタンがなくなったら（検出できなくなったら終了）というイメージ。
ここまでのアルゴリズムは特定のゲーム用途になる。

アルゴリズム自体はＡＩでは難しそうなので、ゲームごとに作りこみが必要そうだし、
広告が見れる状態の広告ボタンもゲームごとにマチマチなので、その都度画像を採取してＡＩに学習させる必要があるかもしれない。

しかも、B)の">>"の要素も取り入れたアルゴリズムを考慮する必要がある。


B)は単純に画像を採取して学習させるという作業が必要
C)も同じかもしれない

D)はまだ良くわからない。とりあえず、自分のスマホ向けに開発して、他のデバイスにも展開するようなイメージかなぁ。


改造日記
==========

2022/12/14
---------------

超単純なバージョンの完成をまずは目指す。
枠組みさえできれば、後はデータを集めて学習させるだけという作業に集中できるので。

pytorch側の改造
　・detectした結果をpythonのデータファイル(たしか、pickleとかいったやつ)で、保存する

gaa側の改造
　・screen_shotをscpで送る(serviceクラスのscp対応、sshpassが使える)
　・pytorchクラス側でdetectを実行する
　・結果を取得する
　・（pickleファイルを開き）結果を解析する(closeのスコアがもっとも高いpositionを抽出)
　・ためしに、画面に表示してみる

gaa側の改造
　・touchに対応する。

