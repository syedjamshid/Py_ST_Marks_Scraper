import streamlit as st
import os, shutil, logging

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
    else:
        st.error('You have Nothing to Do Here 🤪')


