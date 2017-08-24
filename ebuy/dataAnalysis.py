#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/27 0027 18:06
# @Author  : Aries
# @Site    : 
# @File    : dataAnalysis.py
# @Software: PyCharm
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读入数据
test_set = pd.read_csv('raw/TestSet.csv')
train_set = pd.read_csv('raw/TrainingSet.csv')
test_subset = pd.read_csv('raw/TestSubset.csv')
train_subset = pd.read_csv('raw/TrainingSubset.csv')

# 输出查看 train_set 的数据
# train_set.info()  # 打印结果见 result--1 总共有28列，每一列都有258588条数据，即总共：258588条记录

# print(train_set[:3]) # 打印前三条数据，查看属性值

# 第一列属性EbayID为每条拍卖记录的ID号，与预测拍卖是否成功没有联系，因此在模型训练时将该特征去除。
# QuantitySold属性为1时代表拍卖成功，为0时代表拍卖失败，其中SellerName拍卖卖方的名字与预测拍卖是否成功时没有多大的关系，因此在训练时也将该特征去除
train = train_set.drop(['EbayID','QuantitySold','SellerName'],axis=1)
train_target = train_set['QuantitySold']

# 获取总特征数
_, n_features = train.shape

# 可视化数据，取出一部分特征，量量组成对看数据在这个2维平面上的分布情况：
# isSold： 拍卖成功为1， 拍卖失败为0
df = DataFrame(np.hstack((train,train_target[:, None])), columns=range(n_features) + ["isSold"])
_ = sns.pairplot(df[:50], vars=[2,3,4,10,13], hue="isSold", size=1.5)

# 从第3,9,12,16维特征的散列图及柱状图可看出，这几个维度并不是有很好地区分度，横纵坐标的值分别代表不同维度之间的正负相关性，为了查看数据特征之间的相关性，
# 及不同特征与类别isSold之间的关系，我们可以利用seaborn中的热度图来显示其两两组队之间的相关性
plt.figure(figsize=(10,10))

# 计算数据的相关性矩阵
corr = df.corr()

# 产生遮挡出热度图上三角部分的mask，因为这个热度图为对称矩阵，所以只输出下三角部分即可
mask = np.zeros_like(corr,dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# 产生热度图中对应的变化的颜色
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# 调用seanborn中的heat创建热度图
sns.heatmap(corr, mask=mask, cmap=cmap, vmax = .3,
                square=True, xticklabels=5, yticklabels=2,
                linewidths=.5, cbar_kws={"shrink":.5})

# 将yticks旋转至水平方向，方便查看
plt.yticks(rotation=0)

plt.show()

# 上幅图中，颜色越偏向红色的相关性越大，越偏向蓝色的相关性越小且负相关，白色即两个特征之间没有多大的关联，通过最后一行可看出，不同维的属性与类别isSold之间的关系，
# 其中第3,9,12,16维特征与拍卖是否会成功有很强的 正相关性， 其中3,9,12,16分别对应属性SellerClosePercent，HitCount, SellerSaleAvgPriceRatio和BestOffer，表示当这些属性的值越大时越有可能使拍卖成功，
# 其中第6维特征StartingBid与成功拍卖isSold之间的呈现较大的负相关性，可看出当拍卖投标的底线越高则这项拍卖的成功性就越低。
#通过这幅热度图的第一列我们还可以看出不同特征与价格Price之间的相关性。同样的我们可以根据这些相关性，选出比较有利于我们实现本次课程的第二个任务—— 拍卖价格预测 的特征。


'''
    三、利用数据预测拍卖是否会成功

由于我们的数据量比较大，且特征维度也不是特别少，因此我们一开始做baseline时，就不利用SVM 支持向量机 这些较简单的模型，因为当数据量比较大，且维度较高时，有些简单的机器学习算法就并不是很高效，且可能训练到最后都不收敛并耗时。

根据scikit-learn提供的机器学习算法使用图谱：

们根据图谱推荐先使用SGDClassifier，其全称为Stochastic Gradient Descent 随机梯度下降，通过梯度下降法在训练过程中优化目标函数使得预测值与真实值之间的误差loss最小化。
SGDClassifier每次训练过程没有用到所有的训练样本，而是随机的从训练样本中选取一部分进行训练。而且SGD对特征值的大小比较敏感，而通过上面的数据展示，可以知道在我们的数据集里有数值较大的数据，
如：Category。因此我们可以先用sklearn.preprocessing中提供的StandardScaler对数据进行预处理，使其每个属性的波动幅度不要太大，有助于训练时函数收敛。
'''