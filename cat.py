from datetime import datetime

class UniqueID():
    uniqueid=0
    def __init__(self):
      type(self).uniqueid=type(self).uniqueid+1
    currentYear = datetime.now().year
    def Create_UniqueId(self):
        a=self.uniqueid
        a=str(a)
        if(len(a)<4):
            empty=""
            for i in range(4-len(a)):
                empty+='0'
            a=empty+a
        UniqueID=str(self.currentYear)+a
        print(UniqueID)
        return UniqueID
