##############
Load Balancing
##############

Requirements
============

Es soll ein Load Balancer mit mindestens 2 unterschiedlichen Load-Balancing Methoden
(jeweils 7 Punkte) implementiert werden (ähnlich dem PI Beispiel [1]; Lösung zum
Teil veraltet [2]). Eine Kombination von mehreren Methoden ist möglich.
Die Berechnung bzw. das Service ist frei wählbar!

Folgende Load Balancing Methoden stehen zur Auswahl:

* Weighted Round-Round
* Least Connection
* Least Connected Slow- Start Time
* Weighted Least Connection
* Agent Based Adaptive Balancing / Server Probes

Um die Komplexität zu steigern, soll zusätzlich eine "Session Persistence" 
(2 Punkte) implementiert werden.

Auslastung
~~~~~~~~~~

Es sollen die einzelnen Server-Instanzen in folgenden Punkten belastet werden können:

* Memory (RAM)
* CPU Cycles
* I/O Zugriff (Harddisk)

Bedenken Sie dabei, dass die einzelnen Load Balancing Methoden unterschiedlich
auf diese Auslastung reagieren werden. Dokumentieren Sie dabei aufkommenden
Probleme ausführlich.
Tests

Die Tests sollen so aufgebaut sein, dass in der Gruppe jedes Mitglied mehrere
Server fahren und ein Gruppenmitglied mehrere Anfragen an den Load Balancer stellen.
Für die Abnahme wird empfohlen, dass jeder Server eine Ausgabe mit entsprechenden
Informationen ausgibt, damit die Verteilung der Anfragen demonstriert werden kann.

Modalitäten
~~~~~~~~~~~

Gruppenarbeit: 2 Personen
Abgabe: Protokoll mit Designüberlegungen / Umsetzung / Testszenarien, Sourcecode
(mit allen notwendigen Bibliotheken), Java-Doc, Jar

Design
======

We decided to use HTTP, in particular Nginx, as it already supports load balancing
as a reverse proxy.

This saves implementation time, as you only have to configure the server.

Nginx installation
==================

To install Nginx, follow the instructions below.

Alternatively, one can also use the system's package manager, the package name
is nginx.


.. code:: bash

    wget http://nginx.org/download/nginx-1.7.8.tar.gz
    tar xf nginx-1.7.8.tar.gz
    cd nginx-1.7.8/
    ./configure --prefix=$(pwd)/..
    make
    make install

Nginx configuration
===================

All the following configuration is done in the file nginx.conf, which can be found
either in /usr/local/nginx/conf/ or in whether directory you compiled Nginx in.

Balanced servers
================

To show how Nginx' balancing works, we are starting 4 Python-based web servers.

There are 3 available implementations:

* Memory load (memory_load.py)
* CPU cycles (cpu_load.py)
* I/O (io_load.py)

The servers are being started like this (Python3 required):

.. code:: bash

    # should point to the directory where the README.pdf can be found
    BASE=`pwd`
    cd $BASE/web/
    screen -c /dev/null -dmS server1 python3 load.py 8001
    cd $BASE/web/server2
    screen -c /dev/null -dmS server2 python3 load.py 8002
    cd $BASE/web/server3
    screen -c /dev/null -dmS server3 python3 load.py 8003
    cd $BASE/web/server4
    screen -c /dev/null -dmS server4 python3 load.py 8004
    cd $BASE


The general form is like this:

.. code:: bash

    python3 load.py <port>


e.g.:

.. code:: bash

    [..]
    python3 load.py 8001
    [..]


This starts the webserver, listening on port 8001 on all IPs (0.0.0.0).


To access one the implementations, go to one of the following URLS:

* /cpu - CPU load
* /memory - Memory load
* /io - I/O (HDD) load

If none of the above is specified, a static HTML page will be delivered with
the "endpoint" server's port (aka. the servers behind NGinx).


Weighted Round-Round
====================

.. code:: conf

    worker_processes  99;

    events {    
        worker_connections  1024;
    }

    http {
      upstream balancer{
        server 127.0.0.1:8001 weight=3;
        server 127.0.0.1:8002 weight=2;
        server 127.0.0.1:8003 weight=1;
        server 127.0.0.1:8004 weight=1;
      } 
        
      server { 
        listen 8000;
        server_name balancer.web;
        location / {
          proxy_pass http://balancer;
        }
      } 
    }

Least Connection
================

.. code:: conf

    worker_processes  99;

    events {    
        worker_connections  1024;
    }

    http {
      upstream balancer{
        least_conn;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
        server 127.0.0.1:8004;
      } 
        
      server { 
        listen 8000;
        server_name balancer.least_conn;
        location / {
          proxy_pass http://balancer;
        }
      } 
    }

Session Persistence
===================

In Nginx, session persistence can be achieved by using the 'ip_hash' algorithm.
The ip_hash algorithm will assign a client to a server on their first request
and reconnect to the same server on each consecutive one.

If the assigned server becomes unavailable, the client will be re-assigned to
a new server.

Nginx decides which server will be used based on the client's IP address, in
IPv4 the first three octets, in IPv6 the entire address.

It is also possible to weigh each server (similar to weighted RR above).

.. code:: conf

    worker_processes  99;

    events {    
        worker_connections  1024;
    }

    http {
      upstream balancer{
        ip_hash;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
        server 127.0.0.1:8004;
      } 
        
      server { 
        listen 8000;
        server_name balancer.least_conn;
        location / {
          proxy_pass http://balancer;
        }
      } 
    }


Testing
=======

In order to test the balancing, we use the tool Apache Bench, short 'ab', which
simulates c concurrent connections and runs until n total requests were completed.

.. code:: bash

    ab -n 1000000 -c 20 http://127.0.0.1:8000/index.html

The above runs a test with 5 concurrent connections and 100 total requests.

Weighted Round Robin
~~~~~~~~~~~~~~~~~~~~

Memory:

.. image:: _static/mem_weightedrr.jpg
    :width: 70%

*One can see that the LB balances the load around the different instances*

CPU:

.. image:: _static/cpu_weightedrr.jpg
    :width: 70%


I/O:

.. image:: _static/io_weightedrr1.jpg
    :width: 70%

.. image:: _static/io_weightedrr2.jpg
    :width: 70%

Least connection
~~~~~~~~~~~~~~~~

Memory:

.. image:: _static/mem_leastconn.jpg
    :width: 70%

*Different from weightedRR, each instance gets a request (as all are at low load atm)*

CPU:

.. image:: _static/cpu_leastconn.jpg
    :width: 70%


I/O:

.. image:: _static/io_leastconn.jpg
    :width: 70%

Session persistence
~~~~~~~~~~~~~~~~~~~

For this test, we use simple static webpages, to not waste resources on the server.

Request 1:

.. image:: _static/persistence_req1.jpg
    :width: 70%

Request 2:

.. image:: _static/persistence_req2.jpg
    :width: 70%

Request 3:

.. image:: _static/persistence_req3.jpg
    :width: 70%


Time recording
==============

Andreas Willinger
~~~~~~~~~~~~~~~~~

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
Design                            2014-12-12 08:00 08:30   00:30
Least connection                  2014-12-12 08:30 09:00   00:30
Session persistence               2014-12-12 09:00 09:10   00:10
Testing, documentation            2014-12-12 09:10 10:00   00:50
Load                              2014-12-12 10:20 12:40   02:20
Load                              2015-01-09 08:15 09:00   00:45
I/O, Memory fixing                2015-01-09 09:00 10:40   01:40
Testing                           2015-01-13 10:20 11:00   00:40
**TOTAL**                                                **06:45**
================================= ========== ===== ===== =========

Jakob Klepp
~~~~~~~~~~~

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
design                            2014-12-12 08:00 08:30   00:30
Weighted Round-Robin              2014-12-12 08:30 09:00   00:30
vagrant file                      2014-12-12 09:00 10:30   01:30
load                              2014-12-12 10:30 13:00   02:30
selection load type by path       2015-01-09 08:30 09:30   01:00
debugging                         2015-01-09 09:30 10:45   01:15
**TOTAL**                                                **07:15**
================================= ========== ===== ===== =========

Sources
=======

.. _1:

[1] "Praktische Arbeit 2 zur Vorlesung 'Verteilte Systeme' ETH Zürich, SS 2002", Prof.Dr.B.Plattner, übernommen von Prof.Dr.F.Mattern
     http://www.tik.ee.ethz.ch/tik/education/lectures/VS/SS02/Praktikum/aufgabe2.pdf
     last visited: 2014-12-12

.. _2:

[2] "loseung2.zip"
     http://www.tik.ee.ethz.ch/education/lectures/VS/SS02/Praktikum/loesung2.zip
     last visited: 2014-12-12

.. _3:

[3] "Using nginx as HTTP load balancer"
     http://nginx.org/en/docs/http/load_balancing.html
     last visited: 2014-12-12

.. _4:

[4] "Nginx Loadbalancing.rst"
     https://gist.github.com/jklepp-tgm/8912919
     last visited: 2014-12-12


.. header::

    +-------------+-------------------+------------+
    | Title       | Author            | Date       |
    +=============+===================+============+
    | ###Title### | Andreas Willinger | 2015-01-16 |
    |             | — Jakob Klepp     |            |
    +-------------+-------------------+------------+

.. footer::

    ###Page### / ###Total###
