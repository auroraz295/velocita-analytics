#2.1 - CLASSE BICICLETTA
class Bicicletta:
    def __init__(self, id_bici:str, tipo:str, stazione_corrente:str, km_percorsi:float, disponibile:bool):
        self.id_bici = id_bici
        self.tipo = tipo
        self.stazione_corrente = stazione_corrente
        self._km_percorsi = km_percorsi
        self.disponibile = disponibile
        
    #METODI
    def noleggia(self, utente:str):
        if not self.disponibile:
            raise ValueError("La bici non può essere noleggiata.")
        self.disponibile = False
        return f"Noleggio\n Bici {self.id_bici}\n Utente: {utente}"
        
    def restituisci(self, stazione:str, km_aggiunta:float):
        self.stazione_corrente = stazione
        self.km_percorsi += km_aggiunta
        self.disponibile = True
        
        return f"Stazione corrente: {self.stazione_corrente}\n Km percorsi: {self._km_percorsi}\n Disponibile: {"si" if self.disponibile else "no"}"
    
    def __str__(self):
        disponibile = "disponibile" if self.disponibile else "non disponibile"
        return f"[{self.id_bici}] | {self.tipo} | {self.stazione_corrente} | {self._km_percorsi} | {disponibile}"
    
    def __repr__(self):
        return f"Bicicletta({self.id_bici} - {self.tipo} - {self.stazione_corrente} - {self._km_percorsi} - {self.disponibile})"
    
    #3.2 INCAPSULAMENTO 
    @property 
    def km_percorsi(self):
        return self._km_percorsi
    
    def aggiungi_km(self, km:float):
        if km <= 0:
            raise ValueError("I km non possono essere inferiori a 0.")
        
        self._km_percorsi += km
        return self._km_percorsi
    
#2.2 - CLASSE FLOTTA BICI
class FlottaBici:
    def __init__(self, citta:str):
        self.citta = citta 
        self.biciclette = []
        
    #METODI
    def aggiungi(self, bici:Bicicletta):
        self.biciclette.append(bici)
    
    def rimuovi(self, id_bici:str):
        for bici in self.biciclette:
            if bici.id_bici == id_bici:
                self.biciclette.remove(bici)
                return f"Bici {id_bici} rimossa."
            
        raise KeyError(f"Bici {id_bici} non trovata.")
    
    def cerca_per_id(self, id_bici:str):
        for bici in self.biciclette:
            if bici.id_bici == id_bici:
                return bici
            
        raise KeyError(f"Bici {id_bici} non trovata.")    
    
    def disponibili(self):
        bici_disponibili = []
        for bici in self.biciclette:
            if bici.disponibile:
                bici_disponibili.append(bici)
            
        return bici_disponibili
                
    
    def statistiche(self):
        totale = len(self.biciclette)
        disponibili = len(self.disponibili())
        in_uso = totale - disponibili
        km_totali_flotta = sum(bici.km_percorsi for bici in self.biciclette)
        km_medi_per_bici = km_totali_flotta / totale
    
        return {"Totale:" : totale, "Disponibili:" : disponibili, "In uso:": in_uso, "KM totali flotta:": km_totali_flotta, "KM medi per bici:": km_medi_per_bici}
   
    def __len__(self):
        return len(self.biciclette)
    
    @classmethod
    def da_lista(cls, citta: str, dati: list) -> "FlottaBici":
        istanza_flotta = cls(citta)
        for item in dati:
            bici = Bicicletta(id_bici = item['id'], tipo = item['tipo'], stazione_corrente = item['stazione'], km_percorsi = item['km'], disponibile=True)
            istanza_flotta.aggiungi(bici)
        return istanza_flotta
    
    
#3.1 - SOTTOCLASSI BICICLETTA
class BiciclettaClassica(Bicicletta):
    def __init__(self,id_bici, tipo, stazione_corrente, km_percorsi, disponibile, taglia:str):
        super().__init__(id_bici, tipo, stazione_corrente, km_percorsi, disponibile)
        
        self.taglia = taglia 
    
    #OVERRIDE METODO STR
    def __str__(self):
        disponibile = "disponibile" if self.disponibile else "non disponibile"
        return f"[{self.id_bici}] | {self.tipo} | {self.taglia} | {self.stazione_corrente} | {self.km_percorsi} | {disponibile}"
    
    
class BiciclettaElettrica(Bicicletta):
    def __init__(self,id_bici, tipo, stazione_corrente, km_percorsi, disponibile, batteria_percentuale:int):
        super().__init__(id_bici, tipo, stazione_corrente, km_percorsi, disponibile)
        
        self.batteria_percentuale = batteria_percentuale
        
    #METODI
    def ricarica(self, percentuale:int):
        self.batteria_percentuale = self.batteria_percentuale + percentuale
        if self.batteria_percentuale > 100:
            self.batteria_percentuale = 100

    #OVERRIDE METODI
    def noleggia(self, utente:str):
        if self.disponibile:
            if self.batteria_percentuale < 20: 
                raise ValueError("La bici non può essere noleggiata.")
            else:
                self.disponibile = False
                return f"Noleggio\n Bici {self.id_bici}\n Utente: {utente}"
            
    def __str__(self):
        disponibile = "disponibile" if self.disponibile else "non disponibile"
        return f"[{self.id_bici}] | {self.tipo} | {self.batteria_percentuale}% | {self.stazione_corrente} | {self.km_percorsi} | {disponibile}"
    

#3.3 POLIMORFISMO
#sfrutto la funzione definita __str__ in ogni sottoclasse, ognuna con i suoi override
#in modo tale che per ogni sottoclasse recupererà la str giusta

def stampa_flotta(biciclette:list):
    for bici in biciclette:
        print(bici)
        
#esempio chiamata 
istanze_miste = [BiciclettaClassica("MI-101", "Classica" ,"Cadorna", 52.0, True, "L"),
                 BiciclettaElettrica("TO-202", "Elettrica", "Porta Nuova", 120.5, True, 85)]
stampa_flotta(istanze_miste)