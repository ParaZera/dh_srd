# Countdowns
**Countdowns** repräsentieren einen Zeitraum oder eine Reihe von Ereignissen, die einem zukünftigen Effekt vorausgehen.
Ein Countdown beginnt mit einem Startwert.
Wenn ein Countdown **voranschreitet**, wird er um 1 reduziert.
Der Effekt des Countdowns wird ausgelöst, wenn der Countdown 0 erreicht.

> Hinweis: Du kannst Countdowns verfolgen, indem du Würfel "herunterdrehst" oder Kästchen abhakst.

**Standard-Countdowns** schreiten jedes Mal voran, wenn eine spielende Person einen Aktionswurf macht.
Wenn eine Antagonisten- oder Umgebungsfähigkeit auf einen `Countdown [n]` verweist, dann bedeutet das einen Standard-Countdown mit einem Startwert von `n`.

**Dynamische-Countdowns** schreiten um bis zu 3 voran, abhängig von den Ergebnissen der Aktionswürfe.
**Konsequenz-Countdowns** sind dynamische Countdowns zu negativen Effekten.
**Fortschritts-Countdowns** sind dynamische Countdowns zu positiven Effekten.

Dynamische Countdowns schreiten entsprechend dieser Tabelle voran:

## Dynamisches Countdown-Voranschreiten

| Wurfergebnis | Fortschritts-Voranschreiten | Konsequenz-Voranschreiten |
|--------------|----------------------------|---------------------------|
| Fehlschlag mit Angst | Kein Voranschreiten | Um 3 reduzieren |
| Fehlschlag mit Hoffnung | Kein Voranschreiten | Um 2 reduzieren |
| Erfolg mit Angst | Um 1 reduzieren | Um 1 reduzieren |
| Erfolg mit Hoffnung | Um 2 reduzieren | Kein Voranschreiten |
| Kritischer Erfolg | Um 3 reduzieren | Kein Voranschreiten |

## Erweiterte Countdown-Funktionen

- Countdowns mit **zufälligen Startwerten**

- **Schleifen-Countdowns,** die sich auf ihren Startwert zurücksetzen, nachdem ihr Countdown-Effekt ausgelöst wurde

- **Steigende Countdowns**, die ihren Startwert jedes Mal um 1 erhöhen, wenn sie eine Schleife durchlaufen

- **Sinkende Countdowns**, die ihren Startwert jedes Mal um 1 verringern, wenn sie eine Schleife durchlaufen

- **Verknüpfte Fortschritts- und Konsequenz-Countdowns**, die gleichzeitig entsprechend denselben Aktionswurf-Ergebnissen voranschreiten

- **Langfristige Countdowns**, die nach dem **Rasten** anstatt nach Aktionswürfen voranschreiten