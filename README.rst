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
~~~~~~~~~~~~~~~~~~~

All the following configuration is done in the file nginx.conf, which can be found
either in /usr/local/nginx/conf/ or in whether directory you compiled Nginx in.

Balanced servers
~~~~~~~~~~~~~~~~

To show how Nginx' balancing works, we are starting 4 Python-based web servers,
each of them serving a HTML page.
The http.server library is a very small Python3 standard library, which can serve
static HTML pages.

The servers are being started like this (Python3 required):

.. code:: bash

    # should point to the directory where the README.pdf can be found
    BASE=`pwd`
    cd $BASE/web/server1
    screen -c /dev/null -dmS server1 python3 -m http.server 8001
    cd $BASE/web/server2
    screen -c /dev/null -dmS server2 python3 -m http.server 8002
    cd $BASE/web/server3
    screen -c /dev/null -dmS server3 python3 -m http.server 8003
    cd $BASE/web/server4
    screen -c /dev/null -dmS server4 python3 -m http.server 8004
    cd $BASE

Weighted Round-Round
~~~~~~~~~~~~~~~~~~~~

.. code:: conf

    #user  nobody;
    worker_processes  99;

    #error_log  logs/error.log;
    #error_log  logs/error.log  notice;
    #error_log  logs/error.log  info;

    #pid        logs/nginx.pid; 


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
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~

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
~~~~~~~


Least connection
----------------

In order to test the balancing, we use the tool Apache Bench, short 'ab', which
simulates c concurrent connections and runs until n total requests were completed.

.. code:: bash

    ab -n 1000000 -c 20 http://127.0.0.1:8000/index.html

The above runs a test with 20 concurrent connections and 1000000 total requests.

When doing that test to a single webserver, the site is either very slow or
entirely unresponsive.

With load balancing, the site is still available, see the following tests:

.. image:: static/request1.jpg
    :width: 90%
    
.. image:: static/request2.jpg
    :width: 90%
    
.. image:: static/request3.jpg
    :width: 90%
    
.. image:: static/request4.jpg
    :width: 90%

Time recording
~~~~~~~~~~~~~~

Andreas Willinger
-----------------

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
Design                            2014-12-12 08:00 08:30   00:30
Least connection                  2014-12-12 08:30 09:00   00:30
Session persistence               2014-12-12 09:00 09:10   00:10
Testing, documentation            2014-12-12 09:10   
**TOTAL**                                                **00:00**
================================= ========== ===== ===== =========

Jakob Klepp
-----------

================================= ========== ===== ===== =========
Task                              Date       From  To    Duration
================================= ========== ===== ===== =========
design                            2014-12-12 08:00 08:30   00:30
Weighted Round-Robin              2014-12-12 08:30 09:00   00:30
vagrant file                      2014-12-12 09:00 
**TOTAL**                                                **00:00**
================================= ========== ===== ===== =========

Sources
~~~~~~~

[1] "Praktische Arbeit 2 zur Vorlesung 'Verteilte Systeme' ETH Zürich, SS 2002", Prof.Dr.B.Plattner, übernommen von Prof.Dr.F.Mattern (http://www.tik.ee.ethz.ch/tik/education/lectures/VS/SS02/Praktikum/aufgabe2.pdf)
[2] http://www.tik.ee.ethz.ch/education/lectures/VS/SS02/Praktikum/loesung2.zip
[3] "Using nginx as HTTP load balancer", NGINX, http://nginx.org/en/docs/http/load_balancing.html, last visited: 2014-12-12