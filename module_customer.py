# module_customer.py
class customer:
    def __init__(self, username, password, vorname, nachname, adresse, plz):
        self.username = username 
        self.password = password
        self.vorname = vorname
        self.nachname = nachname
        self.adresse = adresse
        self.plz = plz

    def username(self):
        return self.username
    
    def password(self):
        return self.username
    

    def vorname(self):
        return self.vorname

    def nachname(self):
        return self.nachname
    
    def adresse(self):
        return self.adresse

    def plz(self):
        return self.plz