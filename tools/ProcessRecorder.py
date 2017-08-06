import sys, json
from copy import deepcopy
import time


class ProcessRecorder:
    def __enter__(self):
        return self

    def __init__(self, processName='DefaultProcess', localDataSet=dict(),
                 begin=None, total=None, warningMessage='Processing', jsonDir=''):
        self.processName = processName
        # localDataSet is for datas used in process
        self.localDataSet = localDataSet
        # warningMessage is for output current process
        self.warningMessage = warningMessage
        self.jsonDir = jsonDir
        self.count = begin
        self.total = total
        # self.process is for process bar
        self.process = -1
        # jsonStorage contains localDataSet of many processName
        self.jsonStorage = {}
        self.load_process()

        self.lastAddTime = time.time()

    def load_process(self):
        try:
            with open('%sProcessRecorder.json' % self.jsonDir) as f:
                self.jsonStorage = json.loads(f.read())

            print('ProcessRecorder: Load process')

            process_data = self.jsonStorage[self.processName]
            # only dictate above may move to except
            for key in self.localDataSet:
                if key in process_data:
                    self.localDataSet[key] = process_data[key]
            if self.count is None:
                self.count = process_data['__count']
            if self.total is None:
                self.total = process_data['__total']
        except:
            print('ProcessRecorder: New process')
            if self.count is None:
                self.count = 0
            if self.total is None:
                self.total = 100

    def store_process(self):
        '''
        process is recorded in ProcessRecorder.json
        __count:
        __total:
        '''
        self.jsonStorage[self.processName] = deepcopy(self.localDataSet)
        self.jsonStorage[self.processName]['__count'] = self.count
        self.jsonStorage[self.processName]['__total'] = self.total
        with open('%sProcessRecorder.json' % self.jsonDir, 'wb') as f:
            f.write(json.dumps(self.jsonStorage))

    def clear_storage(self):
        tmpJson = self.jsonStorage
        if self.processName in tmpJson:
            del tmpJson[self.processName]
        with open('%sProcessRecorder.json' % self.jsonDir, 'w') as f:
            f.write(json.dumps(tmpJson))

    def add(self, i=1):
        ''' add self.count and refresh output if process has increase by 1% '''
        # thisAddTime = time.time()
        # addTime = thisAddTime - self.lastAddTime
        # self.lastAddTime = thisAddTime
        self.count += i
        percent = float(self.count) * 100 / self.total
        percent = int(percent)
        if self.process < percent:
            self.process = percent
            print('%s: %s%s\r' % (self.warningMessage, self.process, '%'))
            # sys.stdout.write('%s: %s%s\r' % (self.warningMessage, self.process, '%'))
            # sys.stdout.flush()

    def __exit__(self, exc_type, exc_value, exc_tb):
        ''' in case for with-statement '''
        self.store_process()


if __name__ == '__main__':
    import time

    with ProcessRecorder(localDataSet={'name': None, 'num': None, 'price': 1}, warningMessage='First recorder') as pr:
        for key, value in pr.localDataSet.items(): print('%s: %s' % (key, value))
        for i in range(30):
            pr.add()
            time.sleep(0.05)
        pr.localDataSet['name'] = 'LittleCoder'
        pr.localDataSet['num'] = 1
        pr.localDataSet['price'] = '$1.99'
    print('Pretent the program is closed and we start a new one')
    with ProcessRecorder(localDataSet={'name': None, 'num': None, 'price': None},
                         warningMessage='First recorder') as pr:
        for key, value in pr.localDataSet.items(): print('%s: %s' % (key, value))
        for i in range(30):
            pr.add()
        time.sleep(0.05)
