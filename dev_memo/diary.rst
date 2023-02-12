===============
GAA改造日記
===============

全体的な人気をすべてこちらに集約することにする。
すでにバラけたものを集約すること無く、新しい情報からこちらに集約する。

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

