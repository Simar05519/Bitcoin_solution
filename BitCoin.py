# to read csv file
from csv import reader

# global varibles

data = {} 
maxCut = 0 
maxID = '' 

class MempoolTransaction():
    
    def __init__(self, txid, fee, weight, parents):
        global maxCut
        global maxID
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = [parent for parent in parents.strip().split(';')]
        if(self.parents[0] == '' and self.weight <= 4000000):
            data[self.txid] = {
                'fee': self.fee,
                'weight': self.weight,
                'parent': []
            }
            if(self.fee > maxCut):
                maxCut = self.fee
                maxID = self.txid
        else:
            if set(self.parents).issubset(data.keys()):
                amt = self.weight
                cut = self.fee
                for parent in self.parents:
                    if((amt + data[parent]['weight']) <= 4000000):
                        amt += data[parent]['weight']
                        cut += data[parent]['fee']
                    else:
                        break
                data[self.txid] = {
                                    'fee': cut,
                                    'weight': amt,
                                    'parent': self.parents
                                }
                if(cut > maxCut):
                    maxCut = cut
                    maxID = self.txid
            else:
                return

def parse_mempool_csv():
    with open("mempool.csv", "r") as file:
        next(file)
        csv_reader = reader(file)
        for row in csv_reader:
            MempoolTransaction(row[0], row[1], row[2], row[3])


parse_mempool_csv()
open("block.txt", "w").close()
f = open("block.txt", "a")

def func_add(array):
    
    for key in array:
        if set(key).issubset(data.keys()):
            func_add(data[key]['parent'])
        
        f.write(f"{key} -> ")

for  key,val in data.items():
    
    if val['parent']:
    
        func_add(val['parent'])
    
    f.write(f"{key}\n")
    

f.close()
print("Successfully completed!!")