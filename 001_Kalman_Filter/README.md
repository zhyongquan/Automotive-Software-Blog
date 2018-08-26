# 卡尔曼滤波
[原文](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)

这篇文章提供了简单直观的卡尔曼滤波推导，目的是把这个有用的工具介绍给学生，不需要很强大的数学背景。最复杂的数学层面是理解推导，可以把2个高斯方程相乘，并得到紧凑形式。

卡尔曼滤波已经有50多年了，但仍是今天使用的最重要和最常用的数据融合算法。以Rudolf E.Kalman的名字命名，卡尔曼滤波的巨大成功是因为它的计算量小，优雅的递归性能，并且它的状态就是具有高斯误差的一阶线性系统的最有估计。卡尔曼滤波的典型应用包括平滑噪声数据，提供兴趣参数的估计。应用包括全球定位系统接收器，收音机中锁相循环，平滑笔记本电脑触摸板输出，以及很多其他。

从理论角度，卡尔曼滤波允许在一阶动态系统内精确推导的算法，一阶动态系统是贝叶斯模型，类似于隐藏的马尔科夫模型，但是潜在变量的状态空间是连续的，且所有潜伏和观测变量都是高斯分布的（通常是一个多元高斯分布）。本课程的目的是让受到此描述困惑，或者害怕理解卡尔曼滤波基础，通过简单直接的推导。
## 关系
卡尔曼滤波（以及他的变型，比如扩展卡尔曼滤波、无损卡尔曼滤波）是一个最受欢迎和最流行的数据融合算法，在信息处理领域。最著名的早期应用是阿波罗导航系统，带领阿姆斯特朗到月球，并且（最重要的）带他回来。今天，卡尔曼滤波工作于每个卫星导航设备，每个智能手机和很多电脑游戏中。

卡尔曼滤波是典型的向量代数衍生，最小平均平方估计。这个方法适用于对数学有自信的学生，而不适用于没有很强数学基础学科的学生。本文，卡尔曼滤波有一个简单的物理学例子中的牛顿第一定律，利用了关键属性，高斯分布。特别是2个高斯分布的乘积是另一个高斯分布。
## 前提
这篇文章不是针对一个卡尔曼滤波小白学生，想要了解，的教程，反而是一个直观介绍对数学基础不强的学生。读者应当了解卡尔曼滤波中的矢量符号和术语，例如状态向量和协方差。本文的目的是针对那些想要教授卡尔曼滤波给他人的，或者已经对卡尔曼有些了解，但不能完全理解他的基础。这篇文章不适用于小白的教学工具，他们需要一个章节，而不是简单的图片和传达。
## 问题描述
卡曼滤波模型假设在时刻 $t$ 的系统状态，可从之前 $t-1$ 时刻得到，通过公式：

$$
\boldsymbol{x}_t=\boldsymbol{F}_t\boldsymbol{x}_{t-1}+\boldsymbol{B}_t\boldsymbol{u}_t+\boldsymbol{w}_t
$$

其中

- $\boldsymbol{x}_t$ 是包含时刻 *t* 系统感兴趣的名词（例如位置、速度、朝向）
- $\boldsymbol{u}_t$ 是包含所有输入的向量（方向盘撞角、节气门设置、刹车力）
- $\boldsymbol{F}_t$ 是状态转移矩阵，表示每个系统状态参数在 *t*-1 时刻对 *t* 时刻的影响（例如时刻 *t*-1 位置和速度都影响时刻 *t* 的位置有影响）
- $\boldsymbol{B}_t$ 表示 $\boldsymbol{u}_t$ 中每个输入参数的影响（例如节气门状态对系统速度和位置的影响）
- $\boldsymbol{w}_t$ 表示每个参数的过程噪声。假设过程噪声是一个平均值是0的多元正态分布，协方差矩阵是 $\boldsymbol{Q}_t$ 。

系统的测量值也可用如下模型表示：

$$
\boldsymbol{z}_t=\boldsymbol{H}_t\boldsymbol{x}_{t}+\boldsymbol{v}_t\tag{2}
$$

其中：

- $\boldsymbol{z}_t$ 是测量向量。
- $\boldsymbol{H}_t$ 是转换矩阵，映射状态向量参数到测量域。
- $\boldsymbol{v}_t$ 包含了每个观测量的测量噪声。和过程噪声类似，测量噪声是均值0的高斯白噪声，协方差 $\boldsymbol{R}_t$ 。
![图1][1]
图1：此图展示了使用的一维系统。

接下来的推导，我们使用一个简单的一维跟踪问题，指的是火车延铁轨运动（见图1）。在这个问题中，我们可以建立一些示例向量和矩阵。状态向量 $\boldsymbol{x}_t$ 包含了火车的位置和速度：

$$
\boldsymbol{x}_t=\left[
\begin{matrix}
x_t\\
\dot{x}_t
\end{matrix}
\right]
$$

火车驾驶员可能会使用刹车或油门，可以认为是一个作用力 $f_t$ 和火车质量 $m$。这些控制信息存储在控制向量

$\boldsymbol{u}_t$中：
$$
\boldsymbol{u}_t=\frac{f_t}{m}
$$

在 $\Delta{t}$ 时间内（$t-1$ 到 $t$）,作用力和刹车、油门，以及和位置、速度的关系，用如下公式表示：

$$
\boldsymbol{x}_t=\boldsymbol{x}_{t-1}+(\dot{\boldsymbol{x}}_{t-1}\times\Delta{t})+\frac{f_t(\Delta{t})^2}{2m}\\
\dot{\boldsymbol{x}}_{t}=\dot{\boldsymbol{x}}_{t-1}+\frac{f_t\Delta{t}}{m}
$$

这些线性公式可以写成矩阵形式：

$$
[\begin{matrix}
\boldsymbol{x}_t\\
\dot{\boldsymbol{x}}_{t}
\end{matrix}]=[\begin{matrix}
1&\Delta{t}\\
0&1
\end{matrix}][\begin{matrix}
\boldsymbol{x}_{t-1}\\
\dot{\boldsymbol{x}}_{t-1}
\end{matrix}]+[\begin{matrix}
\frac{(\Delta{t})^2}{2}\\
\Delta{t}
\end{matrix}]\frac{f_t}{m}
$$

和公式1对比，可以得到：

$$
\boldsymbol{F}_t=[\begin{matrix}
1&\Delta{t}\\
0&1
\end{matrix}]\\
\boldsymbol{B}_t=[\begin{matrix}
\frac{(\Delta{t})^2}{2}\\
\Delta{t}
\end{matrix}]
$$

系统真实状态 $\boldsymbol{x}_t$ 不能直接观测，卡尔曼滤波提供了一种算法，可以通过合并系统和噪声测量模型，得到估计值  $\hat{\boldsymbol{x}}_t$。状态向量中兴趣参数的估计现在可以通过概率密度函数（pdfs），而不是离散值。卡尔曼滤波建立在高斯pdfs之上，通过下面“解决”方案推导。为了全面描述高斯方程，我们需要知道方差和协方差，这些存储在协方差矩阵 $\boldsymbol{P}_t$。$\boldsymbol{P}_t$的主对角线是状态向量相关参数的方差。非对角线是状态变量参数的协方差。在一个良好模型，一维线性系统中，测量误差是一个平局值为0的高斯分布，卡尔曼滤波是一个最有估计。在本文中，卡尔曼滤波等式允许我们通过和并之前的知识，系统预测和噪声测量，进行递归计算 $\hat{\boldsymbol{x}}_t$ 。

卡尔曼滤波算法包含2个阶段：预测和测量更新。预测阶段的标准卡尔曼滤波等式：

$$
\hat{\boldsymbol{x}}_{t|t-1}=\boldsymbol{F}_t\hat{\boldsymbol{x}}_{t-1|t-1}+{\boldsymbol{B}}_{t}{\boldsymbol{u}}_{t}\tag{3}
$$$$
\boldsymbol{P}_{t|t-1}=\boldsymbol{F}_t{\boldsymbol{P}}_{t-1|t-1}\boldsymbol{F}_t^T+\boldsymbol{Q}_t\tag{4}
$$

其中：

$\boldsymbol{Q}_t$ 是过程噪声的协方差，和噪声控制输入相关连。等式（3）在前面已经推导过。我们可按如下方法推导出等式（4）。预测值 $\hat{x}_{t|t-1}$ 和未知真实值 ${x}_t$ 的协方差是：

$$
{P}_{t|t-1}=E[({x}_{t}-\hat{x}_{t|t-1})(\hat{x}_{t|t-1})^T]
$$

观察（3）和（1）的区别：

$$
{x}_{t}-\hat{x}_{t|t-1}=F({x}_{t-1}-\hat{x}_{t|t-1})+w_t\\
\Rightarrow{P}_{t|t-1}=E[(F({x}_{t-1}-\hat{x}_{t|t-1})+w_t)\times(F({x}_{t-1}-\hat{x}_{t|t-1})+w_t)^T]\\
=FE[(x_{t-1}-\hat{x}_{t-1|t-1})\times(x_{t-1}-\hat{x}_{t-1|t-1})^T]\times{F^T}\\
+FE[(x_{t-1}-\hat{x}_{t-1|t-1})w_t^T]\\
+E[{w_t}x_{t-1}-\hat{x}_{t-1|t-1}^T]F^T\\
+E[w_t{w_t^T}]
$$

状态估计误差和过程噪声是不相关的：

$$
E[(x_{t-1}-\hat{x}_{t-1|t-1})w_t^T]=E[w_t(x_{t-1}-\hat{x}_{t-1|t-1})]=0
$$$$
\Rightarrow{P}_{t|t-1}=FE[(x_{t-1}-\hat{x}_{t-1|t-1})\times(x_{t-1}-\hat{x}_{t-1|t-1})^T]\times{F^T}+E[w_t{w_t^T}]\\
\Rightarrow{P}_{t|t-1}=FP_{t-1|t-1}F^T+Q_t
$$

测量值更新等式：

$$
\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}+\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})\tag{5}
$$$$
\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}\tag{6}
$$

式中

$$
\boldsymbol{K}_t=\boldsymbol{P}_{t|t-1}\boldsymbol{H}_t^T(\boldsymbol{H}_tP_{t|t-1}\boldsymbol{H}_t^T+\boldsymbol{R}_t)^{-1}\tag{7}
$$

本文中，我们从牛顿第一定律推导出等式[(5)-(7)]。
## 求解
卡尔曼滤波使用一维循迹问题，指的是火车沿着铁轨运动。每次测量时，我们希望得到火车位置的最佳估计值（或者更准确的说，火车顶上天线的位置）。信息来自两个方面：1.基于上一次已知的位置和速度进行的预测值；2.火车轨道旁边测量的天线位置。预测值和测量值一起提供火车最优估计。系统如图1所示。

![图2][2]

图2：时刻 $t=0$ 系统初始位置。红色的高斯分布表示了火车预测位置的初始可信度。箭头指向右边，表示火车的初速度。

如图2所示，系统初始状态（时刻 $t=0$s）在精度范围内。火车的位置是高斯分布。下一时刻（$t=1$s），我们可以估计火车的可能位置，基于已知的 $t=0$ 限制，例如它的位置和速度，以及最大可能的加速度和减速度等。实际上，我们可能知道一些驾驶员刹车和油门的控制输入。任意情况下，我们有心位置的预测，如图3所示的新平局值和方差的高斯分布。数学上对应的公式（1）。方差增加了，见公式（2），意味着精度减少了和 $t=0$ 相比较，因为来自加速和减速的不确定任意过程噪声。

![图3][3]

图3：$t=1$ 时刻的火车预测位置和预测值的不确定等级。火车位置的可信度降低了，比如我们不确定火车火车是否有加速或减速在 $t=0$ 到 $t=1$ 之间。

时刻 $t=1$，我们使用无线电定位系统测量了火车的位置，这个用图4中的蓝色高斯分布表示。我们通过组合预测值和测量值，得到火车位置的最优估计。这个通过2个关联的pdf相乘得到。如图5中绿色正态分布。

此处使用了高斯方程的关键属性：2个高斯方程的积是另一个高斯方程。这是至关重要的，使它可以把无限个高斯分布相乘，但是结果却不增加复杂度和参数；每次之后，一个新的分布可用高斯方程表示。这是卡尔曼滤波优雅迭代的关键。

上述图形中的描述被用于数学地推到卡尔曼滤波的测量值更新等式。

图3中红色高斯方程表示预测值分布，等式如下：

$$
y_1(r,\mu_1,\sigma_1)\triangleq\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\frac{(r-\mu_1)^2}{2\sigma_1^2}}\tag{8}
$$

![图][4]

图4中测量值正态分布：

$$
y_2(r,\mu_2,\sigma_2)\triangleq\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\frac{(r-\mu_2)^2}{2\sigma_2^2}}\tag{9}
$$

这2个方程相融合，例如同时考虑预测和测量（见图5）。新正太分布：

![图5][5]

$$
\begin{align}
y_{fused}(r;\mu_2,\sigma_2,\mu_2,\sigma_2) &= \frac1{\sqrt{2\pi\sigma_1^2}}e^{-\frac{(r-\mu_1)^2}{2\sigma_1^2}}\times\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\frac{(r-\mu_2)^2}{2\sigma_2^2}}\\
&= \frac1{\sqrt{2\pi\sigma_1^2\sigma_2^2}}e^{-(\frac{(r-\mu_1)^2}{2\sigma_1^2}+\frac{(r-\mu_2)^2}{2\sigma_2^2})}\tag{10}
\end{align}
$$

新方程中的二次项可以折叠，然后整个表达式的高斯形式：

$$
y_{fuesd}(r,\mu_{fused},\sigma_{fused})=\frac{1}{\sqrt{2\pi\sigma_{fused}^2}}e^{-\frac{(r-\mu_fused)^2}{2\sigma_fused^2}}\tag{11}
$$

其中：

$$
\mu_{fused}=\frac{\mu_1\sigma_2^2+\mu_2\sigma_1^2}{\sigma_1^2+\sigma_2^2}=\mu_1+\frac{\sigma_1^2(\mu_2-\mu_1)}{\sigma_1^2+\sigma_2^2}\tag{12}
$$
$$
\sigma_{fused}^2=\frac{\sigma_1^2\sigma_2^2}{\sigma_1^2+\sigma_2^2}=\sigma_1^2-\frac{\sigma_1^4}{\sigma_1^2+\sigma_2^2}\tag{13}
$$

最后2个等式表示了卡尔曼滤波算法中测量值更新的步骤。然后，为了演示更通用的例子，我们需要考虑一个延伸。

上面的例子中，假设预测值和测量值在相同坐标系和相同单位。这导致了特别简洁的公式来表示预测值和测量值的更新步骤。实际上，需要一个方程吧预测值和测量值映射到相同域。我们的例子向更实际方向扩展，火车预测位置是一个沿铁轨的以米为单位的新距离，但是航程测量值的时间单位是秒。为使预测值和测量值的分布可以相乘，一个必须转化到另一个的域，标准做法是影响预测值到测量值，使用一个转换矩阵 $\boldsymbol{H}_t$。

重新回顾（8）和（9），不考虑 $y_1$ 和 $y_2$ 以沿铁路米为单位，认为 $y2$ 是秒为单位的时间，无线电信号从发射器位置 $x=0$ 到火车天线的时间。空间分布 $y_1$ 转换到测量域，通过一个系数 $c$，光的速度。等式（8）和（9）重写成：

$$
y_1(s;\mu_1,\sigma_1,c)\triangleq\frac1{\sqrt{2\pi(\dfrac{\sigma_1}{c})^2}}e^{-\dfrac{(s-\frac{\mu_1}{c})^2}{2(\frac{\sigma_1}{c})^2}}\tag{14}
$$

且

$$
y_2(s;\mu_2,\sigma_2,c)\triangleq\dfrac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(s-\mu_2)^2}{2\sigma_2^2}}\tag{15}
$$

式中两个分布都是定义在测量域中，无线电信号在时间“s”轴，测量单位是秒。

根据之前的推导,我们得到:

$$
\frac{\mu_{fused}}{c}=\frac{\mu_1}{c}+\frac{(\frac{\sigma_1}{c})^2(\mu_2-\frac{\mu_1}{c})}{(\frac{\sigma}{c})^2+\sigma_2^2}\\
\Rightarrow\mu_{fused}=\mu_1+(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2+\sigma_2^2})\cdot(\mu_2-\frac{\mu_1}{c})
$$

带入 $H=1/c$ 和 $K=(H\sigma_1^2)/(H^2\sigma_1^2+\sigma_2^2)$ 得到：

$$
\mu_{fused}=\mu_1+K\cdot(\mu_2-H\mu_1)\tag{17}
$$

融合方差估计变成：

$$
\frac{\sigma_{fused}^2}{c^2}=(\frac{\sigma_1^2}{c})-\frac{(\frac{\sigma_1}{c})^4}{(\frac{\sigma_1}{c})^2+\sigma_2^2}\\
\Rightarrow\sigma_{fused}^2=\sigma_1^2-(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2+\sigma_2^2})\frac{\sigma_1^2}{c}\\
=\sigma_1^2-KH\sigma_1^2\tag{18}
$$

我们现在比较标量推导结果和卡尔曼算法中的向量和矩阵：

- $\mu_{fused}\rightarrow\hat{\boldsymbol{x}_{t|t}}$：数据融合的状态向量
- $\mu_1\rightarrow\hat{\boldsymbol{x}_{t|t-1}}$：数据融合前的状态向量，例如：预测
- $\sigma_{fused}^2\rightarrow\boldsymbol{P}_{t|t}$：数据融合的协方差矩阵
- $\sigma_1^2\rightarrow\boldsymbol{P}_{t|t-1}$：数据融合前的协方差矩阵
- $\mu_2\rightarrow\boldsymbol{z}_t$：测量向量
- $\sigma_2^2\rightarrow\boldsymbol{R}_t$：不确定矩阵，即测量噪声
- $H\rightarrow\boldsymbol{H}_t$：映射参数到测量域的转换矩阵
- $k=\frac{H\sigma_1^2}{H^2\sigma_1^2+\sigma_2^2}\rightarrow\boldsymbol{K}_t=\boldsymbol{P}_{t|t-1}\boldsymbol{H}_t^T(\boldsymbol{H}_tP_{t|t-1}\boldsymbol{H}_t^T+\boldsymbol{R}_t)^{-1}$：卡尔曼增益

现在很轻易的可以看出标准卡尔曼滤波等式，和前面推导的（17）和（18）：

$$
\mu_{fused}=\mu_1+K\cdot(\mu_2-H\mu_1)\rightarrow\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}+\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})\\
\sigma_{fused}^2=\sigma_1^2-KH\sigma_1^2\rightarrow\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}
$$

## 结论
卡尔曼滤波可通过标量数学，基本代数操作、易理解的实验来教授。这个方法允许学生没有很强的数学基础去理解卡尔曼滤波是的核心数学，通过高斯方程循环推导。


  [1]: https://s1.ax1x.com/2018/08/26/PbtiDA.jpg
  [2]: https://s1.ax1x.com/2018/08/26/Pbtpge.jpg
  [3]: https://s1.ax1x.com/2018/08/26/Pbt9jH.jpg
  [4]: https://s1.ax1x.com/2018/08/26/PbtFHI.jpg
  [5]: https://s1.ax1x.com/2018/08/26/PbtPud.jpg
