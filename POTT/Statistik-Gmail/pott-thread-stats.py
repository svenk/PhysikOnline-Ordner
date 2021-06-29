#!/usr/bin/python

# expects all those csv files present downloaded by pott generators.

from pylab import *
from scipy import optimize
ion() # interactive plotting on

# Thread-statistiken
A = recfromtxt("pott_num_edits.csv", delimiter="\t", skip_header=1, invalid_raise=False)
num_edits = array([ a[1] for a in A ])

## p = b, C, alpha
#fitfunc = lambda p,x: p[0] + p[1] * x**(-p[2])
#errfunc = lambda p,x,y: fitfunc(p,x) - y
## initial guess:
#p0 = [20., 1000., 2.0]
#
#p1, success = optimize.leastsq(errfunc, p0[:], args=())


subplot(2,1,1)
hist(num_edits, bins=20)
xlabel("Anzahl Ticketantworten")
ylabel("Anzahl Tickets")
title("Histogramm: Wie viel Antworten kriegt ein Ticket?")

subplot(2,1,2)
loglog(num_edits, "o-")
ylabel("Anzahl Ticketantworten")
title("Verteilung der Ticketantworten")
