import smtplib

def CheckSmtpServer():
    try:
        logging.info('Checking SMTP') 
        Smtp = smtplib.SMTP(os.getenv('MServer',default='smtp-mail.outlook.com'),os.getenv('MPort',default=587))
        Smtp.ehlo()
        Smtp.quit()
        return True
    except:
        return False

#Lol, This is Generated with ChatGPT
