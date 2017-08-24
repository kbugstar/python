#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/28 0028 11:50
# @Author  : Aries
# @Site    : 
# @File    : Price_pred.py
# @Software: PyCharm
'''
四、预测拍卖最终成交价格

由于在价格的分布是在一个连续的区间上，因此这与预测拍卖是否会成功是不同的，预测价格是一个回归预测，而判断拍卖是否会成功是一个分类任务。

同样根据机器学习算法使用图谱，在这里我们采取SGDRegressor，其他使用情况与预测拍卖是否成功时差不多，创建Price_pred.py, 代码如下：

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
import random
from sklearn.preprocessing import MinMaxScaler

# prepare data
test_subset = pd.read_csv('raw/TestSubset.csv')
train_subset = pd.read_csv('raw/TrainingSubset.csv')

# 训练集
train = train_subset.drop(['EbayID','Price','SellerName'],axis=1)
train_target = train_subset['Price']

scaler = MinMaxScaler()
train = scaler.fit_transform(train)
n_trainSamples, n_features = train.shape

# ploting example from scikit-learn
def plot_learning(clf,title):

    plt.figure()
    validationScore = []
    trainScore = []
    mini_batch = 500
    # define the shuffle index
    ind = list(range(n_trainSamples))
    random.shuffle(ind)

    for idx in range(int(np.ceil(n_trainSamples / mini_batch))):
        x_batch = train[ind[idx * mini_batch: min((idx + 1) * mini_batch, n_trainSamples)]]
        y_batch = train_target[ind[idx * mini_batch: min((idx + 1) * mini_batch, n_trainSamples)]]

        if idx > 0:
            validationScore.append(clf.score(x_batch, y_batch))
        clf.partial_fit(x_batch, y_batch)
        if idx > 0:
            trainScore.append(clf.score(x_batch, y_batch))

    plt.plot(trainScore, label="train score")
    plt.plot(validationScore, label="validation socre")
    plt.xlabel("Mini_batch")
    plt.ylabel("Score")
    plt.legend(loc='best')
    plt.title(title)

sgd_regresor = SGDRegressor(penalty='l2',alpha=0.001)
plot_learning(sgd_regresor,"SGDRegressor")

# 准备测试集查看测试情况
test = test_subset.drop(['EbayID','Price','SellerName'],axis=1)
test = scaler.fit_transform(test)
test_target = test_subset['Price']

print("SGD regressor prediction result on testing data: %.3f" % sgd_regresor.score(test,test_target))

plt.show()

'''
测试结果： SGD regressor prediction result on testing data: 0.933

由于SGDRegressor的回归效果还不错，因此我们没有在进一步的选择其他的模型进行尝试，有兴趣的同学可以在这方面在多改进参数，或者尝试其他的方法看预测效果如何。



五、总结

本次课程我们学习了如何使用scikit-learn进行数据分析，其实在数据分析过程中，运用到机器学习的算法进行模型训练并不是最主要的，很多时候是如何在前期进行数据预处理。
这过程中包括数据的筛选，和特征工程等，在进行一项数据挖掘任务时，我们可能会花更多的时间在数据预处理和特征工程上，但是这些准备工作做好后，可使得我们之后的模型训练过程事半功倍。
在scikit-learn官方文档中也有许多数据库和算法实现例子，并且有很多数据可视化的例子，运用这些例子也能帮助我们快速入门机器学习这个领域。

参考资料：
http://scikit-learn.org/stable/auto_examples/manifold/plot_lle_digits.html#sphx-glr-auto-examples-manifold-plot-lle-digits-py
https://www.kancloud.cn/digest/machine-learning-dm
'''