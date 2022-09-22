import requests
class Node:
    def __init__(self,value=None):
        self.value = value
        self.next = None

class Cryptos:
    def __init__(self,search,altname,base,quote):
        self.search = search
        self.altname = altname
        self.base = base
        self.quote = quote
    
    

    def fetch_price(self):
        try:
            price = requests.get('https://api.kraken.com/0/public/Depth?pair=' + self.search).json()['result'][self.search]['bids'][0][0]
        except:
            price = requests.get('https://api.kraken.com/0/public/Depth?pair=' + self.base + self.quote).json()['result'][self.base + self.quote]['bids'][0][0]
        return price

    def fetch_volume(self):
        volume = requests.get('https://api.kraken.com/0/public/Depth?pair=' + self.search).json()['result'][self.search]['bids'][0][2]
        return volume


def siphon(request, string):
    
    for i in range(0,len(string)):
        if string[i:i + len(request):] == request:
            return True

class LinkedList:
    def __init__(self):
        self.head = Node()

    def appendList(self,data ):
        new_node = Node(data)
        current = self.head
        while current.next != None:
            current = current.next
        current.next = new_node
    
    def length(self):
        current = self.head
        total = 0
        while current.next != None:
            total+= 1
            current = current.next
        return total
    
    def addToFront(self, val):
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            
        temp = self.head
        self.head = new_node
        new_node.next=temp

        return self


    def returnFront(self):
        
        return self.head


    def print_values(self):
        runner = self.head
        
        while (runner != None):
            print(runner.value)
            runner = runner.next
        return self
    
    
    def addToBack(self, val):
        if self.head == None: # if the list is empty
            self.addToFront(val) # run the addToFront method
            return self # make sure the rest of this function does not occur 
        new_node = Node(val) # create new instance
        runner = self.head
        while(runner.next != None):
            runner = runner.next
        runner.next = new_node
        return self

    def removeFromFront(self):
        if self.head == None:
            return None
        temp = self.head
        #  move the head pointer to the next node
        head = self.head.next
        temp = None
        
    def display(self):
        elems = []
        cur_node = self.head
        while cur_node.next != None:
            cur_node=cur_node.next
            elems.append(cur_node.value)
        print(elems)
        return elems

    def get(self,index):
        if index>=self.length():
            print('ERROR out of range')
            return None
        cur_idx = 0 
        cur_node =self.head
        while True:
            cur_node=cur_node.next
            if cur_idx==index: 
                return cur_node.value
            cur_idx+=1
    
    def getByContent(self, content):
        cur_node = self.head
        cur_index = 0
        cur_indices = []
        while cur_node.next:
            cur_node=cur_node.next
            if not siphon(content,cur_node.value.search):
                pass
            else:
                cur_indices.append(cur_index)
            # if cur_node.value.search == content:
            #     return cur_index
            
            cur_index+=1
        return cur_indices

    def contains(self, value):
        cur_node = self.head
        while True:
            cur_node=cur_node.next
            if cur_node.value==value:
                return True
            else:
                return False

resp = requests.get('https://api.kraken.com/0/public/AssetPairs')

json = resp.json()['result']

def get_all():
    linkedTest = LinkedList()
    for value in json:
        search = value
        altname = json[value]['altname']
        base = json[value]['base']
        quote = json[value]['quote']
        linkedTest.appendList(Cryptos(search,altname,base,quote))
        
    return linkedTest

favs = []
all = get_all()

ethSearch = all.getByContent('XETHZUSD')[0]
btcSearch = all.getByContent('XXBTZUSD')[0]
solSearch = all.getByContent('SOLUSD')[1]
crvSearch = all.getByContent('CRVUSD')[0]
adaSearch = all.getByContent('ADAUSD')[0]
dotSearch = all.getByContent('DOTUSD')[0]

favs.append(all.get(crvSearch))
favs.append(all.get(ethSearch))
favs.append(all.get(solSearch))
favs.append(all.get(btcSearch))
favs.append(all.get(adaSearch))
favs.append(all.get(dotSearch))
