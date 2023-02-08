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

2. closeの認識、利用箇所でラベルがcloseかどうかを気にしていないので、それをフィルタリングするようにする。つまりcloseを識別したいのであれば、*close*の指定を行う。など。

SSD
-----

1. 学習結果のテストプログラムの実装。

ResNet34
------------

gaa_learning_task
-------------------------


game_eye
-----------------


gaa_lib
-----------

1. detection_result.pyをgaa_libに昇格。また、各利用者がgaa_libを読み込み。

実施済みのissue
====================

gaa
-----


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

game_eye
-----------------

1. SSDを呼び出すときにbest_weightを指定　→　完了

commit 4205ec5bf3e436ffcd37ea86431db680c50187c9 (HEAD -> master, origin/master)


gaa_lib
-----------




