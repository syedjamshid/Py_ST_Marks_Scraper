import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from MailSend import *
import logging
from CheckMail import *

logging.basicConfig(filename='Log.txt',format='%(asctime)s  %(clientip)-15s  %(levelname)s: %(message)s',level=logging.INFO)
logging.info('App Started')
st.set_page_config(page_title='SVCET Marks',page_icon='👋', layout='centered')

#--Session Initilization--
if 'PDF_Name' not in st.session_state:
    st.session_state['PDF_Name'] = ''
if 'StudName' not in st.session_state:
    st.session_state['StudName'] = ''

#--Header--
coll1, coll2 = st.columns(2)
with coll1:
    st.title("SVCET Results :stuck_out_tongue_winking_eye:")
    st.subheader("Generate Your Results Easy and :blue[Faster] :rocket:")
with coll2:
    st.markdown('<p><img alt="" src="https://svcetedu.org/wp-content/uploads/2020/03/ll.jpg" style="height:81px; margin-top:30px; width:350px align:center" /></p>',unsafe_allow_html=True)


#--Form--
col1, col2 = st.columns(2)
with col1:
    Roll = st.text_input("Enter Your RollNumber:")
    Passwd = st.text_input("Enter Your Password:")
    Sem = st.slider('Semester', 1, 8, 2)
with col2:
    Admission = st.selectbox('Admission Type: ',('Regular', 'Lateral Entry'))
    StudMail=st.text_input('Enter Your Mail :blue[(Optional -Marks Copy Will Be Sent to Mail)]')
    submit_button = st.button("Get Results", key="submit",help="Fill All The Above Details")
#--Remove Footer--
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("""<p style="text-align:center"><a href="mailto:teamvillain4u+ReportRender@hotmail.com"><span style="font-family:Comic Sans MS,cursive"><span style="font-size:9px"><strong>if you are svcet admin, wana to stop this contact here</strong></span></span></a></p>""",unsafe_allow_html=True)
st.markdown("""<p style="text-align:center"><strong>Made With&nbsp;❤️</strong></p>""",unsafe_allow_html=True)
if submit_button:
    logging.info('Scraping for '+Roll+' '+str(Sem))
    with st.container():
        Total_Process = st.progress(0)
        Url='https://svceta.org/BeesERP/Login.aspx?ReturnUrl=/BeesERP/'
        Roll=Roll.upper()
        fourm={
            "__LASTFOCUS":"",
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"/wEPDwUKLTk1NzEzMjEyNWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDEltZ1VzZXJQaG90b6Y0cgLFn3Bx0z1CYV2nK6HA95DJ0iJRCNXNMDmBgHg5",
            "__VIEWSTATEGENERATOR": "9331F466",
            "__EVENTVALIDATION": "/wEdAAVjVyBLqiX1cxjkBW0I57t2lSfEvot8s98xACen5j++l9L5WsiImyZWZthxHYT/WpZjemWCTRgEB59HPczIGVNwgWOkgugWB5Cq9dYD7toQNOvpRVNtIoB52WCSDT2a3G5fv9JeSWAnZlfxpyP/oCEU",
            "txtUserName": Roll,
            "btnNext": "Next"
        }
        Headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        ErrorMessage=''

        try:
            s=requests.Session()
            #==============[Just Counter]===============
            res=s.get('https://bit.ly/COUNT__ER',headers=Headers)
            #===========================================
            res=s.post(Url,data=fourm,timeout=15)
            b=BeautifulSoup(res.text,'html.parser')
            #print(b.find('span',id="lblWarning").text) 
            if(b.find('span',id="lblWarning").text!='User Name is Incorrect'):
                LoginKeys={}
                for raw in b.find('form').find_all('input'):
                    try:
                        LoginKeys[raw['id']]=raw['value']
                    except:
                        pass
                LoginKeys['txtPassword']=Passwd
            else:
                ErrorMessage='Roll Number/User Name is Incorrect'
            Total_Process.progress(15)
            if(ErrorMessage==''):
                res2=s.post(Url,data=LoginKeys)
                b2=BeautifulSoup(res2.text,"html.parser")

                #Scraping All The Post Request Hedders
                if(b2.head.title.text!='Bees Erp Login'):
                    namestr=b2.find('span',class_="studentname mb-5").text.split('       ')
                    name1=namestr[1].split('(')
                    StudName=name1[0].strip()
                else:
                    ErrorMessage='Given Password Is Worng'
                Total_Process.progress(30)
                if(ErrorMessage==''):
                    Keys1={}
                    for raw in b2.find('form').find_all('input'):
                        try:
                            Keys1[raw['id']]=raw['value']
                        except:
                            pass
                    Keys1['__EVENTTARGET']='ctl00$cpHeader$ucStud$lnkOverallMarksSemwise'
                    Total_Process.progress(40)

                    res2=s.post('https://svceta.org/BeesERP/StudentLogin/MainStud.aspx',Keys1)
                    b3=BeautifulSoup(res2.text,"html.parser")
                    Keys2={}
                    #Scraping All The Post Request Hedders
                    for raw in b3.find('form').find_all('input'):
                        if('ctl00_cpStud_btn' not in raw['id']):
                            try:
                                Keys2[raw['id']]=raw['value']
                            except:
                                pass
                    Total_Process.progress(50)#print(Keys2)
                    #Scraping Available Semisters And Mid Results
                    Btns={}
                    Sems=1 if Admission=='Regular' else 3
                    for btns in b3.find_all('input',class_="btn btn-success btn-sm"):
                        Btns[Sems]={btns['name']:btns['value']}
                        Sems=Sems+1
                    #print(Btns)
                    if(Sem not in Btns.keys()):
                        ErrorMessage=f'Semister {Sem} Results are not Released Yet.\nNote: Fee Due Also a Cause for Not Showing your Results'
                    FKeys={}
                    FKeys.update(Keys2)
                    FKeys.update(Btns[Sem])
                    Total_Process.progress(60)

                    res3=s.post('https://svceta.org/BeesERP/StudentLogin/Student/OverallMarksSemwise.aspx',data=FKeys)
                    bres3=BeautifulSoup(res3.text,"html.parser")

                    Department=bres3.find('span',id="ctl00_cpHeader_ucStudCorner_lblStudentStatus").text
                    ResultsTable = bres3.find('table',id="ctl00_cpStud_grdSemwise")

                    SemDetails=bres3.find('span',id="ctl00_cpStud_lblSemDetails").text
                    Total_Process.progress(80)
                      
                    Total_Process.progress(90)
                    SemSGPA=bres3.find('span',id="ctl00_cpStud_lblSemSGPA").text
                    SemCGPA=bres3.find('span',id="ctl00_cpStud_lblSemCGPA").text

                    #Marks f-String
                    PrintMarks=f'''
                        <p><strong><span style="font-size:16px">Student Name : {StudName}&nbsp;&nbsp;</span></strong></p>
                        <p><strong><span style="font-size:16px">RollNumber : {Roll}&nbsp;&nbsp;</span></strong></p>
                        <p><strong><span style="font-size:16px">Department : {Department}&nbsp;&nbsp;</span></strong></p>
                        <p><strong><span style="font-size:16px">{SemDetails}&nbsp;&nbsp;</span></strong></p>{ResultsTable}
                        <p>&nbsp;</p>
                        <div align="right" style="color:Blue;font-size:large;font-weight:bold;">{SemSGPA}  -   {SemCGPA}</div>
                        <p style="text-align:right"><span style="color:#ffffff"><span style="background-color:#000000">--Generated by Team </span></span><a href="https://t.me/I_AmKarthi"><span style="color:#ffffff"><span style="background-color:#000000">Villlain4U</span></span></a><span style="color:#ffffff"><span style="background-color:#000000">--</span></span><br />
                        &nbsp;</p>
                        <p style="text-align:center"><strong><a href="https://svcet.onrender.com/">Generate Easy And Faster Results</a></strong></p>
                        '''
                    #==============[Just Counter]===============
                    res=s.get('https://bit.ly/PRINT_ED',headers=Headers)
                    #===========================================
                    Total_Process.progress(100)
                    st.header('Here You Go :stuck_out_tongue_winking_eye:')
                    st.markdown(PrintMarks, unsafe_allow_html=True)
                    logging.info('DONE '+Roll)
                    TeamV="""\
                        <p style="text-align:center"><strong><a href="https://github.com/syedjamshid/Py_ST_Marks_Scraper">Team Villain4U</a></strong></p>
                        """
                    st.markdown(TeamV,unsafe_allow_html=True)
                    logging.info('Getting Details From Table')
                    bres3=BeautifulSoup(res3.text,"html.parser")
                    SemDetails=bres3.find('span',id="ctl00_cpStud_lblSemDetails").text
                    #Scraping all The Table Headings
                    for Heads in ResultsTable.find_all('tr',align="center"):
                        C=0
                        Marks_Headings=''
                        for Head in Heads.find_all('th'):
                            if(C==2):
                                Marks_Headings=Marks_Headings+Head.font.text.center(48,' ')+'  '
                            else:
                                Marks_Headings=Marks_Headings+Head.font.text+'  '
                            C=C+1
                    #Scraping all The Marks
                    Marks_SubWise=''
                    TotalRows=0
                    for Rows in ResultsTable.find_all('tr',align="left"):
                        TotalRows+=1
                        C=0
                        for Columns in Rows.find_all('td'):
                            if(C==0):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(5," ")
                            elif (C==1):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(11," ")
                            elif (C==2):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(50," ")
                            elif (C==3):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(14," ")
                            elif (C==4):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(12," ")
                            elif (C==5):
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(9," ")
                            else:
                                Marks_SubWise=Marks_SubWise+Columns.font.text.center(8," ")+'\n'
                            C=C+1
                    logging.info('Got the Details \n'+' '*24+' Now Creating Pdf')
                    #Generating PDF
                    Dir=os.getenv('Dir',default='PDFs')
                    if Dir not in os.listdir():
                        os.mkdir(Dir)
                    pdf = FPDF('L','mm','Letter')
                    pdf.add_page()
                    pdf.set_font('times','B',18)
                    pdf.cell(0,16,'SRI VENKATESWARA COLLEGE OF ENGINEERING & TECHNOLOGY',ln=True,border=True,align='C')
                    pdf.cell(0,4,ln=True)
                    pdf.set_font('Times','',14)
                    pdf.cell(0,8,f'Student Name: {StudName}',ln=1,align='L')
                    pdf.cell(0,8,f'RollNo: {Roll}',ln=1,align='L')
                    pdf.set_font('times','B',16)
                    pdf.cell(0,12,f'{SemDetails.strip()}',ln=1,align='C')
                    pdf.set_font('Courier','B',11)
                    pdf.cell(0,5,f'{Marks_Headings}',ln=1,align='C')
                    pdf.cell(0,5,'='*110,ln=1,align='C')
                    pdf.set_font('Courier','',11)
                    Index_Start=0
                    Index_End=111
                    for i in range(1,TotalRows):
                        pdf.cell(0,5,Marks_SubWise[Index_Start:Index_End],ln=1,align='C')
                        Index_Start+=110
                        Index_End+=110

                    pdf.set_font('Courier','B',11)
                    pdf.cell(0,5,'='*110,ln=1,align='C')
                    pdf.cell(0,5,' '*84+SemSGPA+' '*4+SemCGPA,ln=1,align='C')
                    pdf.cell(0,5,' '*60+'-Team Villain4U https://github.com/Karthi-Villain',ln=1,align='C')
                    pdf.set_font('times','',9)
                    pdf.cell(0,40,'',ln=1)
                    pdf.cell(0,5,"Note: Don't Depend on this Marks, This is Just for an Instant Review of Your Marks. Please Check Your Marks Later from Here https://svceta.org/BeesERP/Login.aspx",ln=1)
                    pdf.cell(0,5,"Marks & PDF are Generated With https://svcet.onrender.com/")
                    PDF_Name=f'{Dir}/Roll-{Roll}_Sem-{Sem}.pdf'
                    pdf.output(PDF_Name)
                    logging.info('PDF Generated Successfully '+PDF_Name+'\n'+' '*24+'Download Started on Client Side')
                    #Getting Session Strings
                    st.session_state['PDF_Name']=PDF_Name
                    st.session_state['StudName']=StudName
                    with open(PDF_Name, "rb") as Pdf_file:
                        PDFbytes = Pdf_file.read()
                    c1,c2,c3=st.columns(3)
                    with c2:
                        st.download_button(label="Download PDF", key='3',
                                data=PDFbytes,
                                file_name=PDF_Name,
                                mime='application/octet-stream')
                    st.success("✅ PDF Downloaded Successfully\nCheck Side Bar for Other Features.(Top Left -> arrow)")                    
                    st.sidebar.success("✅ PDF Downloaded Successfully\nCheck Side Bar for Other Features.")                    

                LOKeys={}
                LOKeys['__EVENTTARGET']='ctl00$cpHeader$ucStudCorner$lnkLogOut'
                LOKeys.update(Keys2)
                LogOut=s.post('https://svceta.org/BeesERP/StudentLogin/Student/OverallMarksSemwise.aspx',data=LOKeys)
                
        except Exception as Ex:
            
            if Ex!='' and ErrorMessage!='':
                logging.info(Ex)
                st.error(ErrorMessage)
                logging.info(ErrorMessage)
            if ErrorMessage=='' and res.status_code==200:
                logging.info('SVCET Site Cant be Reached Right Now')
                st.error('SVCET Site Cant be Reached Right Now\n Taking Long Time To Reach\n Please Try after Some Time.')
        else:
            if ErrorMessage!='':
                st.error(ErrorMessage)
                logging.info(ErrorMessage)

            #--Mailing--
            if StudMail!='':
                if CheckSmtpServer(os.getenv('MServer',default='smtp-mail.outlook.com'),os.getenv('MPort',default=587)):
                    logging.info("SMTP server is accessible."+os.getenv('MServer',default='smtp-mail.outlook.com')+'-'+str(os.getenv('MPort',default=587)))
                    st.write("You Will Recieve a Mail Shortly :smirk:")
                    SendMails(PrintMarks,StudName,StudMail,Roll)

                else:
                    logging.info("SMTP server is not accessible."+os.getenv('MServer',default='smtp-mail.outlook.com')+'-'+str(os.getenv('MPort',default=587)))
