====================================
学習に利用する画像群の管理について
====================================

現在におけるgaaの学習用画像の管理についてメモしておく(忘れないように)。
学習用画像は、フレームワークが変わったとしても使い回しが効く共通的なもののため、
ちゃんと管理が必要だと思う。


管理のカテゴリ
===============

ざっくりと以下に大別できる


1. 元ネタ画像をもとにdata augumentationで大量生成

   1. すでにdata augumentationされたもの

   2. これから新しい元ネタ画像をもとに、data augumentationしようとするもの


2. ゲーム画像

   1. すでにあるデータにアノテーションが加えられたもの

   2. これからアノテーションしていくもの

3. 単に学習結果を確認するために用意したゲーム画像

学習用画像の作成は以下のサーバで使い分けて実施している。

1. dataaugサーバ：元ネタ画像からdata augumentationを実行して大量生成

2. image labelingサーバ：アノテーションのみを実行するサーバ

data augumentation用のプログラムは以下になる

https://github.com/miyakz1192/ml_study.git

ここのjupyter notebook。用途によって使い分けている(後述)

それぞれについて、メモしておく


1-1. 元ネタを元にdata augumentationされて大量生成。すでにdata augumentationされたもの
======================================================================================

ja_charsの場合
----------------

data augumentation用のサーバ(dataaug)でjupyter notebook(darknet/charactor.ipynb)を使っている。
これを実行すると、./ja_chars/配下に大量のjpg画像が生成される。

annotationは固定になっているので、/home/a/labelImg/annotation_data_master/ja_char/master.xml
を元ネタにlily2にあるget_augmentation_data_ja_char.shを実行すると、xml付きのannotation data群(jpg/xmlの組)が
手元にダウンロードされる便利スクリプトになっている。

それをpytorchサーバに持って行って展開する形。train.txt val.txt などのtrain/valの比率などはその場で適当に決めている。

closeの場合
-------------

こちらのほうはもっと適当で、dataaugサーバでjupyter notebook(darknet/data_augmentation_2.ipynb)で生成されたもの(data_aug_close配下に生成)
されたものを適当にxmlを作ってpytorchサーバに配置している。以下、ja_charsの場合と同様。


1-2. これから新しい元ネタ画像をもとに、data augumentationしようとするもの
======================================================================================

概ね以下の流れで実施する。

1. 元ネタ画像をgimpを使って切り出して(closeならclose)、それを単体のjpgとして保存

2. 元ネタ画像をdata augumentationするプログラムをjupyter notebookで作成していく。理由は、生成された画像を確認しながらすすめることに適しているため。(自動化には向かないので、別途スクリプト化は必要か) 

3. 次にimglabelingサーバでVOC形式やその他の形式でannotationデータを作る。生成したannotationデータは上記No2で作成されたすべての画像共通になるので、これを使いまわせる。元ネタのannotationデータをどこかに保存しておく

3. lily2にて、生成されたjpgファイルとannotationデータが対になるようにしてtar.gzを生成。ダウンロードする


2-1. すでにあるデータにアノテーションが加えられたもの
===========================================================

ゲーム画像。これはケースとして少ないので無視していく。捨てても良い。
data augumentationして大量学習させるほうが重要なので。

3. 単に学習結果を確認するために用意したゲーム画像
======================================================

こっちはpytorchサーバのimgdataディレクトリに大量に格納されている。

問題
=====

1. 今後新しい元ネタ画像をもとに、data augumentationしたいという要望が増えそうだが、いちいち個別の手順で回していたら大変。

2. 管理が適当なので、どこに何のデータがあるかわからない。

   1. マスターデータとしてソース管理すべきは何か。

   2. 自動生成される画像はソース管理から外す。

　 3. 常に最新の学習データが自動でぽんと生成されるようにしておきたい 

3. ソース管理の適当さ

   1. data augumentationで自動生成するプログラムの管理。jupyterで作るのは良いが、自動化に向かない。

4. 単に学習結果を確認するために用意したゲーム画像の管理

   data augumentationデータは元ネタからいつでも同じデータが自動生成されるので良いが、このケースはそうではない。

問題に対する対応方針
=========================

管理のフレームワークを作っていき、学習データ作成環境を構築していく感じにする。
サーバが分かれているので、それも考慮していきたい。

なお、この学習データを生成する手順自体はgame ad augumentationに限ったものではないので、
他の用途に使えるように一般的な？名前のリポジトリを作ってソース管理していくことにする。
(しばらくはこっちの環境作成に注力する必要がありそう。。。)

https://github.com/miyakz1192/dl_image_manager.git
