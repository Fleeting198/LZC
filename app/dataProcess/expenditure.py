# coding=utf-8
#
# 02-11 Built by 陈骏杰
#   输入 原始数据：日期和对应消费增量，日期模式。
#   输出 符合对应模式的日期和余额（初始量0 + 增量）
#   模式：天0，周1，月2，季3，年4。

def main(mdates, mamounts, mode_date):

    if mode_date == 0:
        # 日期降维
        mdates = map(lambda d: d.date(), mdates)

        i = 1  # 切片跳过0号，从1号开始
        while i < len(mdates):    # 检测当前序号是否存在以全部遍历
            # 取当前和前一个记录的日期（天）
            # 若日期为同一天，合并日期和对应增量
            if mdates[i] == mdates[i - 1]:
                mdates = mdates[:i-1] + mdates[i:]  # 日期去除
                mamounts[i] += mamounts[i-1]  # 增量合并
                mamounts = mamounts[:i-1] + mamounts[i:]  # 增量去除
            i += 1

        # 计算余额变化
        for i in range(len(mamounts))[1:]:
            mamounts[i] += mamounts[i - 1]

    return mdates, mamounts