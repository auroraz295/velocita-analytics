import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from modulo_pandas import df_finale, df_corse, df_bici, df_utenti

#7 - VISUALIZZAZIONE 
plt.rcParams['font.size'] = 10

#GRAFICO 1 - SERIE TEMPORALE CORSE 
#figura
plt.figure(figsize=(8, 4))

#group by per data e citta
df_timeline = df_corse.groupby(['data_corsa', 'citta']).size().unstack(fill_value=0)

#linea per ogni città nel grafico a linee
for citta in df_timeline.columns:
    plt.plot(df_timeline.index, df_timeline[citta], label=citta)
    
#etichette + titolo + legenda
plt.title("Volume Giornaliero delle Corse per Città")
plt.xlabel("Data")
plt.ylabel("Numero di Corse")
plt.legend()

#salva in png
plt.savefig("velocita-analytics/output/01_serie_temporale.png")

#domanda di business: "come varia il volume delle corse giornaliere per ogni città?"

#GRAFICO 2 - DISTRIBUZIONI DURATE PER CITTA
#tema
sns.set_theme(style="whitegrid")

#figura 
plt.figure(figsize=(8, 4))

#grafico a barre con kde 
sns.histplot(data=df_corse, x='durata_minuti', hue='citta', kde=True, multiple='stack', palette='muted')

#etichette + titolo
plt.title("Distribuzione della Durata delle Corse per Città")
plt.xlabel("Durata in Minuti")
plt.ylabel("Conteggio Corse")

#salva in png
plt.savefig("velocita-analytics/output/02_distribuzione_durate.png")

#domanda di business: "quanto durano in minuti le corse in ogni città?"

#GRAFICO 3 - CORSE PER FASCIA ORARIA E TIPO 
df_fasce_bici = df_corse.merge(df_bici[['id_bici', 'tipo']], on='id_bici')

#figura
plt.figure(figsize=(8, 4))

#grafico a barre
sns.countplot(data=df_fasce_bici, x='fascia_oraria', hue='tipo', palette='Set2')

#etichetta + titolo
plt.title("Distribuzione delle Corse per Fascia Oraria e Tipologia Mezzo")
plt.xlabel("Fascia Oraria")
plt.ylabel("Numero di Corse")

#salva in png
plt.savefig("velocita-analytics/output/03_fasce_orarie.png")

#domanda di business: "l'utilizzo della bicicletta elettrica o classica, varia in base alla fascia oraria?"

#GRAFICO 4 - SCATTER DURATA VS. VELOCITA 
#figura
plt.figure(figsize=(8, 4))

colori_mappa = {'Milano': 'blue', 'Roma': 'green', 'Torino': 'orange'}

#colore diverso per ogni città
for citta, gruppo in df_corse.groupby('citta'):
    plt.scatter(gruppo['durata_minuti'], gruppo['velocita_media'], alpha=0.7, label=citta, c=colori_mappa[citta])

#linea di tendenza complessiva con np.polyfit
#np.polyfit cerca la retta che passa più vicina a tutti i punti del grafico
p = np.polyfit(df_corse['durata_minuti'], df_corse['velocita_media'], 1)
x_linea = np.linspace(df_corse['durata_minuti'].min(), df_corse['durata_minuti'].max(), 100)
plt.plot(x_linea, np.polyval(p, x_linea), color='red', linestyle='--', label='Trend Globale')

#etichette + titolo + legenda
plt.title("Correlazione tra Durata Corsa e Velocità Media")
plt.xlabel("Durata (minuti)")
plt.ylabel("Velocità Media (km/h)")
plt.legend()

#salva in png
plt.savefig("velocita-analytics/output/04_scatter_durata_velocita.png")

#domanda di business: "c'è una correlazione tra la durata della corsa e la velocità media?"

#GRAFICO 5- DASHBOARD RIEPILOGATIVA 
#creazione griglia per i subplot
fig, axs = plt.subplots(2, 2, figsize=(12, 6))
fig.suptitle("Dashboard Direzionale - VeloCittà Analytics", fontsize=16, weight='bold')

#alto sx - bar chart corse per città
corse_citta = df_corse['citta'].value_counts()
axs[0, 0].bar(corse_citta.index, corse_citta.values, color=['skyblue', 'salmon', 'lightgreen'])
axs[0, 0].set_title("Totale Corse per Città")
axs[0, 0].set_ylabel("Frequenza")

#alto dx: pie chart abbonamenti utenti
abbonamenti = df_utenti['tipo_abbonamento'].value_counts()
axs[0, 1].pie(abbonamenti.values, labels=abbonamenti.index, autopct='%1.1f%%', colors=['gold', 'orchid'], startangle=90)
axs[0, 1].set_title("Ripartizione Tipologia Utenti")

#basso sx: bar chart costo totale per città
ricavi_citta = df_corse.groupby('citta')['costo_stimato'].sum()
axs[1, 0].bar(ricavi_citta.index, ricavi_citta.values, color=['darkblue', 'darkred', 'darkgreen'])
axs[1, 0].set_title("Ricavi Totali Stimati per Città (€)")
axs[1, 0].set_ylabel("Euro (€)")

#basso dx: boxplot durate per tipo corsa 
sns.boxplot(data=df_corse, x='tipo_corsa', y='durata_minuti', ax=axs[1, 1], palette='Pastel1', order=['breve', 'media', 'lunga'])
axs[1, 1].set_title("Varianza della Durata per Categoria di Corsa")
axs[1, 1].set_xlabel("Fascia Corsa")
axs[1, 1].set_ylabel("Minuti")

plt.tight_layout()

#salva in png
plt.savefig("velocita-analytics/output/05_dashboard.png")

plt.show()