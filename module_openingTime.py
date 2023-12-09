# module_item.py
class OpeningTime:
    def __init__(self,id,restaurantId,day,fromTime,toTime):
        self.id = id
        self.restauratId = restaurantId
        self.day = day
        self.fromTime = fromTime
        self.toTime = toTime
    
    def id(self):
        return self.id;
        
    def restaurantId(self):
        return self.restauratId

    def day(self):
        return self.day
        
    def fromTime(self):
        return self.fromTime
    
    def toTime(self):
        return self.toTime
    