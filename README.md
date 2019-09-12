# **The Nature Conservancy Fisheries Monitoring**

> 你能识别并将鱼分类吗？
>

​		本次小学期，我们小组五人（王岩、袁野、龚凯雄、仇中豪、李锡铭）完成了马锐老师安排的一项任务——**基于Kaggle数据集的数据分析**——[Nature Conservancy Fisheries Monitoring Competition](https://www.kaggle.com/c/the-nature-conservancy-fisheries-monitoring)。这是一个关于将在渔船上拍摄的照片进行分类的任务，其最终奖金数目高达150000美金。这是我们五人第一次参加Kaggle比赛，即使这个比赛目前已经关闭，但是仍然让我们在人工智能、图像识别等方面有了进一步的理解与认识。

## 	**Problem statement**

​		世界上近一半的人将海洋食品作为他们的主要蛋白质来源。在西太平洋和中太平洋地区，世界上**60%**的金枪鱼被非法捕捞。非法的、未报告和无管制的捕捞活动正在威胁着海洋生态系统、全球海洋食品供应以及当地的生态环境。大自然保护协会(**The Nature Conservancy**)正与当地、区域以及全球的合作伙伴合作，以保护未来的渔业。

​		目前，协会期望通过使用相机大幅度扩大对捕捞活动的监测，来填补相关的监测数据空白。尽管获取原始数据有各种途径，但是手工处理原始数据仍然是一项十分耗时耗力的工作。

​		这也就是为什么该协会尝试与Kaggle社区进行合作，寻求自动检测并对鱼的品种进行分类。这将加速视频审查过程，而更快的审查和更可靠的数据能够使各国重新分配人力资源，提升监管效果，而更重要的是，这将会保护我们赖以生存的地球。

## **Dataset**

​		训练数据集包括了3792张图片，而第一阶段的测试集包括1000张图片。本次比赛原本包括两个阶段：第一阶段是公开的测试集，所有队伍都可以获得阶段一的1000张图片，各参赛队伍将预测结果按照指定格式提交；而第二阶段在比赛进行期间没有提供给参赛队伍，参赛队伍需要将自己的模型或算法提交，由Kaggle运行程序后得出结果并进行评价。而我们的目标，就是训练一个模型来进行检测并将鱼的品种分为8个类别：

- Albacore Tuna(长鳍金枪鱼)
- Bigeye Tuna(大眼金枪鱼)
- Dolphinfish(鲯鳅)
- Moonfish(月亮鱼)
- Shark(鲨鱼)
- Yellowfin Tuna(黄鳍金枪鱼)
- Others(其他种类)
- No Fish(没有鱼)

下图展示了一些图片的例子(鱼用红色包围框圈出)：

![image-20190910172949280](/Users/Jetpack/Library/Application Support/typora-user-images/image-20190910172949280.png)

​		而由于这个比赛现在已经截止，所以两个阶段的测试数据都已经放在了网站上，包括第一阶段1000张，第二阶段12153张。而比赛的评判也从第一阶段提交分类结果、第二阶段提交模型变成了两阶段同时评测分类结果。

​		本次比赛将使用多种类对数损失(multi-class logarithmic loss)评价，每个图像都标有一个正确的类，对于每个图像都需要提交一组预测的概率。概率公式是：

​							$logloss=−\frac{1}{N}\sum_{i=1}^{N}\sum_{j=1}^{M}y_{ij}log(p_{ij})$

​		N表示测试集中的图片数量，M表示图像的种类，log表示自然对数。如果图片i属于第j类，那么yij为，其他为0。pij表示预测i属于j类的概率。

## **Exploration**

​		在运行一些简单的脚本之后，我们很快发现在这次比赛的数据中存在一些方面让这次的比赛变得很具有挑战性。

### 1)种类分布非常不平衡

![class Distribution Histogram](https://flyyufelix.github.io/img/cls_dist.png)

​		从上面的种类分布直方图，我们可以很清楚的看到，“ALB"种类一共有1719个样本，占据了整个数据集的45%，然而“LAG”和“DOL”分别只有67和117个样本。最终，我们的模型在识别这些种类的时候会出现一些麻烦。

### 2)样本缺少多样性

​		由于我们的样本大多来自于海洋捕捞船只上的摄像机。导致来自同一时间序列的图片具有很高的相似性。比如下图展示的两张来自“LAG”的图片，他们就很相似。同样的情况也出现在其他种类的数据集，这就导致了我们在进行网络训练时有一点问题。

![Video Sequence](https://flyyufelix.github.io/img/sample_video_seq.png)

### 3)种类模糊

​		一些种类，例如“ALB”，“BET”和“YFT”，彼此之间是非常相似的。即使我们肉眼看都很难辨别一些图片到底是属于哪个种类。就如下面这三张图片，人的肉眼都很难分辨出其到底属于哪种鱼。

![image-20190911193738945](/Users/Jetpack/Library/Application Support/typora-user-images/image-20190911193738945.png)

------

## First Attempt: Pretrained ConvNets on Full Image

------

## Detection and Localization

​		即使是凭借我们自己的分析，也可以得出结论：先进行Object Detection(物体识别)，再进行Classification(分类)得出的结果一定会强于直接对全图进行Classification(分类)的结果，因为如果进行Object Detection后，将识别出的鱼作为分类网络的输入，那么该网络只会提取鱼的特征；而如果将全图作为分类网络的输入，那么网络便会提取出所有的特征，很大的可能会将除了鱼之外的其他特征作为判别标准，从而导致结果下降。

​		所以，为了进行Object Detection，我们需要训练一个可以对图片进行识别并生成Bounding Box的网络。而目前被广泛应用的Object Detection网络有Faster R-CNN、YOLO等。王岩最开始尝试了使用Faster R-CNN网络进行预测，但是尝试了几天，配置环境以及运行demo都遇到了难点，没有找到解决办法，所以最终决定转为使用YOLO。

#### YOLO(You Only Look Once)

​		YOLO是一个因其简便性和速度快而著称的object detection模型。与Faster R-CNN的5-7 fps相比，YOLO可以达到45 fps。因此，YOLO尤其适合实时Object Detection任务，例如流媒体上的物体检测。

​		YOLO首先将原始输入图像划分为N*N个方块区域，然后将其拟合到卷积神经网络，输出M组物体置信度得分以及Bounding Box坐标，其中M取决于N。整个模型都是端到端训练的。

![image-20190911200841216](/Users/Jetpack/Library/Application Support/typora-user-images/image-20190911200841216.png)

​		本次我们组使用了**YOLO v3**，这是YOLO的改进网络，在保证了速度的同时，提升了识别准确率，同时也提升了对小物体的识别成功率。而具体实现方面，我组使用了darknet，这是一个比较小众的深度学习框架，但是其有着几个独有的优点：

- 易于安装：在makefile里面选择自己需要的附加项（cuda，cudnn，opencv等）直接make即可，几分钟完成安装；
- 没有任何依赖项：整个框架都用C语言进行编写，可以不依赖任何库，连opencv作者都编写了可以对其进行替代的函数；
- 结构明晰，源代码查看、修改方便：其框架的基础文件都在src文件夹，而定义的一些检测、分类函数则在example文件夹，可根据需要直接对源代码进行查看和修改；
- 友好python接口：虽然darknet使用c语言进行编写，但是也提供了python的接口，通过python函数，能够使用python直接对训练好的.weight格式的模型进行调用；

具体来讲，我组首先从网上下载了原始训练数据的标注数据，即Bounding Box的坐标信息等组成的.json文件；接下来，将.json文件做处理，生成darknet可以使用的对应格式的.txt标注数据；然后修改配置文件，由于我们决定将检测与分类作为两个阶段来进行处理，所以将检测只设置一类——鱼，这样在Object Detection的时候，网络会将任意种类的鱼圈出Bounding Box，这样会提高网络的准确性，然后配置训练集、验证集和测试集的地址以及batch size、CPU/GPU等各种训练参数。接下来我组迭代了10000次，并保存了每1000次的权重：

![image-20190911203004298](/Users/Jetpack/Library/Application Support/typora-user-images/image-20190911203004298.png)

通过测试，我们最终选择了7000次迭代生成的权重，测试结果如下：

![prediction7000](/Users/Jetpack/Desktop/Study/mini-semester-2019/prediction7000.jpg)

我们运用该网络，将所有测试集13153张图片进行Object Detection，将最终结果保存到.txt文件中，然后将每张图片识别出的Bounding Box的坐标读取并按其对原图进行剪裁，生成了只含有鱼的分类网络的输入：

![image-20190911203431543](/Users/Jetpack/Library/Application Support/typora-user-images/image-20190911203431543.png)

至此，我们基本完成了Object Detection任务。


