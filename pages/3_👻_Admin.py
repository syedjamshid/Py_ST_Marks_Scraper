import streamlit as st
import os, shutil, logging , smtplib

st.title('🚫:red[Restricted]🚫')
st.subheader(':blue[Only for Admins]')
ParentDir=os.path.dirname(__file__).replace("pages","")
Dir=os.getenv('Dir',default='PDFs')
col1,col2,col3=st.columns([1,1,1])
with col2:
    st.image(os.getenv('Avatar',default='https://github.com/Karthi-Villain/Py_Marks_Scraper/raw/main/Admin.png'),width=224)
    Secret=st.text_input('Secret Key',placeholder='Enter the Secret Key:')

    if Secret == os.getenv('Secret'):
        logging.info('Login Successful')
        st.success('Login Successful')
        Clear_Data=st.button('Clear Data')
        "-----"
        Hosts = ["smtp-mail.outlook.com", "smtp.office365.com","smtp.mail.yahoo.com"]
        Ports = [587, 25, 465]

        Host=st.selectbox('Host',Hosts)
        Port=st.selectbox('Port',Ports)
        CheckSMTP=st.button("Check SMTP")
        Log=open(ParentDir+'/Log.txt')
        st.download_button('Download Log File',
                        data=Log.read(),
                        file_name='Log.txt',
                        mime='text/plain')
        logging.info('Log file Exported Successful')

        if Clear_Data:
            try:
                shutil.rmtree(ParentDir+Dir+'\\')
                logging.info('Cleared Data Successfully - '+ParentDir+Dir)
            except Exception as e:
                logging.warning(e)
        
        if CheckSMTP:
            try:
                logging.info('Checking SMTP') 
                Smtp = smtplib.SMTP(Host,Port)
                Smtp.ehlo()
                Smtp.quit()
                st.success('Working With'+Host+' - '+str(Port))
                logging.info("SMTP server is accessible. "+Host+' - '+str(Port))
                
            except:
                logging.info("SMTP server is not accessible. "+Host+' - '+str(Port))
            else:
                os.environ['MServer']=Host
                os.environ['MPort']=str(Port)
                logging.info('Changed Env Variables to '+Host+' - '+str(Port))
            
    else:
        st.error('You have Nothing to Do Here 🤪')


import streamlit as st
import os, shutil, logging , smtplib

st.title('🚫:red[Restricted]🚫')
st.subheader(':blue[Only for Admins]')
ParentDir=os.path.dirname(__file__).replace("pages","")
Dir=os.getenv('Dir',default='PDFs')
col1,col2,col3=st.columns([1,1,1])
with col2:
    st.image(os.getenv('Avatar',default='https://github.com/Karthi-Villain/Py_Marks_Scraper/raw/main/Admin.png'),width=224)
    Secret=st.text_input('Secret Key',placeholder='Enter the Secret Key:')

    if Secret == os.getenv('Secret'):
        logging.info('Login Successful')
        st.success('Login Successful')
        Clear_Data=st.button('Clear Data')
        "-----"
        Hosts = ["smtp-mail.outlook.com", "smtp.office365.com","smtp.mail.yahoo.com"]
        Ports = [587, 25, 465]

        Host=st.selectbox('Host',Hosts)
        Port=st.selectbox('Port',Ports)
        CheckSMTP=st.button("Check SMTP")
        Log=open(ParentDir+'/Log.txt')
        st.download_button('Download Log File',
                        data=Log.read(),
                        file_name='Log.txt',
                        mime='text/plain')
        logging.info('Log file Exported Successful')

        if Clear_Data:
            try:
                shutil.rmtree(ParentDir+Dir+'\\')
                logging.info('Cleared Data Successfully - '+ParentDir+Dir)
            except Exception as e:
                logging.warning(e)
        
        if CheckSMTP:
            try:
                logging.info('Checking SMTP') 
                Smtp = smtplib.SMTP(Host,Port)
                Smtp.ehlo()
                Smtp.quit()
                st.success('Working With'+Host+' - '+str(Port))
                logging.info("SMTP server is accessible. "+Host+' - '+str(Port))
                
            except:
                logging.info("SMTP server is not accessible. "+Host+' - '+str(Port))
            else:
                os.environ['MServer']=Host
                os.environ['MPort']=str(Port)
                logging.info('Changed Env Variables to '+Host+' - '+str(Port))
            
    else:
        st.error('You have Nothing to Do Here 🤪')
