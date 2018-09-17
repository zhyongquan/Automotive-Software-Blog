# 粒子滤波(particle filter)
参考文章[《An introduction to particle filters》](https://www.it.uu.se/katalog/andsv164/Teaching/Material/PF_Intro_2014_AndreasSvensson.pdf)。

基本原理：随机选取预测域的 $N$ 个点，称为粒子。以此计算出预测值，并算出在测量域的概率，即权重，加权平均就是最优估计。之后按权重比例，重采样，进行下次迭代。

使用范围：适用于非高斯分布、非线性系统，当无法知道状态空间分布时。

此算法存在的问题是：粒子数量越多，计算越精确，但计算量也会增加，且随着迭代，有些粒子权重变得很小，导致粒子枯竭。

|滤波算法|适用范围|优点|缺点|
|:--:|:--:|:--:|:--:|
|卡尔曼滤波|线性高斯分布|计算量小||
|粒子滤波|非线性，非高斯分布||计算量大|

# 1 状态空间模型(state space model)
线性高斯状态空间模型：

$$
x_{t+1}=Ax_t+Bu_t+w_t\\
y_t=Cx_t+Du_t+e_t
$$

式中 $w_t$ 和 $e_t$  是预测噪声（或称为过程噪声）和测量噪声的高斯分布，且$\Bbb{E}[w_tw_t^T]=Q$，$\Bbb{E}[e_te_t^T]=R$。

更通用的状态空间模型：

$$
x_{t+1}\sim{f}(x_{t+1}|x_t,u_t)\\
y_t\sim{g}(y_t|x_t,u_t)
$$

## 2 滤波-寻找$p(x_t|y_1:t)$
线性高斯问题：

- 卡尔曼滤波(kalman filter)

非线性问题：

- 扩展卡尔曼滤波(extend kalman filter)，无损卡尔曼滤波(unscented kalman filter)
- 粒子滤波

## 3 概念
生成一系列 $x_t$ 的假设，保留概率最大的，传播到 $x_{t+1}$。保留最大概率 $x_{t+1}$，传播到 $x_{t+2}$，依此类推。

## 4 算法
### 4.1 初始化 
在预测值空间内随机选取 $N$ 个粒子 $x_1^i$，并分配权重 $w_i$： $x_1^i\sim{p}(x_1)$， $w_i=\frac1{N}$，式中 $i=1,...,N$。

![此处输入图片的描述][1]

### 4.2 迭代
按照以下顺序，循环执行，$t=1,...,T$。
 
1.估算每个粒子的权重 $w_t^i=g(y_t|x_t^i,u_t)$。下图黑色圆点面积越大，权重越大。

![此处输入图片的描述][2]

2.计算估计值

加权求平均。

3.从 $\{x_t^i,w_t^i\}_{i=1}^N$ 重采样 $\{x_t^i\}_{i=1}^N$。下图红色圆点是新粒子。

![此处输入图片的描述][3]

4.通过采样 $f(\cdot|x_{t-1}^i,u_{t-1})$ 传播 $x_t^i$。

![此处输入图片的描述][4]

### 4.2.1 代码
用Matlab代码描述如下

```matlab
X(:,1) = random(i_dist,N,1);
w(:.1) = ones(N,1)/N;
for t =1:T
   w(:,t) = pdf(m_dist,y(t)-g(x(:,t));
   w(:,t) = w(:,t)/sum(w(:,t));
   Resample x(:,t)
   x(:,t+1) = f(x(:,t),u(t))+random(t_dist,N,1);
end
```

### 4.2.2 结果

在 $t=5$ 时刻：

![此处输入图片的描述][5]

最终输出：

![此处输入图片的描述][6]

### 4.3 重采样(resampling)
- 使用 $N$ 个红色相同大小的点表示 $N$ 个不同大小的黑色点。黑色表示上次计算的权重，红色表示下次采样的点。从图中可以看出，当权重越高时，下次被选中的概率更高。

![此处输入图片的描述][7]

- 可以看作是从类别分布中采样。
- 避免粒子枯竭（particle depletion ，很多权重是0的粒子）。
- Matlab代码如下：

```matlab
v = rand(N,1);
wc = cumsum(w(:,t);
[ ,ind1] = sort([v:wc]);
ind = find(ind1<=N)-(0:N-1)';
x(:,t)=x(ind,t);
w(:,t)=ones(N,1)./N;
```

- 90年代研究的重点是使粒子滤波更实用。
- 出现了很多不同属性和效率的技术（上述的Matlab代码只是其中之一）。
- 计算复杂度。没必要每次迭代都进行重采样。可以使用“消耗测量”的方法，当超过阈值时，才需要重采样。
- 有时为了数学计算原因，使用对数权重。

## 4.4 权重

通过前期的测量，可以得到一个pdf（probability density function，概率密度函数），用于权重计算。权重计算：

$$
w_t^i\varpropto{w}_{t-1}^i\frac{p(y_t|x_t^i)p(x_k^i|x_{t-1}^i)}{q(x_t^i|x_{t-1}^i,y_i)}
$$

更多可以参考[小木虫](http://muchong.com/html/201303/5624587.html)。

## 5 计算复杂度
理论上，粒子滤波计算复杂度是  $\mathcal{O}(NTn_x^2)$，其中 $N$ 是粒子数量，$T$ 是迭代次数， $n_x$ 是状态数量。而卡尔曼滤波是 $\mathcal{O}(Tn_x^3)$。

可能的瓶颈：

- 重采样
- 似然估算（权重计算）
- 从 $f$ 中为演算采样（提示：使用建议分布！）

## 6 软件
软件包有：

- Python：pyParticleEst
- Matlab：PFToolbox，PFLib
- C++：Particle++

## 7 术语

- 自举粒子滤波(boostrap particle filter) $\approx$ 标准粒子滤波。
- 序列蒙特卡罗(sequential monte carlo, SMC) $\approx$ 粒子滤波。

## 8 汇总
当粒子数量达到无穷大 $N=\infty$，粒子滤波最准确。构建一个方程 $g(x_t)$ ,用它评价 $x_t$ 最有估计 $\hat{g}(x_t)$。

$$
\Bbb{E}\left[\hat{g}(x_t)-\Bbb{E}[g(x_t)]\right]^2\leq\frac{p_t\|g(x_t)\|_{sup}}{N}
$$

如果系统以指数的速度遗忘（例如线性系统），还需要一些额外的弱假设，$p_t=p<\infty$，例如：

$$
\Bbb{E}\left[\hat{g}(x_t)-\Bbb{E}[g(x_t)]\right]^2\leq\frac{C}{N}
$$

## 9 扩展

- 平滑：寻找 $p(x_t|y_{1:T})$（间距平滑）或 $p(x_{1:t}|y_{1:T})$（节点平滑）替代 $p(x_t:y_{1:T})$（滤波）：离线数据（$y_{1:T}$） 必须存在；增加了计算负载。
- 如果 $f(x_{t+1}|x_t,u_t)$ 不适用，可以使用建议分布。实际上，存在最优的建议分布（关于减少方差）。
-  Rao-Blackwellization用于线性/非线性混合模型。
-  系统识别：PMCMC，SMC2。

## 10 例子
状态方程如下：

$$
x_k=\frac{x_{k-1}}{2}+\frac{25x_{k-1}}{1+x_{k-1}^2}+8\cos(1.2(k-1))+v_k
$$

$$
y_k=\frac{x_k^2}{20}+n_k
$$


## 11 QA
### 11.1 什么是线性高斯模型？
预测后仍是高斯分布，且概率不变。
### 11.2 其他文章
- [《Particle Filter Tutorial 粒子滤波：从推导到应用》](https://blog.csdn.net/heyijia0327/article/details/40899819)



  [1]: https://s1.ax1x.com/2018/08/28/PL4f5q.png
  [2]: https://s1.ax1x.com/2018/08/28/PL4XI1.png
  [3]: https://s1.ax1x.com/2018/08/28/PL5Cse.png
  [4]: https://s1.ax1x.com/2018/08/28/PL5uQS.png
  [5]: https://s1.ax1x.com/2018/08/28/PL5sF1.png
  [6]: https://s1.ax1x.com/2018/08/28/PLIgNn.png
  [7]: https://s1.ax1x.com/2018/08/28/PLIy7j.png
