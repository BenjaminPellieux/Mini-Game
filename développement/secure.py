from time import strftime,gmtime
from smtplib import SMTP

def raporteur(text):
	serveur=SMTP("smtp.gmail.com",587)
	serveur.starttls()
	serveur.login('sspameur@gmail.com','i_hate_ISN')
	msg=text
	subject="raporteur Game   "+strftime("%a, %d %b %Y %H:%M:%S")
	body="subject: {}\n\n{}".format(subject,msg)
	serveur.sendmail('sspameur@gamil.com','sspameur@gmail.com',body)
	serveur.quit() 