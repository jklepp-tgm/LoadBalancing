Load Balancing
==============

Aufgabenstellung
~~~~~~~~~~~~~~~~

Es soll ein Load Balancer mit mindestens 2 unterschiedlichen Load-Balancing Methoden (jeweils 7 Punkte) implementiert werden (ähnlich dem PI Beispiel [1]; Lösung zum Teil veraltet [2]). Eine Kombination von mehreren Methoden ist möglich. Die Berechnung bzw. das Service ist frei wählbar!

Folgende Load Balancing Methoden stehen zur Auswahl:

* Weighted Round-Round
* Least Connection
* Least Connected Slow- Start Time
* Weighted Least Connection
* Agent Based Adaptive Balancing / Server Probes

Um die Komplexität zu steigern, soll zusätzlich eine "Session Persistence" (2 Punkte) implementiert werden.
Tests

Die Tests sollen so aufgebaut sein, dass in der Gruppe jedes Mitglied mehrere Server fahren und ein Gruppenmitglied mehrere Anfragen an den Load Balancer stellen. Für die Abnahme wird empfohlen, dass jeder Server eine Ausgabe mit entsprechenden Informationen ausgibt, damit die Verteilung der Anfragen demonstriert werden kann.

Modalitäten

Gruppenarbeit: 2 Personen
Abgabe: Protokoll mit Designüberlegungen / Umsetzung / Testszenarien, Sourcecode (mit allen notwendigen Bibliotheken), Java-Doc, Jar

Nginx installation
~~~~~~~~~~~~~~~~~~

.. code:: bash

    wget http://nginx.org/download/nginx-1.7.8.tar.gz
    tar xf nginx-1.7.8.tar.gz
    cd nginx-1.7.8/
    ./configure --prefix=$(pwd)/..
    make
    make install

Weighted Round-Round
~~~~~~~~~~~~~~~~~~~~

Session Persistence
-------------------

Least Connection
~~~~~~~~~~~~~~~~

Session Persistence
-------------------

Time recording
~~~~~~~~~~~~~~

Andreas Willinger
-----------------

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
**TOTAL**                                                **00:00**
================================= ========== ===== ===== =========

Jakob Klepp
-----------

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
design                            2014-12-12 08:00 08:30   00:30
Weighted Round-Robin              2014-12-12 08:30 
**TOTAL**                                                **00:00**
================================= ========== ===== ===== =========

Sources
~~~~~~~

[1] "Praktische Arbeit 2 zur Vorlesung 'Verteilte Systeme' ETH Zürich, SS 2002", Prof.Dr.B.Plattner, übernommen von Prof.Dr.F.Mattern (http://www.tik.ee.ethz.ch/tik/education/lectures/VS/SS02/Praktikum/aufgabe2.pdf)
[2] http://www.tik.ee.ethz.ch/education/lectures/VS/SS02/Praktikum/loesung2.zip
