class menuItem:
    def __init__(self, itemId, name,preis,beschreibung,category):
        self.itemId = itemId
        self.name = name
        self.preis = preis
        self.beschreibung = beschreibung
        self.category = category

    def itemId(self):
        return self.itemId
    
    def name(self):
        return self.name
    
    def preis(self):
        return self.preis
    
    def beschreibung(self):
        return self.beschreibung

    def category(self):
        return self.category 
 