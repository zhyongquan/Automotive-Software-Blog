# 卡尔曼滤波
本文使用火车运动的例子进行卡尔曼滤波的推导和Python实现。
## 1. 简介
卡拉曼滤波广泛应用于数据融合领域，如阿波罗导航系统，汽车多传感器融合等。
卡尔曼滤波可以用如下公式表示：
<div align=center>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" title="\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}+\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" title="\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" /></a>
</div>
式中：

- <a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t}" title="\hat{\boldsymbol{x}}_{t|t}" /></a> 表示 *t* 时刻的最优估计
- <a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t-1}" title="\hat{\boldsymbol{x}}_{t|t-1}" /></a> 表示 *t*-1 时刻对 *t* 时刻的预测
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{K}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{K}_t" title="\boldsymbol{K}_t" /></a> 表示测量值和预测值的协方差矩阵
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{z}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{z}_t" title="\boldsymbol{z}_t" /></a> 表示 *t* 时刻的测量值
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{H}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{H}_t" title="\boldsymbol{H}_t" /></a>
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{P}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{P}_{t|t-1}" title="\boldsymbol{P}_{t|t-1}" /></a>


## 2. 推导
### 2.1 前提
如图所示，火车沿铁轨运动，要求解火车天线的位置，<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{x}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{x}_t" title="\boldsymbol{x}_t" /></a> 包含了火车位置和速度：
<div align=center>
<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{x}_t=\left[&space;\begin{matrix}&space;x_t\\&space;\dot{x}_t&space;\end{matrix}&space;\right]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{x}_t=\left[&space;\begin{matrix}&space;x_t\\&space;\dot{x}_t&space;\end{matrix}&space;\right]" title="\boldsymbol{x}_t=\left[ \begin{matrix} x_t\\ \dot{x}_t \end{matrix} \right]" /></a>
</div>
火车受到 <a href="https://www.codecogs.com/eqnedit.php?latex=f_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_t" title="f_t" /></a> 的力，火车质量 *m*，

![图1][1]


  [1]: https://s1.ax1x.com/2018/08/26/PbtiDA.jpg
  [2]: https://s1.ax1x.com/2018/08/26/Pbtpge.jpg
  [3]: https://s1.ax1x.com/2018/08/26/Pbt9jH.jpg
  [4]: https://s1.ax1x.com/2018/08/26/PbtFHI.jpg
  [5]: https://s1.ax1x.com/2018/08/26/PbtPud.jpg
