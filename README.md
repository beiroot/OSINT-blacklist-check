Check if you ip/domain is in popular blacklists. 
The script can be used in console or can be easily crontabbed to send you its results everyday via email.

The list is taken from the file blacklists.txt. You can update it with whichever blacklist provider you like.


-------------------------------------------

Blacklist checker.

Usage:
    blacklist-checker [options] --file=<file> [--smtp=<server> --from=<from> --to=<to>] ip <ip>...
    blacklist-checker [options] --file=<file> [--smtp=<server> --from=<from> --to=<to>] domain <domain>...
    blacklist-checker -h | --help

Options:
  -h  --help     Show this screen.
  -t <timeout>   Sets dns query timeout [default: 1]
  -l <lifetime>  Sets dns query lifetime [default: 1]

-t and -l are used to set dns query timeout (wait for response from the server) and lifetime (wait for query to execute)


-------------------------------------------

EXAMPLE USE:

FOR DOMAINS:
/opt/blacklist-checker/blacklist-checker --file=/opt/blacklist-checker/blacklists.txt --smtp=smtp.server.pl --from=noreply@domain.pl --to=email@domain.pl domain mx1.domain.pl mx2.domain.pl

FOR IPs:
/opt/blacklist-checker/blacklist-checker --file=/opt/blacklist-checker/blacklists.txt --smtp=smtp.server.pl --from=noreply@domain.pl --to=email@domain.pl ip 1.1.1.1 8.8.8.8 


-------------------------------------------


RESULTS:
(coloured)
                   virus.rbl.jp: FAILED
        web.dnsbl.sorbs.net: NOT LISTED
             wormrbl.imp.ch: NOT LISTED
               zen.spamhaus.org: LISTED
     zombie.dnsbl.sorbs.net: NOT LISTED


FAILED means the blacklist operator couldn't reached



-------------------------------------------

TO DO:
A switch that would allow to silent the script when crontabbed and send info to e.g log.
