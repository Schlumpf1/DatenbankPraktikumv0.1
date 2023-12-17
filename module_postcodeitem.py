# module_postcode.py
class postcodeitem:
    def __init__(self,postcodeId,restaurant_username,postcode):
        self.postcodeId = postcodeId
        self.restaurant_username = restaurant_username
        self.postcode = postcode
        
    def postcodeId(self):
        return self.postcodeId

    def restaurant_username(self):
        return self.restaurant_username
        
    def postcode(self):
        return self.postcode
    