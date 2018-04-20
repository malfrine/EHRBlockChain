# EventNode data carrier classes

#master
class MasterEventData:
    def __init__(self, timeStamp, visitId):
        self.timeStamp = timeStamp
        self.visitId = visitId

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

#event subclasses
class CheckIn(MasterEventData):
    def __init__(self, timeStamp, visitId):
        super(MasterEventData, self).__init__(timeStamp, visitId)

class CheckOut(MasterEventData):
    def __init__(self, timeStamp, visitId):
        super(MasterEventData, self).__init__(timeStamp, visitId)

class Death(MasterEventData):
    def __init__(self, timeStamp, visitId):
        super(MasterEventData, self).__init__(timeStamp, visitId)

class InsulinAdmin(MasterEventData):
    def __init__(self, insulinStartTime, visitId, insulinEndTime, insulinAmount):
        super(MasterEventData, self).__init__(insulinStartTime, visitId)
        self.endTime = insulinEndTime
        self.amount = insulinAmount

class PatientDescriptor:
    def __init__(self, patient_id):
        self.id = patient_id

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