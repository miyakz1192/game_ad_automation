========================
GAA関連のissues
========================

GitHubのissuesの機能を使って、GAAの機能コンポ(サービス)ごとにissueを管理したら良いのではないかという話もありそうだが、
記事が散らばって管理がめんどくさいので全部ここに集約しておく。

未実施のissue
================

gaa
-----

8. closeの認識精度が悪い(間違って検出、検出しない。など）

6. UserWarningがうざくて、ログが埋まる

10. adbuttonの認識をSSDを使わずに固定された座標で対応するようにする(優先度低？今のadbutton認識の精度が悪ければ検討)

5. GAA側のimage logging。

7. 動作が重い。とにかく重い。(issue No9の実施によりちょっと様子見)

SSD
-----

1. 学習結果のテストプログラムの実装。

2. 画像認識classの定数値の自動決定。データセットを読み込み、labelを列挙。それをuniq掛けて、セットしていけば良い(sortなどするとラベル順が安定してよいかな)。

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

1. master/image.jpgからannotation xmlを自動生成する。例えば、master/image.jpgが300 x 100の画像だとすると、annotationの画像サイズを指定するところもそのサイズだし、ピッタリサイズなのでxmin/ymin,xmax/ymaxの自動的に決定されるので。

  


実施済みのissue
====================

gaa
-----
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

2. resnet34/ssdごとにprojectsの内容を切り替えられるようにする。commonと各アルゴリズム固有のモノを分ける。::
  commit 2c7a50ded24b6ac237b79098067dced7e06f817d (HEAD -> master, origin/master, origin/HEAD)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sat Feb 11 15:20:24 2023 +0000
  
      support for changing projects each algo




