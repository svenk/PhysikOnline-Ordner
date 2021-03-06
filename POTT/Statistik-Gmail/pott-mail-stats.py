#!/usr/bin/python

# expects all those csv files present downloaded by gmail and pott
# generators.

from pylab import *
from datetime import date, datetime, timedelta
import csv
from collections import Counter
from scipy.interpolate import *
ion() # interactive plotting on

# Thread-statistiken
# (die werden in dieser Python-File hier nicht benoetigt)
A = recfromtxt("pott_num_edits.csv", delimiter="\t", skip_header=1, invalid_raise=False)
num_edits = array([ a[1] for a in A ])

# daraus kann man jetzt tolle preferential-attachment-statistiken machen

def parse_pott_time(tstamp):
	# exemplary stamp: 2014-10-09T09:49:15+02:00. Ignore timezone
	return datetime.strptime(tstamp[0:len('2014-10-09T09:49:15')], "%Y-%m-%dT%H:%M:%S")
def parse_imap_time(tstamp):
	# exemplary stamp: Sat, 25 Oct 2014 09:55:34 -0000. Ignore timezone
	from email.utils import mktime_tz, parsedate_tz
	return	datetime.fromtimestamp(mktime_tz(parsedate_tz(tstamp)))
	

# Zeit-Statistiken: POTT-Stats
B = recfromtxt("pott_all_edits.csv", delimiter="\t", skip_header=1)
P = array([ parse_pott_time(b[1]) for b in B ])
# in P sind nun eine Menge Zeitstempel fuer den POTT

# Zeit-Statistiken: GMail-Stats.
# numpy ist zu doof das einzulesen
cr = csv.reader(open('gmail-po-statistics-oct2014.csv', "rb"), delimiter="\t")
C = list(cr)[1:]

def is_pott_mail(csv_line):
	return "POTT" in csv_line[0] # POTT in subject of mail

CnP = filter(lambda m: not is_pott_mail(m), C)
print "%d von %d E-Mails sind POTT-Notifications (%f %%)" % (len(C)-len(CnP), len(C), 1-float(len(CnP))/len(C))

G = array([ parse_imap_time(c[1]) for c in CnP])
# in G sind nun eine Menge Zeitstempel fuer Gmail


# Histogramme erstellen
dataLabels = ["POTT-Tickets", "E-Mails"]
data = [P, G]

# a lot of helper functions to get month/week resolutions:
def week_start_date(year, week):
    d = date(year, 1, 1)    
    delta_days = d.isoweekday() - 1
    delta_weeks = week	
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta

# round to month by truncating the day of mont
binMonths = lambda d: date(d.year, d.month, 1)
binWeeks = lambda d: week_start_date(d.year, d.isocalendar()[1])
# choose your binning
binable = binMonths
dataCounter = [ Counter(map(binable, datelist)) for datelist in data ]

# make the time axis
timeBins = sorted(set(flatten([ c.keys() for c in dataCounter ])))
dataBins = [[d[k] for k in timeBins] for d in dataCounter]

# make the matplotlib num timeaxis
timeBinNum = map(date2num, timeBins)
timeSpace = linspace(min(timeBinNum), max(timeBinNum), 300)

# plot
fig, ax = subplots(1)
colors = "bg" # rcmy

for label, data, c in zip(dataLabels,dataBins, colors):
	# interpolieren
	f2 = interp1d(timeBinNum, data, kind='cubic')
	plot_date(timeSpace, f2(timeSpace), "-", label=label, color=c)
	plot_date(timeBinNum, data, "o", color=c, clip_on=False)

fig.autofmt_xdate() # rotate according...
ax.set_ylim(0,axis()[-1]) # crop negative values (interpolation)

legend()

