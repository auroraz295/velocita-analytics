import numpy as np

#5.1 - GENERAZIONE DATI
np.random.seed(42)

#creazione 500 valori interi con distribuzione normale
durate = np.random.normal(loc=28, scale=12, size=500).astype(int)
durate = np.clip(durate, 1, None) 

km = durate * np.random.uniform(0.15, 0.25, size=500)
km = np.round(km, 2)

velocita = km / (durate / 60)

#print shape
print("Shape delle tre variabili")
print(f"Durate: {durate.shape}")
print(f"KM: {km.shape}")
print(f"Velocita: {velocita.shape}")

#print dtype
print("\nDtype delle tre variabili")
print(f"Durate: {durate.dtype}")
print(f"KM: {km.dtype}")
print(f"Velocita: {velocita.dtype}")

#print min, max, media, std
print("\nRiepilogo delle tre variabili")
print(f"Durate:\n MIN: {durate.min()} | MAX: {durate.max()} | MEDIA: {durate.mean()} | STD: {durate.std()}")
print(f"KM:\n MIN: {km.min()} | MAX: {km.max()} | MEDIA: {km.mean()} | STD: {km.std()}")
print(f"Velocita:\n MIN: {velocita.min()} | MAX: {velocita.max()} | MEDIA: {velocita.mean()} | STD: {velocita.std()}")


#5.2 - SLICING E SELEZIONE
#prime 10 e ultime 10 corse da durate
prime10 = durate[:10]
ultime10 = durate[-10:]

print(f"\nPrime 10 corse: {prime10}\n Ultime 10 corse: {ultime10}")

#fancy indexing 
indici = durate[[0, 42, 99, 150, 200, 350, 499]]

#maschera booleana per corse con durate > 45 e distanza media
maschera_lunghe = durate > 45
distanza_media_lunghe = km[maschera_lunghe].mean()

print(f"\nDistanza media corse: {distanza_media_lunghe}")

#indice della corsa con velocità max e min
indice_max = np.argmax(velocita)
indice_min = np.argmin(velocita)

print(f"\nIndice corsa velocità massima: {indice_max} \nIndice corsa velocità minima: {indice_min}")

#5.3 - STATISTICHE E NORMALIZZAZIONE 
#percentili 25, 50, 75, 90 durate
percentile25 = np.percentile(durate, 25)
percentile50 = np.percentile(durate, 50)
percentile75 = np.percentile(durate, 75)
percentile90 = np.percentile(durate, 90)

print(f"\nPercentile 25: {percentile25} \nPercentile50: {percentile50} \nPercentile75: {percentile75} \nPercentile90: {percentile90}")

#normalizzazione
durate_norm = (durate - durate.min()) / (durate.max() - durate.min())

#deve rientrare tra 0 e 1 
print(f"\nNormalizzazione minima: {durate_norm.min()}")
print(f"Normalizzazione massima: {durate_norm.max()}")

#correlazione di Pearson
#np.corrcoef restituisce una matrice 2x2
correlazione = np.corrcoef(durate, km)
r_pearson = correlazione[0, 1]

print(f"\nCoefficiente di correlazione di Pearson: {r_pearson}\n")
#risultato 0.93, essendo vicina a 1 significa che c'è una correlazione forte tra la durata e i km,
#quindi all'aumentare di una aumenta anche l'altra simultaneamente

#5.4 - SERIE TEMPORALE SIMULATA
#generazione 30 giorni di corsa
corse = np.random.randint(80, 200, size=30)

#media mobile a 7 giorni
#array con 7 elementi per i 7 giorni
kernel = np.ones(7) / 7

#np.convolve fa scorrere il kernel di 7 giorni sui 30
#valid permette di calcolare la media quando la finestra dei 7 giorni è piena
media_mobile = np.convolve(corse, kernel, mode='valid')

#giorno con picco max e min
giorno_max = np.argmax(corse) + 1
giorno_min = np.argmin(corse) + 1

#print giorno, corse, media mobile
#stampo i 30 giorni
for i in range(30):
    
    #dato che la media mobile è possibile averla solo dopo i 7 giorni, 
    #se i è maggiore di 6 avremo la media, altrimenti no
    if i >= 6:
       valore =  media_mobile[i-6] 
       print(f"Giorno {i+1} | Corse: {corse[i]} | Media mobile: {valore}")
       
    else:
        print(f"Giorno {i+1} | Corse: {corse[i]} | Media mobile: non disponibile")

