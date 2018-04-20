# EventNode data carrier classes

#master
class MasterEventData:
    def __init__(self, timeStamp):
        self.timeStamp = timeStamp

#inheritences
class CheckIn(MasterEventData):
    pass

class CheckOut(MasterEventData):
    pass

class Death(MasterEventData):
    pass

class InsulinAdmin(MasterEventData):
    def __init__(self, amount):
        self.amount = amount

# linked list event node
class EventNode:
    def __init__(self, timeStamp, eventType):
        self.data = MasterEventData(timeStamp)
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, timeStamp, eventType):
        self.data = MasterEventData(timeStamp, eventType)

    def setNext(self,newnext):
        self.next = newnext

class EHRLink:

    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        temp = item
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())