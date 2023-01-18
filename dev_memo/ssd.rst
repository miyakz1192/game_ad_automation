==================================================
SSD
==================================================

まず、過去の"トライ3"で以下の問題が合った。

トライ3の考察
==============

上手く認識しないバッテンに傾向あり。以下の施策が効果あがりそうな気配。

1. 白地に黒色のバッテン(BCOW) 

2. ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの(WCOBFAT)

3. 薄いグレー地に白色のバッテン(WCOLG)

あとは、ja_charのパターンをもっと増やせば(現在1000文字)、認識精度が上がるかもしれない。なので、

4. ja_charデータのさらなる追加(目安+1000?)

トライ4の実行
===============

まず、3についてデータを追加してSSDを学習して試してみよう。
4はやらない。1と2は3の様子見で。

1も2も3も上手くdetectせず。
おそらく、黒字に白地バッテンと3の画像がコントラストが真逆なので、上手く学習できていないと思われ。

なので、close(黒字に白地バッテン)と、WCOLGを分けてみる。
まずは、

closebcow
closewcobfat
closewcolg
close

に分けてみる。それでも良くない。

トライ5の実行
==============

ここで前々から気になっていた、SSDで物体検出をする前にエッジ加工した画像を入力することを考えてみる。
このため、学習するcloseもエッジ加工したものを学習した重みを作ってみる。
closeedgedを学習させて、ssdを通す(predict.py)を通す前にエッジ検出させる。
そうすると、概ねcloseの位置を検出するようになった。ただし、誤検出は多い。
これはResNet34でフォローする方向性。

● NGのリスト(再学習が必要)

ただし、以下について、ssdでも(edged)でも検出しなかった。
小さいclose。edge加工後の画像ではcloseは乗っているので、ssd側の問題か。

以下もちょっと違う感じのclose

hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-53-51-24_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-47-20-13_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-40-04-37_56bd83b73c18fa95b476c6c0f96c6836.jpg

これは検出しないのはなんでだろう。丸付きのcloseとして学習する必要があるか。
hit enter file==> imgdata/ru_Screenshot_2022-12-17-00-42-38-93_56bd83b73c18fa95b476c6c0f96c6836.jpg

漫画背景のclose。edge画像ではcloseが明確に確認できるが、、
hit enter file==> imgdata/ru_Screenshot_2022-12-17-00-44-59-62_56bd83b73c18fa95b476c6c0f96c6836.jpg

●　これ以上頑張らずに捨てるもの(GLAY)
進捗中の以下をcloseとしてご認識するが、これは正直むずかしい。。。

hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-44-38-20_56bd83b73c18fa95b476c6c0f96c6836.jpg

がっつり漢字背景(100%かぶる)はやっぱり認識しない。これは捨てたほうが良い。

hit enter file==> imgdata/ru_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg

これはずるい。
hit enter file==> imgdata/ru_Screenshot_2022-12-19-10-36-23-02_56bd83b73c18fa95b476c6c0f96c6836.jpg
edgeにすると、closeの左半分がぐちゃぐちゃになる

これは最悪。人間が見てもcloseと判別が難しいレベルだし、edge画像でもcloseが表示されない。
hit enter file==> imgdata/ru_Screenshot_2022-12-19-10-47-58-33_56bd83b73c18fa95b476c6c0f96c6836.jpg
すてても良い。

●　以下顕著な結果となったもの(GOOD)

ただし、以下をcloseと認識するようになったのは驚き。

hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-44-05-48_56bd83b73c18fa95b476c6c0f96c6836.jpg

しかし、ちょっとくらい漢字は背景(20%位)はＯＫなのは驚き
hit enter file==> imgdata/ru_Screenshot_2022-12-08-18-26-54-47_56bd83b73c18fa95b476c6c0f96c6836.jpg


とはいえども、edgeでcloseが表示されるようになれば、上記のような人間が見ても難しいレベルでもcloseと認識されるようになったのは驚き。
hit enter file==> imgdata/ru_Screenshot_2022-12-21-15-54-22-41_56bd83b73c18fa95b476c6c0f96c6836.jpg
t enter file==> imgdata/ru_Screenshot_2022-12-21-16-03-42-18_56bd83b73c18fa95b476c6c0f96c6836.jpg

FATでぼやっとした(白地に薄いグレーでclose)でもcloseと認識。これも若干驚きの結果を得た。
hit enter file==> imgdata/ru_Screenshot_2022-12-21-16-07-09-38_56bd83b73c18fa95b476c6c0f96c6836.jpg

トライ6の計画と実行
========================

計画
-----

トライ5で学習させたja_charはedgedじゃなかった。このため、edged画像を入力とした際にja_charの検出があまりなかった。
(そもそも、入力edged画像にja_charぽいものが皆無だったということもあるかもしれないが)。

ただ、現状の重みでは非edgedなja_charを学習してしまっているため、本来ではないので、ja_charをedged画像にしたものを学習させることにする。

また、上記トライ5で上手く検出しなかったclose(NGリスト)に関しても新しくprojectを作って学習させる

実行結果
----------

結果は全然だめだった。今までちゃんと認識していたcloseも全く認識せず。
理由はおそらく、以下の画像種別についてclose4をラベルcloser。その他をcloseにしたためかもしれない。
本当はそれぞれ違うcloseとして認識する必要があったのかも

closee1:
closee2:
closee3:
closee4:
closee5:
closeedged:

トライ7の計画と実行
=========================

計画
-----

上記の勘をうけて、各closeを違うcloseなラベルにする。わかりやすさのため、project名とlabel名を合わせることにする。

実行結果
----------

全くだめ。トライ6と変わらず。
ここで、デバックのため、１つ１つ行ってみる。
まずは、closeedgedを追加して、それからcosee1~5といくが、close4だけを抜かして追加してみる。

以下、サイズがダメなのかな。修正してためしてみたけど、結果は同じ。

::

  @dataaug:~/dl_image_manager$ diff -u projects/closeedged/master/image_extended.xml  backup_project/close/master/image_extended.xml  
  --- projects/closeedged/master/image_extended.xml	2023-01-17 14:13:27.996172267 +0000
  +++ backup_project/close/master/image_extended.xml	2023-01-15 06:20:38.924421923 +0000
  @@ -6,21 +6,21 @@
   		<database>Unknown</database>
   	</source>
   	<size>
  -		<width>64</width>
  -		<height>64</height>
  +		<width>32</width>
  +		<height>32</height>
   		<depth>1</depth>
   	</size>
   	<segmented>0</segmented>
   	<object>
  -		<name>closeedged</name>
  +		<name>close</name>
   		<pose>Unspecified</pose>
   		<truncated>1</truncated>
   		<difficult>0</difficult>
   		<bndbox>
   			<xmin>1</xmin>
   			<ymin>1</ymin>
  -			<xmax>64</xmax>
  -			<ymax>64</ymax>
  +			<xmax>32</xmax>
  +			<ymax>32</ymax>
   		</bndbox>
   	</object>
   </annotation>
  a@dataaug:~/dl_image_manager$ 


backup/bad_20230118_close_weight_0.7472505326704545.pth

なお、edged画像の入力とgood_backup/close_weight_0.4379034004363406_20221227.pthの相性は良い。
この重みのタイムスタンプを見ると、2022/12/28だった。つまりこの時の訓練画像は非edge。
つまり、非エッジで学習させた重みと、エッジ画像の入力は相性が良い様子。

ここで１つ。面白いことに気づいた。今まで、認識しなかったcloseは位置が悪いのではないか？ということだ。
以下の画像だが、最初認識しなかったclose画像を少しずつ場所を移動したものだ。::

  a@pytorch:~/pytorch_ssd$ ls -l funny_experiment/
  total 56
  -rw-rw-r-- 1 a a 10530 Jan 18 14:08 edged_ng1.jpg
  -rw-rw-r-- 1 a a  6946 Jan 18 14:10 edged_ng2.jpg
  -rw-rw-r-- 1 a a  8162 Jan 18 14:12 edged_ng3.jpg
  -rw-rw-r-- 1 a a  8156 Jan 18 14:09 edged_ok1.jpg
  -rw-rw-r-- 1 a a  8172 Jan 18 14:11 edged_ok2.jpg
  a@pytorch:~/pytorch_ssd$ 
  
edged_ok1,2は左上に配置。edged_ng1,2,3は少しずつ左上から右下方向にずらして行ったもの。
ある位置で全く同じclose模様だけど、認識する、しないといったことが確認できた。

どこかの記事で「SSDは位置を学習するものだ」と見た記憶がある。多分、これがそうなんだろう。
ということは、単純に、closeedgedの模様だけで、位置のバリエーションを変更するだけで、
認識率があがるのでは？ということになる。

以下、過去認識しなかったcloseである。ドンピシャで、すべて右上である。

hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-53-51-24_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-47-20-13_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-40-04-37_56bd83b73c18fa95b476c6c0f96c6836.jpg

これは検出しないのはなんでだろう。丸付きのcloseとして学習する必要があるか。
hit enter file==> imgdata/ru_Screenshot_2022-12-17-00-42-38-93_56bd83b73c18fa95b476c6c0f96c6836.jpg

漫画背景のclose。edge画像ではcloseが明確に確認できるが、、
hit enter file==> imgdata/ru_Screenshot_2022-12-17-00-44-59-62_56bd83b73c18fa95b476c6c0f96c6836.jpg

トライ5で時々右上でも認識したのは、おそらく、訓練画像の中に微妙にサイズが大きいclose(82 x 82)とかが混じっていた影響かもしれない。
というわけで、以下の仮説が生まれてきた。

1. 訓練画像はカラーが良い(エッジにすると却って認識率が低下？)
2. 訓練画像は従来通り400 x 400として、従来の左上配置に加え、右上配置も加える(projectは分けたほうが扱いやすいかもしれない)
3. 入力画像はエッジが良い(画像から余計な情報が削ぎ落とされるためか)

トライ8の計画と実行
======================

計画
------

まず、トライ5で使った訓練画像を復活させる::

  a@dataaug:~/dl_image_manager$ ls projects/close* | grep projects
  projects/close:
  projects/closebcow:
  projects/closegb:
  projects/closewcobfat:
  projects/closewcolg:
  a@dataaug:~/dl_image_manager$ 

ちょっと無駄が多いが、現状１つの訓練画像に対して、１つのannotation前提で作ってしまっているため、
右上配置のために同じようなプロジェクトを作る必要がある。
例えば、closeだったら、master/image.jpgは同じなんだけど、image_extended.xmlが右上配置になっている。
また、しかし、daug.pyのなかで使うDataAugmentationのクラスに対して、右上モードになっている。という感じで。

その上でDetaAugmentationのクラスを拡張して、右上に配置するモードを追加してみる。

プロジェクト名の規約を追加するデフォルトで左上配置とする。"ru_"の接頭辞をつけると、右上配置にする。
  

  






おまけ1
==========

テスト用のゲーム画像（スマホサイズの縦長)に本当のcloseの位置(正解)をアノテーションしたものを入力として、自動テストするためのプログラムを作成する。
そのプログラムはディレクトリを読みこんで画像.jpg,画像.xml(VOC形式)とする。画像内部に複数のアノテーションを仕込むことができる。

以下の計算によって、スコアリングを行う。
　box_score・・・答えのboxに近いboxの個数。近いとは、答えの左上の座標(ans origin)に関して、推測のans originがおおよそx%の近傍にあれば、1点カウントする。さらに答えのwidthと推測のwidthがおおよそx%であれば1点。heightも同様に1点。という加点方式で行く。推測のカウント/4 * 答えのbox数 * 100がbox_score
　label_score・・・ 答えのboxに対して、3点を稼いだ推測のboxがあれば、そのすべての推測boxのlabelと答えのlabelとを比較して等しければ100%。
　　　　　　　　　　答えのboxに対して、2点を稼いだ推測のboxがあれば、そのすべての推測boxのlabelと答えのlabelとを比較して等しければ60%。
　　　　　　　　　　答えのboxに対して、1点を稼いだ推測のboxがあれば、そのすべての推測boxのlabelと答えのlabelとを比較して等しければ30%。
　　　　　　　　　　答えのboxに対して、点を稼いだ推測のboxが１つもなければ、0%

  x値・・・近傍の%であり、テストの厳しさの指標。デフォルトで10%

