class order:
    def __init__(self,orderId, status, date,time,text,restaurant_username,customer_username):
        self.orderId = orderId
        self.status = status
        self.date = date
        self.time = time
        self.text = text
        self.restaurant_username = restaurant_username
        self.customer_username = customer_username
    
    def orderId(self):
        return self.orderId

    def status(self):
        return self.status
        
    def date(self):
        return self.date
    
    def time(self):
        return self.time
    
    def text(self):
        return self.text

    def restaurant_username(self):
        return self.restaurant_username
    
    def customer_username(self):
        return self.customer_username

    def __str__(self) -> str:
        return "Order: [" +str(self.orderId) +"]"+ self.status + " , Date: "+str(self.date) +" , Time: "+str(self.time) + ", text: " + str(self.text)+ ", Restaurant: " + self.restaurant_username + ", Customer: " + self.customer_username;