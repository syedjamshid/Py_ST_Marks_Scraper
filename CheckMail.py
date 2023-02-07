import smtplib
import logging
def CheckSmtpServer(Host, Port):
    try:
        logging.info('Checking SMTP') 
        Smtp = smtplib.SMTP(Host,int(Port))
        Smtp.ehlo()
        Smtp.quit()
    except :
        return False
    else:
        return True
#Lol, This is Generated with ChatGPT
