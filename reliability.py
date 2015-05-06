
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
    def __init__(self, busnum, num):
        self.consumers = num
        self.load = num*800
        self.bus = busnum

class Feeder():
    def __init__(self, frombus, tobus, length):
        self.start = frombus
        self.end = tobus
        self.length = length

def main():
    network= {'feeder':[], 'load':[]}
    print("Create the network \n")
    print("Press the following Feeder(F), Load(L) or exit(X)")
    while True:
        option = input("Choose your option: ")
        if option == 'F':
            inp = ''
            while True:
                inp = input("Enter feeder details: ")
                if inp == 'x': break
                temp = inp.split()
                feed = Feeder(int(temp[0]), int(temp[1]), int(temp[2]))
                network['feeder'].append(feed)
                
        elif option == 'L':
            inp = ''
            while True:
                inp = input("Enter load details: ")
                if inp == 'x': break
                temp = inp.split()
                load = Load(int(temp[0]))
                network['load'].append(load)
        elif option == 'x':
            break
    print(network)
        

if __name__ == '__main__':
    main()
