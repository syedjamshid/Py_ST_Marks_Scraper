import smtplib

def CheckSmtpServer(Host, Port):
    try:
        Smtp = smtplib.SMTP(Host, Port)
        Smtp.ehlo()
        Smtp.quit()
        return True
    except:
        return False

# Example usage
Host = "smtp-mail.outlook.com"
Port = 587

if CheckSmtpServer(Host, Port):
    print("SMTP server is accessible")
else:
    print("SMTP server is not accessible")

#Lol, This is Generated with ChatGPT
