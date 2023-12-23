# module_item.py
class item:
    def __init__(self,itemId,speisekartenId,name,preis,beschreibung,bild, category):
        self.itemId = itemId
        self.speisekartenId = speisekartenId
        self.name = name
        self.preis = preis
        self.beschreibung = beschreibung
        self.bild = bild
        self.category = category
    
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

    def category(self):
        return self.category    
    
    def __str__(self) -> str:
        return "Item: [" +str(self.itemId) +"]"+ self.name+ " , Preis: "+str(self.preis) +" €, SpeisekartenId: "+str(self.speisekartenId) + ", Kategorie: " + self.category
    