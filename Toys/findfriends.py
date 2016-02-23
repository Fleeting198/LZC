import sys, datetime, time, traceback, json
from MysqlClient import MysqlClient, get_data_from_source
from TimeCalculate import TimeCalculate


class FriendMap:
    def __init__(self, tableName, idItem, fixedItem, orderBy, maxRange):
        self.tableName = tableName
        self.searchItem = (idItem, fixedItem, orderBy)
        self.maxRange = maxRange
        self.mc = MysqlClient()
        self.calculate_time()
        self.fixedList = self.get_fixed_list(fixedItem)
    def calculate_time(self):
        print 'Calculating time...'
        self.totalNum = self.mc.query('select count(*) from %s'%self.tableName)[0][0]
        print 'This search will take around %s seconds'%(self.totalNum / 1e6 * 2)
    def get_fixed_list(self, fixedItem):
        try:
            with open('%sList.json'%self.tableName) as f: l = json.loads(f.read())
            print 'Got user specificed fixed item list'
        except:
            l = []
            c = 0
            process = 0
            sys.stdout.write('Creating fixed item list')
            dataSource = self.mc.data_source('select %s from %s'%(fixedItem, self.tableName))
            while 1:
                data = dataSource()
                # show process
                c += 1
                if process < c * 100 / self.totalNum:
                    sys.stdout.write('\r')
                    sys.stdout.flush()
                    process = c * 100 / self.totalNum
                    sys.stdout.write('Creating fixed item list: %s%s'%(process, '%'))
                if data is None: break
                if not data[0] in l: l.append(data[0])
            with open('%sList.json'%self.tableName, 'w') as f: f.write(json.dumps(l))
            print '\nGot list'
        return l
    def calculate(self):
        try:
            nameDict = {}
            process = -1
            for itemId in xrange(len(self.fixedList)):
                # idItem, orderBy
                if process < itemId * 100 / len(self.fixedList):
                    process = itemId * 100 / len(self.fixedList)
                    sys.stdout.write('\r')
                    sys.stdout.flush()
                    sys.stdout.write('Calculating friend map of %s: %s%s'%(self.tableName, process, '%'))
                dataSource = self.mc.data_source('select %s,%s from %s where %s="%s" order by %s'%(
                    self.searchItem[0], self.searchItem[2], self.tableName, self.searchItem[1], self.fixedList[itemId], self.searchItem[2]))
                idListFindingFriends = []
                def add_friend_point(personA, personB):
                    if not nameDict.has_key(personA): nameDict[personA] = {}
                    if not nameDict[personA].has_key(personB): nameDict[personA][personB] = 0
                    nameDict[personA][personB] += 1
                while 1:
                    data = dataSource()
                    if data is None: break
                    idListFindingFriends.append(data)
                    for iff in idListFindingFriends[:-1]:
                        if data[1] - iff[1] <= datetime.timedelta(0, self.maxRange):
                            add_friend_point(data[0], iff[0])
                            add_friend_point(iff[0], data[0])
                        else:
                            idListFindingFriends = idListFindingFriends[1:]
        except:
            traceback.print_exc()
        print 'Processing Finished'
        return nameDict

if __name__ == '__main__':
    config = {'tableName' : 'acrec', 'idItem' : 'user_id', 'fixedItem' : 'node_des', 'orderBy' : 'ac_datetime', 'maxRange' : 60}
    # config = {'tableName' : 'consumption', 'idItem' : 'user_id', 'fixedItem' : 'dev_id', 'orderBy' : 'con_datetime', 'maxRange' : 60}
    fm = FriendMap(**config)
    @TimeCalculate
    def fn(): return fm.calculate()
    r = fn()
    print 'It took %ss'%r[0]
    with open('%sFriendMap.json'%config['tableName'],'w') as f: f.write(json.dumps(r[1]))
