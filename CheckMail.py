import smtplib

def CheckSmtpServer(Host, Port):
    try:
        logging.info('Checking SMTP') 
        Smtp = smtplib.SMTP(Host,Port))
        Smtp.ehlo()
        Smtp.quit()
        return True
    except:
        return False

#Lol, This is Generated with ChatGPT
