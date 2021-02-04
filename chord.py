import multiprocessing as ml
from message import message
from multiprocessing.managers import BaseManager

SERVER=-1
GUEST=-2
n=100
class Chord():
    def __init__(self,n):
        self.n=n
        self.connection=ml.Queue()
        self.nodes=[(i,ml.Queue()) for i in range(n)]
        self.activeNodes=[False for i in range(n)]
        self.guest=ml.Queue()
    def get_inbox(self,id):
        return self.nodes[id][1]
    def get_guest_queue(self):
        while(self.guest.empty()==False):
            self.guest.get(False)
        return self.guest
    def send_to_node(self,id,data):
        if id==SERVER:
            self.connection.put(data)
            return
        if id==GUEST:
            self.guest.put(data)
            return
        self.nodes[id][1].put(data)
    def start(self):
        print("chord server started successfully")
        while (True):
            msg=self.connection.get()
            if msg.reciever !=SERVER:
                self.connection.put(msg)
            else:
                if (msg.data[0]=="forward"):
                    temp_msg=msg.data[1]
                    self.send_to_node(temp_msg.reciever,temp_msg)
                if (msg.data[0] == "preds"):
                    id=msg.data[1]
                    for i in range(id-1,-1,-1):
                        if self.activeNodes[i]:
                            self.send_to_node(msg.sender,(message(SERVER,msg.data,("presresp",i))))
                            break
                    for i in range(self.n-1,id,-1):
                        if self.activeNodes[i]:
                            self.send_to_node(msg.sender,(message(SERVER,msg.data,("presresp",i))))
                            break
                    self.send_to_node(msg.sender, (message(SERVER, msg.data, ("presresp", id))))
                if (msg.data[0]=="sucs"):
                    if True not in self.activeNodes:

                        self.send_to_node(msg.sender, message(SERVER, msg.sender, ("sucsresp", False)))
                    else:
                        for i in range(self.n):
                            if self.activeNodes[i]:
                                self.send_to_node(self.nodes[i][0],
                                                  data=message(msg.sender, self.nodes[i][0], ("sucs", msg.data[1])))
                                break
                if(msg.data[0]=="add"):
                    self.activeNodes[msg.data[1]]=True
                    for i in range(len(self.nodes)):
                        if self.nodes[i][0]!=msg.data[1] and self.activeNodes[i]:
                            self.send_to_node(self.nodes[i][0],message(SERVER,self.nodes[i][0],("added",msg.data[1])))


                if (msg.data[0]=="remove"):
                    self.activeNodes[msg.data[1]]=False
                    for i in range(len(self.nodes)):
                        if self.nodes[i][0]!=msg.data[1] and self.activeNodes[i]:
                            self.send_to_node(self.nodes[i][0],message(SERVER,self.nodes[i][0],("removed",msg.data[1])))


class myManager(BaseManager):
    pass

def run_server(c):
    c.start()
def start(n):
    chord_server=Chord(n)
    p=ml.Process(target=run_server,args=(chord_server,))
    p.start()
    myManager.register('get_connection',callable=lambda :chord_server.connection)
    myManager.register('get_inbox',callable=chord_server.get_inbox)
    myManager.register('get_guest_queue',callable=chord_server.get_guest_queue)
    m = myManager(address=('localhost', 50000), authkey=b'abc')
    s = m.get_server()
    s.serve_forever()
if __name__ == '__main__':
    start(n)