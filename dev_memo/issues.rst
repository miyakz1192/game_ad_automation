========================
GAA関連のissues
========================

GitHubのissuesの機能を使って、GAAの機能コンポ(サービス)ごとにissueを管理したら良いのではないかという話もありそうだが、
記事が散らばって管理がめんどくさいので全部ここに集約しておく。

未実施のissue
================

gaa
-----

5. GAA側のimage loggingとlogviewer。

22. scrcpyが取得するサイズが864x1920以外の場合、リトライするとかゲームの再起動を促すとか

8. closeの認識精度が悪い(間違って検出、検出しない。など）
 → 　類似でissue21を発行資料→ a@scrcpy:~/game_ad_automation/bad_case/issue_21$ 

19. ちゃんと認識して良いケースで認識せず。issue19。調査資料は、/home/a/game_ad_automation/bad_case/issue_19。このissueは画像サイズが多少変わっても、精度に大きな影響がないようにする検討に変更。認識精度という括りでは、No8と類似
  
6. UserWarningがうざくて、ログが埋まる

10. adbuttonの認識をSSDを使わずに固定された座標で対応するようにする(優先度低？今のadbutton認識の精度が悪ければ検討)


7. 動作が重い。とにかく重い。(issue No9の実施によりちょっと様子見)

16. debug_result_showで見た時になぜか、closeとclosegbが混在して見える場合がある。SSDとResNet34でラベルが合っていない？？？

20. issue20資料参照。再現性あり。ミダスのての広告を観るボタンが灰色なのが原因？？？なお、saveで失敗しているケースなので、/tmp/adbutton.jpgは前野データであり、参考にならないことに注意。その後の調査により原因がわかって、このissueの課題としては、scrcpyが取得する画面のサイズに応じて、extract時の切り出しサイズや切り出しの初期posを決定するという課題に変化


SSD
-----

1. 学習結果のテストプログラムの実装。

2. 画像認識classの定数値の自動決定。データセットを読み込み、labelを列挙。それをuniq掛けて、セットしていけば良い(sortなどするとラベル順が安定してよいかな)。

※　注意projects_store/common配下にautocloseデータが入っているので、こいつをマージするようにssd側のマージ設定が必要。ResNet34と仕様や処理を共通化出来るかもしれない。

ResNet34
------------

gaa_learning_task
-------------------------


game_eye
-----------------


gaa_lib
-----------

1. detection_result.pyをgaa_libに昇格。また、各利用者がgaa_libを読み込み。

2. image loggingをgaa_libに昇格して、GAA本体に組み込む

dl_image_manager
----------------------




実施済みのissue
====================

gaa
-----

24. closeの自動学習(半自動学習)の仕組み(issue 25と同じ)
25. images/autoclose/true_close, false_close保存の実装
    → 　完了::
  commit e26905f94295b520c245abc4795ff93653e17a36
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Tue Mar 14 14:21:21 2023 +0000
  
      issue 25. In GAA saving true/false close supported

23. 超小手先だけど、closeの候補を選び出す場合、TOPと同点のclose候補が複数ある場合、WidthとHeightの差の絶対値が一番小さいもの(要するに正方形に一番近いもの)を選び出す。根本的にはResNet34の認識精度を向上することにあるが、このヒューリスティックな方法は結構強力かもしれん
    →　完了::
  commit 190fe45031bb4ccac1ebd8189b04d0fb389a5ae4 (HEAD -> master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Fri Mar 10 16:41:34 2023 +0000
  
      issue23. select best close which width and height may same in __select_best_close
  

18. 17と同じ件。以下のコードの比較の所がきっとバグっている::
    513     def __wait_scene_common(self, message, finish_cond, try_count=1):
    514         for i in range(try_count): 
    515             big_log(message)
    516             self.__print_state()
    517             target_screen_shot_file = self.scrcpy_s.get_screen_shot(file_name="/tmp/gaa_wait_scene_common_target.jpg")
    518             initial_image = self.initial_screen_shot_file.load()
    519             target_image = target_screen_shot_file.load()
    520             if initial_image.eq(target_image) == finish_cond:
    521                 print("INFO: initial_image.eq(target_image) == %s" % (str(finish_cond)))
    522                 return True
    523 
    524         return False
  ここでどうもFalseを返しているらしい。~/game_ad_automation/bad_case/issue_18にファイルを置いておいた。::

  commit dfe592ea8222775d9019b2b819be9117969b7be5
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 8 15:20:20 2023 +0000
  
      issue 18. eq method threshold changed 0.7 to 0.5

17. 画面の遷移判定が変。PUSH CLOSE BUTTON->WAIT FOR SCENE AD TO INITIALで期待値としては画面遷移だがなぜか、"INFO: screen not changed. try scaning close again"とでて、CLOSEボタンのスキャンが始まってしまう(issue 14と類似)
　→　途中まで実施(しばらく様子見)::

  commit 508d9c2e3dfb2391729c2790e104268d1793a718
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Mon Mar 6 16:10:16 2023 +0000
  
      push midas touch

14.ハングする場合がある(diary.rstの2023/02/24の「あと遭遇したエラーで」を参照)::
  [DEBUG] wait for input
  TRACE: touch position
  TRACE: touch position=767,191
  [DEBUG] wait for 15
  scrcpy 1.24 <https://github.com/Genymobile/scrcpy>
  INFO: Connecting to 192.168.110.178:40871...
  failed to connect to 192.168.110.178:40871
  ERROR: Could not connect to 192.168.110.178:40871
  ERROR: Server connection failed
  [DEBUG] touch pos!!!

  commit 243c4ca65a908408febce9bfd329f8cb7151f8f6 (HEAD -> master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 8 15:03:20 2023 +0000
  
      issue 14
2. closeの認識、利用箇所でラベルがcloseかどうかを気にしていないので、それをフィルタリングするようにする。つまりcloseを識別したいのであれば、*close*の指定を行う。など。　→　雑だけど完了。

4.「広告をみる」ボタンを考慮した対応をGAA本体側に施す。 → ちょっとできた::

  commit a3a629dc7f60ebbe6981fb2e05eb7d5f9910b8e4
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Thu Feb 9 15:11:22 2023 +0000
  
      ad button loop support

1. (ResNet34?) 確信度0.8以上のものを報告するようにする。→ 完了

3. lu/ruの切り出し。どうも400 x 400は切り出し過ぎ。誤検出する領域が広がってしまう。このため、SSD/ResNet34への入力サイズは400 x 400にするんだけど、実際の切り出し領域はもう少し、400 x 400の上半分、つまり、400 x 200くらいにしても十分closeが入ると思われる。
   →　完了::

  commit 1e1db1d306dfada1c37e66627a2d9ed4c574c098
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sun Feb 19 14:05:33 2023 +0000
  
      extract left/right upper with remain_height

9. No7の軽減策だが、画面の遷移を認識する仕組みを考える。例えば、いまだとadbuttonを押した後、ゲームのほうで広告をロード中とかの理由で広告に遷移しない場合がある。その場合、広告が流れているとGAA側は誤認識して、closeを押しに行こうとするので、変にゲーム画面が遷移する場合がある。このようなケースを防止するために、画面が変わったかどうかを判定する仕組みが必要。たとえば、beforeとafterで画面全体をとっておき、どれくらいの画素数が変わったかで判断する。例えば、50%以上画素が変化した場合は画面が遷移したなどで判定できるようにする。
　　→　完了::
  commit f70bb392392337b9550fc453826069eeb4147142 (HEAD -> master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sun Feb 19 14:59:20 2023 +0000
  
      image eq supported

11. scrcpyで画面が取れない場合に再度リトライする仕組み→　完了::
  commit 7721d2c89b339e924de88690708a1455f0b0379b (HEAD -> master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sun Feb 19 15:51:29 2023 +0000
  
      scrcpy failed retry supported

12. closeボタンやad buttonが見つからない場合の異常系の考慮が無い。
　→　完了

13. ミダスの手を押下できない
　→　完了

15. ffmpegでOutput file emptyなるエラーがでて、結果GAAが異常終了
    →　完了::
  commit 6aec62adc9623558361a7066a50f58898c586d57
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Mon Mar 6 14:34:46 2023 +0000
  
      retry self.__call_scrcpy_cmd_with_retry if self.__call_ffmpeg_cmd fails

11. 誤認識が発生して人間が手動でcloseボタンなどを押下して画面を遷移させた場合、GAAが正しい状態を認識できない。
　→　完了

  

SSD
-----

2. 最終的なベストの重みファイルをbest_weight.pthで保存する→　完了

commit b534329c61cf2065a3e1f9487dd9f359024b100f (HEAD -> gaa_v1, origin/gaa_v1)


ResNet34
------------

1. 最終的なベストの重みファイルをbest_weight.pthで保存する →　完了

commit 71c9d416604c6cf26295b20c83120e5835963aba (HEAD -> master, origin/master)

2. 動作時に読み込む重みをbest_weight.pthにする →　完了

commit 71c9d416604c6cf26295b20c83120e5835963aba (HEAD -> master, origin/master)

2. ResNet34のbin/calc_exp.pyが使い勝手悪すぎ。closeを自動認識してほしい。いまだとcloseに対応するindexを指定することになっているので滅茶不便すぎ。
　→　完了::
  
  commit a9c7a31fe6972bab8c9fb0b92f010634f41c0dc7 (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Tue Feb 21 15:04:43 2023 +0000
  
      go_aux.sh support new bin/calc_exp.py
  
  commit 04d1d3f9dae5ef68e65d882c0d6d754ebf777d7a
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Tue Feb 21 15:00:50 2023 +0000
  
      bin/calc_exp.py support calc_as,calc_target
  

gaa_learning_task
-------------------------

1. デプロイ機能の実装 →　完成

2. depoy.pyにて、SSDとResNet34の各々において、data_set.tar.gzを展開する処理を忘れていたので、追加してみたいとおもう。→　完了

1. algo選択サポートOK::
  commit 37216edd40f8701f904afa05580e0700fc05245d (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sat Feb 11 15:25:56 2023 +0000
  
      select algo support

1. gaa_learning_taskで進捗状況がわからない。リモート実行するログを常に吐き出すようにしたい。learn_batchの結果を逐一出力。以下のURLが参考になるか。
   https://qiita.com/megmogmog1965/items/5f95b35539ed6b3cfa17
   →　完了::
  commit e9e9e82b03ec1b8116d7d3ff273b20ef9c9f301b (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Tue Feb 21 14:00:09 2023 +0000
  
      realtime output of long time script(ex: learn.sh) supported
  

game_eye
-----------------

1. SSDを呼び出すときにbest_weightを指定　→　完了

commit 4205ec5bf3e436ffcd37ea86431db680c50187c9 (HEAD -> master, origin/master)


gaa_lib
-----------

dl_image_manager
-------------------

4. bin/auto_project.pyの実装
　→　完了::
  
  commit 07cbbca8129005f53ea1f3e5d19e1065708060f7 (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Thu Mar 16 14:39:18 2023 +0000
  
      bug fix in file/number_suffix.py
  
  commit cd70521b34bc9c8f4a7e8e829bb9a021320db4dc (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Thu Mar 16 14:42:23 2023 +0000
  
      issue4 fix(bin/auto_project.py)
  

3. bin/merge_project.pyで引数に受けたテキストファイルを追加のsrcとして認識するようにする。
 →　完了::
  
  commit 11b65a5d0ab2bef49add6e40c04b770e368e0911 (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sun Mar 12 16:08:42 2023 +0000
  
      in merge_project.py additional target src project in specified text file

2. resnet34/ssdごとにprojectsの内容を切り替えられるようにする。commonと各アルゴリズム固有のモノを分ける。::
  commit 2c7a50ded24b6ac237b79098067dced7e06f817d (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sat Feb 11 15:20:24 2023 +0000
  
      support for changing projects each algo

2. projectsのマージ操作を実現する機能(diary.rstに実装アイデアのメモあり) →　完了::
  
  commit 813ba9dc866a0d09342dc16a9cd6cefdfdfe12cb (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 1 15:34:32 2023 +0000
  
      bin/merge_project.py in build.sh
  
  commit b8af116f5abbd5bbbb8a9c01a34a269e91ca084f
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 1 15:32:56 2023 +0000
  
      bin/merge_project.py delete src project support
  
  commit 59f8822856074463db7dd7e3a0e63fa1bedc0bdc
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 1 15:25:32 2023 +0000
  
      bin/merge_project.py bug fix and config support
  
  commit f601be73b90d37dd73bdfbc46fd57444296d1009
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 1 15:11:57 2023 +0000
  
      bin/merge_project.py ver 0.5
  
  commit 7cb8998ceb2ca38a0d21262114a0275503379792
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Wed Mar 1 14:06:42 2023 +0000
  
      bin/merge_project.py

1. master/image.jpgからannotation xmlを自動生成する。例えば、master/image.jpgが300 x 100の画像だとすると、annotationの画像サイズを指定するところもそのサイズだし、ピッタリサイズなのでxmin/ymin,xmax/ymaxの自動的に決定されるので。bin/gen_anno_xml.py。
   →　完了::
  
  commit 97150c37db0f266d85ad823f35f95bdd6943126e (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sun Mar 12 15:43:36 2023 +0000
  
      bin/gen_anno_xml.py added
