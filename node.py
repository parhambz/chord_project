import multiprocessing as ml
from random import randint
import message
import  math
SERVER=-1
STARTER=-4
class ChordNode():
    def __init__(self,id,q,inbox,n):
        self.ft=[]
        self.id=id
        self.data=[]
        self.sucs=-1
        self.pred=-1
        self.connection=q
        self.inbox=inbox
        self.n=n
    def send_to_node(self,msg):
        if msg.reciever==SERVER:
            self.connection.put(msg)
            return
        self.connection.put(message(self.id,SERVER,("forward",msg)))
    def is_sucs_me(self,num):
        if (num==self.id or self.sucs==self.id):
            return True

        if (self.pred>self.id):
            if num>self.pred:
                return True
        if (num>self.pred and num<self.id):
            return True
    def requestSucs(self,num):
        if (self.is_sucs_me(num)):
            return self.id
        self.send_to_node(message(self.id,self.sucs,("sucs",num)))
        while(True):
            msg = self.inbox.get()
            if (msg.data[0]=="sucsresp"):
                data = msg.data
                break
            self.connection.put(msg)
        return data[1]

    def fillFt(self):
        n=self.n
        lenFT=math.ceil(math.log2(n))
        for i in range(lenFT):
            self.ft[i]=self.requestSucs((self.id+ 2**i)%n)
    def run(self):
        while(True):
            msg=self.inbox.get()
            if (msg.data[0] == "preds"):
                self.send_to_node(message(self.id,msg.sender,("predsresp",self.pred)))
            if (msg.data[0]=="sucs"):
                if (self.is_sucs_me(msg.data[1])):
                    self.send_to_node(message(self.id,msg.sender,("sucsresp",self.id)))
                else:
                    self.send_to_node(message(msg.sender, self.sucs, msg.data))
                '''
                    for i in range(len(self.ft)-1):
                        if self.ft[i]>=msg.data[1] and self.ft[i+1]:
                            self.send_to_node(message(msg.sender,self.ft[i-1],msg.data))
                            break
                '''
            if (msg.data[0]=="added"):
                self.fillFt()
            if (msg.data[0] == "setpreds"):
                self.pred=msg.data[1]
            if (msg.data[0] == "setsucs"):
                    self.sucs = msg.data[1]
            if (msg.data[0]=="adddata"):
                self.data.append(msg.data[1])
                

def start(connection,inbox,id,sucs,preds,n):

    node=ChordNode(id,connection,inbox,n)
    connection.put(message(id,SERVER,("add",id)))
    node.send_to_node(message(id,sucs,("setpreds",id)))
    node.send_to_node(message(id, preds, ("setsucs", id)))
    node.sucs=sucs
    node.pred=preds
    #node.fillFt()
    node.run()
