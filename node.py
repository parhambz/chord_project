import multiprocessing as ml
from random import randint
import message
import  math
SERVER=-1
STARTER=-4
class ChordNode():
    def __init__(self,id,q):
        self.ft=[]
        self.id=id
        self.data=[]
        self.sucs=-1
        self.pred=-1
        self.connection=q
    def requestSucs(self,num):
        if (num==self.id):
            return self

        self.connection.put(message(self.id,self.sucs,("sucs",num)))
        while(True):
            msg = self.connection.get()
            if (msg.reciever == self.id and msg.data[0]=="sucsresp"):
                data = msg.data
                break
            self.connection.put(msg)
        return data[1]

    def fillFt(self,n):
        lenFT=math.ceil(math.log2(n))
        for i in range(lenFT):
            self.ft[i]=self.requestSucs(self.id+ 2**i)
    def run(self):
        while(True):
            msg=self.connection.get()
            if msg.reciever != SERVER:
                self.connection.put(msg)
            else:
                if (msg.data[0] == "preds"):
                    if self.sucs==msg.sender :
                        self.connection.put(message(self.id,msg.sender,("predsresp",self.id)))
                if (msg.data[0]=="sucs"):
                    if (msg.data[1]==self.id):
                        self.connection.put(message(self.id,msg.sender,("sucsresp",self.id)))
                    elif(msg.data[1]<=self.sucs):
                        self.connection.put(message(self.id, msg.sender, ("sucsresp", self.sucs)))
                    else:
                        for i in range(len(self.ft)):
                            if self.ft[i]>=msg.data[1]:
                                self.connection.put(message(msg.sender,self.ft[i-1],msg.data))
                                break
                if (msg.data[0]=="added"):
                    if msg.data[1]<self.sucs and msg.data[1]>self.id:
                        self.sucs=msg.data[1]
                        self.connection.put(message(self.id,msg.data[1],("setpred",self.id)))

                    if msg.data[1]>self.pred and msg.data[1]<self.id:
                        for d in self.data:
                            if d[0]<msg.data[1]:
                                self.connection.put(message(self.id,msg.data[1],("adddata",d)))
                if (msg.data[0] == "setpred"):
                    self.pred=msg.data[1]
                if (msg.data[0]=="adddata"):
                    self.data.append(msg.data[1])
                
def add(q,n):
    id=0
    while (True):
        id = randint(0, n)
        q.put(message(STARTER, SERVER, ("sucs", id)))
        data = ()
        while (True):
            msg = q.get()
            if (msg.reciever == -4):
                data = msg.data
                break
            q.put(msg)
        if (data[1] != id):
            break
    return (id,data[1])

def start(q,n):
    ids=add(q,n)
    n=ChordNode(ids[0],q)
    n.sucs=ids[1]
    q.put(message(ids[0], ids[1], ("setpred", ids[0])))
    q.put(message(ids[0], SERVER, ("add", ids[0])))
    n.run()

