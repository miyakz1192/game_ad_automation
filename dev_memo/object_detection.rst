===============================
物体検出の開発メモ
===============================


課題
=====

以下のgitレポでの考察を引き継いでここで行う。

  https://github.com/miyakz1192/ml_study/blob/master/pytorch/hello_pytorch.rst


漢字や日本語は誤検出が多いがそれなりに検出出来るようにはなった。しかし、以下のような困った事態が発生した

使った重みは以下。::
  a@pytorch:~/pytorch_ssd$ sha256sum close_weight_0.6436714378563133.pth
  15ba29eab2f8162bb5663d07acb812986c06b063a2bc542974e6db43a93cb94e  close_weight_0.6436714378563133.pth
  a@pytorch:~/pytorch_ssd$ 

  ※　若干古い重み。2022/12/27のweights/close_weight_0.4379034004363406.pthでは試していないのだが、多分、同じ。


1. 本物ののcloseなのにja_charと誤認識してしまう
   hit enter file==> imgdata/lu_Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ただ、こちらは、白地に黒色のバッテン。いままで、黒字に白色のバッテンを学習していたので、コントラストが逆。
   このタイプのバッテンは一度もinputしていない。なので、ja_charと判定されたか。


2. 本物のcloseだけどcloseと認識しない。

   hit enter file==> imgdata/ru_Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの


あと、薄いグレー地に白色のバッテンは相変わらず認識してくれない。

hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg

hit enter file==> imgdata/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg

hit enter file==> imgdata/ru_Screenshot_2022-12-07-15-40-28-75_56bd83b73c18fa95b476c6c0f96c6836.jpg

このバッテンは人間でもわかりにくい感じがするが、見分けがつく。
これより薄いグレーにしたら、インアクティブなバッテンとの区別がつかなくなりそうでかなり微妙な路線。

hit enter file==> imgdata/ru_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg

これは漢字を背景に、薄いグレーの上に白地のバッテンが重なったもの。
closeは認識しないが、ja_charは認識した例。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836.jpg

closeもja_charも特に認識しない。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg

本物のcloseはあるのだけど、やっぱり薄いグレー地に白色のバッテンは弱い。
代わりに変な所をcloseと認識(0.62)


hit enter file==> imgdata/ru_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg

ただ、どういうことか、こちらの画像では薄いグレー地に白のバッテンは0.83で認識

hit enter file==> imgdata/lu_Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
同上(0.84)

あとは、画像残っていたけど、力尽きた。時間あれば追加確認。

以下、最初のトライでＮＧが出た画像で今回のトライで認識されていいるNG(例：薄グレー地に白バッテンなど)を除いたものを確認。
結果、誤検出はなくなり、今回の重みはかなり進歩していることが確認できた。

以下、2022/12/27版のweights/close_weight_0.4379034004363406.pthで確認。

hit enter file==> data/lu_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：「本当のcloseがそもそも含まれない画像。しかし、漢字をcloseとご検出してしまっている。
漢字が多いと確かに、closeのバッテン(クロス)が含まれるので、ここを誤検出している。
漢字は厄介だ。。。」
　→　漢字をcloseと誤認識することはなくなった。ja_charを数文字検出

hit enter file==> data/ru_Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：本当のcloseがそもそも含まれない画像。宣伝のゲームの中にcloseと誤検出されるものが混じってしまっている。
　→　closeの誤認識はなくなった。

hit enter file==> data/lu_Screenshot_2022-12-05-20-23-33-26_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：ゲーム画像を誤検出。見た感じバッテンの要素は全然なさそうだが、、、
　→　誤検出はなくなった。

hit enter file==> data/lu_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：漢字を誤検出
　→　誤検出はなくなった。ja_charを数文字検出

hit enter file==> data/lu_Screenshot_2022-12-08-18-32-13-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ： 誤検出。ただし、0.6と低い数値だが。
　→　closeの誤検出はなくなった。ja_charを２文字検出。ただし、いずれも誤検出。closeの誤検出はなくなったので良しとする。

hit enter file==> data/lu_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ：   漢字を誤検出。白色のバッテンを検出しないのはエライのだが、「残」を0.95とかなり高い確率で誤検出。
　→　closeの誤検出はなくなった。ja_charを正しく検出。

hit enter file==> data/lu_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ： 漢字「者」を0.84で高い誤検出
 →　誤検出はなくなった

hit enter file==> data/lu_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ： ゲーム中の顔？を0.95位で高い誤検出
　→　誤検出はなくなった。

hit enter file==> data/ru_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
  最初のトライ： 充電の電池記号を0.86で誤検出。なんで。。。
　→　誤検出はなくなった。

hit enter file==> data/ru_Screenshot_2022-12-10-10-17-54-32_56bd83b73c18fa95b476c6c0f96c6836.jpg
  最初のトライ： closeは無いのだが、他の麻雀牌とか背景っぽいものをご認識してしまっている0.7位
　→　誤検出はなくなった。


トライ3の考察
==============

上手く認識しないバッテンに傾向あり。以下の施策が効果あがりそうな気配。

1. 白地に黒色のバッテン

2. ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの

3. 薄いグレー地に白色のバッテン

あとは、ja_charのパターンをもっと増やせば(現在1000文字)、認識精度が上がるかもしれない。なので、

4. ja_charデータのさらなる追加(目安+1000?)


トライ4の準備
==================

まずは、白地に黒色のバッテンを学習させてみることにする。

closewというprojectをつくり、sample/daug.pyのsuiteでdata augmentationをしている。
なお、ラベルはclose。(close projectと同じ、あえて同じラベルにしてみている)

ラベルを別にしたらどうか？という考えもあるが、まずは、同じラベルで行ってみることにした。
