# http_to_carbon_graphite
A simple translation service from http requests to graphite (carbon)

At the current state there is no easy way to limit access to carbon if you are using proxy and proxy again etc.
This is a simple idea of a web server which translates http requests and sends them to carbon through http
so you can use nginx or apache and rewrite it with some IP restricions or even header/hashes.

I am using a lot of custom scripts behind a proxy and doing reverse proxy to port 2003 is not ideal when you need to close all network connections
and deal with re-connection etc. This is a very simple approach that I just need thus I am sharing it for someone with a simillar problem.


Usage example:

Don't detach:

`docker run -ti --rm -e "DEBUG=1" -e "GRAPHITE_PORT_2003_TCP_ADDR=2003" -e "GRAPHITE_IP_ADDR=127.0.0.1" -p 127.0.0.1:12006:12006 shellmaster/http_to_carbon_graphite`

Daemon mode: 

When you have locally a proxy server in front of it:

`docker run -d -e "GRAPHITE_PORT_2003_TCP_ADDR=2003" -e "GRAPHITE_IP_ADDR=127.0.0.1" -p 127.0.0.1:12006:12006 shellmaster/http_to_carbon_graphite`

Access to everyone:

`docker run -d -e "GRAPHITE_PORT_2003_TCP_ADDR=2003" -e "GRAPHITE_IP_ADDR=127.0.0.1" -p 12006:12006 shellmaster/http_to_carbon_graphite`


The web server inside the container is listening on port 12006 you can use whatever you wish :)


Optional Variables to Use:

`GRAPHITE_PORT_2003_TCP_ADDR` -- port that carbon is listening on
`GRAPHITE_IP_ADDR` -- carbon IP address
`DEBUG=1` -- will show all access logs (no ip or date, it's only for debug mode) -- it will be super spammy, I am sending more than 10 000 metrics per 10 seconds



And how to send some data to it:

`curl -s http://127.0.0.1:12006/rafal-pc1/varnish/objects/active/1453232 > /dev/null`

if you want to see what is being sent:

`curl -i http://127.0.0.1:12006/rafal-pc1/varnish/objects/active/1453232`

Or (mostly for Windows users) just open your browser and go to:

`http://127.0.0.1:12006/rafal-pc1/varnish/objects/active/1453232`


Good luck!
