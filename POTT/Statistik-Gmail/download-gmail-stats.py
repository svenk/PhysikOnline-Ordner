#!/usr/bin/python
#
# Slurpt Email-Details in CSV-Stdout.
# erwartet Gmail-Passwort auf Stdin.
#
#


import sys
import imaplib
import getpass # may be used for password input
import email
import email.header
import datetime

def decode_header(value):
	return ' '.join((item[0].decode(item[1] or 'utf-8').encode('utf-8') for item in email.header.decode_header(value)))

def log(msg):
	# easy python3 compatibility
	print >>sys.stderr, msg



M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login("sven.koeppel@gmail.com", getpass.getpass())

rv, mailboxes = M.list()
log(mailboxes)

folder = "Physik eLearning"
folder = "BioKemika"

rv, data = M.select('"%s"' % folder)

# slurp a lot of mails
rv, data = M.search(None, "ALL")
mail_ids = data[0].split()

log("Slurping %d mails from folder '%s' as CSV output!" % (len(mail_ids), folder))

print "Title \t Date"
for mail_id in mail_ids:
	rv, data = M.fetch(mail_id, '(RFC822)')
	msg = email.message_from_string(data[0][1])
	# subject decode:
	subject = decode_header(msg['Subject'])
	# make sure there is no bad character breaking CSV
	subject = subject.translate(None, "\n\r\t")
	# raw date
	date = msg['Date']

	# write a CSV line
	print "%s\t%s" % (subject, date)
