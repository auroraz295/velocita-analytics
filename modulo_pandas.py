import numpy as np
import pandas as pd

from demo import classifica_corsa

#6.1 - CREAZIONE DATAFRAME
#creo 20 id bici 
id_bici = [f"[{i}]" for i in range(1, 21)]
#creo 25 id utenti
id_utenti = [2000 + i for i in range(1, 26)]

#record citta, date e fasce per random.choice
citta = ["Milano", "Roma", "Torino"]
date = ["2026-04-15", "2026-04-16", "2026-04-17"]
fasce = ["Mattina", "Pomeriggio", "Sera", "Notte"]

dati_corse = {"id_corsa" : [1000 + i for i in range(80)], 
            "id_bici" : [np.random.choice(id_bici) for _ in range(80)],
            "id_utente" : [2000 + np.random.randint(1, 30) for _ in range(80)],
            "citta" : [np.random.choice(citta) for _ in range(80)], 
            "data_corsa" : [np.random.choice(date) for _ in range(80)],
            "durata_minuti" : [float(np.random.randint(5, 60)) for _ in range(80)], 
            "km_percorsi" : [round(np.random.uniform(1.0, 12.0), 2) for _ in range(80)],
            "fascia_oraria" : [np.random.choice(fasce) for _ in range(80)]}

dati_bici = {"id_bici" : id_bici,
            "tipo" : [np.random.choice(["classica", "elettrica"]) for _ in range(20)],
            "citta" : [np.random.choice(citta) for _ in range(20)], 
            "anno_acquisto" : [np.random.randint(2022, 2027) for _ in range(20)],
            "costo_acquisto" : [round(np.random.uniform(500.0, 1500.0), 2) for _ in range(20)]}

dati_utenti = {"id_utente" : id_utenti,
             "nome" : [f"Utente_{i}" for i in range(25)],
             "citta" : [np.random.choice(citta) for _ in range(25)],
             "tipo_abbonamento" : [np.random.choice(["Basic", "Premium"]) for _ in range(25)],
             "data_iscrizione": [np.random.choice(["2025-11-12", "2026-01-20", "2026-03-05"]) for _ in range(25)]}
             
#trasformo i dizionari in dataframe
df_corse = pd.DataFrame(dati_corse)
df_bici = pd.DataFrame(dati_bici)
df_utenti = pd.DataFrame(dati_utenti)
             
#inserimento 5 duplicati e 8 NaN tra durata_minuti e km_percorsi

#copio le prime 5 righe e le aggiungo al dataframe
duplicati = df_corse.head(5)
df_corse = pd.concat([df_corse, duplicati], ignore_index=True)

#prendo delle righe a caso 
righe_nan_durata = [10, 20, 30, 40]
righe_nan_km = [15, 25, 35, 45]

#sostituisco con i valori NaN
for riga in righe_nan_durata:
    df_corse.at[riga, "durata_minuti"] = np.nan

for riga in righe_nan_km:
    df_corse.at[riga, "km_percorsi"] = np.nan

print(df_corse)

#6.2 - PULIZIA DATI
#print prima della pulizia 
print(df_corse.info())
print(df_corse.describe())

#rimuovo duplicati
df_corse = df_corse.drop_duplicates()

#NaN durata minuti 
df_corse['durata_minuti'] = df_corse.groupby('citta')['durata_minuti'].transform(lambda x: x.fillna(x.median()))

#NaN km_percorsi
df_corse['km_percorsi'] = df_corse['km_percorsi'].fillna(df_corse['durata_minuti'] * 0.18)

#conversione data_corsa stringa - datetime
df_corse['data_corsa'] = pd.to_datetime(df_corse['data_corsa'])

#aggiunta colonna mese e giorno settimana
df_corse['mese'] = df_corse['data_corsa'].dt.month
df_corse['giorno_settimana'] = df_corse['data_corsa'].dt.day_name()

#print dopo la pulizia
print(df_corse.info())
print(df_corse.describe())

#6.3 - APPLY E COLONNE DERIVATE
#applico classifica_corsa()
df_corse['tipo_corsa'] = df_corse['durata_minuti'].apply(classifica_corsa)

#calcolo velocità media
df_corse['velocita_media'] = df_corse['km_percorsi'] / (df_corse['durata_minuti'] / 60)

#calcolo costo_stimato
def calcola_costo(minuti):
    if minuti < 15:
        return 1.50
    elif 15 <= minuti <= 45:
        return 2.50 + 0.10 * (minuti - 15)
    else:
        return 5.00 + 0.08 * (minuti - 45)

df_corse['costo_stimato'] = df_corse['durata_minuti'].apply(calcola_costo)

#6.4 - AGGREGAZIONE E MERGE
#groupby per citta
agg_citta = df_corse.groupby('citta').agg(
    numero_corse=('id_corsa', 'count'),
    durata_media=('durata_minuti', 'mean'),
    km_totali=('km_percorsi', 'sum'),
    costo_totale=('costo_stimato', 'sum'))

#groupby per fascia_oraria
agg_fascia = df_corse.groupby('fascia_oraria').agg(
    numero_corse=('id_corsa', 'count'),
    velocita_media=('velocita_media', 'mean'))

#pivot table
pivot_corse = df_corse.pivot_table(index='citta', columns='tipo_corsa', values='id_corsa', aggfunc='count', fill_value=0)

#merge 
#rinomino le colonne citta perché sono uguali
df_bici_rinominato = df_bici.rename(columns={'citta': 'citta_bici'})
df_utenti_rinominato = df_utenti.rename(columns={'citta': 'citta_utente'})

df_unito = df_corse.merge(df_bici_rinominato, on='id_bici')
df_finale = df_unito.merge(df_utenti_rinominato, on='id_utente')

#print prime 5 righe
print(df_finale.head(5))

#5 biciclette con più corse
top_bici = df_corse['id_bici'].value_counts().head(5)

print(f"\n5 biciclette con più corse:\n {top_bici}")

#3 utenti premium con costo totale più alto
top_premium = df_finale[df_finale['tipo_abbonamento'] == 'Premium'].groupby('id_utente')['costo_stimato'].sum().sort_values(ascending=False).head(3)

print(f"\n3 utenti premium con costo totale più alto:\n {top_premium}")

#statistica aggiuntiva - 3 fasce orarie con più corse
top_fasce = df_corse['fascia_oraria'].value_counts().head(3)

print(f"\n3 fasce orarie con più corse:\n {top_fasce}")

#statistica aggiuntiva - 5 corse più lunghe di km
top_corse = df_corse[['id_corsa', 'citta', 'km_percorsi', 'durata_minuti']].sort_values(by='km_percorsi', ascending=False).head(5)

print(f"\n5 corse più lunghe in km:\n {top_corse}")

print(df_finale)