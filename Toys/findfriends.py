import sys, datetime, time, traceback, json
from MysqlClient import MysqlClient, get_data_from_source
from TimeCalculate import TimeCalculate

class ProcessRecorder:
    def __init__(self, processName = 'DefaultProcess', begin = 0, total = 0, warningMessage = ''):
        self.processName = processName
        self.warningMessage = warningMessage
        self.process = -1
        self.count = begin
        self.total = total
        self.load_process()
    def load_process(self):
        try:
            with open('%s.json'%self.processName) as f: process_data = json.loads(f.read())
            self.count = process_data['count']
            self.total = process_data['total']
            self.currentPlace = process_data['currentPlace']
        except:
            self.currentPlace = ''
    def store_process(self):
        process_data = {'count': self.count, 'total': self.total, 'currentPlace': self.currentPlace,}
        with open('%s.json'%self.processName, 'w') as f: f.write(json.dumps(process_data))
    def add(self, i = 1):
        self.count += i
        if self.process < self.count * 100 / self.total:
            self.process = self.count * 100 / self.total
            sys.stdout.write('\r')
            sys.stdout.flush()
            sys.stdout.write('%s%s%s'%(self.warningMessage, self.process, '%'))
    def set_current_place(self, currentPlace):
        self.currentPlace = currentPlace

class FriendMap:
    def __init__(self, tableName, idItem, fixedItem, orderBy, maxRange):
        self.tableName = tableName
        self.searchItem = (idItem, fixedItem, orderBy)
        self.maxRange = maxRange
        self.mc = MysqlClient()
        self.prepare_environment()
    def prepare_environment(self):
        print 'Calculating the total work...'
        self.totalNum = self.mc.query('select count(*) from %s'%self.tableName)[0][0]
        self.pr = ProcessRecorder(processName = self.tableName, total = self.totalNum, warning = 'Calculating friend map of %s'%self.tableName)
        if self.pr.count == 0:
            try:
                self.mc.query('select * from %s limit 1'%(self.tableName + 'env'))
            except:
                self.mc.query('create table %s (user_id text, ac_datetime datetime, node_des text)'%(self.tableName + 'env')) 
                print 'Restructure the data storage...'
                s = self.mc.data_source('select * from %s order by node_des desc, ac_datetime desc'%self.tableName)
                count = 0
                while 1:
                    data = s()
                    if data is None: break
                    self.mc.query('insert into %s values("%s", "%s", "%s")'%(self.tableName + 'env', data[0], data[1], data[2]))
                    count += 1
                    if count >= int(1e5):
                        count = 0
                        self.mc._connection.commit()
            self.mc._connection.commit()
    def calculate(self):
        try:
            dataSource = self.mc.data_source('select * from %s limit %s,100'%(self.tableName + 'env', self.pr.count))
            currentPlace = self.pr.currentPlace
            def add_friend_point(personA, personB):
                if not nameDict.has_key(personA): nameDict[personA] = {}
                if not nameDict[personA].has_key(personB): nameDict[personA][personB] = 0
                nameDict[personA][personB] += 1
            while 1:
                data = dataSource()
                if data is None: break
                self.pr.add()
                if currentPlace != data[2]:
                    if currentPlace != '': self.mc.insert_data('%s_friendmap'%self.tableName[:3], **{'%s'%currentPlace: json.dumps(nameDict)})
                    currentPlace = data[2]
                    self.pr.set_current_place(data[2])
                    nameDict = {}
                    idListFindingFriends = []
                idListFindingFriends.append(data)
                for iff in idListFindingFriends[:-1]:
                    if data[1] - iff[1] <= datetime.timedelta(0, self.maxRange):
                        add_friend_point(data[0], iff[0])
                        add_friend_point(iff[0], data[0])
                    else:
                        idListFindingFriends = idListFindingFriends[1:]
        except:
            # store the current process
            print '\nProcess stopped when processing %s'%currentPlace
            traceback.print_exc()
            self.pr.store_process()
        if data is None: self.mc.insert_data('%s_friendmap'%self.tableName[:3], **{'%s'%currentPlace: json.dumps(nameDict)})
        print '\nProcessing Finished'

if __name__ == '__main__':
    config = {'tableName' : 'acrec', 'idItem' : 'user_id', 'fixedItem' : 'node_des', 'orderBy' : 'ac_datetime', 'maxRange' : 60}
    # config = {'tableName' : 'consumption', 'idItem' : 'user_id', 'fixedItem' : 'dev_id', 'orderBy' : 'con_datetime', 'maxRange' : 60}
    fm = FriendMap(**config)
    @TimeCalculate
    def fn(): return fm.calculate()
    r = fn()
    print 'It took %ss'%r[0]
