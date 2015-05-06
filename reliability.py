
class Bus():
    def __init__(self, num):
        self.number = num
        self.feeders = []
        self.loads = []

    def addFeeder(self, feeder):
        if (feeder.start == self.number) or (feeder.end == self.number):
            self.feeders.append(feeder)

    def addLoad(self, load):
        self.loads.append(load)

class Load():
    def __init__(self, id, num, busnum):
        self.consumers = num
        self.load = num*0.8
        self.bus = busnum
        self.id = id

    def __repr__(self):
        return "<Load load:%.5skW at bus:%s>" % (self.load, self.bus)
    
class Feeder():
    def __init__(self, id, frombus, tobus, length):
        self.id = id
        self.start = frombus
        self.end = tobus
        self.length = length

    def __repr__(self):
        return "<Feeder from:%s to:%s length:%s>" % (self.start, self.end, self.length)

def getFeeders(feeds):
    '''
    Format of the data in the text file is as follows:
    ID START END LENGTH
    '''
    with open('feeder.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            feed = Feeder(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]))
            feeds.append(feed)

def getLoads(loads):
    '''
    Format of the data in the text file is as follows:
    ID NUM_OF_CONSUMERS BUS
    '''
    with open('load.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            load = Load(int(temp[0]), int(temp[1]), int(temp[2]))
            loads.append(load)

def main():
    network= {'feeder':[], 'load':[], 'bus':[]}
    getFeeders(network['feeder'])
    getLoads(network['load'])
    print(network)
        

if __name__ == '__main__':
    main()
