#!/usr/bin/env python
# coding: utf-8
from tools.MysqlClient import MysqlClient
from scipy.cluster.vq import kmeans2, vq, whiten
from numpy import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class KmeansOnPovertyIndicator():
    def __init__(self):
        self.mc = MysqlClient()
        self.dataSet = self.getDataSet()

    def getDataSet(self):
        selectCol = ['index_vals', 'index_times', 'index_per']
        sql = "select %s from individual" % (",".join(selectCol))

        dataSet = []
        self.mc.cursor.execute(sql)
        for row in self.mc.cursor:
            if row[0] is None: continue
            dataSet.append(row)

        dataSet = array(dataSet)
        return dataSet

    def kmeans(self, k):
        whitened = whiten(self.dataSet)
        centroid, label = kmeans2(whitened, k)
        self.printResult(centroid, label)

    def printResult(self, centroid, label):
        print '输出聚类结果：'
        for i in xrange(len(centroid)):
            print '聚类%d：' % i
            print centroid[i]
            print '样本个数：%d' % self.dataSet[label == i].shape[0]
            print self.dataSet[label == i]

    def pltDataSet(self):
        x, y, z = self.dataSet[:, 0], self.dataSet[:, 1], self.dataSet[:, 2]
        ax = plt.subplot(projection='3d')  # 创建一个三维的绘图工程

        scale = 2000
        ax.scatter(x[:scale], y[:scale], z[:scale], c='y')

        ax.set_zlabel('intension')  # 坐标轴
        ax.set_ylabel('times')
        ax.set_xlabel('value')
        plt.show()


if __name__ == '__main__':
    pj = KmeansOnPovertyIndicator()
    pj.pltDataSet()
    # pj.kmeans(4)
