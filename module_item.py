# module_item.py
class item:
    def __init__(self,itemId,speisekartenId,name,preis,beschreibung,bild):
        self.itemId = itemId
        self.speisekartenId = speisekartenId
        self.name = name
        self.preis = preis
        self.beschreibung = beschreibung
        self.bild = bild
    
    def itemId(self):
        return self.itemId

    def speisekartenId(self):
        return self.speisekartenId
        
    def name(self):
        return self.name
    
    def preis(self):
        return self.preis
    
    def beschreibung(self):
        return self.beschreibung

    def bild(self):
        return self.bild
    