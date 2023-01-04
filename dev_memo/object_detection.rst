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

トライ4の評価
=================

重みは以下を使用::

  -rw-rw-r-- 1 a a 105166065 Dec 28 12:45 close_weight_0.44697260103727643.pth

以下の過去のＮＧに対して評価

1. 本物ののcloseなのにja_charと誤認識してしまう
   hit enter file==> imgdata/lu_Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ただ、こちらは、白地に黒色のバッテン。いままで、黒字に白色のバッテンを学習していたので、コントラストが逆。
   このタイプのバッテンは一度もinputしていない。なので、ja_charと判定されたか。

　　　→　今回、こちらは本物のcloseをcloseとして0.96、ja_charとして0.93で検出した。ただし、時刻をなぜか0.90で誤検出しており、
　　　　今後改善が必要か。数字を覚えこませる必要が出てきた。


2. 本物のcloseだけどcloseと認識しない。

   hit enter file==> imgdata/ru_Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの

   　→　closeとして0.97,ja_charとして0.83で認識しており上手く行っている


あと、薄いグレー地に白色のバッテンは相変わらず認識してくれない。

hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　上手く行っている。closeを0.85で認識

hit enter file==> imgdata/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　上手く行っている。closeを0.75で認識

hit enter file==> imgdata/ru_Screenshot_2022-12-07-15-40-28-75_56bd83b73c18fa95b476c6c0f96c6836.jpg

このバッテンは人間でもわかりにくい感じがするが、見分けがつく。
これより薄いグレーにしたら、インアクティブなバッテンとの区別がつかなくなりそうでかなり微妙な路線。

　→　上手く行っている。closeを0.96で認識


hit enter file==> imgdata/ru_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg

これは漢字を背景に、(スケた)薄いグレーの上に白地のバッテンが重なったもの。
closeは認識しないが、ja_charは認識した例。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836(1).jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-08-23-19-13-78_56bd83b73c18fa95b476c6c0f96c6836.jpg


　→　closeは認識しなかった。ja_charは認識。ただし、漢字の上にスケた薄グレー地に白バッテンは、closeともja_charとも認識しない。
　　余分な考察かもだが、万、円をja_charとして認識しないのがちょっと気になる。この２つの文字は学習対象ではある。
    万、円をそれぞれ別のclassとして定義せず、ja_charとして定義してしまっているので、区別ができにくいモデルになってしまったのが原因なんだろう。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg

本物のcloseはあるのだけど、やっぱり薄いグレー地に白色のバッテンは弱い。
代わりに変な所をcloseと認識(0.62)

　→　closeの誤認識はなくなった。何も検出なし。


hit enter file==> imgdata/ru_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg

ただ、どういうことか、こちらの画像では薄いグレー地に白のバッテンは0.83で認識
　→　closeを0.99で認識

hit enter file==> imgdata/lu_Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
同上(0.84)
　→　　こちらは0.68で認識

hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-36-48-57_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　これは上手く行っている。昔は検出しなかった。


以下、別件のNG

hit enter file==> imgdata/lu_Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.jpg
　数字をcloseとしてご認識してしまっている。数字の学習が必要かと。

hit enter file==> imgdata/lu_Screenshot_2022-11-19-10-01-08-52_56bd83b73c18fa95b476c6c0f96c6836.jpg
　しかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われる→　本物のclose(白地に黒のバッテン)をcloseではなく、ja_char0.99で誤認識してしまった模様。
　　バッテンと漢字が本質的に似ているのが原因かと思われる(例：十の45度回転させたものがバッテンになるので、CNNを使ってざっくり抽象的にＮＮが
　しかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われるしかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われる　理解してしまえば、十もバッテンも違いがわからなくなる)。。
　　漢字も斜めの線を書くような文字は膨大にあるし。。。
   バしかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われるしかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われるしかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われるッテンを強くモデルに認識させたほうが良いのか？他のcloseのパターンも追加学習が必要？？？

　

hit enter file==> imgdata/lu_Screenshot_2022-11-19-10-01-46-26_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-17-10-04-26-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-17-10-07-32-67_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　漢字、カタカナなどのもじを完全にcloseとご認識してしまっている！！！これは結構クリティカル
     上から３番目の事例は、0.82のcloseは正解。0.99のcloseは誤認識している状態。
     ２つの検出したcloseを別のAIでもう一回判別してみるという、答え合わせ、別のＡＩで再検証みたいなものは
     必要かもしれない

hit enter file==> imgdata/lu_Screenshot_2022-11-21-12-10-27-45_56bd83b73c18fa95b476c6c0f96c6836.jpg
 →　○の中に？を0.65と低いがcloseとして誤認識


hit enter file==> imgdata/lu_Screenshot_2022-12-04-23-41-33-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　確か、昔はちゃんとcloseが認識できていたやつかも。本物のcloseをja_char 1.00と超誤認識

hit enter file==> imgdata/lu_Screenshot_2022-12-04-23-45-39-70_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/lu_Screenshot_2022-12-17-10-04-26-95_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　確か、昔はちゃんとcloseが認識できていたやつかも。本物のcloseをja_char と超誤認識

hit enter file==> imgdata/lu_Screenshot_2022-12-04-23-53-21-90_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　スピーカのアイコンをcloseと誤認識(0.86で結構でかい)
hit enter file==> imgdata/lu_Screenshot_2022-12-04-23-55-37-57_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/lu_Screenshot_2022-12-17-10-02-33-37_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　同様

hit enter file==> imgdata/lu_Screenshot_2022-12-17-10-07-32-67_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　「の」をcloseと認識(0.65)
hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-49-02-73_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　漢字をcloseと誤認識

hit enter file==> imgdata/lu_Screenshot_2022-12-17-22-01-47-13_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　化粧品の画像を0.76で誤認識

hit enter file==> imgdata/lu_Screenshot_2022-12-19-10-36-23-02_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　変なもんを0.82でcloseと誤認

hit enter file==> imgdata/lu_Screenshot_2022-12-21-16-07-09-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　文字をcloseと同時にja_charと認識。白地に黒の文字

※　closeの認識は0.9以上を採用すれば誤認識はなさそう(0.95以上？？)

hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-35-14-37_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　ただ、こちらは0.94~0.96で高い誤認識

hit enter file==> imgdata/lu_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
 →　数字を0.67でcloseと誤認識

hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　上手く行っている。closeを0.85で認識

★　★　★
hit enter file==> imgdata/ru_Screenshot_2022-12-04-23-43-31-18_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　これは厳しい。LOARDS MOBILEの画面で、白に近い薄い青空（絵）の上に白のバッテン。人間でも認識しづらい。
　　　（がよーくみれば認識できる。人間ならば認識できそう）単純に白のバッテンではなく、白のバッテンの周りに
　　とても薄く黒のモヤがかかっており、それがあるため、白の×であることが辛うじて認識出来るという感じ。
　　非常に厄介なパターン
hit enter file==> imgdata/ru_Screenshot_2022-12-19-10-36-23-02_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-21-16-03-42-18_56bd83b73c18fa95b476c6c0f96c6836.jpg

　→　これは更に厳しい。人間でもなかなかわからないかもしれない。ギリギリわかるかもしれないってれべる

バッテンもja_charも同じような枠組みで学習させているのがまずいんじゃないか。
バッテンはバッテンとして特徴を持っているので、それを強調させて覚えこませるとか、何か、必要じゃないか
（帰納バイアス的な何か)

hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-43-12-59_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　ゲーム画像の「ス」をcloseと誤認識(0.61で低いが)

hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-44-05-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　白の○　の中に　、白の×　。これをcloseと認識せずに、ja_charと認識(0.99)。
　　白地の×を検出するはずだが、何故か検出せず。
hit enter file==> imgdata/ru_Screenshot_2022-12-06-10-44-38-20_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　ただし、こちらは全く似たような感じだけど、closeで0.77で認識

hit enter file==> imgdata/ru_Screenshot_2022-12-21-15-54-22-41_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　ただし、こっちはほぼ、白地に白のバッテン（白バッテンの周りに薄いもや）を0.88で認識している。
　　LOARDS MOBILEとの違いは白地か、そうでないか。ということはわかってきている。
hit enter file==> imgdata/ru_Screenshot_2022-12-21-16-07-09-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
　→　白地に薄いグレーのバッテンを認識(0.81)

トライ4の考察
================

トライ３の考察は以下だった。
「上手く認識しないバッテンに傾向あり。以下の施策が効果あがりそうな気配。」

1. 白地に黒色のバッテン 
   →　たしかに、白地に黒を認識するようになったが、ja_charとの誤認識も存在した。別途対策が必要

2. ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの
   →  No1と同様

3. 薄いグレー地に白色のバッテン
   →　こちらはこういったprojectを用意しなくてもNo1のprojectを追加するだけで何故か、認識しだした（理由は全く不明！）

あとは、ja_charのパターンをもっと増やせば(現在1000文字)、認識精度が上がるかもしれない。なので、

4. ja_charデータのさらなる追加(目安+1000?)
   →　今回は試していないので効果は不明

また、以下のこともわかった。

5. 数字をcloseとして誤認識している。これは数字を学習させることで解決出来る可能性が高い。数字の姿はバッテンと共通する所が少ないと思われるので、数字はja_charと違うクラスにしたほうが、全体的なcloseの精度向上に寄与するものと想定

6. 白地に黒のバッテンをja_charとして誤認識してしまう。
   おそらく、漢字とバッテンが本質的に似ている（例：十と✕　の比較）がある。複雑な漢字は更に、払い、縦、横などで✕　に似てくる部分が生じてくる。しかし、人間が見ると、明らかに漢字と✕　は違う。帰納バイアスを入れるとか、別のＡＩによる結果の検証などが有効かと思われる

7. ○　の中に？をcloseとして誤認識

8. ○　の中に✕　をcloseとして認識しない(ja_charとして誤認識)

9. スピーカーや手のアイコンをcloseとして誤認識(0.86などとでかい)

10. 誤認識するパターンとそうでないパターンをざっくりと分けるため、0.6でなく、0.8をしきい値にしたほうがよい。

11. 漢字が背景にあるのは認識しない。
    
12. 薄い青空に白地のＢＡＴＴＥＮＮも認識しない

対策の検討
----------

1. 数字を学習させる(数字をcloseと誤認することへの対策)

2. ○　の中に?を別のラベルとして学習させ、closeと区別を付けさせる(○　の中の？をcloseとして誤認することへの対策)

3. ○　の中に✕　を新たにcloseシリーズとして加える(○　の中に　✕　をcloseシリーズとして認識させること）

4. DLによる画像認識なのかわからんけど、バッテンの特徴を抽出するような何かを考える。 (漢字とcloseを誤認識することへの対策)

5. 漢字が背景にあるのは、もう、諦める(努力の割にはみのりが少なそうな直感あり)


何気に一番重要なのはNo4っぽい。ただ、良いアイデアが全然浮かばない。
例えば、バッテンは同じ値の画素が直線上にある程度伸びており、その線分の中点を通り、直角に交わるまた、同じような直線があるとき、バッテンと見なせそうだけど、おそらく、漢字にもバッテンを一部に含むような漢字がある。このような両者を比較した際に、バッテンと漢字（バッテンを部分的に含むような漢字）の区別がつかないだろう。おそらく、CNNが原因でこうなっているのだと思う。

要するに、SSDでざっくりと物体を検出したら、その先は厳密な何らかの方法でバッテンかどうかを最終判断するような感じの処理が良いのかな？？

トライ5
========

ゼロつくdeep learningで認識度99%の畳み込みネットワークが最後に紹介されていたため、この活用を検討する。
要するに、SSDでざっくりと物体を検出した後、その画像がcloseか否かを別のAIで判別するというアイデア。

この作戦は、実行時間を要する(SSDによる物体検出時間＋CONVNETによる画像判別時間）問題があるが、精度を向上したいため、
実行時間はとりえず、度外視で考えてみる。

ここで、漢字、ひらがな、カタカナをja_charとよぶことにする。

ひとまず、ゼロつくの8章、Deep Convnet(DCONVNET)に対して、ja_char画像1000文字+closeを判別させることを考えてみる。
それには、ja_char1000文字の各文字をdata augmentationして300文字くらいに水増しする。よって、ja_char30万データセットの画像が出来上がる計算である。
それにcloseももちろん加えるので正確には+300画像である。

90%以上の確率でja_charとcloseを区別できるようにしたい。

せっかくテスト画像生成フレームワークを作ったため、それを活用する。

DCONVNETのトレーニング/テストデータの構造について
--------------------------------------------------------

例えば、mnistデータの読み込みのコードは以下。::

  (x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)

  print(x_train.shape)
  print(t_train.shape)
  
  print(x_test.shape)
  print(t_test.shape)
  
  (60000, 1, 28, 28)
  (60000,)
  (10000, 1, 28, 28)
  (10000,)
  
ここで、::

  (60000, 1, 28, 28)
   ^^^^^  ^^ ^^  ^^
   画像数 チャネル数  width , heightだから

また、t_については、ラベル。::

  img = x_train[0]
  label = t_train[0]
  print(label)

imgは数字の5の画像。labelには"5"(整数値)が入っている

今回、どうするか？
-----------------------

各ja_char,closeにたいして、数値を割り当てる。closeは一番最後で1001で良いとする。
まず、今回の実験は自分の中で結構大規模な感じがするので、ja_char_big_testブランチを作ってテストする。

バックアップは以下に採取しておいた。::
  
  a@dataaug:~$ ls -ls backup/
  total 16656
  16656 -rw-rw-r-- 1 a a 17053424 Dec 30 15:57 dl_image_manager_20221230.tar.gz
  a@dataaug:~$ 

まず、projectの作り方を工夫する必要がある。
ja_charそれぞれに対して、0からの連番で割当する。
projects/ja_char_<number>/という形式にする。それぞれのja_char_<number>に対して、
ラベル(<number>)とja_charの実体（例：漢字）が割り当てられる。
各ja_charに対して、普通にmasterが格納される。

このprojectをどうやって自動生成するか。ja_charのdaugを工夫してやる必要がある。

これを使って、各ja_charの画像を創りだしたら、それに応じてprojectを作って、
masterをそこに置くイメージ。

今回の実験では400 x 400に拡張せずに、64 x 64で一回やって見る。

結果として、1000文字の画像をdata augmentationしてclose/closewを作った。
closeは黒背景に白地のバッテンなので、他のja_charと条件が違う(白地に黒字）ので、とりあえず除外してみた。
現在、build_all.py中。CPU1個なので時間がかかるのでしばらく放置。

次にbuild data setが動くかどうかを考える。
DCONVNET用のdata setを作る必要がある。pytorch_ssdとは違うデータ・セットになる。
今回は、pytorch_ssd用のデータ・セットをさらに、DCONVNET用に解釈し、pickleとして保存するスクリプト(dataset/gaa.py)を作成することにした。


dataset/gaa.pyについて
----------------------

dataset/gaa.pyの外部仕様として、例えば、サブディレクトリch09にchange dirして、
python3 ../dataset/gaa.pyのように使用する。

中身の考慮点は以下。

build data setまでは現状のスクリプト(build_data_set.py)を使えるが、
それを読み込んでデータを返す関数を設計する必要がある。

ja_charに対して割り当てられるべきラベルについては、画像ファイルja_char_<label_num>_<number>.jpg
にすでに埋め込まれている。

ImageSets/Main/train.txtを読み込み、行を読み込む
   ja_char_<label_num>_<number>のパターン
     ja_char_<label_num>_<number>.jpgを読み込みnumpy配列で保持(データ)。
　　 labelを読み込み、label-データのリストのハッシュにストア。labelに対応するデータリストにデータをappendする
　　ラベルチェック用のリストにlabelをappendする
   closew_<number>のパターン
     closew_<number>.jpgを読み込みnumpy配列で保持(データ)。
     label=1000として、上記ハッシュのデータリストにデータをappend

   closewのlabel=1000が上記チェック用リストに存在するかを確認して、存在するならコンフリクトとしてエラー終了(raise)

   ハッシュをkey,valでぐるぐる回しながら、データとそれに対するラベルの配列を作っていく

test.txtについても同様に実施して、データとラベルの配列を作っていく
　
     
本当は、ラベルとprojectの対応を厳密に管理するデータベースが必要なんだろうな。。。。
かなり改善の余地ありかも。

とりあえず、ja_charは0~999までなので、1000をclosewにlabelを割り当てる(ハードコーディング)

dataset/gaa.py作成時に出くわした問題
----------------------------------------------

np.arrayのappendを使うとすごく重いので、np.stackを使うと高速に実行できる。やはり、numpyはfor文を使ってはダメ。

今度、np.stackで操作すると、すべての配列のサイズが合っていないとだめとか。
400 x 400なデータを取り除いて、64 x 64で統一する作業というか、確認。
もしかしたら、projectをbuildするときに、ゴミっぽい400 x 400(最近、400 x 400 から 64 x 64に変更したので）が残っていた可能性あり。
projectをbuildするスクリプトでbuild配下をcleanする必要あるんではないか。

次にch09/train_deepnet.py実行時に以下の問題が発生。::

  /home/a/deep-learning-from-scratch/ch09
  Traceback (most recent call last):
    File "train_deepnet.py", line 25, in <module>
      trainer.train()
    File "/home/a/deep-learning-from-scratch/ch09/../common/trainer.py", line 71, in train
      self.train_step()
    File "/home/a/deep-learning-from-scratch/ch09/../common/trainer.py", line 44, in train_step
      grads = self.network.gradient(x_batch, t_batch)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 102, in gradient
      self.loss(x, t)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 83, in loss
      y = self.predict(x, train_flg=True)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 79, in predict
      x = layer.forward(x)
    File "/home/a/deep-learning-from-scratch/ch09/../common/layers.py", line 57, in forward
      out = np.dot(self.x, self.W) + self.b
    File "<__array_function__ internals>", line 180, in dot
  ValueError: shapes (100,4096) and (1024,50) not aligned: 4096 (dim 1) != 1024 (dim 0)
  a@dataaug:~/deep-learning-from-scratch/ch09$ 

np.dotで行列のサイズが合っていない。ってか、どのレイヤで発生しているんだ？ってことでデバッグメッセージを追加。::
  
  /home/a/deep-learning-from-scratch/ch09
  INFO: forward conv1
  INFO: forward conv2
  INFO: forward pooling1
  INFO: forward conv3
  INFO: forward conv4
  INFO: forward pooling2
  INFO: forward conv5
  INFO: forward conv6
  INFO: forward poolong3
  INFO: forward affine1
  Traceback (most recent call last):
    File "train_deepnet.py", line 25, in <module>
      trainer.train()
    File "/home/a/deep-learning-from-scratch/ch09/../common/trainer.py", line 71, in train
      self.train_step()
    File "/home/a/deep-learning-from-scratch/ch09/../common/trainer.py", line 44, in train_step
      grads = self.network.gradient(x_batch, t_batch)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 102, in gradient
      self.loss(x, t)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 83, in loss
      y = self.predict(x, train_flg=True)
    File "/home/a/deep-learning-from-scratch/ch09/deep_convnet.py", line 79, in predict
      x = layer.forward(x)
    File "/home/a/deep-learning-from-scratch/ch09/../common/layers.py", line 61, in forward
      out = np.dot(self.x, self.W) + self.b
    File "<__array_function__ internals>", line 180, in dot
  ValueError: shapes (100,4096) and (1024,50) not aligned: 4096 (dim 1) != 1024 (dim 0)
  a@dataaug:~/deep-learning-from-scratch/ch09$ 

一番最初のアフィンレイヤで発生。もうちょっとデバッガで詳しく調べてみると。::
  
  > /home/a/deep-learning-from-scratch/common/layers.py(63)forward()
  -> out = np.dot(self.x, self.W) + self.b
  (Pdb) self.x.shape
  (100, 4096)
  (Pdb) self.W.shape
  (1024, 50)
  (Pdb) self.b.shape
  (50,)
  (Pdb) np.dot(self.x, self.W).shape
  *** ValueError: shapes (100,4096) and (1024,50) not aligned: 4096 (dim 1) != 1024 (dim 0)
  (Pdb) 

なるほど、train_deepnet.pyの以下が怪しかった。重みの行列サイズがハードコーディングだった。
そこで、今回のサイズに合わせて修正（下の行、ハードコーディングに変わりないけどｗ）::

        #self.params['W7'] = weight_init_scales[6] * np.random.randn(64*4*4, hidden_size)
        self.params['W7'] = weight_init_scales[6] * np.random.randn(4096, hidden_size)

この辺をちゃんと自動化しようとしたら結構大変そうだね。けど、これで動けばとりあえず良し。
修正後::
  
  /home/a/deep-learning-from-scratch/ch09
  INFO: forward conv1
  INFO: forward conv2
  INFO: forward pooling1
  INFO: forward conv3
  INFO: forward conv4
  INFO: forward pooling2
  INFO: forward conv5
  INFO: forward conv6
  INFO: forward poolong3
  INFO: forward affine1
  > /home/a/deep-learning-from-scratch/common/layers.py(63)forward()
  -> out = np.dot(self.x, self.W) + self.b
  (Pdb) p self.x.shape
  (100, 4096)
  (Pdb) p self.W.shape
  (4096, 5000)
  (Pdb) np.dot(self.x, self.W).shape
  (100, 5000)
  (Pdb) p  self.b.shape
  (5000,)
  (Pdb) 

うむ。

DCONVNETでの学習
----------------------

2023/1/4に学習開始。lossは順調に下がっている感じがする。いろいろと間違いがあるかもしれないが、
とりあえず動作しているので学習が完了するまでしばらく放置しておく。

ちなみにモデルの構造はこんな感じ。::

  network = DeepConvNet(input_dim=(3,64,64),output_size=1001) #ja_chars and closew 
  trainer = Trainer(network, x_train, t_train, x_test, t_test,
                    epochs=200, mini_batch_size=1000,
                    optimizer='Adam', optimizer_param={'lr':0.001},
                    evaluate_sample_num_per_epoch=1000)
  
      def __init__(self, input_dim=(1, 28, 28),
                   conv_param_1 = {'filter_num':16, 'filter_size':3, 'pad':1, 'stride':1},
                   conv_param_2 = {'filter_num':16, 'filter_size':3, 'pad':1, 'stride':1},
                   conv_param_3 = {'filter_num':32, 'filter_size':3, 'pad':1, 'stride':1},
                   conv_param_4 = {'filter_num':32, 'filter_size':3, 'pad':2, 'stride':1},
                   conv_param_5 = {'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                   conv_param_6 = {'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                   hidden_size=5000, output_size=10):

バッチサイズを30から1000に変更。output_sizeは当然、1001に変更済み。
hidden_sizeを50から5000に変更。実は、これは数億程度のオーダーだと良いとのことだが、
個人ＰＣの範囲だとちょと辛い。
