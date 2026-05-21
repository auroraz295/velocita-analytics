#1.2 - FUNZIONI DI UTILITA'

def calcola_durata_minuti(ora_inizio:str, ora_fine:str):
    #formato input HH:MM
    #conversione str - int
    ora_inizio = int(ora_inizio[:2])
    ora_fine = int(ora_fine[:2])
    
    min_inizio = int(ora_inizio[3:])
    min_fine = int(ora_fine[3:])
    
    minuti_inizio = ora_inizio * 60 + min_inizio
    minuti_fine = ora_fine * 60 + min_fine
    
    #errore se i minuti di inizio sono inferiori a quelli di fine
    if minuti_fine < minuti_inizio:
        raise ValueError("L'ora fine non può essere precedente a ora inizio.")
    
    return minuti_fine - minuti_inizio

def classifica_corsa(durata_minuti:int):
    if durata_minuti < 15:
        return "breve"
    elif 15<= durata_minuti <= 45:
        return "media"
    else:
        return "lunga"

#da list diventa un dict 
def riepilogo_corse(lista_durate:list):
    if not lista_durate:
        return {"totale": 0, "media": 0, "max": 0, "min" : 0, "breve": 0, "media": 0, "lunga": 0}
    
    lista_minuti = []
    for ora_inizio, ora_fine in lista_durate:
        minuti = calcola_durata_minuti(ora_inizio, ora_fine)
        lista_minuti.append(minuti)
    
    numero_corse = len(lista_minuti)
    somma = sum(lista_minuti)
    v_max = max(lista_minuti)
    v_min = min(lista_minuti)
    
    breve = 0 
    media = 0 
    lunga = 0 
    
    for d in lista_minuti:
        somma += d
        if d > v_max:
            v_max = d 
        if d < v_min:
            v_min = d 
            
    classifica = classifica_corsa(d)
    if classifica == "breve":
        breve += 1
    elif classifica == "media":
        media += 1
    else:
        lunga += 1
        
    return {"totale": somma, "media": somma/numero_corse, "max": v_max, "min" : v_min, "breve": breve, "media": media, "lunga": lunga}
    
