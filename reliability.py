
class Network():
    def __init__(self, num):
        self.bus = self.addBuses(num)
        self.feeder = self.addFeeder()
        
    def addBuses(self,num):
        buses = {}
        for item in range(1, num+1):
            bus = Bus(item)
            loads = getLoads()
            for load in loads:
                bus.addLoad(load)
            buses[item] = bus
        return buses

    def addFeeder(self):
        feeds = {}
        feeders = getFeeders()
        feeders.reverse()
        for feeder in feeders:
            feeds[feeder.id] = feeder
            self.bus[feeder.start].totalload += self.bus[feeder.end].totalload
        return feeds

    def __repr__(self):
        return "<Network Buses:%s Feeders:%s>" % (len(self.bus), len(self.feeder))

class Bus():
    def __init__(self, num):
        self.id = num
        self.loads = {}
        self.connectedload = 0
        self.totalload = 0


    def addLoad(self, load):
        if load.bus == self.id:
            self.loads[load.id] = load
            self.connectedload += load.load
            self.totalload += load.load

    def __repr__(self):
        loadlist = list(self.loads.keys())
        loads = ''
        for elem in loadlist:
            loads += str(elem) + ' '
        return "<Bus Number: %s\tLoads: %s\tConnected Load: %.5skW\tTotal Load: %.6skW>" % (self.id, loads, self.connectedload, self.totalload)

class Load():
    def __init__(self, id, num, busnum):
        self.consumers = num
        self.load = num*0.8
        self.bus = busnum
        self.id = id

    def __repr__(self):
        return "<Load Demand:%.5skW\t@ Bus:%s>" % (self.load, self.bus)
    
class Feeder():
    def __init__(self, id, frombus, tobus, length):
        self.id = id
        self.start = frombus
        self.end = tobus
        self.length = length

    def __repr__(self):
        return "<Feeder from:%s to:%s length:%s>" % (self.start, self.end, self.length)

def getFeeders():
    '''
    Format of the data in the text file is as follows:
    ID START END LENGTH
    '''
    feeds = []
    with open('feeder.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            feed = Feeder(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]))
            feeds.append(feed)
    return feeds

def getLoads():
    '''
    Format of the data in the text file is as follows:
    ID NUM_OF_CONSUMERS BUS
    '''
    loads = []
    with open('load.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            load = Load(int(temp[0]), int(temp[1]), int(temp[2]))
            loads.append(load)
    return loads


def main():
    lvgrid = Network(12)

if __name__ == '__main__':
    main()
