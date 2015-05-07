
TEMP_FAULT_PROBABILITY = 0.11
PERMANENT_FAULT_PROBABILITY = 0.075
TEMP_FAULT_DURATION = 7
PERMANENT_FAULT_DURATION = 75

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
            self.bus[feeder.start].total_load += self.bus[feeder.end].total_load
        return feeds

    def get_fault_probability(self):
        ranklist = {}
        for key in self.feeder:
            temp = self.feeder[key].length/1000 * TEMP_FAULT_PROBABILITY
            perm = self.feeder[key].length/1000 * PERMANENT_FAULT_PROBABILITY
            ranklist[key] = (temp + perm) * self.bus[self.feeder[key].end].total_load
        return ranklist

    def get_total_feeder_length(self):
        total = 0
        for (key,value) in self.feeder.items():
            total += value.get_length()
        return total

    def get_total_network_load(self):
        total = 0
        for (key,value) in self.bus.items():
            total += value.get_total_load()
        return total
    
    def __repr__(self):
        return "<Network Buses:%s Feeders:%s>" % (len(self.bus), len(self.feeder))

class Bus():
    def __init__(self, num):
        self.id = num
        self.loads = {}
        self.connected_load = 0
        self.total_load = 0

    def get_total_load(self):
        return self.total_load

    def addLoad(self, load):
        if load.bus == self.id:
            self.loads[load.id] = load
            self.connected_load += load.load
            self.total_load += load.load

    def __repr__(self):
        loadlist = list(self.loads.keys())
        loads = ''
        for elem in loadlist:
            loads += str(elem) + ' '
        return "<Bus Number: %s\tLoads: %s\tConnected Load: %.5skW\tTotal Load: %.6skW>" % (self.id, loads, self.connected_load, self.total_load)

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

    def get_length(self):
        return self.length

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
    ranking = lvgrid.get_fault_probability()
    #ranklist = sorted(ranking.items(), key= lambda x: x[1], reverse=True)
    #print(ranklist)
    length = lvgrid.get_total_feeder_length()
    total_demand = lvgrid.get_total_network_load()
    num_of_faults = (TEMP_FAULT_PROBABILITY + PERMANENT_FAULT_PROBABILITY) * length / 1000
    load_interrupted = (lvgrid.bus[1].total_load + lvgrid.bus[2].total_load)
    tiepi = (load_interrupted) * (TEMP_FAULT_DURATION + PERMANENT_FAULT_DURATION) / total_demand
    niepi = TEMP_FAULT_PROBABILITY + PERMANENT_FAULT_PROBABILITY
    print("Total feeder length: %s m " % (length))
    print("Total demand: %s kW" %(total_demand))
    print("No. of faults per year: ", num_of_faults)
    print("TIEPI: %s mins/yr" %(tiepi))
    print('NIEPI: %s int/yr' %(niepi))
    

if __name__ == '__main__':
    main()
