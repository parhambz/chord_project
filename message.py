class message():
    def __init__(self,sender,reciever,data):
        self.sender=sender
        self.reciever=reciever
        self.data=data
    def __str__(self):
        return "message from "+str(self.sender) +" to "+str(self.reciever)+" data:\n"+str(self.data)