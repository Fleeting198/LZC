import sys, datetime, time, traceback, json
import MySQLdb
from MysqlClient import MysqlClient, get_data_from_source
from TimeCalculate import TimeCalculate
from ProcessRecorder import ProcessRecorder


class FriendMap:
    def __init__(self, tableName, idItem, fixedItem, orderBy, maxRange):
        self.tableName = tableName
        self.searchItem = (idItem, fixedItem, orderBy)
        self.maxRange = maxRange
        self.mc = MysqlClient()
        self.prepare_environment()

    def prepare_environment(self):
        print 'Calculating the total work...'
        self.totalNum = self.mc.query('select count(*) from %s' % self.tableName)[0][0]
        self.restructTableName = 'restructed_%s' % self.tableName
        self.pr = ProcessRecorder(processName=self.tableName,
                                  localDataSet={'nameDict': {}, 'currentPlace': '', 'idListFindingFriends': []},
                                  total=self.totalNum,
                                  warningMessage='Calculating friend map of %s' % self.tableName)
        try:
            self.mc.restruct_table(self.tableName, [('node_des', ''), ('ac_datetime', '')], self.restructTableName)
        except:
            print 'Storage has been restructed to %s' % self.restructTableName
        self.mc.query('create table if not exists %s_friendmap (k text, v longtext)' % self.tableName[:3])

    def calculate(self):
        try:
            dataSource = self.mc.data_source('select * from %s limit %s,100' % (self.restructTableName, self.pr.count))

            def add_friend_point(personA, personB):
                if not self.pr.localDataSet['nameDict'].has_key(personA):
                    self.pr.localDataSet['nameDict'][personA] = {}
                if not self.pr.localDataSet['nameDict'][personA].has_key(personB):
                    self.pr.localDataSet['nameDict'][personA][personB] = 0
                self.pr.localDataSet['nameDict'][personA][personB] += 1

            while 1:
                data = dataSource()
                if data is None: break
                self.pr.add()
                if self.pr.localDataSet['currentPlace'] != data[2]:
                    if self.pr.localDataSet['currentPlace'] != '' and self.pr.localDataSet['nameDict']:
                        self.mc.insert_data('%s_friendmap' % self.tableName[:3],
                                            items=[self.pr.localDataSet['currentPlace'],
                                                   MySQLdb.escape_string(json.dumps(self.pr.localDataSet['nameDict']))])
                    self.pr.localDataSet['currentPlace'] = data[2]
                    self.pr.localDataSet['nameDict'] = {}
                    self.pr.localDataSet['idListFindingFriends'] = []
                for iff in self.pr.localDataSet['idListFindingFriends']:
                    if iff[1] - data[1] <= datetime.timedelta(0, self.maxRange):
                        add_friend_point(data[0], iff[0])
                        add_friend_point(iff[0], data[0])
                    else:
                        del self.pr.localDataSet['idListFindingFriends'][0]
                self.pr.localDataSet['idListFindingFriends'].append(data)
        except:
            # store the current process
            print '\nProcess stopped when processing %s' % self.pr.localDataSet['currentPlace']
            traceback.print_exc()
            self.pr.store_process()
        if data is None:
            self.mc.insert_data('%s_friendmap' % self.tableName[:3], items=[self.pr.localDataSet['currentPlace'],
                                                                            MySQLdb.escape_string(json.dumps(
                                                                                self.pr.localDataSet['nameDict']))])
        print '\nProcessing Finished'


if __name__ == '__main__':
    config = {'tableName': 'acrec', 'idItem': 'user_id', 'fixedItem': 'node_des', 'orderBy': 'ac_datetime',
              'maxRange': 60}
    # config = {'tableName' : 'consumption', 'idItem' : 'user_id', 'fixedItem' : 'dev_id', 'orderBy' : 'con_datetime', 'maxRange' : 60}
    fm = FriendMap(**config)


    @TimeCalculate
    def fn():
        return fm.calculate()


    r = fn()
    print 'It took %ss' % r[0]
