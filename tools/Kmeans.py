# coding:utf-8

from numpy import array, sqrt, zeros, random, inf, mean

"""
kmeans算法和bikmeans二分聚类算法的具体实现
实际调用的方法是kmeansProcess，将二分聚类的结果包装成簇心和标签队列返回
"""


def loadData():
    from sklearn import datasets
    iris = datasets.load_iris()
    x = iris.data
    data = x[:, [1, 3]]
    data = array(data)
    return data


def euclidDistance(p1, p2):
    """
    欧几里得距离
    :param p1: 样本点
    :param p2: 样本点
    :return: 欧几里得距离
    """
    return sqrt(sum((p1 - p2) ** 2))


def rand_center(data, k):
    """
    生成k个随机点作为簇心
    :param data: np.ndarry类型的样本点数据
    :param k: 指定簇心数
    :return centroids: 簇心列表
    """
    dim = data.shape[1]  # n维度
    centroids = zeros((k, dim))  # k个簇心，n个维度
    for i in range(dim):  # 遍历维度
        # 计算该维度最大值和最小值
        dmax, dmin = max(data[:, i]), min(data[:, i])
        # 簇心随机为最大值和最小值之间
        centroids[:, i] = dmin + (dmax - dmin) * random.rand(k)
    return centroids


def kmeans(data, k=2):
    """
    原始的kmeans算法
    :param data: np.ndarry类型的样本点数据
    :param k: 指定簇心数
    :return: centroids: 簇心列表
    :return: dataState: 样本点信息: (所属簇心号，距该簇心距离的平方)
    :return: SSE: 误差平方和
    """
    numSamples = data.shape[0]  # 输入矩阵的一维长度，即样本点个数
    centroids = rand_center(data, k)  # 随机生成k个初始簇心
    dataState = zeros((numSamples, 2))  # 初始化样本点信息矩阵，填0

    changed = True  # 样本点所属簇心是否发生变化
    while changed:
        changed = False
        # 遍历样本点
        for i in range(numSamples):
            minDist = inf
            minIndex = 0

            # 遍历簇心,找到距离样本i最近的簇心
            for j in range(k):
                dist = euclidDistance(data[i], centroids[j])
                if dist < minDist:
                    minDist = dist
                    minIndex = j

            # 如果找到的最近簇心不是原来簇心,设置标记继续循环
            if dataState[i, 0] != minIndex:
                changed = True
                dataState[i, 0] = minIndex
                dataState[i, 1] = minDist ** 2

        # 将各簇心重新定位到各簇的平均中心点
        for i in range(k):
            centroids[i] = mean(data[dataState[:, 0] == i], axis=0)

    SSE = sum(dataState[:, 1])  # 计算误差平方和
    return centroids, dataState, SSE


def biKmeans(data, k):
    """
    二分kmeans
    :param data: np.ndarry类型的样本点数据
    :param k: 最终要达到的簇心数
    :return: centroids: 簇心列表
    :return: dataState: 样本点信息: (所属簇心号，距该簇心距离的平方)
    :return: SSE: 误差平方和
    """
    numSamples = data.shape[0]  # 样本点个数
    dataState = zeros((numSamples, 2))  # 初始化样本点信息矩阵，填0
    centroids = [mean(data, axis=0)]  # 初始唯一簇心

    # 遍历样本点，计算到初始簇心的距离
    for i in range(numSamples):
        dataState[i, 1] = euclidDistance(centroids[0], data[i]) ** 2

    # 开始二分循环,直到簇心数量达到目标数量
    while len(centroids) < k:
        # 遍历簇心，找到最优的二分簇心(SSE最大)
        maxSSE = -1
        best_centToSplit = 0
        for i in range(len(centroids)):
            SSE = mean(data[dataState[:, 0] == i, 1], axis=0)
            if SSE > maxSSE:
                maxSSE = SSE
                best_centToSplit = i

        numSplitTest = 5  # 尝试多次二分的次数
        minSSE = inf
        best_newCentroids = []
        best_dataState = []
        dataToSplit = data[dataState[:, 0] == best_centToSplit, :]  # 要二分的簇的样本点矩阵
        # 开始尝试多次二分
        for i in range(numSplitTest):
            # 调用基本聚类算法，簇心数2
            splitCents, splitDataState, splitSSE = kmeans(dataToSplit, 2)

            # 选择两个新簇的SSE之和最小的一次
            if splitSSE < minSSE:
                minSSE = splitSSE
                best_newCentroids = splitCents.copy()
                best_dataState = splitDataState.copy()

        # 加上新簇心信息
        # 二分的簇心换成两个新簇心中的第一个
        centroids[best_centToSplit] = best_newCentroids[0, :]
        # 新样本点中指向第一个新簇心的指针换成簇心集中的序号
        best_dataState[best_dataState[:, 0] == 0, 0] = best_centToSplit

        # 第二个新簇心用添加的方式
        centroids.append(best_newCentroids[1, :])
        # 第二簇心的样本集指向新的序号
        best_dataState[best_dataState[:, 0] == 1, 0] = len(centroids) - 1

        dataState[dataState[:, 0] == best_centToSplit, :] = best_dataState

    SSE = sum(dataState[:, 1])
    return centroids, dataState, SSE


# 二维matplotlib散点图展示
def showCluster(dataSet, k, centroids, labels):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']

    # draw all samples
    for i in range(numSamples):
        markIndex = int(labels[i])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize=12)

    plt.show()


def kmeansProcess(dataSet, k):
    """返回簇心和所属簇标签列表，代码中实际调用的是这个"""
    dataSet = array(dataSet)
    centroids, dataState, SSE = biKmeans(dataSet, k)

    # 计数每个簇心的样本点数量
    cntPtsOfCentroids = [0] * len(centroids)
    for e in dataState:
        cntPtsOfCentroids[int(e[0])] += 1

    # 将样本点数量0的簇心的横坐标标记为-1，在GetJson_ConAbility判断跳过
    for i in range(len(centroids)):
        if not cntPtsOfCentroids[i]:
            centroids[i][0] = -1

    labels = dataState[:, 0]

    return centroids, labels


if __name__ == "__main__":
    data = loadData()
    k = 4
    centroids, dataState, SSE = biKmeans(data, k)
    print(centroids)
    print(dataState)
    labels = dataState[:, 0]
    showCluster(data, k, centroids, labels)
