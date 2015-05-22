
TEMP_FAULT_PROBABILITY = 0.11
PERMANENT_FAULT_PROBABILITY = 0.075
TEMP_FAULT_DURATION = 15
PERMANENT_FAULT_DURATION = 75

class Network():
    def __init__(self, num, feeders, loads):
        self.bus = self.addBuses(num, loads)
        self.feeder = feeders
        
    def addBuses(self,num, loads):
        buses = {}
        for item in range(1, num+1):
            bus = Bus(item, Load(100, 0, 0, item))
            for k,v in loads.items():
                if v.bus == item:
                    bus = Bus(item, v)
            buses[bus.id] = bus
        return buses

    def addFeeder(self):
        feeds = {}
        feeders = getFeeders()
        feeders.reverse()
        for feeder in feeders:
            feeds[feeder.id] = feeder
            self.bus[feeder.start].total_load += self.bus[feeder.end].total_load
        return feeds

    def get_fault_probability(self):
        ranklist = {}
        for key in self.feeder:
            temp = self.feeder[key].length/1000 * TEMP_FAULT_PROBABILITY
            perm = self.feeder[key].length/1000 * PERMANENT_FAULT_PROBABILITY
            ranklist[key] = (temp + perm) * self.bus[self.feeder[key].end].total_load
        return ranklist

    def get_total_feeder_length(self, bus):
        total = 0
        feeds = []
        for (key, value) in self.feeder.items():
        	if value.start == bus:
        		feeds.append(key)
        for feed in feeds:
        	total += self.get_total_feeder_length(self.feeder[feed].end)
        	total += self.feeder[feed].length
        return total

    def get_total_network_load(self):
        total = 0
        for (key,value) in self.bus.items():
            total += value.get_total_load()
        return total
    
    def __repr__(self):
        return "<Network Buses:%s Feeders:%s>" % (len(self.bus), len(self.feeder))

class Bus():
    def __init__(self, num, load):
        self.id = num
        self.connected_load = load

    def __repr__(self):
        return "<Bus Number: %s\tConnected Load: %.5skW>" % (self.id, self.connected_load.load)

class Load():
    def __init__(self, id, num, load, busnum):
        self.consumers = num
        self.load = load
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
        self.ms = False

    def get_length(self):
        return self.length

    def __repr__(self):
        return "<Feeder from:%s to:%s length:%s Km>" % (self.start, self.end, self.length)

def getFeeders():
    '''
    Format of the data in the text file is as follows:
    ID LENGTH START END
    '''
    feeds = {}
    with open('feeder.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            feed = Feeder(int(temp[0]), int(temp[2]), int(temp[3]), float(temp[1]))
            feeds[feed.id] = feed
    return feeds

def getLoads():
    '''
    Format of the data in the text file is as follows:
    ID BUS LOAD NUM_OF_CONSUMERS
    '''
    loads = {}
    with open('load.txt', 'r') as f:
        for entry in f:
            temp = entry.split()
            load = Load(int(temp[0]), int(temp[3]), float(temp[2]), int(temp[1]))
            loads[load.id] = load
    return loads


def main():
    feeders = getFeeders()
    loads = getLoads()
    net = Network(21, feeders, loads)
    for k,v in net.bus.items():
        print(v)


if __name__ == '__main__':
    main()
