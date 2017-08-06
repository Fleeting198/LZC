# coding: utf-8

def get_single(transactionList):
    """
    统计长度1的项集列表出现次数
    :param transactionList: 事务列表，元素是frozenset
    :param minSuppCount: 支持计数阈值
    :return relationshipDict: 字典，键：长度1项集，值：出现次数
    """
    # 拍平事务列表，统计每个单独值出现在事务中的次数
    elementList = []
    for t in transactionList:
        for e in t:
            elementList.append(e)

    # 统计元素出现次数
    relationshipDict = {}
    for e in elementList:
        if e in relationshipDict:
            relationshipDict[e] += 1
        else:
            relationshipDict[e] = 1

    # 将字典中的键转为frozenset，同时筛选
    relationshipDict = {frozenset((k,)): v for k, v in relationshipDict.items()}

    return relationshipDict


def get_pairs(transactionList, minSuppCount=1):
    """
    统计长度2的项集列表出现次数
    :param transactionList: 原始事务列表
    :param single_result: 筛选过的长度1项集元素列表
    :param minSuppCount: 支持计数阈值
    :return relationshipDict: 字典，键：长度2项集，值：出现次数
    """
    relationshipDict = {}

    for t in transactionList:
        length = len(t)

        # 双层循环构造长度2项集
        for firstIndex in range(length):
            for secondIndex in range(firstIndex + 1, length):
                key = frozenset((t[firstIndex], t[secondIndex]))

                # 统计组合在原事务列表中出现次数
                if key in relationshipDict:
                    relationshipDict[key] += 1
                else:
                    relationshipDict[key] = 1

    relationshipDict = {frozenset(k): v for k, v in relationshipDict.items() if v >= minSuppCount}

    return relationshipDict


def apriori_to_L2(transactionList):
    """
    生成长度最大为2的频繁项集列表
    注意这里的频繁项集统计的是次数不是频率，频率在Relationship.py中
    :param transactionList: 事务列表
    :return: 长度最大为2的频繁项集列表
    """
    transactionList = [list(set(t)) for t in transactionList]
    single_result = get_single(transactionList)
    pair_result = get_pairs(transactionList)
    finalDict = mergeDicts(single_result, pair_result)

    return finalDict


def mergeDicts(d1, d2):
    for k, v in d2.items():
        if k in d1:
            d1[k] += v
        else:
            d1[k] = v
    return d1


if __name__ == '__main__':
    # dataList = [['HPHTNPPY', 'HPZHAPPY', 'XPPLXPPY'], ['HPHTNPPY', 'HPZHAPPY', 'XPPLXPPY'], ['HPHTNPPY', 'HPQNAPTY']]

    dataList = [[4, 3, 1], [5, 3, 2], [5, 3, 2, 1], [5, 2]]

    # dataList = [['PPLTWPAQ', 'PPNLQPXQ', 'XAANTTQQ', 'XALANTXQ', 'XALAWTXQ', 'XALNTTXQ', 'XALNWTXQ', 'XALPATXQ', 'XALQATXQ',
    #              'XAQLLTPQ', 'XAQQLXPQ', 'XAQZWQXQ', 'XATPNHXQ', 'XATTQXXQ', 'XAXWPTPQ', 'XQWXWPXQ'],
    #             ['XALTNTXQ', 'XAQLLXPQ', 'XATATHXQ', 'XATWQXXQ'],
    #             ['PPLQXPLQ', 'PPPHZPLQ', 'PPPZZPZQ', 'PPTZNPZQ', 'XATNQXXQ', 'XATTTHXQ', 'XLPAHHPQ', 'XLPHPXPQ', 'XLPLHHPQ',
    #              'XLQANTPQ']]

    suppData = apriori_to_L2(dataList)
    for k, v in suppData.items():
        print(k, v)
