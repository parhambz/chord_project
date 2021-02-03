import multiprocessing as ml
import node
import message
SERVER=-1
class Chord():
    def __init__(self,n):
        self.n=n
        self.connection=ml.Queue()
        self.nodes=[]
    def send_to_node(self,id,data):
        for n in self.nodes:
            if n[0]==id:
                n[1].put(data)
    def start(self):
        while (True):
            msg=self.connection.get()
            if msg.reciever !=SERVER:
                self.connection.put(msg)
            else:
                if (msg.data[0]=="sucs"):
                    if len(self.nodes)!=0:
                        self.connection.put(message(msg.sender,self.nodes[0],("sucs",msg.data[1])))
                    else:
                        self.connection.put(message(SERVER,msg.sender,("resp",(msg.data[1],-2))))
                if(msg.data[0]=="add"):
                    for i in self.nodes:
                        self.connection.put(message(SERVER,i,("added",msg.data[1])))
                    self.nodes.append(msg.data[1])

                if (msg.data[0]=="remove"):
                    for i in self.nodes:
                        self.connection.put(message(SERVER,i,("added",msg.data[1])))
                    self.nodes.remove(msg.data[1])
