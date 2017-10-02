# Crossover-Assignment
Crossover assignment for Python Software Architect job ad

So i found this job advert online and they wanted a system to log some statistics from some hosts.
The server script connects to hosts it finds in the config.xml file.
It will then upload client.py and some additional files there and then run them
They wanted encryption. Instead of messing with sockets and encryptions to transmit the data, i just piped the data back to the ssh channel. Encryption complete :) I even checked it with Wireshark.
The collected statistics get recorded on a local database.
The server will send emails if there are values above the set limits for each host.
Contact me for more info. :)
