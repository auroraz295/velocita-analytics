#TABELLE DISPONIBILI 
#corse(id_corsa, id_bici, id_utente, stazione_partenza, stazione_arrivo, data_corsa, durata_minuti, km_percorsi)
#biciclette(id_bici, tipo, citta, stazione_corrente, km_totali)
#utenti(id_utente, nome, citta, tipo_abbonamento, data_iscrizione)
#stazioni(id_stazione, nome, citta, n_posti, latitudine, longitudine)

#D1 — Tutte le corse a Milano ordinate per data decrescente. 
#seleziono dalla tabella CORSE l'id corsa, l'id bici, la data corsa e la durata minuti,
#pongo la condizione in cui la stazione di partenza deve essere Milano e ordino per data decrescente.
SELECT id_corsa, id_bici, data_corsa, durata_minuti
FROM corse
WHERE stazione_partenza LIKE "Milano" 
ORDER BY data_corsa DESC;

#D2 — Quante bici elettriche per ogni città? Ordina dalla città con più bici a quella con meno.
#seleziono dalla tabella CITTA città e faccio un count degli id bici, rinominati con alias numero_bici,
#pongo la condizione in cui il tipo bici deve essere elettrica, raggruppo per città e ordino il numero_bici decrescente.
SELECT citta, COUNT(id_bici) AS numero_bici
FROM biciclette
WHERE tipo LIKE "elettrica"
GROUP BY citta
ORDER BY numero_bici DESC;

#D3 — Durata media, massima e minima per tipo di bicicletta. (JOIN richiesto)
#faccio un inner join tra le tabelle BICICLETTE e CORSA, su id_bici, seleziono id bici e media, massima e minimo della durata_corsa, 
#rinominando tutti e tre con degli alias per comodità e raggruppo per tipo bicicletta.
SELECT biciclette.tipo, AVG(corse.durata_minuti) AS durata_media, MAX(corse.durata_minuti) AS durata_massima, MIN(corse.durata_minuti) AS durata_minima
FROM biciclette INNER JOIN corse ON biciclette.id_bici = corse.id_bici
GROUP BY biciclette.tipo;

#D4 — Stazioni di Milano con più di 50 arrivi in aprile 2026. Ordina per conteggio decrescente.
#faccio un inner join tra le tabelle CORSE E BICICLETTE su id_bici, seleziono stazione arrivo e faccio un count su queste per contare i numeri arrivi,
#pongo la condizione in cui la città deve essere milano e la data corsa deve essere tra il 1 aprile e il 30 aprile,
#raggruppo per stazione arrivo e impongo la condizione sul raggruppamento con having in cui il numero arrivi deve essere
#maggiore di 50 e infine ordino per numero arrivi decrescente.
SELECT corse.stazione_arrivo, COUNT(corse.stazione_arrivo) AS numero_arrivi
FROM corse INNER JOIN biciclette ON corse.id_bici = biciclette.id_bici
WHERE biciclette.citta LIKE "Milano" AND corse.data_corsa BETWEEN "2026-04-01" AND "2026-04-30"
GROUP BY corse.stazione_arrivo
HAVING numero_arrivi > 50
ORDER BY numero_arrivi DESC;

#D5 — Utenti "Premium" con almeno 10 corse: mostra numero corse totali e km totali. (JOIN richiesto)
#faccio un inner join tra UTENTI e CORSE su id_utente, seleziono id_utente, faccio un count delle corse e una somma dei km totali,
#pongo la condizione in cui il tipo abbonamento deve essere premium, raggruppo per utente e impongo
#una condizione sul raggruppamento con having in cui il numero corse deve essere almeno di 10 
SELECT utenti.id_utente, COUNT(corse.id_corsa) as numero_corse, SUM(km_percorsi) as km_totali
FROM utenti INNER JOIN corse ON utenti.id_utente = corse.id_utente
WHERE utenti.tipo_abbonamento LIKE "Premium"
GROUP BY utenti.id_utente
HAVING numero_corse >= 10; 

#D6 — Spiega a parole cosa fa questa query e quale informazione di business produce:
#questa query fa due left join sulle tabelle stazioni (as s), corse (c_in) e corse (c_out) su nome e stazione arrivo 
#e poi su nome e stazione partenza. 
#seleziona dalla tabella stazioni il nome e la città, dalla tabella corse fa count degli arrivi, count delle partenze e 
#un count che sottrae numero arrivi - numero partenze come bilancio
#raggruppa tutto per nome e città e ordina dal bilancio decrescente. 


