import streamlit as st
import base64, time
#--Session Initilization--
if 'PDF_Name' not in st.session_state:
    st.session_state['PDF_Name'] = ''
if 'StudName' not in st.session_state:
    st.session_state['StudName'] = ''

st.title('PDF Tool')
if st.session_state['StudName'] !='' and st.session_state['PDF_Name'] !='':
    st.write(st.session_state['StudName']+' Your PDF is Here')
    PDF_Name=st.session_state['PDF_Name']
    with open(PDF_Name, "rb") as Pdf_file:
        PDFbytes = Pdf_file.read()
    c1,c2,c3=st.columns(3)
    with c2:
        st.download_button(label="Download PDF", key='3',
            data=PDFbytes,
            file_name=PDF_Name,
            mime='application/octet-stream')
    base64_Pdf = base64.b64encode(PDFbytes).decode('utf-8')
    PDF_Display=f'<iframe src="data:application/pdf;base64,{base64_Pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(PDF_Display, unsafe_allow_html=True)
else:
    st.error('Generate Your Results First')
    time.sleep(3)
    st.sidebar.error('Generate Your Results First')
