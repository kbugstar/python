#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/24 0024 14:35:15
# @Author  : Aries
# @Site    : 
# @ File    : practice_KMeans.py
# @Software: PyCharm Community Edition
'''
算法描述：
    1、选择k个聚类的初始中心
    2、在第n次迭代中，对任意一个样本点，求其到k个聚类中心的距离，将该样本点归类到距离最小的中心所在的聚类
    3、利用均值等方法更新各类的中心值
    4、对所有的k个聚类中心，如果利用2、3步的迭代更新后，达到稳定，则迭代结束
优点：
    速度快，简单
缺点：
    最终结果和初始点的选择有关，容易陷入局部最优，需要给定k值
'''
import random

import math
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors


class Cluster(object):
    """
        聚类
    """
    def __init__(self,samples):
        if len(samples) == 0:
            # 如果聚类中无样本点
            raise Exception("错误：一个空的聚类！")
        # 属于该聚类的样本点
        self.samples = samples
        #该聚类中的样本点的维度
        self.n_dim = samples[0].n_dim
        # 判断该聚类中所有样本点的维度是否相同
        for sample in samples:
            if sample.n_dim != self.n_dim:
                raise Exception("错误： 聚类中样本点的维度不一致！")

        # 设置初始化的聚类中心
        self.centroid = self.cal_centroid()

    def __repr__(self):
        """
            输出对象信息
        """
        return str(self.samples)

    def update(self, samples):
        """
            计算之前的聚类中心和更新后聚类中心的距离
        """

        old_centroid = self.centroid
        self.samples = samples
        self.centroid = self.cal_centroid()
        shift = get_distance(old_centroid, self.centroid)
        return shift

    def cal_centroid(self):
        """
           对于一组样本点计算其中心点
        """
        n_samples = len(self.samples)
        # 获取所有样本点的坐标（特征）
        coords = [sample.coords for sample in self.samples]
        unzipped = zip(*coords)
        # 计算每个维度的均值
        centroid_coords = [math.fsum(d_list)/n_samples for d_list in unzipped]

        return Sample(centroid_coords)



class Sample(object):
    """
        样本点类
    """
    def __init__(self,coords):
        self.coords = coords # 样本点包含的坐标
        print(type(coords))
        self.n_dim = len(coords) # 样本点维度
    def __repr__(self):
        """
            输出对象信息
        :return: 
        """
        return str(self.coords)



def get_distance(a,b):
    """
        计算距离
    :return: 返回样本点a、b的欧氏距离 
    参考：https://en.wikipedia.org/wiki/Euclidean_distance#n_dimensions
    """
    if a.n_dim != b.n_dim:
        # 如果样本点维度不同
        return Exception("错误：样本点维度不同，无法计算距离！")
    acc_diff = 0.0
    for i in range(a.n_dim):
        square_diff = pow((a.coords[i]-b.coords[i]),2)
        acc_diff += square_diff
    distance = math.sqrt(acc_diff)
    return distance


def gen_random_sample(n_dim,lower,upper):
    """
        生成随机样本
    :param n_dim: 
    :param lower: 
    :param upper: 
    :return: 
    """
    sample = Sample(random.uniform(lower,upper) for _ in range(n_dim))
    return sample


def kmeans(samples,k,cutoff):
    """
        kmeans函数
    :param samples: 
    :param k: 
    :param cutoff: 
    :return: 
    """
    # 随机选k个样本点作为初始聚类中心
    init_samples = random.sample(samples,k)
    # 创建k个聚类，聚类的中心分别为随机初始的样本点
    clusters = [Cluster([sample]) for sample in init_samples] # 122分钟

    # 迭代循环直到聚类划分稳定
    n_loop = 0
    while True:
        # 初始化一组控列表on个语存储每个聚类内的样本点
        lists = [[] for _ in clusters]
        # 开始迭代
        n_loop += 1
        # 遍历样本集中的每个样本
        for sample in samples:
            # 计算样本点sample和第一个聚类中心的距离
            samllest_distance = get_distance(sample,clusters[0].centroid)
            # 初始化术语聚类 0
            cluster_index = 0

            #计算和其他聚类中心的距离
            for i in range(k - 1):
                # 计算样本点sample和聚类中心的距离
                distance = get_distance(sample,clusters[i+1].centroid)
                # 如果存在更小的距离，更新距离
                if distance < samllest_distance:
                    samllest_distance = distance
                    cluster_index = i + 1
            # 找到最近的聚类中心，更新所属聚类
            lists[cluster_index].append(sample)
        # 初始化最大移动距离
        biggest_shift = 0.0
        # 计算本次迭代中，聚类中心移动的距离
        for i in range(k):
            shift = clusters[i].update(lists[i])
            # 计算最大移动距离
            biggest_shift = max(biggest_shift,shift)
        # 如果聚类中心移动的距离小于收敛阈值，即：聚类稳定
        if biggest_shift < cutoff:
            print("第{}次迭代后，聚类稳定".format(n_loop))
            break
    # 返回聚类结果
    return clusters







def run_man():
    """
        主函数
    :return: 
    """
    # 样本个数
    n_samples = 1000
    # 特征个数（特征维度）
    n_feat = 2
    # 特征数值范围
    lower = 0
    upper = 200
    # 聚类个数
    n_cluster = 5
    # 生成随机样本
    samples = [gen_random_sample(n_feat,lower,upper) for _ in range(n_samples)]
    # 收敛阈值
    cutoff = 0.2

    clusters = kmeans(samples,n_cluster,cutoff)

    # 输出结果
    for i,c in enumerate(clusters):
        for sample in c.samples:
            print('聚类--{}，样本点--{}'.format(i,sample))

    # 可视化结果
    plt.subplot()
    color_names = list(mcolors.cnames)
    for i,c in enumerate(clusters):
        x = []
        y = []
        random.choice
        color = [color_names[i]] * len(c.samples)
        for sample in c.samples:
            x.append(sample.coords[0])
            y.append(sample.coords[1])
        plt.scatter(x,y,c=color)
    plt.show()



if __name__ == '__main__':
    run_man()