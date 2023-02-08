===============
GAA改造日記
===============

全体的な人気をすべてこちらに集約することにする。
すでにバラけたものを集約すること無く、新しい情報からこちらに集約する。

2023/2/8
==========

2/7の記録を受けて、作業を実施。
まず、create_taskは正常に終わっていた。
deployもいい感じで終了した。::

  a@dataaug:~/gaa_learning_task$ ./deploy.py  test_run_20230208
  INFO: trying deploying about ssd
  INFO: extracting best weight file from ./output/test_run_20230208/ssd.tar.gz
  INFO: file found, and send it to service
  INFO: /home/a/pytorch_ssd/weights/best_weight.pth uploaded successfully
  INFO: extracting data set file from ./output/test_run_20230208/ssd_dl_image_manager.tar.gz
  INFO: file found, and send it to service
  INFO: /tmp/data_set.tar.gz uploaded successfully
  INFO: extract data_set.tar.gz on remote host
  
  
  
  
  INFO: done
  INFO: trying deploying about resnet34
  INFO: extracting best weight file from ./output/test_run_20230208/resnet34.tar.gz
  INFO: file found, and send it to service
  INFO: /home/a/resset/weights/best_weight.pth uploaded successfully
  INFO: extracting data set file from ./output/test_run_20230208/resnet34_dl_image_manager.tar.gz
  INFO: file found, and send it to service
  INFO: /tmp/data_set.tar.gz uploaded successfully
  INFO: extract data_set.tar.gz on remote host
  
  
  
  
  INFO: done
  INFO: program ended successfully!
  a@dataaug:~/gaa_learning_task$ 

GAA本体をテストランしてみる。（相変わらず精度は悪いが）、動作上は問題なし。
というわけで、本日は以下を実施。

1. 「広告をみる」ボタンをSSD/ResNet34に学習させるcreate_task。ゲーム画像からmaster/image.jpgを作り、annotaionのxmlを作り、create_taskする。

2. 並行して、「広告をみる」ボタンを考慮した対応をGAA本体側に施す。

まずは、1の手順。

1. ゲーム画像を取得して、gimpで「広告をみる」ボタンを切り出す。そのボタンだけが100%ピッタリ入った画像ファイルを作る

2. dl_image_managerでbin/create_project.shを実行してadbuttonプロジェクトを作成する

3. 1の画像を当該プロジェクトのmaster/image.jpgとする。他のプロジェクトを参考にして、annotaion xmlも手動で作成する。画像のw/hは画像のサイズそのもので、originも(1,1)、w/hを画像サイズを考慮したものにする。(この辺自動化してもよいな)

4. ./bin/build_project.py adbuttonしてみてdata augmentationしてみた結果がいい感じか確認する。

5. create_taskを実行する。

※ どうも、ResNet34のepochが5だと精度が悪いっぽいので、10にしてみる。

GAAのAd buttonサポートはプッシュする際の座標変換システムを残してとりあえずコーディングしたので、明日は座標変換システムのコーディングと、create_taskは完了しているだろうから、とりあえずdeployして、今回GAAに追加したコードを動作させてみるの巻。

2023/2/7
===========

best_weight関連のissueをすべて消化して、とりあえず、test_run_20230207としてcreate_taskを実行中。
とりあえず、実行結果を確認して(SSDとResNet34でbest_weightが生成されていること)、deployを試してみる。
その後、gaa本体をテスト実行してみる。

ここまでは上手く行くと思うので、その後は、アルゴリズムの改良を行う。

以前close認識の精度を高めるという話があったが、その前に、広告を見ること自体のルーチンワークの自動化を完結するために、
つまり、「広告をみる」ボタンを認識するタスクを実行してみる。
新たに、create_taskを実行して学習を行う。

学習後にgaaに組み込みを実施する。

なお、現状のgaaでも改良が必要な点が見えていて、issueにした。

広告をみるボタンの認識は結構難しいので、issuesに記載しきれない所はここに記しておく。
まず、closeと違って、「広告をみる」ボタンは画面の中央に出現するため、その点を考慮する必要がある。

取得したゲーム画像を400 x 400に切り取るときに考慮が必要。
上手く行くかわからないが（試行錯誤が必要かもだが）、取得したスクリーンサイズの中央に400 x 400 の"window"が来るようにして、
そこから、下の方向に、window(400 x 400のブロック)をずらす(stride=1)ように取得していき、GameEyeに渡すイメージ。
(処理時間がまたかさむ。。。)

「広告をみる」ボタンは有効（オレンジ）と無効（灰色）があるが、ResNet34で認識かけようとすると、edgeになって、
白黒にしてしまうから、有効と無効の区別がつかなくなってしまう。なので、アルゴリズムとしては
頭が悪いけど、見つけた広告をみるボタンをとにかく押下していくという作戦を取る。

幸いにして、無効な「広告をみる」ボタンを押下しても何も発生しないので、見つけ次第押していく。
押した結果、次の「広告をみる」ボタンを押す(400 x 400のwindow)を下にスライドしていく。ということをやる。

そうすると、いつの間にか広告を見切るというわけ。

ここまでアルゴリズムを作りこめば、あとはSSD/ResNet34の認識精度と、実効速度改善の問題に帰着できるので、
特定の仕事に集中できるだろう。

現時点では精度が低い原因が良くわからない。一回、深層学習の勉強(含む数学)にダイブすることになる。


2023/2/6
============

depoy.pyにて、SSDとResNet34の各々において、data_set.tar.gzを展開する処理を忘れていたので、追加してみたいとおもう。
→　完了

次は、SSD issueのNo2,3、ResNet34のissueの1,2をやって、gaa_learning_taskのcreate_taskとdepoyが一周回るかをテストしてみよう。


2023/2/5
==========

フレームワークは１週できることを確認したため、以下に取り組む。
※　記事自体はdl_image_manager/doc/start.rstに存在したものをcopyしてきた。

ワークフロー構築のためのメモ
=================================

以下からの引用
https://github.com/miyakz1192/game_ad_automation/commit/6501be44dd9c0bce26ff72607f366df98ba16b4c

以下。::

|物体検出や画像認識の改善のために学習データの追加と学習、検証、実機でのテストプレーという一連のワークフローを効率的に回す仕組みが無いとやってられん。
|SSDとResNet34で学習データと、テスト結果、重みの組を管理する仕組みが必要。
|まずはそこだろうか。あとは、このワークフローが完成してNo2の改善がイマイチとなると、一回、深層学習の基本に戻って調査し直すしかあるまい。

ということで、このworkflowを作ってみることにする。

考慮が必要な点は

1. 学習データの追加が簡単にできること

2. 結果が管理しやすいこと(SSD/ResNetのソースと、学習データ、重みをセットで管理)

3. タスクの状況が見えること

4. 結果のGAAへのデプロイ、アンデプロイが簡単に行えること 


まずは、データの管理方法について検討が必要なのではないか


学習データ(学習タスクアウトプット)の管理単位
-----------------------------------------------

まず、学習データの大元としてはdl_image_managerで管理している各projectが最小単位として考えられる。
各学習データをbuildした結果がdata_setと言える。

つまりdata_set ∋  project群となる。data_set.tar.gzは80MB位。あと、data_set.tar.gzを生成したプログラム(つまりdl_image_manager)もバックアップしたほうが良いので、こちらもバックアップしたい。こちらのサイズは1.8GBくらい(大きい！）

あと、各data_set.tar.gzを元にSSDとResNetで学習を行う。こちらも結果のweightとソースはともにバックアップしておきたい。

この単位を学習タスクアウトプットと一応呼んでおく。

→　2023/2/5：この概念の実装自体は一応完了。

学習タスクアウトプットの生成
-----------------------------------------------

dl_image_managerサーバを基点に以下を実施する

1. 人間が、新規projectなどを作ったり、既存projectに変更を加えたりする

2. 人間がcreate_task.shを実行する

3. create_task.shでは一連の以下が実行される

3-1. ./learn_batch.sh ssdを実行して、projectを再buildして、data_set.tar.gzを生成する。また、ssdで学習を実行する

3-2. dl_image_managerのソースをバックアップする(この際、容量節約のためdata_setディレクトリ配下を削除する。また、data_set.tar.gzはこのバックアップに含まれる)

3-3. ssdサーバ(pytorch)の/home/a/pytorch_ssdをまるごとバックアップして、dl_image_managerにダウンロードする(ssd.tar.gz)

3-4. ./learn_batch.sh resnet34を実行して、projectを再buildして、data_set.tar.gzを生成する。また、resnet34で学習を実行する

3-5. dl_image_managerのソースをバックアップする(この際、容量節約のためdata_setディレクトリ配下を削除する。また、data_set.tar.gzはこのバックアップに含まれる)

3-6. resnet34サーバ(pytorch)の/home/a/ressetをまるごとバックアップして、dl_image_managerにダウンロードする(resnet34.tar.gz)

3.7. 上記アーカイブ群をtarで固めてgaa_learning_task配下のoutputディレクトリに配置しておく

→　2023/2/5：この概念の実装自体は一応完了。



※　注意
---------

lib/dl_image_manager_config.pyをssd/resnet34で入れ替える必要がある。どのような処理が良いかは考える必要がある。
DL_IMAGE_MANAGER_FORCING_GLOBAL_BASE_IMAGE_SIZEをSSD/ResNet34に応じて追記するか、ファイル自体をまるごと置き換えるか。前者のほうがdl_image_manager_config.pyの変更に強そうな気がしなくもないが？？
　→　とりあえず対応。

buildrcが設定されていないとエラーをはくようにすると親切だが、、、、

SSDとResNet34の各タスクで一緒に学習結果をゲーム画像でテストした結果も学習タスクアウトプットに含まれると良い。
　→  ResNet34の方はやった。SSDはテストプログラムが無いので、実施していない。

学習タスクアウトプットの表示と削除
-----------------------------------------------

上記tarがoutputディレクトリにあるのでそれを見れば良い。
outputディレクトリ配下に学習タスクアウトプットの名前がついたディレクトリが更にあって、
そこに簡単なメモを記したtextが入っているといい感じかも

学習タスクアウトプットのデプロイ
---------------------------------

gaa_learning_taskのoutput配下のディレクトリを1つ選択してdepoy.shを実行する
dl_image_managerのbuildrcを読み込み、ssd/resnet34のサーバ(pytorch)に以下を実行する(今の実装では、 ~/gaa_lib/net/easy_sshscp_config.pyにコンフィグを記載する形。これに徐々に移行する)

1. SSDの場合、ssd.tar.gzからタイムスタンプが最新のweightを抜き出して、それをpytorch_ssdサーバの/home/a/pytorch_ssdに配置する(weight/best_weight.pth)

2. ResNet34の場合も同様に実施する(resset34.tar.gz)

→　　完成

memo(debug用):

a@dataaug:~/gaa_learning_task/output/test_run_20230203/temp/resnet34/home/a/resset/weights$ sha256sum   20230110.pth best_weight.pth
a5564f74ac226b920962e50a932d27ee5c250eae326e795110c2690453483cc1  20230110.pth
a5564f74ac226b920962e50a932d27ee5c250eae326e795110c2690453483cc1  best_weight.pth
a@dataaug:~/gaa_learning_task/output/test_run_20230203/temp/resnet34/home/a/resset/weights$ 

a@dataaug:~/gaa_learning_task/output/test_run_20230203/temp/ssd/home/a/pytorch_ssd/weights$ sha256sum  close_weight_1.2027226681531218.pth best_weight.pth
579217773becf8121079affecdf8e3fd065ac3b26ed8e84f9e84f3c83705203e  close_weight_1.2027226681531218.pth
579217773becf8121079affecdf8e3fd065ac3b26ed8e84f9e84f3c83705203e  best_weight.pth
a@dataaug:~/gaa_learning_task/output/test_run_20230203/temp/ssd/home/a/pytorch_ssd/weights$ 



※　注意
------------

GAA経由で動作する場合はbest_weight.pthを参照して動作する必要がある。
学習タスクアウトプットにssd.tar.gzまたはresnet34.tar.gzが無い場合は、その時点でプログラムが中断する。



考えられるシナリオ
----------------------

1. projectを１つ追加する。これは典型的なシナリオでcreate_task.sh/depoy.shが動作しそう

2. SSD/ResNet34のプログラムを改変する。同上。

3. SSDとResNet34で対象とするprojectを変えたい。例えば、SSDではja_charを必要とするし、ResNet34ではやっぱり必要としない(このようなことが今後発生するか不明だけど・・・）、この場合は、create_task.shで実行したいタスクを選択出来るようにしたら良い。(SSDはこっちのprojectsでResNet34はこっちのprojects)など。なので、create_task.shで種別-どのprojectsディレクトリの関連を設定するファイルが必要。それを見て動作。また、dl_image_manager配下にはデフォルトでprojectsディレクトリがあり、こちらがすべてのタスクで使用される仕様のため、例えば、SSD_projectsというディレクトリがあり、こちらがSSD専用のprojectsにしたければ、そちらを指定した設定ファイルを作っておく必要がある。など。


2023/2/3
---------

フレームワークはとりあえず作ってみて流したが、単体実行のlearn_batch.shが何故かコケる。
疲れたので、明日調べる。::

  Traceback (most recent call last):
    File "/home/a/dl_image_manager/projects/ja_char_159/data_augmentation/daug.py", line 6, in <module>
      from data_aug import *
    File "/home/a/dl_image_manager/./lib/data_aug.py", line 1, in <module>
      import keras.utils.image_utils as image
    File "/home/a/.local/lib/python3.8/site-packages/keras/__init__.py", line 20, in <module>
      from keras import distribute
    File "/home/a/.local/lib/python3.8/site-packages/keras/distribute/__init__.py", line 18, in <module>
      from keras.distribute import sidecar_evaluator
    File "/home/a/.local/lib/python3.8/site-packages/keras/distribute/sidecar_evaluator.py", line 17, in <module>
      import tensorflow.compat.v2 as tf
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/__init__.py", line 37, in <module>
      from tensorflow.python.tools import module_util as _module_util
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/__init__.py", line 45, in <module>
      from tensorflow.python.feature_column import feature_column_lib as feature_column
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/feature_column/feature_column_lib.py", line 18, in <module>
      from tensorflow.python.feature_column.feature_column import *
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/feature_column/feature_column.py", line 143, in <module>
      from tensorflow.python.layers import base
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/layers/base.py", line 16, in <module>
      from tensorflow.python.keras.legacy_tf_layers import base
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/keras/__init__.py", line 25, in <module>
      from tensorflow.python.keras import models
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/keras/models.py", line 22, in <module>
      from tensorflow.python.keras.engine import functional
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/keras/engine/functional.py", line 32, in <module>
      from tensorflow.python.keras.engine import training as training_lib
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/keras/engine/training.py", line 44, in <module>
      from tensorflow.python.keras import callbacks as callbacks_module
    File "/home/a/.local/lib/python3.8/site-packages/tensorflow/python/keras/callbacks.py", line 68, in <module>
      import requests
    File "/usr/lib/python3/dist-packages/requests/__init__.py", line 95, in <module>
      from urllib3.contrib import pyopenssl
    File "/usr/lib/python3/dist-packages/urllib3/contrib/pyopenssl.py", line 46, in <module>
      import OpenSSL.SSL
    File "/usr/lib/python3/dist-packages/OpenSSL/__init__.py", line 8, in <module>
      from OpenSSL import crypto, SSL
    File "/usr/lib/python3/dist-packages/OpenSSL/crypto.py", line 1553, in <module>
      class X509StoreFlags(object):
    File "/usr/lib/python3/dist-packages/OpenSSL/crypto.py", line 1573, in X509StoreFlags
      CB_ISSUER_CHECK = _lib.X509_V_FLAG_CB_ISSUER_CHECK
  AttributeError: module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'
  Error in sys.excepthook:


なぜか、エラーが。paramikoをインストールしたせいかな、、、変な所に影響が出ている様子。
なので、複数サービスは同居しないほうが良いってことか、、、
しかし、なんだころ。

以下のURLに助けられた。

https://stackoverflow.com/questions/73830524/attributeerror-module-lib-has-no-attribute-x509-v-flag-cb-issuer-check

まず、pip自体が上手く動かなくなったので（謎）再インストール::

  sudo apt remove python3-pip 
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python3 get-pip.py

この後、再ログイン。(新しく入れたpipのパスを有効にするため)

して、以下を実行::

  pip install pyopenssl --upgrade

SSDとResnetでconfigファイルの入れ替えが必要などやることは残っているが、とりあえずは動作する様子  




2023/01/31
-------------

GameEyeを作って、GAA側に試しに組み込んでテストプレーをしてみたが、使い物にならん。。。多少はcloseを押してくれるけど

1. 動作が遅すぎ(物体検出やResNet34で認識している間に、スマホ側は次の画面に行くので、間違ったところを押しまくる)

2. 誤検出が多い(closeをcloseと認識しなかったり、非closeをcloseと認識してしまうことが多々有り)。この影響でcloseが押下されるので、10分とか。

3. ゲーム中の広告を觀るボタンまで認識して、全部自動化したい

1の動作改善はGPU持っていないのでマルチCPUをフル活用して高速化するしか無いかなぁ。あとは余分な処理の削除か。ただし、今は速度の最適化よりも認識の精度を高めるのが先の気がする。
3はやるだけな気がするけど、No2の課題が大きい。
2はどうしたら良いのだろう。。。。

あと、2の改善のために学習データの追加と学習、検証、実機でのテストプレーという一連のワークフローを効率的に回す仕組みが無いとやってられん。
SSDとResNet34で学習データと、テスト結果、重みの組を管理する仕組みが必要。
まずはそこだろうか。あとは、このワークフローが完成してNo2の改善がイマイチとなると、一回、深層学習の基本に戻って調査し直すしかあるまい。

このワークフロー議論は以下のレポジトリで作業する。
https://github.com/miyakz1192/dl_image_manager

2023/01/28
-----------

SSD/ResNet34で好成績が出たので、これをGAAに組み込む。
今、closeの場所の検出のため、GAAからはpytorch(SSD)を呼び出している。
インタフェースとしてはscpで画像をpytorch(SSD)側に送付して、pytorch(SSD)を動作させ、結果のDetectionResultContainerをダウンロードする。
GAAでDetectionResultContainerを解析する。
インタフェースはDetectionResultContainerなので、これを変更しなければ基本的に問題ない。

このため、GAA側を変えずにpytorch側を変更する。
基本的には、GameEyeというコンポーネントを新たに作成して、そこが、SSDとResNet34を動作させ、結果となるDetectionResultContainerを吐き出す。
GAA側は起動するファイル名の変更のみ。


2022/12/27
------------

画像を管理するフレームワークを作った。今後はこれを使うことで、
データの管理がぐっと楽になると考えられる。

https://github.com/miyakz1192/dl_image_manager.git

今後、画像認識の精度などの話は、dl_image.rstに記載することにする。

2022/12/18
------------

gaaは画像認識の精度さえ向上すれば使い物になりそうだということがわかってきた。
また、scrcpyサービスとgaaサービス本体は同一サーバ(gaa-server)に配備されており、また、
pytorchサービスはこれとは別のサーバに配備されている(pytorch-server)。

したがって、gaaサービスの本質的な質を改善しようと考えた場合、
単にpytorch-serverに着目して改善作業を淡々と行っていけば良いということになる。

よって、これからはしばらく、画像認識、物体検出の精度向上にどっぷりと
取り組むことにする。まず、以下の課題１つ１つについて取り組むことにする。

課題

1.文字を変にcloseと認識してしまう。

　i.逆に大量の文字を学習させれば良い。これでcloseとの区別がつくようになるはず。
2.○　の中にバッテンのタイプを認識できない

　i.このタイプのcloseを学習させる必要あり
3.背景が透けているバッテンが認識されない。

　i.data augmentationで学習データを大量に作る必要がありか。

まず、課題の1から。作戦としては、いろいろとありそう。検討したものをとりあえず列挙していくが。

1. フリーのフォントをトレーニング画像として学習する。

   1. ただしこの方法ではフォントデータの中身を調べる必要があるのでめんどくさそう

2. matplotlibでテキスト描画してsavefigでjpegとしてsaveしてやる(32 x 32画像くらいか?)

   1. matplotlib周りはいじってきたのでなんとかなるか？


ということで2の方法で試してみる。結果として、座標軸も含めて画像がsaveされてしまうので、
学習用のデータとしては具合が悪い(文字データをそのまますぐに学習データとして利用できない）
ことがわかった。

しかし、これはプログラミングの工夫により克服できたため、No2の方法をそのまま採用

2022/12/16~17
-------------

基本的なアルゴリズムの動作は以下のコミットでできるようになった。
ただし、エラー時のリトライとかがなく、かなり使いづらい。

commit bb96851083b2c166039a5f15711951a44b360b57 (HEAD -> master, origin/master, origin/HEAD)
Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
Date:   Fri Dec 16 16:54:38 2022 +0000

    gaa update(naive algo is ver 0.1 done)

さらに、AIの画像認識精度があまく、正しくcloseを押せないという。。。。
エラー時のリトライとかはとりあえず置いておいて、
今後は如何にcloseの認識精度を高めるかについて追求していく必要がある。

課題

・文字を変にcloseと認識してしまう。
　→　逆に大量の文字を学習させれば良い。これでcloseとの区別がつくようになるはず。
・○　の中にバッテンのタイプを認識できない
　→　このタイプのcloseを学習させる必要あり
・背景が透けているバッテンが認識されない。
　→　data augmentationで学習データを大量に作る必要がありか。


2022/12/14
----------------

以下に取り組む。

pytorch側の改造
　・detectした結果をpythonのデータファイル(たしか、pickleとかいったやつ)で、保存する

→　DONE
commit e39a77f459ac568a259531f0a3959280d9e263a6 (HEAD -> gaa_v1, origin/gaa_v1)
Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
Date:   Wed Dec 14 14:56:00 2022 +0000

    pickle data save/load support

commit cebc638fe83c8bc6eab0dc85c1c4f186c90793bf (HEAD -> gaa_v1, origin/gaa_v1)
Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
Date:   Wed Dec 14 15:04:17 2022 +0000

    detection_result.py added

　・screen_shotの左上400 x 400画像と右上 400 x 400画像を生成する。
　・screen_shotをscpで送る(serviceクラスのscp対応、sshpassが使える)
　・pytorchクラス側でdetectを実行する

こちらもＯＫ。ただ、closeじゃない所も変に認識していそうできになる。
今後debuggingしていくこととする。


2022/12/14
---------------

超単純なバージョンの完成をまずは目指す。
枠組みさえできれば、後はデータを集めて学習させるだけという作業に集中できるので。

pytorch側の改造
　・detectした結果をpythonのデータファイル(たしか、pickleとかいったやつ)で、保存する

gaa側の改造
　・screen_shotの左上400 x 400画像と右上 400 x 400画像を生成する。
　・screen_shotをscpで送る(serviceクラスのscp対応、sshpassが使える)
　・pytorchクラス側でdetectを実行する
　・結果を取得する
　　※　各画像（左上、右上）について繰り返して、結果をマージてscoreでソートする
　・（pickleファイルを開き）結果を解析する(closeのスコアがもっとも高いpositionを抽出)
　・ためしに、画面に表示してみる

gaa側の改造
　・touchに対応する。

