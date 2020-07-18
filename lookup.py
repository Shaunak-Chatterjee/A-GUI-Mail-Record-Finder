import re
import smtplib
import dns.resolver
import os
import sys
import time

try:
	# Address used for SMTP MAIL FROM command  
	fromAddress = 'director.south@nciipc.gov.in'

	# Simple Regex for syntax checking
	regex = '[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

	# Email address to verify
	inputAddress = sys.argv[1]
	addressToVerify = str(inputAddress)

	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print('Bad Syntax')
		raise ValueError('Bad Syntax')

	# Get domain for DNS lookup
	domain = str(inputAddress)
	print('Domain:', domain)

	# MX record lookup
	records = dns.resolver.query(domain, 'MX')
	mxRecord = records[0].exchange
	mxRecord = str(mxRecord)
	try:
		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
		server.mail(fromAddress)
		code, message = server.rcpt(str(addressToVerify))
		server.quit()

		#print(code)
		#print(message)

		# Assume SMTP response 250 is success
		if code == 250:
			print('Success Mx records found ->',mxRecord)
			print()

		else:
			print('MX Record not found Manually, Check json')

	except: 
	# catch *all* exceptions
	   e = sys.exc_info()[0]
	   print( "<p>Error: %s</p>" % e )
	   print(mxRecord)
	   print("Checking SPF records again ...")
	   cmd='python spf.py '
	   cmd=cmd+domain
	   os.system(cmd)
except Exception as e:
	print(e)
finally:
   cmd='checkdmarc '
   cmd=cmd+domain
   print(cmd)
   filename=time.strftime("%Y%m%d-%H%M%S")
   cmd=cmd+' -o '+filename+domain+'.json'
   os.system(cmd)  
        

