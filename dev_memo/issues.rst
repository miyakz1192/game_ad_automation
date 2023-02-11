========================
GAA関連のissues
========================

GitHubのissuesの機能を使って、GAAの機能コンポ(サービス)ごとにissueを管理したら良いのではないかという話もありそうだが、
記事が散らばって管理がめんどくさいので全部ここに集約しておく。

未実施のissue
================

gaa
-----

1. (ResNet34?) 確信度0.8以上のものを報告するようにする。

3. lu/ruの切り出し。どうも400 x 400は切り出し過ぎ。誤検出する領域が広がってしまう。このため、SSD/ResNet34への入力サイズは400 x 400にするんだけど、実際の切り出し領域はもう少し、400 x 400の上半分、つまり、400 x 200くらいにしても十分closeが入ると思われる。

4.「広告をみる」ボタンを考慮した対応をGAA本体側に施す。 → ちょっとできた

5. GAA側のimage logging。

6. UserWarningがうざくて、ログが埋まる

7. 動作が重い。とにかく重い。

8. closeを認識する場合は、切り出しが400 x 400でなくても良いのではないか。400 x 200でもよいのでは？No3と重複

9. closeの認識精度が悪い(間違って検出、検出しない。など）

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

gaa_learning_task
-------------------------

1. デプロイ機能の実装 →　完成

2. depoy.pyにて、SSDとResNet34の各々において、data_set.tar.gzを展開する処理を忘れていたので、追加してみたいとおもう。→　完了

1. algo選択サポートOK::
  commit 37216edd40f8701f904afa05580e0700fc05245d (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Sat Feb 11 15:25:56 2023 +0000
  
      select algo support

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




