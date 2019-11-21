## Ziel:
* Auf den Punkt kommen um das bestimmte Problem in Python darzustellen
* Muss nicht komplett funktionieren
* Wie fühlt sich denn die Sprache an
* Single Process Raft verwenden
* Cluster mit verschiedenen Nodes soll gleichen Datenstand haben. 
(Id => name)
* Unterschiede des parallelitätskonzept von anderer Sprache
* Knoten rufen die zwei Funktionen RequestVote und AppendEntries auf
* code mit unit tests abdecken
* Seitenanzahl in pdf konvertieren (10k-20k Zeichen maximal)
* Quellen beachten
* Programmcode auf Github einchecken
* Leser lernt Sprache am Programmcode
-> Einschätzung bezüglich wie gut sich eine Programmiersprache für ein Problem eignet
* Abgabetermin 9.01.2020 (da wird auch die Präsi sein)
* Vortrag 15min
* 2 Termine: Brückstraße 1/QAWARE, Rosenheim
* http://markdown2pdf.com/ 7-10 Seiten als PDF



Concurrent:

* Parallel: 2 CPUs lassen 2 Programme laufen
* Concurrent: Kann auch auf einer CPU nebenläufig laufen	
* Goroutine != Thread
* Thread blockiert.
* Eine Goroutine ist nochmal in sich gescheduled. Also jede Zeile ist quasi parallelisierbar
* Aus Channel lesen ist fair gescheduled

Raft:
- Löst: Wie können zwei Prozesse sicher sein, dass sie die richtigen Daten
und den gleichen Zustand haben
- Was passiert, wenn Daten in einem Prozess geupdated werden?
- Was passiert, wenn ein Prozess plötzlich ausfällt?
- Ein Teil wird durch netzwerk voneinander getrennt(Netzwerk-Partition)
- Problem tritt in jedem zustandsbehafteten verteilten System auf
- Jede verteilte Datenbank muss dieses Problem lösen
- Raft ist sprachenunabhängig
- Wenn die Mehrheit (Quovum) der Knoten noch funktioniert, kann es noch funktionieren
- Nur die Mehrheit der Knoten = konsistent => ungerade Anzahl an Knoten
- Raft ist CP
- 1 Knoten übernimmt die Steuerung (Master, kann auch ausfallen)
- Wenn Master wegfältt, übernimmt das jemand anderrs
- Der Master kontrolliert die Konsistenz der Daten
- Er benutzt ein 2 Phase protokoll =>
Erst werden die Daten geschickt, dann werden die Daten mit einem erneuten
Kommando sichtbar gemacht
- Master verteilt über Heartbeat den Status
- Wenn Follower die Nachricht zuerst bekommt, leitet er diese an den Master
- Wenn kein Heartbeat in bestimmter Zeit kommt, versucht follower über
candidate master zu werden
- Jeder Knoten kennt alle Ips der anderen Knoten
- Wenn zwei Follower gleichzeitig eine Election starten, kann es passieren, 
dass es unentschieden ausgeht => Kein neuer Master => vielleicht Cluster down
- Raft hängt von Term ab und nicht von einer Systemzeit
- Follower hat Election timeout. Dieser wird resettet, sobald er einen
Heartbeat vom Master bekommt
- Master sendet regelmäßige Heartbeats. Dieser ist kleienr als
der Election timeout und variiert (1/3)
- 


- Paper ausdrucken und durchlesen
-  