from multiprocessing import Process
import chord,message,node
from time import sleep
n=32
def test(nodes,c):
    c.put(message.message(5,-1,("sucs",2)))
    resp=nodes[5][1].get()
    print(resp)
if __name__ == '__main__':
    chord_resp=chord.start(n)
    chord_nodes=chord_resp[0]
    chord_connection=chord_resp[1]
    sleep(1)

    p1=Process(target=node.start,args=(chord_connection,chord_nodes[3][1],3,3,3,n,))
    p1.start()
    sleep(1)

    p1 = Process(target=node.start, args=(chord_connection, chord_nodes[10][1], 10, 3, 3, n,))
    p1.start()
    sleep(1)

    p1 = Process(target=node.start, args=(chord_connection, chord_nodes[20][1], 20, 3, 10, n,))
    p1.start()
    sleep(1)
    test(chord_nodes,chord_connection)
