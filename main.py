
import chord,message,node
n=10
if __name__ == '__main__':
    chord_resp=chord.start(n)
    chord_nodes=chord_resp[0]
    chord_connection=chord_resp[1]

