from multiprocessing import Process
import chord,message,node
from time import sleep
n=1000
def test(nodes,c):
    c.put(message.message(5,-1,("sucs",2)))
    resp=nodes[5][1].get()
    print(resp)
if __name__ == '__main__':
    chordServer=Process (target=chord.start,args=(n,))
    chordServer.start()
    sleep(1)

    chordServer = Process(target=node.rand_start, args=(n,))
    chordServer.start()
    sleep(3)

    chordServer = Process(target=node.rand_start, args=(n,))
    chordServer.start()
    sleep(3)

    chordServer = Process(target=node.rand_start, args=(n,))
    chordServer.start()
    sleep(3)

    chordServer = Process(target=node.rand_start, args=(n,))
    chordServer.start()
    sleep(3)

    chordServer = Process(target=node.rand_start, args=(n,))
    chordServer.start()
    sleep(3)
