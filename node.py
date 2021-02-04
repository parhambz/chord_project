from message import message
import  math
from multiprocessing.managers import BaseManager
from random import randint
from multiprocessing import Process,Queue
from time import sleep
SERVER=-1
GUEST=-2
n=100
gnode=None
class ChordNode():
    def __init__(self,id,q,inbox,n):
        self.process=None
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
    def stop(self):
        self.send_to_node(message(self.id,self.pred,("setsucs",self.sucs)))
        self.send_to_node(message(self.id, self.sucs, ("setpreds", self.pred)))
        self.send_to_node(message(self.id,SERVER,("removed",self.id)))
        for d in self.data:
            self.send_to_node(message(self.id,self.sucs,("adddata",d)))
    def is_sucs_me(self,num):
        if (num==self.id or self.sucs==self.id):
            return True

        if (self.pred>self.id):
            if num>self.pred or num<self.id:
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
        print("node",self.id,"started successfully with preds",self.pred,"and sucs",self.sucs)
        while(True):
            print(self.data)

            msg=self.inbox.get()
            if (msg.data[0]=="getdata"):
                for d in self.data:
                    if d[0]==msg.data[1]:
                        self.send_to_node(message(self.id,msg.sender,("dataresp",d)))
                pass
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
                pass
                #self.fillFt()
            if (msg.data[0]=="stop"):
                return self.stop()
            if (msg.data[0] == "setpreds"):
                self.pred=msg.data[1]
            if (msg.data[0] == "setsucs"):
                    self.sucs = msg.data[1]
            if (msg.data[0]=="adddata"):
                self.data.append(msg.data[1])
            if (msg.data[0]=="reqdata"):
                node_id=msg.sender
                if node_id<self.id:
                    for d in self.data:
                        if d[0]>node_id and d[0]<self.id:
                            pass
                        else:
                            self.send_to_node(message(self.id,node_id,("adddata",d)))
                            self.data.remove(d)
                else:
                    for d in self.data:
                        if d[0]<node_id:
                            self.send_to_node(message(self.id, node_id, ("adddata", d)))
                            self.data.remove(d)

class myManager(BaseManager):
    pass
def start(inbox,connection,id,sucs,preds,n):
    node=ChordNode(id,connection,inbox,n)
    connection.put(message(id,SERVER,("add",id)))
    node.send_to_node(message(id,sucs,("setpreds",id)))
    node.send_to_node(message(id, sucs, ("reqdata",None)))
    node.send_to_node(message(id, preds, ("setsucs", id)))
    node.sucs=sucs
    node.pred=preds

    #node.fillFt()
    node.run()
def rand_start(n):
    myManager.register('get_connection')
    myManager.register('get_inbox')
    myManager.register('get_guest_queue')
    m = myManager(address=('localhost', 50000), authkey=b'abc')
    m.connect()
    gq = m.get_guest_queue()
    connection = m.get_connection()

    id=None
    mysucs=None
    while(True):
        rint=randint(0,n)
        connection.put(message(GUEST,SERVER,("sucs",rint)))
        resp=gq.get()
        if resp.data[1]==False:
            id=rint
            mysucs=rint
            break
        if resp.data[1]!=rint:
            id=rint
            mysucs=resp.data[1]
            break
    connection.put(message(GUEST,SERVER,("preds",id)))
    resp=gq.get()
    #pr=Process(target=start,args=(m.get_inbox(id),connection,id,mysucs,resp.data[1],n,))
    #pr.start()
    #return pr
    start(m.get_inbox(id),connection,id,mysucs,resp.data[1],n)


def main():

    pr=Process(target=rand_start,args=(n,))
    pr.start()
    sleep(1)
    #menue(pr)
    #rand_start(n)
if __name__ == '__main__':
    main()