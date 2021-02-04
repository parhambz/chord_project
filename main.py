from multiprocessing import managers
from message import message
n=100
GUEST=-2
SERVER=-1
class myManager(managers.BaseManager):
    pass
def menue(m):


    nid=int(input("enter node number :"))
    connection=m.get_connection()
    print(nid)

    inp = input("1-add data \n 2-sucs  \n 3-stop \n 4-get data \n enter:")
    if inp == "1":
        key=int(input("key"))
        content=input("data:")
        data=(key,content)
        connection.put(message(None,-1,("forward",message(nid,nid,("adddata",data)))))
    elif (inp == "2"):
        key=int(input("enter key :"))
        q=m.get_guest_queue()
        connection.put(message(GUEST, SERVER, ("sucs", key)))
        resp = q.get()
        print(resp.data[1])
    elif(inp=="4"):
        key=int(input("enter key :"))
        q=m.get_guest_queue()
        connection.put(message(GUEST, SERVER, ("forward", message(GUEST, nid, ("getdata", key)))))
        resp = q.get()
        print(resp.data[1])
    elif (inp == "3"):
        connection.put(message(GUEST, SERVER, ("forward", message(GUEST, nid, ("stop", None)))))

    menue(m)
if __name__ == '__main__':
    myManager.register('get_connection')
    myManager.register('get_inbox')
    myManager.register('get_guest_queue')
    m = myManager(address=('localhost', 50000), authkey=b'abc')
    m.connect()
    menue(m)