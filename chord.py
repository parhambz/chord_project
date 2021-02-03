import multiprocessing as ml
import node
import message
SERVER=-1
SUCS=-2
class Chord():
    def __init__(self,n):
        self.n=n
        self.connection=ml.Queue()
        self.nodes=[(i,ml.Queue()) for i in range(n)]
        self.activeNodes=[False for i in range(n)]
    def send_to_node(self,id,data):
        if id==SERVER:
            self.connection.put(data)
            return
        self.nodes[id][1].put(data)
    def start(self):
        while (True):
            msg=self.connection.get()
            if msg.reciever !=SERVER:
                self.connection.put(msg)
            else:
                if (msg.data[0]=="forward"):
                    temp_msg=msg.data[1]
                    self.send_to_node(temp_msg.reciever,temp_msg)
                if (msg.data[0]=="sucs"):
                    if True not in self.activeNodes:
                        self.send_to_node(SERVER, message(SERVER, msg.sender, ("sucsresp", -2)))
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
def run_server(c):
    c.start()
def start(n):
    chord_server=Chord(n)
    ml.Process(target=run_server,args=(chord_server,))
    return (chord_server.nodes,chord_server.connection)