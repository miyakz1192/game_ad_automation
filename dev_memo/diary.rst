===============
GAA改造日記
===============

全体的な人気をすべてこちらに集約することにする。
すでにバラけたものを集約すること無く、新しい情報からこちらに集約する。

2023/03/02
============

try12の結果::

                 precision    recall  f1-score   support
       accuracy                           0.93     30116
      macro avg       0.94      0.93      0.93     30116
   weighted avg       0.94      0.93      0.94     30116

edge化画像の認識結果::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/home/a/resset$ cat calc_exp_res_close.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 209, 100
  0.200000, close, 209, 100
  0.300000, close, 209, 100
  0.400000, close, 209, 100
  0.500000, close, 209, 100
  0.600000, close, 209, 100
  0.700000, close, 209, 100
  0.800000, close, 209, 100
  0.850000, close, 209, 100
  0.870000, close, 209, 100
  0.880000, close, 209, 100
  0.890000, close, 209, 100
  0.900000, close, 209, 100
  1.000000, close, 127, 60
  =====SUM(INVERT RAITIO)=====

not close::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/home/a/resset$ cat calc_exp_res_not_close.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 973, 75
  0.200000, close, 973, 75
  0.300000, close, 972, 75
  0.400000, close, 965, 75
  0.500000, close, 943, 73
  0.600000, close, 913, 71
  0.700000, close, 879, 68
  0.800000, close, 848, 66
  0.850000, close, 834, 65
  0.870000, close, 819, 63
  0.880000, close, 814, 63
  0.890000, close, 805, 62
  0.900000, close, 801, 62
  1.000000, close, 17, 1
  =====SUM(INVERT RAITIO)=====

非edge化画像::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/home/a/resset$ cat calc_exp_res_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 205, 98
  0.200000, close, 205, 98
  0.300000, close, 205, 98
  0.400000, close, 205, 98
  0.500000, close, 205, 98
  0.600000, close, 204, 97
  0.700000, close, 203, 97
  0.800000, close, 203, 97
  0.850000, close, 201, 96
  0.870000, close, 201, 96
  0.880000, close, 201, 96
  0.890000, close, 201, 96
  0.900000, close, 201, 96
  1.000000, close, 157, 75
  =====SUM(INVERT RAITIO)=====


not close::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/home/a/resset$ cat calc_exp_res_not_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 756, 59
  0.200000, close, 756, 59
  0.300000, close, 754, 58
  0.400000, close, 744, 58
  0.500000, close, 733, 57
  0.600000, close, 718, 56
  0.700000, close, 693, 54
  0.800000, close, 674, 52
  0.850000, close, 660, 51
  0.870000, close, 654, 51
  0.880000, close, 650, 50
  0.890000, close, 647, 50
  0.900000, close, 643, 50
  1.000000, close, 74, 5
  =====SUM(INVERT RAITIO)=====

結構優秀。確信度0.9~1.0あたりでベストポイントが探せそう。どうも、0.99位が良さそう。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/re_calc$ cat calc_exp_res_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 205, 98
  0.200000, close, 205, 98
  0.300000, close, 205, 98
  0.400000, close, 205, 98
  0.500000, close, 205, 98
  0.600000, close, 204, 97
  0.700000, close, 203, 97
  0.800000, close, 203, 97
  0.850000, close, 201, 96
  0.870000, close, 201, 96
  0.880000, close, 201, 96
  0.890000, close, 201, 96
  0.900000, close, 201, 96
  0.910000, close, 201, 96
  0.930000, close, 201, 96
  0.950000, close, 201, 96
  0.970000, close, 199, 95
  0.980000, close, 198, 94
  0.990000, close, 197, 94
  1.000000, close, 157, 75
  =====SUM(INVERT RAITIO)=====
  
  a@dataaug:~/gaa_learning_task/output/resnet_only_try12/re_calc$ cat calc_exp_res_not_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 991
  ### CALC targets as label=close,id=990
  INFO: close,990
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 756, 59
  0.200000, close, 756, 59
  0.300000, close, 754, 58
  0.400000, close, 744, 58
  0.500000, close, 733, 57
  0.600000, close, 718, 56
  0.700000, close, 693, 54
  0.800000, close, 674, 52
  0.850000, close, 660, 51
  0.870000, close, 654, 51
  0.880000, close, 650, 50
  0.890000, close, 647, 50
  0.900000, close, 643, 50
  0.910000, close, 638, 49
  0.930000, close, 622, 48
  0.950000, close, 610, 47
  0.970000, close, 587, 45
  0.980000, close, 564, 44
  0.990000, close, 521, 40
  1.000000, close, 74, 5
  =====SUM(INVERT RAITIO)=====

precisionが非常に良い。ということで、このモデルを一旦採用しよう！
これで、ResNet34の学習は一旦打ち止めとする!

gaaのissue11について少し進んだ。


2023/03/01
===========

try11の結果。::

              precision    recall  f1-score   support
    accuracy                           0.93     30116
   macro avg       0.94      0.93      0.93     30116
weighted avg       0.94      0.93      0.93     30116

ということで、相変わらず大変よい結果。
また、変にrecall/precisionが0になっている部分もなさ気。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try11/home/a/resset$ cat calc_exp_res_close.txt 
  dataset size = 100386
  dataset classses = 995
  ### CALC targets as label=close,id=990
  INFO: closegb,992
  INFO: close,990
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 207, 99
  0.200000, close, 207, 99
  0.300000, close, 207, 99
  0.400000, close, 207, 99
  0.500000, close, 207, 99
  0.600000, close, 207, 99
  0.700000, close, 205, 98
  0.800000, close, 205, 98
  0.850000, close, 204, 97
  0.870000, close, 204, 97
  0.880000, close, 202, 96
  0.890000, close, 202, 96
  0.900000, close, 197, 94

真のcloseに関しては完璧に答えきっている::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try11/home/a/resset$ cat calc_exp_res_not_close.txt 
  dataset size = 100386
  dataset classses = 995
  ### CALC targets as label=close,id=990
  INFO: closegb,992
  INFO: close,990
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 1007, 78
  0.200000, close, 1007, 78
  0.300000, close, 1003, 78
  0.400000, close, 993, 77
  0.500000, close, 971, 75
  0.600000, close, 952, 74
  0.700000, close, 922, 71
  0.800000, close, 883, 68
  0.850000, close, 861, 67
  0.870000, close, 840, 65
  0.880000, close, 834, 65
  0.890000, close, 824, 64
  0.900000, close, 815, 63
  =====SUM(INVERT RAITIO)=====

FPについては63%となり、よくはないがかなりマシになっている気がする。::
not edgeだとこんな感じ。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try11/home/a/resset$ cat calc_exp_res_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 995
  ### CALC targets as label=close,id=990
  INFO: closegb,992
  INFO: close,990
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 189, 90
  0.200000, close, 189, 90
  0.300000, close, 186, 88
  0.400000, close, 184, 88
  0.500000, close, 181, 86
  0.600000, close, 171, 81
  0.700000, close, 160, 76
  0.800000, close, 141, 67
  0.850000, close, 135, 64
  0.870000, close, 134, 64
  0.880000, close, 132, 63
  0.890000, close, 131, 62
  0.900000, close, 129, 61
  =====SUM(INVERT RAITIO)=====

  a@dataaug:~/gaa_learning_task/output/resnet_only_try11/home/a/resset$ cat calc_exp_res_not_close_not_edge.txt 
  dataset size = 100386
  dataset classses = 995
  ### CALC targets as label=close,id=990
  INFO: closegb,992
  INFO: close,990
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 676, 52
  0.200000, close, 676, 52
  0.300000, close, 669, 52
  0.400000, close, 652, 50
  0.500000, close, 610, 47
  0.600000, close, 566, 44
  0.700000, close, 523, 40
  0.800000, close, 464, 36
  0.850000, close, 437, 34
  0.870000, close, 424, 33
  0.880000, close, 407, 31
  0.890000, close, 395, 30
  0.900000, close, 382, 29
  =====SUM(INVERT RAITIO)=====

not edgeのほうが成績が良さそう。
確信度0.6を採用すれば、TPも81で、FPは44ということで結構よさ気。
もう一息な気がする。

精度を上げるためのもう１つの可能性として、マージ機能を実施すると良いかもしれない。
なので、こちらを進めて精度が向上するかを試してみよう。
よっしゃ行ってみよう！::
  
  a@dataaug:~/gaa_learning_task$ date ; nohup ./create_task.py  --algo resnet34 resnet_only_try12 &
  Wed 01 Mar 2023 03:38:21 PM UTC
  [1] 3723
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ 
  a@dataaug:~/gaa_learning_task$ cat nohup.out 
  INFO: resnet34
  b'/home/a/dl_image_manager\n'
  resnet34
  [resnet34] replacing projects/* data for specified algo
  a@dataaug:~/gaa_learning_task$ 


条件は以下。(pretrainedは未使用)::

      gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)

んで、epochsは20
  


2023/02/26
===========

2023/02/24のエントリのtry10の評価で「ru_close,ru_closebcow,ru_closegbあたりのデータがあやしいのか。あとでチェックする」
とした所のチェックの続きを実施する。

各学習データについてざっと目を通してみた結果。

ru_close.*.jpg→　問題なさげ

ru_closebcow.*.jpg　→　問題なさ気

ru_closegb.*.jpg →　問題なさ気

と、ここまで、各ru*個々については問題なさ気なのだが、奇妙なことに気づいた。
ru_close,ru_closebcow,ru_closegbはそれぞれ、close,closebcow,closegbとほぼ同じ画像データなのだが、
ラベルとしては違うものと設定してしまっている。

これでは、モデルは同じclose模様をどちらに仕分ければよいかわからないのではないか、、、まずい！
要するに、ru_*系というのはすべてそういうことだ(ResNet34であればru系は不要であった!)。

あと、もうひとつ気づいたのは、以下のprojects群については、すべて同じようなclose模様(微妙に違うのだけど大差は無い)だが、
それぞれ違うラベルに割り当てているということ。これを仮に1つのcloseとしてラベルしたら一体どうなるか？::

  projects/close:
  projects/closebcow:
  projects/closegb:
  projects/closewcobfat:
  projects/closewcolg:

１つ１つ問題を切り分けしていくために、以下の順番で学習を再実施してみることにする。

1. ru*を除いた学習データで再学習

2. close*を1つのラベルにする。ただし、こちらはすでに作ったprojectsの概念を再利用するために、projectsをマージする操作が必要(issueを発行) 

1.についてまずは実行。以下の条件::

        self.model = resnet34(pretrained=True)
         pretrained_weight_fileはなし。
         epochは20

という訳で実行::

   a@dataaug:~/gaa_learning_task$ date ; nohup ./create_task.py  --algo resnet34 resnet_only_try11 &
   Sun 26 Feb 2023 02:28:31 PM UTC
   [1] 1066
   a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
   
   a@dataaug:~/gaa_learning_task$ 
  
メモ:nohup.outには途中失敗した際のゴミログが先頭あたりに含まれているが気にしないように!

以下、dl_image_managerのissue2について実装のアイデアをメモしておく。

projectsマージ機能のメモ
----------------------------

各projectをbuildした後、各画像のファイル名をまとめる先のproject名にしてしまえば良いということになる。これはprojectのマージという新しい役目を持った新しいプログラムを作成するのが素直。projectに破壊的な変更を加える。bin/merge_project.py

まず、マージ先のproject名を指定する。これは１つ(例：close)。
マージ元のproject名を指定する。これは複数(1個以上)。

マージ元の以下を変更する。

1. ファイル名をマージ先のproject名のプレフィックスに変更(この時点でサフィックス、つまり末尾番号については後で述べるので気にしない)

2. annotaion.xmlファイルのファイル名をマージ先のproject名のプレフィックス名に変更する
(この時点でサフィックス、つまり末尾番号については後で述べるので気にしない)::

  a@dataaug:~/dl_image_manager$ cat data_set/Annotations/closebcow_224.xml
  <annotation>
  	<folder>closew</folder>
  	<filename>closebcow_224.jpg</filename>
  	<path>/home/a/labelImg/projects/closew/image_extended.jpg</path>
  	<source>
  		<database>Unknown</database>
  	</source>
  	<size>
  		<width>38</width>
  		<height>39</height>
  		<depth>3</depth>
  	</size>
  	<segmented>0</segmented>
  	<object>
  		<name>closebcow</name>
  		<pose>Unspecified</pose>
  		<truncated>1</truncated>
  		<difficult>0</difficult>
  		<bndbox>
  			<xmin>1</xmin>
  			<ymin>1</ymin>
  			<xmax>38</xmax>
  			<ymax>39</ymax>
  		</bndbox>
  	</object>
  </annotation>
  a@dataaug:~/dl_image_manager$ 

filenameを変更する(先の1のファイル名に変更するだけ)

object/nameをマージ先のproject名に変更する

実装の具体的なアイデア。

1. マージ元とマージ先の設定を書いたコンフィグを読み込む(マージ先のproject名(1個)と、マージ元のproject名(１個以上)。マージ先はマージ元に含めることはできない(エラー)

2. コンストラクタの処理ではマージ先のproject名を元に、projects/buildに格納されているjpgファイル数をカウントする(count)。next_count = count+1とする。

3. 各マージ元について以下の処理を実施する

3-1. <merge元project名>/build配下のjpgファイルの数を数える

3-2. <merge元project名>/build配下のファイル(jpg/xmlファイルが対)の配列を作成する。(3-1のカウントを活用)


2023/02/24
============

try10の評価について::


                     precision    recall  f1-score   support
           990       0.89      1.00      0.94       254
           991       0.89      1.00      0.94       228
           992       0.89      1.00      0.94       168
           993       1.00      0.03      0.06        33
           994       0.52      0.42      0.47        26
           995       0.00      0.00      0.00        32
           996       0.00      0.00      0.00        28
           997       0.00      0.00      0.00        22
           998       0.45      1.00      0.62        26
           999       0.64      0.75      0.69        36
  
      accuracy                           0.93     30265
     macro avg       0.93      0.93      0.93     30265
  weighted avg       0.94      0.93      0.93     30265

995~997まで相変わらず0だけど、他は数字埋まってきたなんだろう。ただ、macroは変わらない。

ラベルは以下。::

  INFO: ru_closewcobfat,998
  INFO: closegb,992
  INFO: ru_closebcow,996
  INFO: close,990
  INFO: ru_closewcolg,999
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  INFO: ru_closegb,997
  INFO: ru_close,995

ru_close,ru_closebcow,ru_closegbあたりのデータがあやしいのか。あとでチェックする
  

非edgeだとより悪くなっていて、しきい値0.6でrecallが61%だが、FPが59%と同じくらいになってしまった。
edgeでも非edgeと似た傾向。
  

try9のテストデータを使った評価について考える。::

                   precision    recall  f1-score   support
              990       0.90      1.00      0.94       233
              991       0.88      1.00      0.93       218
              992       0.87      1.00      0.93       186
              993       0.00      0.00      0.00        31
              994       0.00      0.00      0.00        17
              995       0.00      0.00      0.00        26
              996       0.00      0.00      0.00        30
              997       0.00      0.00      0.00        28
              998       0.40      1.00      0.58        21
              999       0.65      1.00      0.79        34
     
         accuracy                           0.93     30265
        macro avg       0.93      0.93      0.93     30265
     weighted avg       0.94      0.93      0.93     30265

990~999がclose系なのだけど、確かに、macro avgを見ると、precision,recallも良く、それに応じてf1-scoreも大変良くなっている。
しかし、try9でのゲーム画像を使った評価は結構悪い。。

非edgeだと、しきい値0.6でrecallが71%だが、precisionは下がる(FPが48%と高い)。
edgeだと、しきい値0.6でrecallが75だが、precisionは下がる(FPが60%と高い)。
しかし、edgeだとrecallが高い傾向にあるため、もうちょっとしきい値を上げて0.7にしてみたら、
recallが70%になり、FPが53%になる。非edgeと変わんない。

ResNet34だと非edgeでもedgeでもあんまり性能は変わらない気がしてきた。


あと、なぜか、993~997までのデータについてprecisionとrecallが0となっているので、かなり怪しい

あと遭遇したエラーで。::

    231         #TODO: retry if connection error
    232         command = ["scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose"]
    233         proc = subprocess.Popen(command)
    234         print("[DEBUG] wait for %d" % (self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED))
    235         time.sleep(self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED)
    236         print("[DEBUG] touch pos!!!")
    237         command = "echo " + str(int(pos.rect.x+pos.rect.width/2)) + "," + str(int(pos.rect.y+pos.rect.height/2)) + " > " + "mdown_input_pipe"
    238         subprocess.run(command , shell=True)
    239         time.sleep(5)
    240         proc.send_signal(SIGINT)

scrcpyの起動が失敗した場合に、パイプに書き込みに行ってしまって、そこでハング。
__call_scrcpy_cmd_with_retryを呼び出しておけば良いかもしれないけど、__call_scrcpy_cmd_with_retry
でリトライアウトした場合にハングしちゃうのでやっぱりよくない



2023/02/23
==============

resnet_only_try9の結果も思わしくない。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try9/home/a/resset$ cat calc_exp_res_close.txt 
  dataset size = 100881
  dataset classses = 1000
  ### CALC targets as label=close,id=990
  INFO: ru_closewcobfat,998
  INFO: closegb,992
  INFO: ru_closebcow,996
  INFO: close,990
  INFO: ru_closewcolg,999
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  INFO: ru_closegb,997
  INFO: ru_close,995
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, close, 180, 86
  0.200000, close, 180, 86
  0.300000, close, 180, 86
  0.400000, close, 176, 84
  0.500000, close, 174, 83
  0.600000, close, 157, 75
  0.700000, close, 148, 70
  0.800000, close, 109, 52
  0.850000, close, 100, 47
  0.870000, close, 91, 43
  0.880000, close, 87, 41
  0.890000, close, 83, 39
  0.900000, close, 75, 35
  =====SUM(INVERT RAITIO)=====
  0.100000, close, 180, 13
  0.200000, close, 180, 13
  0.300000, close, 180, 13
  0.400000, close, 176, 15
  0.500000, close, 174, 16
  0.600000, close, 157, 24
  0.700000, close, 148, 29
  0.800000, close, 109, 47
  0.850000, close, 100, 52
  0.870000, close, 91, 56
  0.880000, close, 87, 58
  0.890000, close, 83, 60
  0.900000, close, 75, 64
  a@dataaug:~/gaa_learning_task/output/resnet_only_try9/home/a/resset$ cat calc_exp_res_not_close.txt 
  dataset size = 100881
  dataset classses = 1000
  ### CALC targets as label=close,id=990
  INFO: ru_closewcobfat,998
  INFO: closegb,992
  INFO: ru_closebcow,996
  INFO: close,990
  INFO: ru_closewcolg,999
  INFO: closebcow,991
  INFO: closewcolg,994
  INFO: closewcobfat,993
  INFO: ru_closegb,997
  INFO: ru_close,995
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, close, 881, 68
  0.200000, close, 881, 68
  0.300000, close, 879, 68
  0.400000, close, 863, 67
  0.500000, close, 819, 63
  0.600000, close, 769, 60
  0.700000, close, 682, 53
  0.800000, close, 560, 43
  0.850000, close, 444, 34
  0.870000, close, 389, 30
  0.880000, close, 367, 28
  0.890000, close, 335, 26
  0.900000, close, 307, 23
  =====SUM(INVERT RAITIO)=====
  0.100000, close, 881, 31
  0.200000, close, 881, 31
  0.300000, close, 879, 31
  0.400000, close, 863, 32
  0.500000, close, 819, 36
  0.600000, close, 769, 39
  0.700000, close, 682, 46
  0.800000, close, 560, 56
  0.850000, close, 444, 65
  0.870000, close, 389, 69
  0.880000, close, 367, 71
  0.890000, close, 335, 73
  0.900000, close, 307, 76
  a@dataaug:~/gaa_learning_task/output/resnet_only_try9/home/a/resset$ 

確信度0.7を採用したら、正答率70%、誤答率53%となる。
try8よりは正答率が上がった様子。

epochsを積むと精度が上がるっぽいので、続けてみようかなとおもう。
その前に、この状態でテストプレイをしてみる。

そこそこ上手く動いているっぽい。ときどき、人間でも判別が難しいcloseがでてくるし、その場合は人間がcloseを押してあげる必要があるし、非常に動作が重いので、あまり使い物にはならないが、、、、

ただ、GAAの動作を見ていると、予期しない状態遷移に対する考慮がたりないのか、変なループをすることがある。ただ、何が起きているか画面のログを見てもよくわからないので、ログをとりあえず強化（GAAがどの状態に居るかを表示)することにする。

認識精度の向上も１つの課題だが、GAA本体のロジックも多少作りこんだほうが使い勝手の向上に繋がると考える。例えば、以下。

1. 誤認識が発生して人間が手動でcloseボタンなどを押下して画面を遷移させた場合、GAAが正しい状態を認識できない。

2. closeボタンやad buttonが見つからない場合の異常系の考慮が無い。

3. ミダスの手を押下できない

いずれもバグなんだけどね。1~3を改善すると結構使い物になってくるかもしれない。

1.については状態遷移図をちゃんと設計して取り組めば良さそう。「広告をみるボタン」が出ているシーンを初期状態として、それをGAAの最初に採取する(ユーザに「広告をみるボタン」からプログラムをスタートしてもらう前提付きだが)。そうすれば、すべて初期状態を基点として状態を判別できる。すなわち、GAA状態遷移マシンが認識すべき状態は①　初期状態か、②　広告画面かの２つのため。②　は①　の否定を取れば簡単に認識できる。

上記３件は課題としてGAAにissueを発行。

あと、try9をネタとしてtry10をもう20 epochかます。

ただ、try9で以下の成績であり、これ以上かましてもしょうがねーんじゃないかという気もする。::

      accuracy                           0.93     30265
       macro avg       0.93      0.93      0.93     30265
      weighted avg       0.94      0.93      0.93     30265

try10開始::
  
  a@dataaug:~/gaa_learning_task$ nohup ./create_task.py  --algo resnet34 resnet_only_try10 &
  [1] 1974
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ date
  Thu 23 Feb 2023 04:16:26 PM UTC
  a@dataaug:~/gaa_learning_task$ cat nohup.out 
  INFO: resnet34
  b'/home/a/dl_image_manager\n'
  resnet34
  [resnet34] replacing projects/* data for specified algo
  a@dataaug:~/gaa_learning_task$ 
  

  

2023/02/21
==============

resnet_only_try8の結果は悪かった。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try8$ cat calc_exp_res_close.txt 
  INFO: gathering class close as 990
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 990, 196, 93
  0.200000, 990, 196, 93
  0.300000, 990, 192, 91
  0.400000, 990, 179, 85
  0.500000, 990, 167, 79
  0.600000, 990, 145, 69
  0.700000, 990, 121, 57
  0.800000, 990, 89, 42
  0.850000, 990, 52, 24
  0.870000, 990, 41, 19
  0.880000, 990, 38, 18
  0.890000, 990, 34, 16
  0.900000, 990, 31, 14
  =====SUM(INVERT RAITIO)=====
  0.100000, 990, 196, 6
  0.200000, 990, 196, 6
  0.300000, 990, 192, 8
  0.400000, 990, 179, 14
  0.500000, 990, 167, 20
  0.600000, 990, 145, 30
  0.700000, 990, 121, 42
  0.800000, 990, 89, 57
  0.850000, 990, 52, 75
  0.870000, 990, 41, 80
  0.880000, 990, 38, 81
  0.890000, 990, 34, 83
  0.900000, 990, 31, 85
  a@dataaug:~/gaa_learning_task/output/resnet_only_try8$ cat calc_exp_res_not_close
  cat: calc_exp_res_not_close: No such file or directory
  a@dataaug:~/gaa_learning_task/output/resnet_only_try8$ cat calc_exp_res_not_close.txt 
  INFO: gathering class close as 990
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 990, 801, 62
  0.200000, 990, 801, 62
  0.300000, 990, 797, 62
  0.400000, 990, 774, 60
  0.500000, 990, 724, 56
  0.600000, 990, 678, 52
  0.700000, 990, 628, 49
  0.800000, 990, 561, 43
  0.850000, 990, 498, 38
  0.870000, 990, 450, 35
  0.880000, 990, 425, 33
  0.890000, 990, 400, 31
  0.900000, 990, 367, 28
  =====SUM(INVERT RAITIO)=====
  0.100000, 990, 801, 37
  0.200000, 990, 801, 37
  0.300000, 990, 797, 37
  0.400000, 990, 774, 39
  0.500000, 990, 724, 43
  0.600000, 990, 678, 47
  0.700000, 990, 628, 50
  0.800000, 990, 561, 56
  0.850000, 990, 498, 61
  0.870000, 990, 450, 64
  0.880000, 990, 425, 66
  0.890000, 990, 400, 68
  0.900000, 990, 367, 71
  a@dataaug:~/gaa_learning_task/output/resnet_only_try8$ 

確信度0.6を採用すると正答率60%、誤答率50%で我慢すれば利用できるかな？っていう程度。
まだまだだ。

pretrained=Falseにしているのが気にはなるが、epochsを増やしていくと精度もUPしていくことがわかっているので、
try8の結果を元に学習を積み上げる、すなわち、このままepochsを重ねていくことにする。::

  +    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False, pretrained_weight_file="./weights/resnet_only_try8.pth")

  
ただし、ResNet34とgaa_learning_taskの以下が使い勝手が悪く、改善しないとちょっと不便すぎ。

1. gaa_learning_taskで進捗状況がわからない。リモート実行するログを常に吐き出すようにしたい。

2. ResNet34のbin/calc_exp.pyが使い勝手悪すぎ。closeを自動認識してほしい。いまだとcloseに対応するindexを指定することになっているので滅茶不便すぎ。

上記を改善してから、epochsを重ねようと思う。

というわけで、epochsをかさねます。
(pretrained=False,epochs=20,try8を引き継ぎ)::

   1990  nohup ./create_task.py --algo resnet34 resnet_only_try9



2023/02/19
============

ResNet34の認識率が低いのはおそらく、ja_charを学習させていないからだと思う。
その時の結果は今よりも少なくとも良かった。

object_detection_ResNet.rstのトライ7の結果が過去一番良かったことになるが、この時の条件は以下だった。

0. edge加工だと正認識、誤認識率も良好(確信度0.8以上を採用すれば、closeであれば、63~88%の確率で正答)

1. output_sizeが1000を超えている(おそらく1034程度)

2. pytorch本家のチュートリアルの学習時のtransformだとrandom要素があるが、これ、不要じゃない？


ということで、トライ7の条件でやると、トライ7の結果以上のコトは得られないため、トライ7の上手く行った時の条件(edge加工で認識)は変えずに、上記の検討が残っている条件を変えて試してみる。

まず、1についてoutput_sizeを1000にする.::

  a@pytorch:~/resset$ git diff core/resnet34.py
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..6280c8b 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -23,8 +23,9 @@ from gaa import *
   from single import *
   
   class GAAResNet34():
  -    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True, pretrained_weight_file=None):
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
           self.model.fc = nn.Linear(512,output_classes)
           
  @@ -32,6 +33,11 @@ class GAAResNet34():
           self.model.cpu()
           self.verbose = verbose
   
  +        self.best_avg_loss = 100000000000000 #tekitou
  +
  +        if pretrained_weight_file is not None:
  +            self.load(pretrained_weight_file)
  +
       def train_aux(self,epoch):
           total_loss = 0
           total_size = 0
  @@ -54,10 +60,17 @@ class GAAResNet34():
                   print("DEBUG: time=%d, batch_idx=%d, len(data)=%d, batch_idx * len(data)=%d" % (int(e_t-s_t),batch_idx, len(data), batch_idx*len(data)))
               if batch_idx % report == 0:
                   now = datetime.datetime.now()
  +                avg_loss = total_loss / total_size
                   print('[{}] Train Epoch: {} [{}/{} ({:.0f}%)]\tAverage loss: {:.6f}'.format(
                       now,
                       epoch, batch_idx * len(data), len(self.train_loader.dataset),
  -                    100. * batch_idx * len(data) / len(self.train_loader.dataset), total_loss / total_size))
  +                    100. * batch_idx * len(data) / len(self.train_loader.dataset), avg_loss))
  +
  +                if self.best_avg_loss > avg_loss:
  +                    print("BEST LOSS UPDATED!!!")
  +                    self.best_avg_loss = avg_loss
  +                    self.save("./weights/best_weight.pth")
  +
   
               sys.stdout.flush()
   
  @@ -73,6 +86,8 @@ class GAAResNet34():
   
   
       def train(self, dataset, train_ratio=0.7, batch_size=32, epochs=5):
  +        print("INFO: train start. show model info")
  +        print(self.model)
           self.dataset = dataset
           self.batch_size = batch_size
           self.epochs = epochs
  @@ -157,9 +172,10 @@ if __name__ == "__main__":
       print("dataset size = %d" % (len(dataset)))
       print("dataset classses = %d" % (dataset.classes()))
   
  +    #gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False, pretrained_weight_file="./weights/resnet_only_try6.pth")
       gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=100)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

前の重みを一旦引き継いでいない点に注意！(引き継いでいたせいで一回try8が失敗)。そして以下で再試行

::

  a@dataaug:~/gaa_learning_task$ nohup ./create_task.py  --algo resnet34 resnet_only_try8 &
  [1] 212176
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ 
  a@dataaug:~/gaa_learning_task$ cat nohup.out 
  a@dataaug:~/gaa_learning_task$ 

2023/02/20 

いつまでもresnet34のタスクが終わらない、、、原因はepoch=100にしたせい。
これをとりあえず、epoch=10にして再度実行。::
  
  a@dataaug:~/gaa_learning_task$ date ; nohup ./create_task.py  --algo resnet34 resnet_only_try8 &
  Mon 20 Feb 2023 01:10:34 PM UTC
  [1] 424349
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ 
  a@dataaug:~/gaa_learning_task$ 
  a@dataaug:~/gaa_learning_task$ ls output/resnet_only_try8/
  a@dataaug:~/gaa_learning_task$ cat nohup.out 
  a@dataaug:~/gaa_learning_task$ 
  


  


2023/02/13-02/15
=================

pretrained=Falseにして、output classes=10、epoch 20で学習させた結果。
少しだけ良くなっている。もしかしたら、学習続ければ続けるほど行けるかも。実験的にepoch 20 →  40に増やしてみる。
(これで行けるなら、epochを無限位にしてSSD見たいにベストを保存する形にすれば良いかも？)::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try3$ cat calc_exp_res_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 207, 99
  0.500000, 0, 207, 99
  0.600000, 0, 207, 99
  0.700000, 0, 205, 98
  0.800000, 0, 202, 96
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 207, 0
  0.500000, 0, 207, 0
  0.600000, 0, 207, 0
  0.700000, 0, 205, 1
  0.800000, 0, 202, 3
  a@dataaug:~/gaa_learning_task/output/resnet_only_try3$ cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1279, 99
  0.400000, 0, 1252, 97
  0.500000, 0, 1222, 95
  0.600000, 0, 1178, 91
  0.700000, 0, 1143, 89
  0.800000, 0, 968, 75
  0.900000, 0, 17, 1
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1279, 0
  0.400000, 0, 1252, 2
  0.500000, 0, 1222, 4
  0.600000, 0, 1178, 8
  0.700000, 0, 1143, 10
  0.800000, 0, 968, 24
  0.900000, 0, 17, 98
  a@dataaug:~/gaa_learning_task/output/resnet_only_try3$ 

  dataset size = 2871
  dataset classses = 10
                precision    recall  f1-score   support
  
             0       0.86      0.99      0.92       254
             1       0.88      0.96      0.92       241
             2       0.84      1.00      0.91       145
             3       0.00      0.00      0.00        37
             4       0.00      0.00      0.00        37
             5       0.00      0.00      0.00        27
             6       0.00      0.00      0.00        36
             7       0.00      0.00      0.00        27
             8       0.41      0.90      0.56        29
             9       0.43      1.00      0.60        29
  
      accuracy                           0.79       862
     macro avg       0.34      0.49      0.39       862
  weighted avg       0.67      0.79      0.72       862

ロスも減少傾向であり、epochを重ねれば下がりそうな予感。::  

  [2023-02-12 15:22:56.590093] Train Epoch: 19 [1920/2009 (96%)]  Average loss: 0.015847

以下でトライ::

  a@dataaug:~/gaa_learning_task$  nohup ./create_task.py resnet_only_try4 --algo resnet34 &
  [1] 26388
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ date
  Sun 12 Feb 2023 10:38:59 PM UTC
  a@dataaug:~/gaa_learning_task$ 

結果はこう。::

  INFO main
  dataset size = 2871
  dataset classses = 10
                precision    recall  f1-score   support
  
             0       0.88      1.00      0.93       253
             1       0.88      0.99      0.93       233
             2       0.85      0.99      0.91       167
             3       0.00      0.00      0.00        32
             4       0.48      0.96      0.64        25
             5       0.00      0.00      0.00        29
             6       0.00      0.00      0.00        31
             7       0.00      0.00      0.00        30
             8       0.56      0.97      0.71        36
             9       0.00      0.00      0.00        26
  
      accuracy                           0.82       862
     macro avg       0.36      0.49      0.41       862
  weighted avg       0.70      0.82      0.75       862
  
んー。::
  
  a@dataaug:~/gaa_learning_task/output/resnet_only_try4$ cat calc_exp_res_close.txt ; cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 209, 100
  0.600000, 0, 209, 100
  0.700000, 0, 209, 100
  0.800000, 0, 209, 100
  0.900000, 0, 2, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 209, 0
  0.600000, 0, 209, 0
  0.700000, 0, 209, 0
  0.800000, 0, 209, 0
  0.900000, 0, 2, 99
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1279, 99
  0.400000, 0, 1278, 99
  0.500000, 0, 1268, 98
  0.600000, 0, 1254, 97
  0.700000, 0, 1241, 96
  0.800000, 0, 1215, 94
  0.900000, 0, 159, 12
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1279, 0
  0.400000, 0, 1278, 0
  0.500000, 0, 1268, 1
  0.600000, 0, 1254, 2
  0.700000, 0, 1241, 3
  0.800000, 0, 1215, 5
  0.900000, 0, 159, 87
  a@dataaug:~/gaa_learning_task/output/resnet_only_try4$ 

もうちょっと精細にしてみても。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try4$ cat calc_exp_res_close.txt ; cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 209, 100
  0.600000, 0, 209, 100
  0.700000, 0, 209, 100
  0.800000, 0, 209, 100
  0.850000, 0, 209, 100
  0.870000, 0, 127, 60
  0.880000, 0, 44, 21
  0.890000, 0, 4, 1
  0.900000, 0, 2, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 209, 0
  0.600000, 0, 209, 0
  0.700000, 0, 209, 0
  0.800000, 0, 209, 0
  0.850000, 0, 209, 0
  0.870000, 0, 127, 39
  0.880000, 0, 44, 78
  0.890000, 0, 4, 98
  0.900000, 0, 2, 99
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1279, 99
  0.400000, 0, 1278, 99
  0.500000, 0, 1268, 98
  0.600000, 0, 1254, 97
  0.700000, 0, 1241, 96
  0.800000, 0, 1215, 94
  0.850000, 0, 1164, 90
  0.870000, 0, 920, 71
  0.880000, 0, 616, 48
  0.890000, 0, 363, 28
  0.900000, 0, 159, 12
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1279, 0
  0.400000, 0, 1278, 0
  0.500000, 0, 1268, 1
  0.600000, 0, 1254, 2
  0.700000, 0, 1241, 3
  0.800000, 0, 1215, 5
  0.850000, 0, 1164, 9
  0.870000, 0, 920, 28
  0.880000, 0, 616, 51
  0.890000, 0, 363, 71
  0.900000, 0, 159, 87
  a@dataaug:~/gaa_learning_task/output/resnet_only_try4$ 
    
確信度0.87を採用しても正答率60%、誤答率71%となり、誤答率が高すぎ使い物にならないことがわかった。
ただし、::

  [2023-02-12 23:41:54.379113] Train Epoch: 39 [1920/2009 (96%)]  Average loss: 0.014303

epoch数を増やすほどにlossが下がる傾向であることも同時にわかったため、
学習回数を増加させるほど結果がよくなりそうな予感はする。

今回得られた重みをresumeにして、さらにepochを長くすることを実施してみたいと思う。::

  a@pytorch:~/resset$ git diff core/resnet34.py
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..6f4ca87 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -23,8 +23,9 @@ from gaa import *
   from single import *
   
   class GAAResNet34():
  -    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True, pretrained_weight_file=None):
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
           self.model.fc = nn.Linear(512,output_classes)
           
  @@ -32,6 +33,9 @@ class GAAResNet34():
           self.model.cpu()
           self.verbose = verbose
   
  +        if pretrained_weight_file is not None:
  +            self.load(pretrained_weight_file)
  +
       def train_aux(self,epoch):
           total_loss = 0
           total_size = 0
  @@ -73,6 +77,8 @@ class GAAResNet34():
   
   
       def train(self, dataset, train_ratio=0.7, batch_size=32, epochs=5):
  +        print("INFO: train start. show model info")
  +        print(self.model)
           self.dataset = dataset
           self.batch_size = batch_size
           self.epochs = epochs
  @@ -157,9 +163,9 @@ if __name__ == "__main__":
       print("dataset size = %d" % (len(dataset)))
       print("dataset classses = %d" % (dataset.classes()))
   
  -    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
  +    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False, pretrained_weight_file="./weights/resnet_only_try4.pth")
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=100)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

上記の変更にて、try4の重みを元にepoch100を回してみる::

  a@dataaug:~/gaa_learning_task$ nohup ./create_task.py  resnet_only_try5 &
  [1] 33892
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ 

数値が改善する方向になるかを見ていこう。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try5$ cat calc_exp_res_close.txt ; cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 209, 100
  0.600000, 0, 208, 99
  0.700000, 0, 207, 99
  0.800000, 0, 202, 96
  0.850000, 0, 147, 70
  0.870000, 0, 82, 39
  0.880000, 0, 34, 16
  0.890000, 0, 9, 4
  0.900000, 0, 1, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 209, 0
  0.600000, 0, 208, 0
  0.700000, 0, 207, 0
  0.800000, 0, 202, 3
  0.850000, 0, 147, 29
  0.870000, 0, 82, 60
  0.880000, 0, 34, 83
  0.890000, 0, 9, 95
  0.900000, 0, 1, 99
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1281, 100
  0.400000, 0, 1275, 99
  0.500000, 0, 1247, 97
  0.600000, 0, 1208, 94
  0.700000, 0, 1162, 90
  0.800000, 0, 1002, 78
  0.850000, 0, 624, 48
  0.870000, 0, 335, 26
  0.880000, 0, 183, 14
  0.890000, 0, 73, 5
  0.900000, 0, 18, 1
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1281, 0
  0.400000, 0, 1275, 0
  0.500000, 0, 1247, 2
  0.600000, 0, 1208, 5
  0.700000, 0, 1162, 9
  0.800000, 0, 1002, 21
  0.850000, 0, 624, 51
  0.870000, 0, 335, 73
  0.880000, 0, 183, 85
  0.890000, 0, 73, 94
  0.900000, 0, 18, 98
  a@dataaug:~/gaa_learning_task/output/resnet_only_try5$ 

数値はだいぶマシになった。確信度0.85を採用すると、正答率が70%、誤答率が48%(正答率が51%)となる。
少しずつ使い物になってきた感じがする。::

[2023-02-13 14:59:34.859441] Train Epoch: 99 [1920/2009 (96%)]  Average loss: 0.013235

以下。::
  
  INFO main
  dataset size = 2871
  dataset classses = 10
                precision    recall  f1-score   support
  
             0       0.93      1.00      0.96       243
             1       0.91      1.00      0.95       247
             2       0.84      1.00      0.91       178
             3       0.00      0.00      0.00        30
             4       0.21      0.12      0.15        25
             5       0.00      0.00      0.00        19
             6       0.00      0.00      0.00        25
             7       0.00      0.00      0.00        35
             8       0.51      1.00      0.67        31
             9       0.45      0.62      0.52        29
  
      accuracy                           0.84       862
     macro avg       0.38      0.47      0.42       862
  weighted avg       0.73      0.84      0.78       862

もう100 epoch流してみる。::

  a@pytorch:~/resset$ git diff core/resnet34.py
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..9fd4b8b 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -23,8 +23,9 @@ from gaa import *
   from single import *
   
   class GAAResNet34():
  -    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True, pretrained_weight_file=None):
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
           self.model.fc = nn.Linear(512,output_classes)
           
  @@ -32,6 +33,9 @@ class GAAResNet34():
           self.model.cpu()
           self.verbose = verbose
   
  +        if pretrained_weight_file is not None:
  +            self.load(pretrained_weight_file)
  +
       def train_aux(self,epoch):
           total_loss = 0
           total_size = 0
  @@ -73,6 +77,8 @@ class GAAResNet34():
   
   
       def train(self, dataset, train_ratio=0.7, batch_size=32, epochs=5):
  +        print("INFO: train start. show model info")
  +        print(self.model)
           self.dataset = dataset
           self.batch_size = batch_size
           self.epochs = epochs
  @@ -157,9 +163,9 @@ if __name__ == "__main__":
       print("dataset size = %d" % (len(dataset)))
       print("dataset classses = %d" % (dataset.classes()))
   
  -    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
  +    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False, pretrained_weight_file="./weights/resnet_only_try5.pth")
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=100)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

try5の重みを継承して、try6を実行中::

  a@dataaug:~/gaa_learning_task$  nohup ./create_task.py --algo resnet34  resnet_only_try6 &
  [1] 253219
  a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
  
  a@dataaug:~/gaa_learning_task$ 

結果は以下。::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try6$ cat calc_exp_res_close.txt ; cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 208, 99
  0.600000, 0, 204, 97
  0.700000, 0, 199, 95
  0.800000, 0, 103, 49
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 208, 0
  0.600000, 0, 204, 2
  0.700000, 0, 199, 4
  0.800000, 0, 103, 50
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1281, 100
  0.400000, 0, 1278, 99
  0.500000, 0, 1249, 97
  0.600000, 0, 1220, 95
  0.700000, 0, 1179, 92
  0.800000, 0, 934, 72
  0.850000, 0, 64, 4
  0.870000, 0, 6, 0
  0.880000, 0, 1, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1281, 0
  0.400000, 0, 1278, 0
  0.500000, 0, 1249, 2
  0.600000, 0, 1220, 4
  0.700000, 0, 1179, 7
  0.800000, 0, 934, 27
  0.850000, 0, 64, 95
  0.870000, 0, 6, 99
  0.880000, 0, 1, 99
  a@dataaug:~/gaa_learning_task/output/resnet_only_try6$ 

最後のロスは以下。::

   [2023-02-14 01:34:12.224074] Train Epoch: 99 [1920/2009 (96%)]  Average loss: 0.012906

テスト結果は以下。::

  INFO main
  dataset size = 2871
  dataset classses = 10
                precision    recall  f1-score   support
  
             0       0.91      1.00      0.95       214
             1       0.87      1.00      0.93       247
             2       0.86      1.00      0.92       183
             3       0.59      1.00      0.74        37
             4       0.37      1.00      0.54        25
             5       0.00      0.00      0.00        21
             6       0.00      0.00      0.00        37
             7       0.00      0.00      0.00        30
             8       0.00      0.00      0.00        26
             9       0.00      0.00      0.00        42
  
      accuracy                           0.82       862
     macro avg       0.36      0.50      0.41       862
  weighted avg       0.69      0.82      0.75       862

結果としてあまり良くならないのだけど、たまにロスがすごく下がるのはどうしてだろう？::

  [2023-02-14 01:06:25.257378] Train Epoch: 82 [0/2009 (0%)]      Average loss: 0.007635

SSDのときのようにベストのロスを更新したらweightをsaveするようにしてみて、
もう100 epoch実施してみよう。::

  a@pytorch:~/resset$ git diff
  diff --git a/bin/calc_exp.py b/bin/calc_exp.py
  index a0403dd..dd0a348 100755
  --- a/bin/calc_exp.py
  +++ b/bin/calc_exp.py
  @@ -53,7 +53,7 @@ print("INFO: gathering class than %d as %d" % (args.gathering_class_than, args.g
   print("=====RECORD INFO=====")
   print("total = %d" % (len(records)))
   print("=====SUM=====")
  -threshold_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  +threshold_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.87, 0.88, 0.89, 0.9, 1.0]
   for threshold in threshold_list:
          summer(threshold, args.calc_target)
   print("=====SUM(INVERT RAITIO)=====")
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..3fa9d42 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -23,8 +23,9 @@ from gaa import *
   from single import *
   
   class GAAResNet34():
  -    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +    def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True, pretrained_weight_file=None):
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
           self.model.fc = nn.Linear(512,output_classes)
           
  @@ -32,6 +33,11 @@ class GAAResNet34():
           self.model.cpu()
           self.verbose = verbose
   
  +        self.best_avg_loss = 100000000000000 #tekitou
  +
  +        if pretrained_weight_file is not None:
  +            self.load(pretrained_weight_file)
  +
       def train_aux(self,epoch):
           total_loss = 0
           total_size = 0
  @@ -54,10 +60,17 @@ class GAAResNet34():
                   print("DEBUG: time=%d, batch_idx=%d, len(data)=%d, batch_idx * len(data)=%d" % (int(e_t-s_t),batch_idx, len(data), batch_idx*len(data)))
               if batch_idx % report == 0:
                   now = datetime.datetime.now()
  +                avg_loss = total_loss / total_size
                   print('[{}] Train Epoch: {} [{}/{} ({:.0f}%)]\tAverage loss: {:.6f}'.format(
                       now,
                       epoch, batch_idx * len(data), len(self.train_loader.dataset),
  -                    100. * batch_idx * len(data) / len(self.train_loader.dataset), total_loss / total_size))
  +                    100. * batch_idx * len(data) / len(self.train_loader.dataset), avg_loss))
  +
  +                if self.best_avg_loss > avg_loss:
  +                    print("BEST LOSS UPDATED!!!")
  +                    self.best_avg_loss = avg_loss
  +                    self.save("./weights/best_weight.pth")
  +
   
               sys.stdout.flush()
   
  @@ -73,6 +86,8 @@ class GAAResNet34():
   
   
       def train(self, dataset, train_ratio=0.7, batch_size=32, epochs=5):
  +        print("INFO: train start. show model info")
  +        print(self.model)
           self.dataset = dataset
           self.batch_size = batch_size
           self.epochs = epochs
  @@ -157,9 +172,9 @@ if __name__ == "__main__":
       print("dataset size = %d" % (len(dataset)))
       print("dataset classses = %d" % (dataset.classes()))
   
  -    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
  +    gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False, pretrained_weight_file="./weights/resnet_only_try6.pth")
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=100)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

以下で実施。::

  nohup ./create_task.py --algo resnet34  resnet_only_try7 &

  a@dataaug:~/gaa_learning_task/output/resnet_only_try7$ cat calc_exp_res_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 209, 100
  0.600000, 0, 209, 100
  0.700000, 0, 209, 100
  0.800000, 0, 209, 100
  0.850000, 0, 205, 98
  0.870000, 0, 114, 54
  0.880000, 0, 55, 26
  0.890000, 0, 6, 2
  0.900000, 0, 2, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 209, 0
  0.600000, 0, 209, 0
  0.700000, 0, 209, 0
  0.800000, 0, 209, 0
  0.850000, 0, 205, 1
  0.870000, 0, 114, 45
  0.880000, 0, 55, 73
  0.890000, 0, 6, 97
  0.900000, 0, 2, 99
  a@dataaug:~/gaa_learning_task/output/resnet_only_try7$ cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1281, 100
  0.400000, 0, 1281, 100
  0.500000, 0, 1273, 99
  0.600000, 0, 1266, 98
  0.700000, 0, 1251, 97
  0.800000, 0, 1242, 96
  0.850000, 0, 1207, 94
  0.870000, 0, 1043, 81
  0.880000, 0, 787, 61
  0.890000, 0, 370, 28
  0.900000, 0, 130, 10
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1281, 0
  0.400000, 0, 1281, 0
  0.500000, 0, 1273, 0
  0.600000, 0, 1266, 1
  0.700000, 0, 1251, 2
  0.800000, 0, 1242, 3
  0.850000, 0, 1207, 5
  0.870000, 0, 1043, 18
  0.880000, 0, 787, 38
  0.890000, 0, 370, 71
  0.900000, 0, 130, 89
  a@dataaug:~/gaa_learning_task/output/resnet_only_try7$ 

実行したコマンドは以下(参考)。::

./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_close_edge.log > calc_exp_res_close.txt
./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_not_close_edge.log > calc_exp_res_not_close.txt
./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_close.log > calc_exp_res_close_not_edge.txt
./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_not_close.log > calc_exp_res_not_close_not_edge.txt

上記の結果はedge画像をResNet34に通した結果だが、精度が悪い（正答率と誤答率のバランスが取れない)。
しかし、edge画像じゃないものを通してみた結果、以下になった。::

  a@pytorch:~/resset$ !2025
  cat calc_exp_res_close_not_edge.txt ; cat calc_exp_res_not_close_not_edge.txt
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 208, 99
  0.400000, 0, 201, 96
  0.500000, 0, 174, 83
  0.600000, 0, 121, 57
  0.700000, 0, 105, 50
  0.800000, 0, 94, 44
  0.850000, 0, 25, 11
  0.870000, 0, 5, 2
  0.880000, 0, 1, 0
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 208, 0
  0.400000, 0, 201, 3
  0.500000, 0, 174, 16
  0.600000, 0, 121, 42
  0.700000, 0, 105, 49
  0.800000, 0, 94, 55
  0.850000, 0, 25, 88
  0.870000, 0, 5, 97
  0.880000, 0, 1, 99
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1263, 98
  0.400000, 0, 1192, 93
  0.500000, 0, 1106, 86
  0.600000, 0, 980, 76
  0.700000, 0, 894, 69
  0.800000, 0, 732, 57
  0.850000, 0, 184, 14
  0.870000, 0, 103, 8
  0.880000, 0, 59, 4
  0.890000, 0, 39, 3
  0.900000, 0, 20, 1
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1263, 1
  0.400000, 0, 1192, 6
  0.500000, 0, 1106, 13
  0.600000, 0, 980, 23
  0.700000, 0, 894, 30
  0.800000, 0, 732, 42
  0.850000, 0, 184, 85
  0.870000, 0, 103, 91
  0.880000, 0, 59, 95
  0.890000, 0, 39, 96
  0.900000, 0, 20, 98
  a@pytorch:~/resset$ 

確信度0.5を採用すれば正答率50%、誤答率50%となるが、、、ちょっと採用は厳しいなぁ。


2023/02/12
===========

●　まとめ

1. ResNet34のoutputサイズを小さくしてみる(10程度)→　結果ＮＧ

2. ResNet34のoutputサイズはデフォルト(1000)にして、学習させるものはclose系の10数種　→　結果ＮＧ(No1と同等の結果に。ただし、認識する際の確信度は上がっては居るが、誤認識度は100%になるためツカイモンにならん。)


※　outputサイズを10にしたほうが、多少はそれらしい結果になるが、正認識度(正解を正解と判定)が低く、誤認識度(非正解を正解と誤判定)が高く、結果として悪い。ただし、outputサイズが1000で学習物10だと、正認識度は100%近くなるが、誤認識度も100%となり、最悪(すべての与えた画像をcloseと認識しており、学習していないのと同じ)。

3. 今の所、ja_charも学習させたモデルのほうが精度がまだまし。


以下はまだ実施していない

X. close系は1つにまとめて学習

Y. pretrained=Falseにしてみる　→　2023/2/12~13実施中



●　継続。

データセット数を10にしてトライしてみたが、結果はボロボロ::

  a@dataaug:~/gaa_learning_task/output/resnet_only_20230212$ cat calc_exp_res_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 207, 99
  0.500000, 0, 202, 96
  0.600000, 0, 202, 96
  0.700000, 0, 181, 86
  0.800000, 0, 145, 69
  0.900000, 0, 3, 1
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 207, 0
  0.500000, 0, 202, 3
  0.600000, 0, 202, 3
  0.700000, 0, 181, 13
  0.800000, 0, 145, 30
  0.900000, 0, 3, 98
  a@dataaug:~/gaa_learning_task/output/resnet_only_20230212$ cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1281, 100
  0.400000, 0, 1281, 100
  0.500000, 0, 1272, 99
  0.600000, 0, 1256, 98
  0.700000, 0, 1204, 93
  0.800000, 0, 1074, 83
  0.900000, 0, 46, 3
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1281, 0
  0.400000, 0, 1281, 0
  0.500000, 0, 1272, 0
  0.600000, 0, 1256, 1
  0.700000, 0, 1204, 6
  0.800000, 0, 1074, 16
  0.900000, 0, 46, 96
  a@dataaug:~/gaa_learning_task/output/resnet_only_20230212$ 

そもそものtest結果が非常に悪い::
  
  INFO main
  dataset size = 2871
  dataset classses = 10
  [2023-02-11 15:32:55.294456] Train Epoch: 0 [0/2009 (0%)]       Average loss: 0.077206
  ...
  [2023-02-11 15:48:04.508375] Train Epoch: 9 [1728/2009 (86%)]   Average loss: 0.016987
  [2023-02-11 15:48:13.331634] Train Epoch: 9 [1920/2009 (96%)]   Average loss: 0.016523

テストは以下。::

  INFO main
  dataset size = 2871
  dataset classses = 10
                precision    recall  f1-score   support
  
             0       0.89      1.00      0.94       243
             1       0.85      0.99      0.91       228
             2       0.82      0.99      0.90       175
             3       0.47      0.61      0.54        31
             4       0.47      0.67      0.55        27
             5       0.00      0.00      0.00        27
             6       0.00      0.00      0.00        38
             7       0.00      0.00      0.00        36
             8       0.40      0.29      0.33        28
             9       0.50      0.28      0.36        29
  
      accuracy                           0.81       862
     macro avg       0.44      0.48      0.45       862
  weighted avg       0.71      0.81      0.75       862

理由が良くわからないな、、、output classesを無理やり10にしたのが悪かったか。
ja_char込でoutput classesを1000幾つにして実施した時はここまでテストでの精度は悪くなかった。
実際の学習クラスは10にしておいて、output classesはデフォルトのままにして、再度学習してみる。
既存の学習済みだと1000位の学習結果になっている、それでcloseの追加学習をしても、それほど強く重みが更新されないと思ったので、
試しに、epochも10から20に変更してみる。これで変化があるか？

学習チェックのパラメータは以下に気をつける必要がある。が、、クラス数が1000になっているので、上手く計算はしてくれない感じがする。
チェックツールにインデックスの幅を考慮する必要があり、少々めんどくさい。以下では多分、上手く行かないだろう。この考慮がないと。::

./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_close_edge.log > calc_exp_res_close.txt
./bin/calc_exp.py --gathering_class_than 0 --gathering_class_as 0 --calc_target 0 check_res_not_close_edge.log > calc_exp_res_not_close.txt

分類クラス数を1000にシテ実施してみた。結果は相変わらずボロボロである。すべてに対してcloseと答えている::

  a@dataaug:~/gaa_learning_task/output/resnet_only_try2_20230212$ cat calc_exp_res_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 209
  =====SUM=====
  0.100000, 0, 209, 100
  0.200000, 0, 209, 100
  0.300000, 0, 209, 100
  0.400000, 0, 209, 100
  0.500000, 0, 209, 100
  0.600000, 0, 209, 100
  0.700000, 0, 209, 100
  0.800000, 0, 209, 100
  0.900000, 0, 209, 100
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 209, 0
  0.200000, 0, 209, 0
  0.300000, 0, 209, 0
  0.400000, 0, 209, 0
  0.500000, 0, 209, 0
  0.600000, 0, 209, 0
  0.700000, 0, 209, 0
  0.800000, 0, 209, 0
  0.900000, 0, 209, 0
  a@dataaug:~/gaa_learning_task/output/resnet_only_try2_20230212$ cat calc_exp_res_not_close.txt 
  INFO: gathering class than 0 as 0
  =====RECORD INFO=====
  total = 1281
  =====SUM=====
  0.100000, 0, 1281, 100
  0.200000, 0, 1281, 100
  0.300000, 0, 1281, 100
  0.400000, 0, 1281, 100
  0.500000, 0, 1280, 99
  0.600000, 0, 1276, 99
  0.700000, 0, 1273, 99
  0.800000, 0, 1267, 98
  0.900000, 0, 1248, 97
  =====SUM(INVERT RAITIO)=====
  0.100000, 0, 1281, 0
  0.200000, 0, 1281, 0
  0.300000, 0, 1281, 0
  0.400000, 0, 1281, 0
  0.500000, 0, 1280, 0
  0.600000, 0, 1276, 0
  0.700000, 0, 1273, 0
  0.800000, 0, 1267, 1
  0.900000, 0, 1248, 2
  a@dataaug:~/gaa_learning_task/output/resnet_only_try2_20230212$ 

クラスとしては、すべてcloseの様子。::

  a@pytorch:~/resset$ grep "(" check_res_close_edge.log  | awk -F "," '{print $1}' | wc
      209     209     627
  a@pytorch:~/resset$ grep "(" check_res_close_edge.log  |wc
      209     418    4991
  a@pytorch:~/resset$ 

  a@pytorch:~/resset$ tail check_res_close_edge.log
  test_data/dataset_20230125/close/ja_char_65_0.jpg
  INFO main
  dataset size = 2871
  dataset classses = 10
  (0, 0.9837756752967834)
  test_data/dataset_20230125/close/pottedplant_17_0.jpg
  INFO main
  dataset size = 2871
  dataset classses = 10
  (0, 0.9974935054779053)
  a@pytorch:~/resset$ 

非closeは以下。::

  a@pytorch:~/resset$ grep "(" check_res_not_close_edge.log  | wc
     1281    2562   30554
  a@pytorch:~/resset$ grep "(" check_res_not_close_edge.log  | awk -F "," '{print $1}' | wc
     1281    1281    3843
  a@pytorch:~/resset$ tail check_res_not_close_edge.log 
  test_data/dataset_20230125/not_close/pottedplant_43_0.jpg
  INFO main
  dataset size = 2871
  dataset classses = 10
  (0, 0.9879393577575684)
  test_data/dataset_20230125/not_close/pottedplant_45_0.jpg
  INFO main
  dataset size = 2871
  dataset classses = 10
  (0, 0.9959017634391785)
  a@pytorch:~/resset$ 

というわけで、与えたすべての画像をclose系と判断してしまっている様子。これでは使い物にならない。
現状、close系の画像だけを与えて学習させて、close系かそれ以外を判定するのは非常に難しいっぽい。

試しに、pretrained=Falseにしてみたら一体どうなるんだろう。。。::

  a@pytorch:~/resset$ git diff
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..b0c931d 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -24,9 +24,10 @@ from single import *
   
   class GAAResNet34():
       def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
  -        self.model.fc = nn.Linear(512,output_classes)
  +        #self.model.fc = nn.Linear(512,output_classes)
           
           self.device = torch.device("cpu")
           self.model.cpu()
  @@ -159,7 +160,7 @@ if __name__ == "__main__":
   
       gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=20)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

やっぱり、output_sizeを10にしたほうが、まだましなので、pretrained=Falseは試しにoutput_size=10の時にして実施してみることに。::

  a@pytorch:~/resset$ git diff 
  diff --git a/core/resnet34.py b/core/resnet34.py
  index eab3ff3..a6d3a1f 100644
  --- a/core/resnet34.py
  +++ b/core/resnet34.py
  @@ -24,7 +24,8 @@ from single import *
   
   class GAAResNet34():
       def __init__(self, output_classes=None, train_ratio=0.7, batch_size=32, epochs=5, verbose=True):
  -        self.model = resnet34(pretrained=True)
  +        #self.model = resnet34(pretrained=True)
  +        self.model = resnet34(pretrained=False)
           #self.model.fc = nn.Linear(512,35)
           self.model.fc = nn.Linear(512,output_classes)
           
  @@ -33,6 +34,7 @@ class GAAResNet34():
           self.verbose = verbose
   
       def train_aux(self,epoch):
  +        print(self.model)
           total_loss = 0
           total_size = 0
           self.model.train()
  @@ -159,7 +161,7 @@ if __name__ == "__main__":
   
       gaa_resnet_34 = GAAResNet34(output_classes=dataset.classes(), verbose=False)
       if sys.argv[1] == "train":
  -        gaa_resnet_34.train(dataset,epochs=5)
  +        gaa_resnet_34.train(dataset,epochs=20)
           gaa_resnet_34.save("./weights/best_weight.pth")
       elif sys.argv[1] == "test":
           gaa_resnet_34.load("./weights/best_weight.pth")
  a@pytorch:~/resset$ 

実行::

  a@dataaug:~/gaa_learning_task$ nohup ./create_task.py resnet_only_try3 --algo resnet34 &
   [1] 19238
   a@dataaug:~/gaa_learning_task$ nohup: ignoring input and appending output to 'nohup.out'
   
   a@dataaug:~/gaa_learning_task$ date
   Sun 12 Feb 2023 02:50:53 PM UTC
   a@dataaug:~/gaa_learning_task$ 
   
  


2023/02/11
============

GAA関連でたくさんissueが溜まっているが、本日は以下のissueに取り組む::

  9. closeの認識精度が悪い(間違って検出、検出しない。など）

このissueにはこれだ！という確固たる対策は特になく、相変わらずいきあたりばったりではあるが、以下について面白そうだと考えている。

今、SSDとResNet34で同じデータセットを使っている。*close*とja_char*、adbuttonであり、SSDとResNet34で入力サイズを変えているだけが異なる点。

しかし、今までSSDやResNetを触ってきての勘だが、データセットを変えてやったほうが、トータルの精度が上がるのではないか？と考えてみた。

理由は、ResNet34の出力サイズを1000以上にしている点。デフォルトが確か、30位だったので、だいぶ違う感じがする。ニューラルネットの実装を見てみると、一番最後の層がサイズが小さくなっており、入力から出力に至るまでサイズが小さくなっていくのが自然な気がする。しかし、今の利用方法では、最後-1のレイヤが512に対して、最後の層(出力)が、1000以上と何か変な感じになっている。

と思ったら、あんまり変な感じはしないか・・・torchのデフォルトで使うと、1000個の分類になっている::

  >>> from torchvision.models import resnet34
  >>> resnet34()
  ResNet(
    (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    (relu): ReLU(inplace=True)
    (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
    (layer1): Sequential(
      (0): BasicBlock(
        (conv1): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (1): BasicBlock(
        (conv1): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (2): BasicBlock(
        (conv1): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
    )
    (layer2): Sequential(
      (0): BasicBlock(
        (conv1): Conv2d(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (downsample): Sequential(
          (0): Conv2d(64, 128, kernel_size=(1, 1), stride=(2, 2), bias=False)
          (1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (1): BasicBlock(
        (conv1): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (2): BasicBlock(
        (conv1): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (3): BasicBlock(
        (conv1): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
    )
    (layer3): Sequential(
      (0): BasicBlock(
        (conv1): Conv2d(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (downsample): Sequential(
          (0): Conv2d(128, 256, kernel_size=(1, 1), stride=(2, 2), bias=False)
          (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (1): BasicBlock(
        (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (2): BasicBlock(
        (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (3): BasicBlock(
        (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (4): BasicBlock(
        (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (5): BasicBlock(
        (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
    )
    (layer4): Sequential(
      (0): BasicBlock(
        (conv1): Conv2d(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (downsample): Sequential(
          (0): Conv2d(256, 512, kernel_size=(1, 1), stride=(2, 2), bias=False)
          (1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (1): BasicBlock(
        (conv1): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
      (2): BasicBlock(
        (conv1): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (relu): ReLU(inplace=True)
        (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn2): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
    )
    (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
    (fc): Linear(in_features=512, out_features=1000, bias=True)
  )
  >>> 

最後のfcというレイヤがそれ。しかし、いろいろいじってみたら何か変わるのかなぁ。
  
そこで、以下を実施してみようと思う。何が変わるだろうか。

1. ResNet34のoutputサイズを小さくしてみる。現状、1030位（でふぉるとで1000)何が変わるかを観察する。
　→　まず、ResNet34のprojectsに*close*があったが、それだけにする。つまり、ResNet34のタスクを*close*かそうじゃないかを判断するような画像認識器にしてみよう。
　→　そのための依存タスクとして、dl_image_managerにissueを発行。これは、完了

なお、ssdについては以前から変更が無いので、ResNet34のみタスクを実行する。手動で、adbutton_try_20230209/のSSD関連をマージする。

以下を実行::

  a@dataaug:~/gaa_learning_task$ date
  Sat 11 Feb 2023 03:32:02 PM UTC
  a@dataaug:~/gaa_learning_task$ 
  この時刻周辺で以下を実行
  nohup ./create_task.py --algo resnet34 resnet_only_20230212 &

※　分類タスク数を10にするということ。

2. close系は１つにまとめてみる
各projectをbuildした後に、それをまとめてdata_setを作る時の話。例えば、closeとclosewcobfatをcloseとしてまとめてしまうには、
closeとclosewcobfatのファイル名を重複しないように、closewcobfatのファイル群をリネームしてやる必要がある。それに、annotaion xmlのlabel名の変更も必要だ。こういったことを実現する考慮が必要か。マージはdata_setに対する操作のため、build_project.shとは別のコマンドにしたほうが良いと思われるの巻。

※ No1とは別に、独立してやってみる。

3. No1とNo2を一緒にやってみる。

2023/02/09
=============

create_taskは終わった。create_taskが出来てからは、単純に追加する画像とannotaion xmlを用意すれば良いだけなので、非常に作業が簡略化されたし、
deployも簡単に各サービスに重みとDataSetを配布できるので、楽ちんになった。本当に素晴らしい・・・！

昨日の状況::

 | GAAのAd buttonサポートはプッシュする際の座標変換システムを残してとりあえずコーディングしたので、明日は座標変換システムのコーディングと、create_taskは完了しているだろうから、とりあえずdeployして、今回GAAに追加したコードを動作させてみるの巻。
 | 

というわけで、座標変換以外動くかなぁということで、テストしてみる。
一通りやったら、座標変換システムを作る。

・・・・と思ったら、SSDでせっかく「広告をみる」ボタンを認識できたのだが、ResNet34で台無しにしている状態に泣。::

  ===== RUN Game EYE =====
  DEBUG: ['INFO: show classes', "('close', 'closebcow', 'closegb', 'closewcobfat', 'closewcolg', 'ja_char', 'adbutton')", '7', "('close', 'closebcow', 'closegb', 'closewcobfat', 'closewcolg', 'ja_char', 'adbutton', 'def0', 'def1', 'def2', 'def3', 'def4', 'def5', 'def6', 'def7', 'def8', 'def9', 'def10', 'def11', 'def12', 'def13')", '21', 'Loading weights into state dict...', 'Finished!', 'DETECT: adbutton(0.63), x=25,y=37,w=157,h=38 None', 'DETECT: closegb(0.21), x=190,y=4,w=39,h=35 None', 'DETECT: closewcobfat(0.20), x=189,y=6,w=39,h=38 None', 'DETECT: closebcow(0.17), x=22,y=41,w=39,h=30 None', 'DETECT: ja_char(0.12), x=22,y=41,w=39,h=30 None', 'IMAGE_LOG=image_log/20230209141751460753']
  DEBUG: log_dir = image_log/20230209141751460753
  RESNET=377, 0.397532
  RESNET=close, 0.817868
  RESNET=close, 0.640329
  RESNET=377, 0.995619
  RESNET=377, 0.995619
  EYE_RESULT=377, 0.995619, x=22,y=41,w=39,h=30

めんどくさいのでResNet34をバイパスするオプションをGameEyeに作って、adbuttonの場合は、ResNet34をしないようにする。::

  commit c4c3a85d4dba6c547ce68f467a307d60a2c1b23f (HEAD -> master, origin/master)
  Author: kazuhiro MIYASHITA <miyakz1192@gmail.com>
  Date:   Thu Feb 9 14:36:47 2023 +0000
  
      algo selection support

一応、「広告をみる」ボタン対応した。これで、単純に広告を見まくるアルゴリズムの実装は完成したものの、
残念ながら、closeの認識精度が著しく悪く、使い物にならん結果になった。


GAAの動作を観察して気づいた点。

1. closeの認識精度が悪い(間違って検出、検出しない。など）
   →　何か作戦を考えたい。

2. SSDのみだと、adbuttonの認識精度はかなり良い(scoreは低いが、SSDへのインプット画像の切り出し方次第では全然使える)
   → 　とりあえず、SSDのみにして様子見。

3. UserWarningがうざくて、ログが埋まる
   →  issueにあげて管理するが、まだ着手しない。

4. 動作がおもすぎて、せっかく検出しても次の画面に変わってしまったために間違った所を押す悲しい結果に。
   →  issueにあげて管理するが、まだ着手しない。高速化の代わりに画面が変わったかどうかを判断する処理を導入することにしたい(issueで管理しておく、。

5. 動作が重い。とにかく重い。
   →　issueで管理。

6. closeを認識する場合は、切り出しが400 x 400でなくても良いのではないか。400 x 200でもよいのでは？
   →　isssueで管理。


ちなみに、No4の話は、検出した所を押そうとしたときに、押そうとした今の画像を取得し、押す箇所を検出した時の画像と類似度を比較する。
例えば、adbuttonを押したあとにCM画像が流れ、CM画像からcloseを抽出するシーンでは、closeを検出する歳に画面が切り替わったかどうかを
この類似度で判断する。変更度が50%以上なら画面が切り替わったと判断するなど。
あとシーンの認識も必要かも。「広告をみる」を見るwindowsすべてをがーっと抽出して、それぞれのwindowsにadbuttonが含まれていれば、
「広告をみるボタンがあるゲーム画面だ」と判断するなど。
その都度、正しいシーンかを判断する仕組みを入れればよいかと考える。
これくらいなら、取り組めそう。

No5はとりあえず我慢。速度最適化よりもまずは精度。

No6は比較的すぐに取り組めそう。

No1は根気が必要。そもそもなぜ検出精度が悪いのか、SSDが良くない？ResNet34が良くない？問題を切り分ける必要がある。
「広告をみる」ボタンの件ではResNet34が結果を悪化させた結果になった。ResNet34の使い方が間違っているのか?

なお、No1が一番根源的な問題であり、かつ、自分自身が技術的にちゃんと理解していないので、改善の方策もいきあたりばったり。
このため、一度、プログラミングから離れて、理論の勉強（基礎）に戻ることにする。
しばらく、お休み。
  
  
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

