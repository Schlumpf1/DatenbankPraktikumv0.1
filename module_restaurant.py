# module_restaurant.py
class restaurant:
    def __init__(self,username, password, name, oeffnungszeiten, adresse, postleitzahl):
        self.username = username
        self.password = password
        self.name = name
        self.oeffnungszeiten = oeffnungszeiten
        self.adresse = adresse
        self.postleitzahl = postleitzahl
    
    def username(self):
        return self.username

    def password(self):
        return self.password
        
    def name(self):
        return self.name
    
    def oeffnungszeiten(self):
        return self.oeffnungszeiten
    
    def adresse(self):
        return self.adresse

    def bild(self):
        return self.postleitzahl
    
    