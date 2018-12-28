# 标定数据格式介绍-CVX(.CSV)

![][1]

**欢迎关注《汽车软件技术》公众号，回复关键字获取资料。**

## 1. CVX介绍

CVX（Calibration Values Exchange Format）是一种标定数据文件格式，文件后缀是“.csv”，所以一般也统称为csv。

CVX在INCA、CANape等标定软件中都有包含，比如INCA CDM中：

![][3]

## 2. 数据格式

CVX有标准的文档说明（回复“**CVX文档**“获取），一般用Excel打开就可以查看，易用性和可读性也是它广泛应用的原因。本文分别介绍标量、曲线、图表、坐标轴的数据格式，从中可以解读更多内容。

注意：以下都使用英文逗号`,`分隔符，小数位使用英文句号`.`表示。

### 2.1 标量 VALUE

VALUE占据2行，如下所示，标定量KaEGRC_Air_Temperature_Threshhold的值是1.57。

```
,KaEGRC_Air_Temperature_Threshhold
VALUE,,1.57
```

### 2.2 曲线 CURVE

CURVE占据3行。

```
,KvEGRC_Overtemp_Time
CURVE
,,4.78,6,89.12
```

### 2.3 图表 MAP

MAP占据多行。

```
,KaEGRC_Base_Position_Lo_Oct
MAP

,,4.5,3,9,4.89
,,5.345,2.89,6.89
```

### 2.4 坐标轴 AXIS

在CVX文件中，与DCM不同，AXIS是独立存在的，通过如下的形式定义，这表示了KpmGroupAxis_3_26的坐标轴。

```
,KpmGroupAxis_3_26
AXIS_PTS,,600,800,1000
```

## 3. 数据分析

CVX提供了简洁的描述方式，相比较a2l+hex，更容易处理。使用python开发了**pycvx**库，用于标定数据分析。（回复“**CVX代码**”获取）

- 面向对象的程序结构：根据对象属性，创建类结构。

- 标定数据的可视化：使用matplotlib绘图。

```python
from pycvx import cvxinfo

cvx = cvxinfo()
cvx.read("../data/DEMO.CSV")
# find functions:2, calibrations:5, axises:0

DEMO_CURVE = cvx.calibrations["DEMO_CURVE"]
print(DEMO_CURVE)
# name=DEMO_CURVE, description=
# line_start=30, line_end=33
# type=CURVE, unit=
# value=
# [0.30078125, 0.3984375, 0.5, 0.59765625, 0.69921875, 0.80078125, 0.8984375]
# axis x
# name=, description=
# line_start=38, line_end=39
# type=X_AXIS_PTS, unit=revs
# value=
# [120.0, 200.0, 320.0, 400.0, 520.0, 600.0, 720.0]

DEMO_MAP_2 = cvx.getcvxobject("calibration", "DEMO_MAP_2")
DEMO_MAP_2.show()
```

![][2]


[1]: https://s1.ax1x.com/2018/12/27/F240DU.jpg
[2]: https://s1.ax1x.com/2018/12/27/F24BbF.png
[3]: https://s1.ax1x.com/2018/12/28/FWn3H1.png