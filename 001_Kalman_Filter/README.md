# 卡尔曼滤波
本文参考文章[《Understanding the Basis of the Kalman Filter Via a Simple and Intuitive Derivation》](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)，使用火车运动的例子进行卡尔曼滤波的推导，并用Python实现。

## 1. 简介
卡拉曼滤波广泛应用于数据融合领域，如阿波罗导航系统，汽车多传感器融合等。

卡尔曼滤波可以用如下公式表示：
<div align=center>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" title="\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}+\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" title="\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{K}_t=\boldsymbol{P}_{t|t-1}\boldsymbol{H}_t^T(\boldsymbol{H}_tP_{t|t-1}\boldsymbol{H}_t^T&plus;\boldsymbol{R}_t)^{-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{K}_t=\boldsymbol{P}_{t|t-1}\boldsymbol{H}_t^T(\boldsymbol{H}_tP_{t|t-1}\boldsymbol{H}_t^T&plus;\boldsymbol{R}_t)^{-1}" title="\boldsymbol{K}_t=\boldsymbol{P}_{t|t-1}\boldsymbol{H}_t^T(\boldsymbol{H}_tP_{t|t-1}\boldsymbol{H}_t^T+\boldsymbol{R}_t)^{-1}" /></a>
</div>
式中：

- <a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t}" title="\hat{\boldsymbol{x}}_{t|t}" /></a> 表示 *t* 时刻的最优估计。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\hat{\boldsymbol{x}}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{\boldsymbol{x}}_{t|t-1}" title="\hat{\boldsymbol{x}}_{t|t-1}" /></a> 表示 *t*-1 时刻对 *t* 时刻的预测。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{K}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{K}_t" title="\boldsymbol{K}_t" /></a> 系统增益。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{z}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{z}_t" title="\boldsymbol{z}_t" /></a> 表示 *t* 时刻的测量值。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{H}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{H}_t" title="\boldsymbol{H}_t" /></a> 表示转换矩阵，把测量值映射到预测值，统一变量单位。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{P}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{P}_{t|t-1}" title="\boldsymbol{P}_{t|t-1}" /></a> 表示预测值标准差。
- <a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{R}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{R}_t" title="\boldsymbol{R}_t" /></a> 表示测量值的标准差。


## 2. 推导
卡拉曼滤波算法利用了正太分布的特性，系统预测值和测量值都是正太分布，两者相乘得到最优估计的正太分布，减小了标准差，提高了精度。算法计算量小，易收敛。

### 2.1 前提
如图所示，火车沿铁轨运动，要求解火车天线的位置，<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{x}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{x}_t" title="\boldsymbol{x}_t" /></a> 包含了火车位置和速度：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\boldsymbol{x}_t=\left[&space;\begin{matrix}&space;x_t\\&space;\dot{x}_t&space;\end{matrix}&space;\right]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\boldsymbol{x}_t=\left[&space;\begin{matrix}&space;x_t\\&space;\dot{x}_t&space;\end{matrix}&space;\right]" title="\boldsymbol{x}_t=\left[ \begin{matrix} x_t\\ \dot{x}_t \end{matrix} \right]" /></a>
</div>
火车受到 <a href="https://www.codecogs.com/eqnedit.php?latex=f_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_t" title="f_t" /></a> 的力，火车质量 <a href="http://www.codecogs.com/eqnedit.php?latex=m" target="_blank"><img src="http://latex.codecogs.com/gif.latex?m" title="m" /></a>。火车输入信号 <a href="http://www.codecogs.com/eqnedit.php?latex=\boldsymbol{u}_t" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\boldsymbol{u}_t" title="\boldsymbol{u}_t" /></a>：
<div align=center>
<a href="http://www.codecogs.com/eqnedit.php?latex=\boldsymbol{u}_t=\frac{f_t}{m}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\boldsymbol{u}_t=\frac{f_t}{m}" title="\boldsymbol{u}_t=\frac{f_t}{m}" /></a>
</div>
在 <a href="http://www.codecogs.com/eqnedit.php?latex=\Delta{t}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\Delta{t}" title="\Delta{t}" /></a> 时间内，位置、速度和作用力之间的关系：
<div align=center>
<p/>
<a href="http://www.codecogs.com/eqnedit.php?latex=\boldsymbol{x}_t=\boldsymbol{x}_{t-1}&plus;(\dot{\boldsymbol{x}}_{t-1}\times\Delta{t})&plus;\frac{f_t(\Delta{t})^2}{2m}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\boldsymbol{x}_t=\boldsymbol{x}_{t-1}&plus;(\dot{\boldsymbol{x}}_{t-1}\times\Delta{t})&plus;\frac{f_t(\Delta{t})^2}{2m}" title="\boldsymbol{x}_t=\boldsymbol{x}_{t-1}+(\dot{\boldsymbol{x}}_{t-1}\times\Delta{t})+\frac{f_t(\Delta{t})^2}{2m}" /></a>
<p/>
<a href="http://www.codecogs.com/eqnedit.php?latex=\dot{\boldsymbol{x}}_{t}=\dot{\boldsymbol{x}}_{t-1}&plus;\frac{f_t\Delta{t}}{m}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\dot{\boldsymbol{x}}_{t}=\dot{\boldsymbol{x}}_{t-1}&plus;\frac{f_t\Delta{t}}{m}" title="\dot{\boldsymbol{x}}_{t}=\dot{\boldsymbol{x}}_{t-1}+\frac{f_t\Delta{t}}{m}" /></a>
</div>
写成矩阵形式：
<div align=center><p/>
<a href="http://www.codecogs.com/eqnedit.php?latex=\left[\begin{matrix}&space;\boldsymbol{x}_t\\&space;\dot{\boldsymbol{x}}_{t}&space;\end{matrix}\right]=\left[\begin{matrix}&space;1&\Delta{t}\\&space;0&1&space;\end{matrix}\right]\left[\begin{matrix}&space;\boldsymbol{x}_{t-1}\\&space;\dot{\boldsymbol{x}}_{t-1}&space;\end{matrix}\right]&plus;\left[\begin{matrix}&space;\frac{(\Delta{t})^2}{2}\\&space;\Delta{t}&space;\end{matrix}\right]\frac{f_t}{m}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?\left[\begin{matrix}&space;\boldsymbol{x}_t\\&space;\dot{\boldsymbol{x}}_{t}&space;\end{matrix}\right]=\left[\begin{matrix}&space;1&\Delta{t}\\&space;0&1&space;\end{matrix}\right]\left[\begin{matrix}&space;\boldsymbol{x}_{t-1}\\&space;\dot{\boldsymbol{x}}_{t-1}&space;\end{matrix}\right]&plus;\left[\begin{matrix}&space;\frac{(\Delta{t})^2}{2}\\&space;\Delta{t}&space;\end{matrix}\right]\frac{f_t}{m}" title="\left[\begin{matrix} \boldsymbol{x}_t\\ \dot{\boldsymbol{x}}_{t} \end{matrix}\right]=\left[\begin{matrix} 1&\Delta{t}\\ 0&1 \end{matrix}\right]\left[\begin{matrix} \boldsymbol{x}_{t-1}\\ \dot{\boldsymbol{x}}_{t-1} \end{matrix}\right]+\left[\begin{matrix} \frac{(\Delta{t})^2}{2}\\ \Delta{t} \end{matrix}\right]\frac{f_t}{m}" /></a>
</div>


![图1][1]

### 2.2 求解
如图所示，火车的 <a href="http://www.codecogs.com/eqnedit.php?latex=t=0" target="_blank"><img src="http://latex.codecogs.com/gif.latex?t=0" title="t=0" /></a> 初始位置，红色表示位置的高斯分布。箭头指向右边，表示火车的初速度。


![图2][2]

下图红色表示预测值的的正态分布：
<div align=center><p/>
<a href="http://www.codecogs.com/eqnedit.php?latex=y_1(r,\mu_1,\sigma_1)\triangleq\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?y_1(r,\mu_1,\sigma_1)\triangleq\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}" title="y_1(r,\mu_1,\sigma_1)\triangleq\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}" /></a>
</div>


![图3][3]

下图蓝色表示测量值的正太分布：
<div align=center><p/>
<a href="http://www.codecogs.com/eqnedit.php?latex=y_2(r,\mu_2,\sigma_2)\triangleq\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?y_2(r,\mu_2,\sigma_2)\triangleq\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}" title="y_2(r,\mu_2,\sigma_2)\triangleq\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}" /></a>
</div>

![图4][4]

利用正太分布的特性，得到下图绿色估计值的正太分布：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=y_{fused}(r;\mu_2,\sigma_2,\mu_2,\sigma_2)=&space;\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}\times\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}\\&space;=\frac1{\sqrt{2\pi\sigma_1^2\sigma_2^2}}e^{-\left(\dfrac{(r-\mu_1)^2}{2\sigma_1^2}&plus;\dfrac{(r-\mu_2)^2}{2\sigma_2^2}\right)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_{fused}(r;\mu_2,\sigma_2,\mu_2,\sigma_2)=&space;\frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}\times\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}\\&space;=\frac1{\sqrt{2\pi\sigma_1^2\sigma_2^2}}e^{-\left(\dfrac{(r-\mu_1)^2}{2\sigma_1^2}&plus;\dfrac{(r-\mu_2)^2}{2\sigma_2^2}\right)}" title="y_{fused}(r;\mu_2,\sigma_2,\mu_2,\sigma_2)= \frac1{\sqrt{2\pi\sigma_1^2}}e^{-\dfrac{(r-\mu_1)^2}{2\sigma_1^2}}\times\frac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(r-\mu_2)^2}{2\sigma_2^2}}\\ =\frac1{\sqrt{2\pi\sigma_1^2\sigma_2^2}}e^{-\left(\dfrac{(r-\mu_1)^2}{2\sigma_1^2}+\dfrac{(r-\mu_2)^2}{2\sigma_2^2}\right)}" /></a>
</div>

![图5][5]

把相同项折叠起来，则可写成：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=y_{fuesd}(r,\mu_{fused},\sigma_{fused})=\frac{1}{\sqrt{2\pi\sigma_{fused}^2}}e^{-\dfrac{(r-\mu_{fused})^2}{2\sigma_{fused}^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_{fuesd}(r,\mu_{fused},\sigma_{fused})=\frac{1}{\sqrt{2\pi\sigma_{fused}^2}}e^{-\dfrac{(r-\mu_{fused})^2}{2\sigma_{fused}^2}}" title="y_{fuesd}(r,\mu_{fused},\sigma_{fused})=\frac{1}{\sqrt{2\pi\sigma_{fused}^2}}e^{-\dfrac{(r-\mu_{fused})^2}{2\sigma_{fused}^2}}" /></a>
</div>
式中：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{fused}=\frac{\mu_1\sigma_2^2&plus;\mu_2\sigma_1^2}{\sigma_1^2&plus;\sigma_2^2}=\mu_1&plus;\frac{\sigma_1^2(\mu_2-\mu_1)}{\sigma_1^2&plus;\sigma_2^2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{fused}=\frac{\mu_1\sigma_2^2&plus;\mu_2\sigma_1^2}{\sigma_1^2&plus;\sigma_2^2}=\mu_1&plus;\frac{\sigma_1^2(\mu_2-\mu_1)}{\sigma_1^2&plus;\sigma_2^2}" title="\mu_{fused}=\frac{\mu_1\sigma_2^2+\mu_2\sigma_1^2}{\sigma_1^2+\sigma_2^2}=\mu_1+\frac{\sigma_1^2(\mu_2-\mu_1)}{\sigma_1^2+\sigma_2^2}" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_{fused}^2=\frac{\sigma_1^2\sigma_2^2}{\sigma_1^2&plus;\sigma_2^2}=\sigma_1^2-\frac{\sigma_1^4}{\sigma_1^2&plus;\sigma_2^2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_{fused}^2=\frac{\sigma_1^2\sigma_2^2}{\sigma_1^2&plus;\sigma_2^2}=\sigma_1^2-\frac{\sigma_1^4}{\sigma_1^2&plus;\sigma_2^2}" title="\sigma_{fused}^2=\frac{\sigma_1^2\sigma_2^2}{\sigma_1^2+\sigma_2^2}=\sigma_1^2-\frac{\sigma_1^4}{\sigma_1^2+\sigma_2^2}" /></a>
</div>

如果测量值是无线电信号传播时间，则还需要把单位统一，增加光速系数 <a href="http://www.codecogs.com/eqnedit.php?latex=c" target="_blank"><img src="http://latex.codecogs.com/gif.latex?c" title="c" /></a>：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=y_1(s;\mu_1,\sigma_1,c)\triangleq\frac1{\sqrt{2\pi(\dfrac{\sigma_1}{c})^2}}e^{-\dfrac{(s-\frac{\mu_1}{c})^2}{2(\frac{\sigma_1}{c})^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_1(s;\mu_1,\sigma_1,c)\triangleq\frac1{\sqrt{2\pi(\dfrac{\sigma_1}{c})^2}}e^{-\dfrac{(s-\frac{\mu_1}{c})^2}{2(\frac{\sigma_1}{c})^2}}" title="y_1(s;\mu_1,\sigma_1,c)\triangleq\frac1{\sqrt{2\pi(\dfrac{\sigma_1}{c})^2}}e^{-\dfrac{(s-\frac{\mu_1}{c})^2}{2(\frac{\sigma_1}{c})^2}}" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=y_2(s;\mu_2,\sigma_2,c)\triangleq\dfrac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(s-\mu_2)^2}{2\sigma_2^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_2(s;\mu_2,\sigma_2,c)\triangleq\dfrac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(s-\mu_2)^2}{2\sigma_2^2}}" title="y_2(s;\mu_2,\sigma_2,c)\triangleq\dfrac1{\sqrt{2\pi\sigma_2^2}}e^{-\dfrac{(s-\mu_2)^2}{2\sigma_2^2}}" /></a>
</div>
根据之前的推导：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\mu_{fused}}{c}=\frac{\mu_1}{c}&plus;\frac{(\frac{\sigma_1}{c})^2(\mu_2-\frac{\mu_1}{c})}{(\frac{\sigma}{c})^2&plus;\sigma_2^2}\\&space;\Rightarrow\mu_{fused}=\mu_1&plus;\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\right)\cdot(\mu_2-\frac{\mu_1}{c})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\mu_{fused}}{c}=\frac{\mu_1}{c}&plus;\frac{(\frac{\sigma_1}{c})^2(\mu_2-\frac{\mu_1}{c})}{(\frac{\sigma}{c})^2&plus;\sigma_2^2}\\&space;\Rightarrow\mu_{fused}=\mu_1&plus;\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\right)\cdot(\mu_2-\frac{\mu_1}{c})" title="\frac{\mu_{fused}}{c}=\frac{\mu_1}{c}+\frac{(\frac{\sigma_1}{c})^2(\mu_2-\frac{\mu_1}{c})}{(\frac{\sigma}{c})^2+\sigma_2^2}\\ \Rightarrow\mu_{fused}=\mu_1+\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2+\sigma_2^2}\right)\cdot(\mu_2-\frac{\mu_1}{c})" /></a>
</div>
带入 <a href="https://www.codecogs.com/eqnedit.php?latex=H=1/c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?H=1/c" title="H=1/c" /></a> 和 <a href="https://www.codecogs.com/eqnedit.php?latex=K=(H\sigma_1^2)/(H^2\sigma_1^2&plus;\sigma_2^2)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K=(H\sigma_1^2)/(H^2\sigma_1^2&plus;\sigma_2^2)" title="K=(H\sigma_1^2)/(H^2\sigma_1^2+\sigma_2^2)" /></a> 得到：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{fused}=\mu_1&plus;K\cdot(\mu_2-H\mu_1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{fused}=\mu_1&plus;K\cdot(\mu_2-H\mu_1)" title="\mu_{fused}=\mu_1+K\cdot(\mu_2-H\mu_1)" /></a>
</div>
同理：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\sigma_{fused}^2}{c^2}=(\frac{\sigma_1^2}{c})-\frac{(\frac{\sigma_1}{c})^4}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\\&space;\Rightarrow\sigma_{fused}^2=\sigma_1^2-\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\right)\frac{\sigma_1^2}{c}\\&space;=\sigma_1^2-KH\sigma_1^2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\sigma_{fused}^2}{c^2}=(\frac{\sigma_1^2}{c})-\frac{(\frac{\sigma_1}{c})^4}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\\&space;\Rightarrow\sigma_{fused}^2=\sigma_1^2-\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2&plus;\sigma_2^2}\right)\frac{\sigma_1^2}{c}\\&space;=\sigma_1^2-KH\sigma_1^2" title="\frac{\sigma_{fused}^2}{c^2}=(\frac{\sigma_1^2}{c})-\frac{(\frac{\sigma_1}{c})^4}{(\frac{\sigma_1}{c})^2+\sigma_2^2}\\ \Rightarrow\sigma_{fused}^2=\sigma_1^2-\left(\frac{\frac{\sigma_1^2}{c}}{(\frac{\sigma_1}{c})^2+\sigma_2^2}\right)\frac{\sigma_1^2}{c}\\ =\sigma_1^2-KH\sigma_1^2" /></a>
</div>
推导最终结论和卡尔曼方程一致：
<div align=center><p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{fused}=\mu_1&plus;K\cdot(\mu_2-H\mu_1)\rightarrow\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{fused}=\mu_1&plus;K\cdot(\mu_2-H\mu_1)\rightarrow\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}&plus;\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" title="\mu_{fused}=\mu_1+K\cdot(\mu_2-H\mu_1)\rightarrow\hat{\boldsymbol{x}}_{t|t}=\hat{\boldsymbol{x}}_{t|t-1}+\boldsymbol{K}_t(\boldsymbol{z}_t-\boldsymbol{H}_t\hat{\boldsymbol{x}}_{t|t-1})" /></a>
<p/>
<a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_{fused}^2=\sigma_1^2-KH\sigma_1^2\rightarrow\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_{fused}^2=\sigma_1^2-KH\sigma_1^2\rightarrow\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" title="\sigma_{fused}^2=\sigma_1^2-KH\sigma_1^2\rightarrow\boldsymbol{P}_{t|t}=\boldsymbol{P}_{t|t-1}-{\boldsymbol{K}}_{t}{\boldsymbol{H}}_t\boldsymbol{P}_{t|t-1}" /></a>
</div>

### 2.3 迭代
预测值正太分布和测量值正态分布相乘得到新的正太分布，作为下次预测值正态分布。通过不断迭代，逐渐向真实值收敛。

## 3.实现
详细代码见[notebook](Kalman_Filter.ipynb)。

### 3.1 初始化
假设火车匀速运动，初始位置、速度、标准差如下，不考虑质量、推力等因素。且预测值和测量值单位相同。

|<a href="https://www.codecogs.com/eqnedit.php?latex=x_0$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x_0$" title="x_0$" /></a>|<a href="https://www.codecogs.com/eqnedit.php?latex=\dot{x}_0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\dot{x}_0" title="\dot{x}_0" /></a>|<a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_1" title="\sigma_1" /></a>|<a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_2" title="\sigma_2" /></a>|
|:--:|:--:|:--:|:--:|
|0m|1m/s|0.1|0.2|

预测初始值和最优估计初始值是10。

### 3.2 结果
从图中可以看出，即使初始值偏差较大时，经过迭代，系统仍可以收敛到真实值，且最优估计比测量值和预测值更精确。

![图6][6]

### 3.3 比较
系统标准差 <a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_1" title="\sigma_1" /></a>  和 <a href="https://www.codecogs.com/eqnedit.php?latex=\sigma_2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sigma_2" title="\sigma_2" /></a> 代表了预测模型和测量模型的可信度。提高测量模型的可信度，系统更快收敛：

![图7][7]

系统的初始值也很重要，也会影响迭代的速度。

## 4.QA
### 4.1 如何确定标准差？
一般根据传感器特性，通过测量得到。

  [1]: https://s1.ax1x.com/2018/08/26/PbtiDA.jpg
  [2]: https://s1.ax1x.com/2018/08/26/Pbtpge.jpg
  [3]: https://s1.ax1x.com/2018/08/26/Pbt9jH.jpg
  [4]: https://s1.ax1x.com/2018/08/26/PbtFHI.jpg
  [5]: https://s1.ax1x.com/2018/08/26/PbtPud.jpg
  [6]: http://wx4.sinaimg.cn/mw690/0060lm7Tly1fuo3v2ej0lj30rs0dw75k.jpg
  [7]: http://wx1.sinaimg.cn/mw690/0060lm7Tly1fuo3vromzwj30rs0dwgmr.jpg
