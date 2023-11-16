"""
	@Program		   : Python Email Script
	@Author 		   : Adam Hussein
	@Author School	   : Virginia Commonwealth University
	@Author Major	   : Computer Science
	@Description	   : This is the module that runs the email system of BOH.
						 ***This is a personal project that is not intended for public use nor
					  	 for solving any real world problems.***
	@Code Adopted From : https://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems
"""

import smtplib
from email.mime.text import MIMEText

def send_email(sbj, body, recipients):
	sender = 'bankofhusseinboh@gmail.com'
	msg = MIMEText(body)
	msg['Subject'] = sbj
	msg['From'] = sender
	msg['To'] = ', '.join(recipients)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(sender, 'gikwpntoodcmtjxc')
	server.sendmail(sender, recipients, msg.as_string())
	server.quit()