import mysql.connector
import json
import random
from datetime import date
from werkzeug.utils import secure_filename
import os
from flask import Flask,render_template,request,make_response

userid = ""
username=""

gcname=""
gpname=""
gpid=""
gtdate=""
gopsmgr=""
grcname=""
grpname=""
grpid=""
gropsmgr=""
grtotalcsr=""
grtotalsup=""
grtotaltl=""
grtotalastmgr=""
grtotalmgr=""
grtotalmis=""
csradhar=""
supadhar=""
tladhar=""
astmgradhar=""
mgradhar=""
misadhar=""
globalprocessid=""
interviewadhar=""
managercname=""
manageraadharnum=""
managerquail=""
managerexpi=""


app=Flask(__name__)

@app.route('/')
def index():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT DISTINCT(Type_Of_Users) FROM `hrmsemployee`"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('login.html',data=data)


@app.route('/login')
def login():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT DISTINCT(Type_Of_Users) FROM `hrmsemployee`"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('login.html',data=data)

@app.route('/candidatepage')
def candidatepage():
    return render_template('candidatepage.html')

@app.route('/hrhomepage')
def hrhomepage():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    #sql_Query = "select tblcandidate_register.*,Count(*),tblinterview.Interviewer from tblinterview,tblcandidate_register where tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Statuss='Shortlisted';"
    sql_Query="select tblcandidate_register.*,Count(tblinterview.Candid),tblinterview.Interviewer from tblinterview,tblcandidate_register where tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Statuss='Shortlisted' and tblcandidate_register.Candid in(Select cid from tblsalary_data)  group by tblinterview.Candid;"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('hrpage.html',data=data)
    

@app.route('/hrheadpage')
def hrheadpage():
    return render_template('hrheadpage.html')

@app.route('/operations')
def operations():
    return render_template('operations.html')



@app.route('/quality')
def quality():
    return render_template('quality.html')


@app.route('/ceopagehome')
def ceopagehome():
    return render_template('ceopagehome.html')


@app.route('/recruiterhomepage')
def recruiterhomepage():
    return render_template('recruiterhomepage.html')


@app.route('/recruitermanagerhomepage')
def recruitermanagerhomepage():    
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT * FROM tblcandidate_register where Statuss='RecMgr'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    #print(qualification)

    sql_select_Query = "SELECT Eid,Ename FROM hrmsemployee where Type_Of_Users='Operations'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    mgrdata = cursor.fetchall()
    #print(qualification)

    connection.close()
    cursor.close()
    return render_template('recruitermanagerhomepage.html',candidateslist=data,mgrdata=mgrdata)

#Rec Mgr Approval
@app.route('/recmgrapproval')
def recmgrapproval():    
    cid=request.args['cid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT * FROM tblcandidate_register where Statuss='RecMgr'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    #print(qualification)

    sql_select_Query = "SELECT Eid,Ename FROM hrmsemployee where Type_Of_Users='Operations'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    mgrdata = cursor.fetchall()
    #print(qualification)
    
    sql_select_Query = "insert into tblapproved_candidates values ("+cid+")"
    #print(sql_select_Query)    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()

    sql_select_Query = "Update tblcandidate_register set Statuss='Approved' where Candid="+cid+""
    #print(sql_select_Query)    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('recruitermanagerhomepage.html',candidateslist=data,mgrdata=mgrdata)



#Interview Allocation Approval
@app.route('/interviewalloc')
def interviewalloc():    
    cid=request.args['cid']
    mgr=request.args['mgr']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    
    sql_select_Query = "insert into tblinterview(Candid,Interviewer,Process_requirements,Work_experience,Initiative,Language_fluency,Communication_skills,Personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,Rejection_reason) values ("+cid+",'"+mgr+"','','','','','','','','','','')"
    #print(sql_select_Query)    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('savedcandidatesnew.html')


@app.route('/loginverify',methods=['GET','POST'])
def loginverify():
    eid=request.args['name']
    passwords=request.args['pass']
    print(eid)
    print(passwords)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "select * from hrmsemployee where Eid='"+eid+"' and Pswd='"+passwords+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    newdata = cursor.fetchall()
    print(newdata)
    connection.close()
    cursor.close()
    if(len(newdata)>0):
        employeeid=newdata[0][0]
        employeename=newdata[0][1]
        employeetype=newdata[0][2]
        employeepass=newdata[0][3]
        print(employeeid)
        print(employeepass)
        print(employeetype)
        global userid
        userid=employeeid
        global username
        username=employeename
        if employeetype!="":            
            msg=employeetype
        else:
            msg="Credentials not found"
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp
'''            
        if employeetype =="Operations":
            return render_template('operations.html')
        elif employeetype=="Recruiter":
            return render_template('recruiterhomepage.html')
        elif employeetype=="Recruiter Manager":
            return render_template('recruitermanagerhomepage.html')
        elif employeetype=="Quality":
            return render_template('quailty.html')
        elif employeetype=="HR":
            return render_template('hrpage.html')
        elif employeetype=="HR Head":
            return render_template('hrheadpage.html')
        elif employeetype=="CEO":
            print('hi')            
            msg=employeetype
            resp = make_response(json.dumps(msg))
            print(msg, flush=True)
            return resp
            #return render_template('ceopagehome.html',mesge="CEO")
        else:
            print('data not found in the data list')
            mesge="credentails not found"
            return render_template('login.html',mesge=mesge)
    else:
        print('data not found')
        mesge="credentais not found"
        return render_template('login.html',mesge=mesge)
'''




@app.route('/home')
def home():
    return render_template('dashboard.html')


@app.route('/register', methods=['POST','GET'])
def register():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = " SELECT Qualification FROM databank where Qualification<>''"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    qualification = cursor.fetchall()
    #print(qualification)

    sql_select_Query = " SELECT Experience FROM databank where Experience<>''"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    experience = cursor.fetchall()
    #print(experience)

    sql_select_Query = " SELECT Position FROM databank where Position<>''"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    position = cursor.fetchall()
    #print(position)

    sql_select_Query = " SELECT Source_of_walk_in FROM databank where Source_of_walk_in<>''"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    source = cursor.fetchall()
    #print(source)

    connection.close()
    cursor.close()
    return render_template('register.html',qualification=qualification,experience=experience,position=position,source=source)


@app.route('/masters')
def masters():
    return render_template('masters.html')



@app.route('/registerss', methods =  ['GET','POST'])
def candidateregister():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        fnames=request.form.get('fname')
        print(fnames)
        lnames = request.form.get('lname')
        print(lnames)        
        dob = request.form.get('dob')
        print(dob)
        age = request.form.get('age')
        print(age)
        gen = request.form.get('gender')
        print(gen)
        adders1 = request.form.get('address1')
        print(adders1)
        adders2 = request.form.get('address2')
        print(adders2)
        city = request.form.get('city')
        print(city)
        pin = request.form.get('pin')
        print(pin)
        state = request.form.get('state')
        print(state)
        email = request.form.get('email')
        print(email)
        phnum = request.form.get('phonenumber')
        print(phnum)
        addrnum= request.form.get('addrnum')
        print(addrnum)
        quali = request.form.get('Qualification')
        print(quali)
        exper = request.form.get('experience')
        print(exper)
        posi = request.form.get('position')
        print(posi)
        walkin = request.form.get('Walkin')
        print(walkin)
        language = request.form.get('selres')
        print(language)
        stdates = request.form.get('stdate')
        print(stdates)
        prod_mas = request.files.get('cv')
        filename = secure_filename(prod_mas.filename)
        try:
            prod_mas.save(os.path.join("./static/Resumes/", filename))
        except Exception as e:
            print('Failed to upload to local: '+ str(e))
            print('local upload failed')
        try:
            import ftplib  
            # Fill Required Information
            HOSTNAME = "182.50.132.56"
            USERNAME = "TransactHRMS"
            PASSWORD = "Transact@696"
              
            # Connect FTP Server
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
              
            # force UTF-8 encoding
            ftp_server.encoding = "utf-8"
              
            # Enter File Name with Extension
            #fileroot=os.path.dirname(os.path.abspath(__file__))
            #print(fileroot)            
            # Read file in binary mode
            with open(filename, "rb") as file:
                # Command for Uploading the file "STOR filename"
                ftp_server.storbinary(f"STOR {filename}", file)
              
            # Get list of files
            ftp_server.dir()
              
            # Close the Connection
            ftp_server.quit()
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            print('FTP upload failed')
            

        coletts = request.form.get('covlet')
        print(coletts)
        
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "insert into tblcandidate_register(first_name,last_name,DOB,age,gender,address1,address2,city,pincode,state,email_address,phonenumber,adhar_number,qualification,experience,Positionapplied,walk_in_with,Languages_known,startdate,cv,cover_letter,Statuss) values('"+fnames+"','"+lnames+"','"+dob+"','"+age+"','"+gen+"','"+adders1+"','"+adders2+"','"+city+"','"+pin+"','"+state+"','"+email+"','"+phnum+"','"+addrnum+"','"+quali+"','"+exper+"','"+posi+"','"+walkin+"','"+language+"','"+stdates+"','"+filename+"','"+coletts+"','Open')"
        print(sql_Query) 
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close() 
        return render_template('register.html',data="Data loaded successfully")


   




@app.route('/process')
def processs():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_select_Query = "SELECT Ename FROM hrmsemployee where Type_Of_Users='Operations'"
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    sql_select_Query2 = "SELECT distinct Position FROM databank where Position<>''"
    cursor.execute(sql_select_Query2)
    data2 = cursor.fetchall()
    print(data2)
    connection.close()
    cursor.close()
    return render_template('process.html',data=data,data2=data2)



@app.route('/ceopage')
def ceopage():
    print('hi')
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT ProcessID,CreatedDate,ProcessName,OPSManager,TargetDate,Statuss FROM tblproc_setup order by ProcessId desc" #WHERE Statuss='Pending' 
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    newdata = cursor.fetchall()
    print(newdata)
    connection.close()
    cursor.close()
    return render_template('ceopage.html',newdata=newdata)



@app.route('/ceoprocesspage', methods =  ['GET','POST'])
def ceoprocesspage():
    pid=request.args['pid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT * from tblproc_setup where ProcessID='"+pid+"'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('ceoprocesspage.html',data=data)



@app.route('/ceoviewprocess', methods =  ['GET','POST'])
def ceoviewprocess():
    pname = request.args['pname']
    proID=request.args['pid']
    opsmgr = request.args['opsmgr']
    targetdate = request.args['tdate']
    global gpname 
    gpname = pname
    global gpid
    gpid=proID
    global gopsmgr 
    gopsmgr = opsmgr
    global gtdate 
    gtdate = targetdate
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/managerupdate', methods =  ['GET','POST'])
def managerupdate():
    aadhar_num = request.args['aadhar_num']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update candidate_register set recruiter_mgr_status='Approved' where adhar_number='"+aadhar_num+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Approved successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/managerupdatereject', methods =  ['GET','POST'])
def managerupdatereject():
    aadhar_num = request.args['aadhar_num']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update candidate_register set recruiter_mgr_status='Rejected' where adhar_number='"+aadhar_num+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Rejected successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


newprocessid=""

@app.route('/searchcandidates')
def searchcandidates():
    global grpname
    pname=grpname
    global grpid
    processid=grpid
    global newprocessid
    newprocessid=processid
    global gropsmgr
    opsmgr=gropsmgr
    global grtotalcsr
    totalcsr=grtotalcsr
    global grtotalsup
    totalsup=grtotalsup
    global grtotaltl
    totaltl=grtotaltl
    global grtotalastmgr
    totalastmgr=grtotalastmgr
    global grtotalmgr
    totalmgr=grtotalmgr
    global grtotalmis
    totalmis=grtotalmis
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT * from  recruiter where Process_Name='"+pname+"' and Prcess_ID='"+processid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    sql_select_Query2 = "SELECT Position FROM `databank`"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query2)
    data2 = cursor.fetchall()
    print(data2)
    connection.close()
    cursor.close()
    return render_template('searchcandidates.html',pname=pname,processid=processid,opsmgr=opsmgr,totalcsr=totalcsr,totalsup=totalsup,totaltl=totaltl,totalastmgr=totalastmgr,totalmgr=totalmgr,totalmis=totalmis,data=data,data2=data2)




@app.route('/recruiterpage')
def recruiterpage():
    global userid
    employeeid=userid
    global username
    employeename=username
    print(employeeid)
    print(employeename)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT ProcessName,ProcessID,OPSManager,tblreclist.*,recruiter.* FROM tblreclist,tblproc_setup,recruiter WHERE tblproc_setup.ProcessID=tblreclist.ProcId and recruiter.Prcess_ID=tblreclist.ProcId"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('recruiterpage.html',data=data)


opsmgr=""

@app.route('/selectedcandidates')
def selectedcandidates():
    global userid
    employeeid=userid
    global username
    employeename=username
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select distinct tblcandidate_register.Candid,tblcandidate_register.* from tblinterview,tblcandidate_register where tblinterview.Statuss='Selected' and tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Initiative=''"
    
    print(sql_Query)
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    '''
    addrnum=data[0][12]
    print(addrnum)
    sql_select_Query2 = "select Process_id from candidate_register where adhar_number='"+addrnum+"'"
    print(sql_select_Query2)
    cursor.execute(sql_select_Query2)
    data2 = cursor.fetchall()
    print(data2)
    sql_select_Query3 = "select OPSManager from proc_setup where ProcessID='"+data2[0][0]+"'"
    print(sql_select_Query3)
    cursor.execute(sql_select_Query3)
    data3 = cursor.fetchall()
    print(data3)
    data3=data3[0][0]
    global opsmgr
    opsmgr=data3
    connection.close()
    cursor.close()
    '''
    return render_template('selectedcandidates.html',data=data)



@app.route('/viewcandidate')
def viewcandidate():
    pname = request.args['pname']
    pid=request.args['pid']
    opsmgr = request.args['opsmgr']
    totalcsr = request.args['totalcsr']
    totalsup=request.args['totalsup']
    totaltl=request.args['totaltl']
    totalastmgr=request.args['totalastmgr']
    totalmgr=request.args['totalmgr']
    totalmis=request.args['totalmis']
    global grpname
    grpname=pname
    global grpid
    grpid=pid
    global gropsmgr
    gropsmgr=opsmgr
    global grtotalcsr
    grtotalcsr=totalcsr
    global grtotalsup
    grtotalsup=totalsup
    global grtotaltl
    grtotaltl=totaltl
    global grtotalastmgr
    grtotalastmgr=totalastmgr
    global grtotalmgr
    grtotalmgr=totalmgr
    global grtotalmis
    grtotalmis=totalmis
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp



@app.route('/managerviewcandidate')
def managerviewcandidate():
    cname = request.args['cname']
    cadhar=request.args['cadhar']
    cqulific = request.args['cqulific']
    cexpri = request.args['cexpri']
    global managercname
    managercname=cname
    global manageraadharnum
    manageraadharnum=cadhar
    global managerquail
    managerquail=cqulific
    global managerexpi
    managerexpi=cexpri
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp



@app.route('/managercandidateview')
def managercandidateview():
    global managercname
    cname=managercname
    global manageraadharnum
    cadhar=manageraadharnum
    global managerquail
    cquali=managerquail
    global managerexpi
    cexpi=managerexpi
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "SELECT * FROM `candidate_register` where first_name='"+cname+"' and adhar_number='"+cadhar+"' and recruiter_mgr_status='Pending' "
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('managercandidateview.html',data=data)


  


@app.route('/newrequisition') 
def newrequisition():
    global gpname 
    pname= gpname
    global gpid
    pis=gpid
    global gopsmgr 
    opsmgr = gopsmgr
    global gtdate
    targetdate = gtdate
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_select_Query = "select * from tblproc_setup where  ProcessID='"+pname+"' and OPSManager='"+opsmgr+"' and TargetDate='"+targetdate+"'"
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(sql_select_Query)
    print(data)
    sql_select_Query3="SELECT * FROM databank"
    cursor.execute(sql_select_Query3)
    data3 = cursor.fetchall()
    print("--------------------------------------------")
    print(data3)
    
    connection.close()
    cursor.close()
    
    totalcsr=data[0][5]
    reguler=data[0][6]
    buffer=data[0][7]
    Supervisor=data[0][10]
    tl=data[0][13]
    astmgr=data[0][19]
    mgr=data[0][16]
    mis=data[0][22]
    print(totalcsr)
    print(reguler)
    print(buffer)
    print(Supervisor)
    print(tl)
    skills=data3[0][0]
    data2=data3[0][3]
    print("---------------------------------------------------")
    print(data2)
    shift_timing=data[0][4]
    Qualifications=data[0][1]
    Experiences=data3[0][2]
    languages=data[0][6]
    return render_template('newrequisition.html',data=data,totalcsr=totalcsr,reguler=reguler,buffer=buffer,Supervisor=Supervisor,tl=tl,data3=data3,skills=skills,Qualifications=Qualifications,Experiences=Experiences,astmgr=astmgr,mgr=mgr,mis=mis,shift_timing=shift_timing,languages=languages)




@app.route('/processlist')
def processlist():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "select Ename from hrmsemployee where Eid='"+str(interviewer)+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_select_Query = "SELECT ProcessID,ProcessName,OPSManager,TargetDate FROM tblproc_setup where Statuss='Approved' and OPSManager='"+data2+"'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()
    return render_template('processlist.html',data=data)



@app.route('/rejectprocess',methods =  ['GET','POST'])
def rejectprocess():
    pid=request.args['pid']
    comments=request.args['comments']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update proc_setup set statuss='reject' , comments_for_rejection='"+comments+"' where ProcessID='"+pid+"' "
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/approveprocess',methods =  ['GET','POST'])
def approveprocess():
    pid=request.args['pid']
    totcsr=request.args['totcsr']
    totsup=request.args['totsup']
    tottl=request.args['tottl']
    totmgr=request.args['totmgr']
    totamgr=request.args['totamgr']
    totmis=request.args['totmis']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update tblproc_setup set Statuss='Approved' where ProcessID='"+pid+"' "
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)


    if totcsr!="":
        totcsr=int(totcsr)
    else:
        totcsr=0
        
    if totsup!="":
        totsup=int(totsup)
    else:
        totsup=0
        
    if tottl!="":
        tottl=int(tottl)
    else:
        tottl=0
        
    if totmgr!="":
        totmgr=int(totmgr)
    else:
        totmgr=0
        
    if totamgr!="":
        totamgr=int(totamgr)
    else:
        totamgr=0
        
    if totmis!="":
        totmis=int(totmis)
    else:
        totmis=0
    '''
    print(totcsr)
    print(totsup)
    print(tottl)
    print(totmgr)
    print(totamgr)
    print(totmis)
    '''

    for i in range(totcsr):
        tid="CSR"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','CSR','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
   
    for i in range(totsup):
        tid="Sup"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','Supervisor','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)    
   
    for i in range(tottl):
        tid="TL"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','Team Lead','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)   
   
    for i in range(totmgr):
        tid="Mgr"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','Manager','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)   
   
    for i in range(totamgr):
        tid="AMgr"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','Asst. Manager','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)  
   
    for i in range(totmis):
        tid="MIS"+str(i+1)
        sql_select_Query = "insert into tblreclist(ProcId,Taskid,Designation,Statuss) values ("+pid+",'"+tid+"','MIS','Open')"
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)  

    
    connection.commit()
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp
    




@app.route('/viewprocess', methods =  ['GET','POST'])
def newrequisitions():
    pname = request.args['pname']
    proID=request.args['pid']
    opsmgr = request.args['opsmgr']
    targetdate = request.args['tdate']
    global gpname 
    gpname = pname
    global gpid
    gpid=proID
    global gopsmgr 
    gopsmgr = opsmgr
    global gtdate 
    gtdate = targetdate
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp




    

@app.route('/createnewprocess', methods =  ['GET','POST'])
def createnewprocess():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    pname = request.args['pname']
    opsmgr = request.args['opsmgr']
    targetdate = request.args['targetdate']
    salarybudget = request.args['salarybudget']
    tot_csr = request.args['tot_csr']
    regular = request.args['regular']
    buffer = request.args['buffer']
    csr_min = request.args['csr_min']
    csr_max = request.args['csr_max']
    tot_sup = request.args['tot_sup']
    sup_min = request.args['sup_min']
    sup_max = request.args['sup_max']
    tot_tl = request.args['tot_tl']
    tl_min = request.args['tl_min']
    tl_max = request.args['tl_max']
    tot_astmgr = request.args['tot_astmgr']
    ast_max = request.args['ast_max']
    ast_min = request.args['ast_min']
    tot_mgr = request.args['tot_mgr']
    mgr_min=request.args['mgr_min']
    mgr_max=request.args['mgr_max']
    tot_mis=request.args['tot_mis']
    mis_min=request.args['mis_min']
    mis_max=request.args['mis_max']
    cursor = connection.cursor()
    today = date.today()
    tdate = today.strftime("%d-%b-%Y")
    #print("d4 =", d4)
    sql_Query = "insert into tblproc_setup(ProcessName,OPSManager,TargetDate,SalaryBudget,TotCSR,Regular,Buffer,CSRMinSal,CSRMaxSal,Supervisor,SupMinSal,SupMaxSal,TeamLeader,TLMinSal,TLMaxSal,Managers,MgrMinSal,MgrMaxSal,AsstMgrs,AsstMinSal,AsstMaxSal,MIS,MISMinSal,MISMaxSal,Statuss,RejectionComments,CreatedDate) values('"+pname+"','"+opsmgr+"','"+targetdate+"','"+salarybudget+"','"+tot_csr+"','"+regular+"','"+buffer+"','"+csr_min+"','"+csr_max+"','"+tot_sup+"','"+sup_min+"','"+sup_max+"','"+tot_tl+"','"+tl_min+"','"+tl_max+"','"+tot_astmgr+"','"+ast_max+"','"+ast_min+"','"+tot_mgr+"','"+mgr_min+"','"+mgr_max+"','"+tot_mis+"','"+mis_min+"','"+mis_max+"','Pending','','"+tdate+"')"
    print(sql_Query)    
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


""" @app.route('/updatenewprocess', methods =  ['GET','POST'])
def updatenewprocess():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cname = request.args['cname']
    pname = request.args['pname']
    pid = request.args['pid']
    opsmgr = request.args['opsmgr']
    targetdate = request.args['targetdate']
    overallbudget = request.args['overallbudget']
    salarybudget = request.args['salarybudget']
    totSupervisor = request.args['totSupervisor']
    totteamleder = request.args['totteamleder']
    totopsmgr = request.args['totopsmgr']
    regular = request.args['regular']
    buffer = request.args['buffer']
    minsal1 = request.args['minsal1']
    maxsal1 = request.args['maxsal1']
    minsal2 = request.args['minsal2']
    maxsal2 = request.args['maxsal2']
    minsal3 = request.args['minsal3']
    maxsal3 = request.args['maxsal3']
    training = request.args['training']
    quality = request.args['quality']
    cursor = connection.cursor()
    sql_Query = "update  proc_setup set ClientName='"+cname+"' , ProcessName='"+pname+"',OPSManager='"+opsmgr+"',TargetDate='"+targetdate+"',OverallBudget='"+overallbudget+"',SalaryBudget='"+salarybudget+"',CSR='"+totopsmgr+"',Regular='"+regular+"',Buffer='"+buffer+"',Supervisor='"+totSupervisor+"',TeamLeader='"+totteamleder+"',CSRMinSal='"+minsal1+"',CSRMaxSal='"+maxsal1+"',SupMinSal='"+minsal2+"',SupMaxSal='"+maxsal2+"',TLMinSal='"+minsal3+"',TLMaxSal='"+maxsal3+"',Training='"+training+"',Quality='"+quality+"',statuss='pending' where ProcessID='"+pid+"' "
                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp
 """



@app.route('/recruit', methods =  ['GET','POST'])
def recruiterscsr():
    pname = request.args['pname']
    pid=request.args['pid']
    tdate = request.args['tdate']
    job_type = request.args['job_type']
    total_csr=request.args['total_csr']
    buffer=request.args['buffer']
    reguler=request.args['reguler']
    qualification = request.args['qualification']
    experience = request.args['experience']
    skills = request.args['skills']
    shift_timing= request.args['shift_timing']
    langs = request.args['language']
    gender = request.args['gender']
    description = request.args['description']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="select *  from recruiter  where  Process_Name='"+pname+"' and  Prcess_ID='"+pid+"'" 
    print(query)
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    connection.commit()
    print(len(data))
    cur.close()
    connection.close()
    if(len(data)==0):
            connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
            cursor = connection.cursor()
            sql_Query = "insert into recruiter(Process_Name,Prcess_ID,Target_Date,Job_type,Regular,Buffer,total_CSR,CSRqualification,CSRexperience,CSRSkills,CSRShift_Timing,CSRLanguages,CSRGender,CSRdiscription) values('"+pname+"','"+pid+"','"+tdate+"','"+job_type+"','"+reguler+"','"+buffer+"','"+total_csr+"','"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')" 
            cursor.execute(sql_Query)
            print(sql_Query)
            connection.commit() 
            connection.close()
            cursor.close()
            msg="Data stored successfully"
            resp = make_response(json.dumps(msg))
            print(msg, flush=True)
            return resp
    else:
        msg="alredy registerd"      
        resp=make_response(json.dumps(msg))
        return resp
    

    



@app.route('/recruitsup', methods =  ['GET','POST'])
def recruiterssup():
   pname = request.args['pname']
   tdate = request.args['tdate']
   pid = request.args['pid']
   print(pid)
   totlsup=request.args['totalsup']
   job_type = request.args['job_type']
   qualification = request.args['qualification']
   experience = request.args['experience']
   skills = request.args['skills']
   shift_timing= request.args['shift_timing']
   langs = request.args['language']
   gender = request.args['gender']
   description = request.args['description']
   connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
   cur=connection.cursor()
   query="select *  from recruiter   where   Prcess_ID='"+pid+"'" 
   print(query)
   cur.execute(query)
   data=cur.fetchall()
   print(data)
   connection.commit()
   print(len(data))
   cur.close()
   connection.close()
   if(len(data)>0):
       connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
       cursor = connection.cursor()
       sql_Query = "UPDATE recruiter SET total_SUP='"+totlsup+"', SUPjob_type='"+job_type+"',SUPqualification = '"+qualification+"',SUPexperience='"+experience+"',SUPSkills='"+skills+"',SUPShift_Timing='"+shift_timing+"',SUPLanguages='"+langs+"',SUPGender='"+gender+"',SUPdiscription='"+description+"' WHERE Prcess_ID = '"+pid+"'" 
       cursor.execute(sql_Query)
       connection.commit()
       connection.close()
       cursor.close() 
       msg="Data stored successfully"
       resp = make_response(json.dumps(msg))
       print(msg, flush=True)
       return resp
   else:
       connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
       cursor = connection.cursor()
       sql_Query = "insert into recruiter (Process_Name,Prcess_ID,Target_Date,total_SUP,SUPjob_type,SUPqualification,SUPexperience,SUPSkills,SUPShift_Timing,SUPLanguages,SUPGender,SUPdiscription)values('"+pname+"','"+pid+"','"+tdate+"','"+totlsup+"', '"+job_type+"', '"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')"
       cursor.execute(sql_Query)
       connection.commit()
       connection.close()
       cursor.close() 
       msg="registerd successfully"
       resp=make_response(json.dumps(msg))
       return resp




@app.route('/recruittl', methods =  ['GET','POST'])
def recruiterstl():
    pname = request.args['pname']
    tdate = request.args['tdate']
    pid = request.args['pid']
    print(pid)
    totle_tl=request.args['totletl']
    print(totle_tl)
    job_type = request.args['job_type']
    qualification = request.args['qualification']
    experience = request.args['experience']
    skills = request.args['skills']
    shift_timing= request.args['shift_timing']
    langs = request.args['language']
    gender = request.args['gender']
    description = request.args['description']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="select *  from recruiter   where   Prcess_ID='"+pid+"'" 
    print(query)
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    connection.commit()
    print(len(data))
    cur.close()
    connection.close()
    if(len(data)>0):
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "UPDATE recruiter SET  total_TL='"+totle_tl+"',TLjob_type='"+job_type+"',TLqualification = '"+qualification+"',TLexperience='"+experience+"',TLSkills='"+skills+"',TLShift_Timing='"+shift_timing+"',TLLanguages='"+langs+"',TLGender='"+gender+"',TLdiscription='"+description+"' WHERE Prcess_ID = '"+pid+"'" 
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp
    else:
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "insert into recruiter (Process_Name,Prcess_ID,Target_Date,total_TL,TLjob_type,TLqualification,TLexperience,TLSkills,TLShift_Timing,TLLanguages,TLGender,TLdiscription)values('"+pname+"','"+pid+"','"+tdate+"','"+totle_tl+"', '"+job_type+"', '"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')"
        cursor.execute(sql_Query)
        connection.commit()
        connection.close()
        cursor.close() 
        msg="registerd sucessfully"
        resp=make_response(json.dumps(msg))
        return resp



@app.route('/recruitastmgr', methods =  ['GET','POST'])
def recruitersastmgr():
    pname = request.args['pname']
    tdate = request.args['tdate']
    pid = request.args['pid']
    print(pid)
    totle_astmgr=request.args['countofastmgr']
    print(totle_astmgr)
    job_type = request.args['job_type']
    qualification = request.args['qualification']
    experience = request.args['experience']
    skills = request.args['skills']
    shift_timing= request.args['shift_timing']
    langs = request.args['language']
    gender = request.args['gender']
    description = request.args['description']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="select *  from recruiter   where   Prcess_ID='"+pid+"'" 
    print(query)
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    connection.commit()
    print(len(data))
    cur.close()
    connection.close()
    if(len(data)>0):
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "UPDATE recruiter SET  total_Astmgr='"+totle_astmgr+"',Astmgr_job_type='"+job_type+"',Astmgr_qualification = '"+qualification+"',Astmgr_experience='"+experience+"',Astmgr_Skills='"+skills+"',Astmgr_Shift_Timing='"+shift_timing+"',Astmgr_Languages='"+langs+"',Astmgr_Gender='"+gender+"',Astmgr_discription='"+description+"' WHERE Prcess_ID = '"+pid+"'" 
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp
    else:
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "insert into recruiter (Process_Name,Prcess_ID,Target_Date,total_Astmgr,Astmgr_job_type,Astmgr_qualification,Astmgr_experience,TLSkills,Astmgr_Shift_Timing,Astmgr_Languages,Astmgr_Gender,Astmgr_discription) values('"+pname+"','"+pid+"','"+tdate+"','"+totle_astmgr+"', '"+job_type+"', '"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')"
        cursor.execute(sql_Query)
        connection.commit()
        connection.close()
        cursor.close() 
        msg="alredy registerd"
        resp=make_response(json.dumps(msg))
        return resp






@app.route('/recruitmgr', methods =  ['GET','POST'])
def recruitermgr():
    pname = request.args['pname']
    tdate = request.args['tdate']
    pid = request.args['pid']
    print(pid)
    total_mgr=request.args['countofmgr']
    print(total_mgr)
    job_type = request.args['job_type']
    qualification = request.args['qualification']
    experience = request.args['experience']
    skills = request.args['skills']
    shift_timing= request.args['shift_timing']
    langs = request.args['language']
    gender = request.args['gender']
    description = request.args['description']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="select *  from recruiter   where   Prcess_ID='"+pid+"'" 
    print(query)
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    connection.commit()
    print(len(data))
    cur.close()
    connection.close()
    if(len(data)>0):
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "UPDATE recruiter SET  total_Mgr='"+total_mgr+"',Mgr_job_type='"+job_type+"',Mgr_qualification = '"+qualification+"',Mgr_experience='"+experience+"',Mgr_Skills='"+skills+"',Mgr_Shift_Timing='"+shift_timing+"',Mgr_Languages='"+langs+"',Mgr_Gender='"+gender+"',Mgr_discription='"+description+"' WHERE Prcess_ID = '"+pid+"'" 
        print(sql_Query)
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp
    else:
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "insert into recruiter (Process_Name,Prcess_ID,Target_Date,total_Mgr,Mgr_job_type,Mgr_qualification,Mgr_experience,Mgr_Skills,Mgr_Shift_Timing,Mgr_Languages,Mgr_Gender,Mgr_discription) values('"+pname+"','"+pid+"','"+tdate+"','"+total_mgr+"', '"+job_type+"', '"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')"
        cursor.execute(sql_Query)
        connection.commit()
        connection.close()
        cursor.close() 
        msg="alredy registerd"
        resp=make_response(json.dumps(msg))
        return resp



@app.route('/recruitmis', methods =  ['GET','POST'])
def recruitmis():
    pname = request.args['pname']
    tdate = request.args['tdate']
    pid = request.args['pid']
    print(pid)
    total_mis=request.args['countofmis']
    print(total_mis)
    job_type = request.args['job_type']
    qualification = request.args['qualification']
    experience = request.args['experience']
    skills = request.args['skills']
    shift_timing= request.args['shift_timing']
    langs = request.args['language']
    gender = request.args['gender']
    description = request.args['description']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="select *  from recruiter where Prcess_ID='"+pid+"'" 
    print(query)
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    connection.commit()
    print(len(data))
    cur.close()
    connection.close()
    if(len(data)>0):
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "UPDATE recruiter SET  total_Mis='"+total_mis+"',Mis_job_type='"+job_type+"',Mis_qualification = '"+qualification+"',Mis_experience='"+experience+"',Mis_Skills='"+skills+"',Mis_Shift_Timing='"+shift_timing+"',Mis_Languages='"+langs+"',Mis_Gender='"+gender+"',Mis_discription='"+description+"' WHERE Prcess_ID = '"+pid+"'" 
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp
    else:
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
        sql_Query = "insert into recruiter (Process_Name,Prcess_ID,Target_Date,total_Mis,Mis_job_type,Mis_qualification,Mis_experience,Mis_Skills,Mis_Shift_Timing,Mis_Languages,Mis_Gender,Mis_discription) values('"+pname+"','"+pid+"','"+tdate+"','"+total_mis+"', '"+job_type+"', '"+qualification+"','"+experience+"','"+skills+"','"+shift_timing+"','"+langs+"','"+gender+"','"+description+"')"
        cursor.execute(sql_Query)
        connection.commit()
        connection.close()
        cursor.close() 
        msg="alredy registerd"
        resp=make_response(json.dumps(msg))
        return resp




#Sunil
@app.route('/searchcand', methods =  ['GET','POST'])
def searchcand():
    qual=request.args['qual']
    exp=request.args['exp']
    shift=request.args['shift']
    lang=request.args['lang']
    gen=request.args['gen']
    
    languages= lang.split(',')
    shifts=shift.split(',')
    print(shifts)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query="SELECT * FROM tblcandidate_register where qualification = '"+qual+"' and Statuss='Open' and experience='"+exp+"' and ("
    for i in range(len(languages)):
        sql_Query=sql_Query+"Languages_known like '%"+languages[i]+"%' or "
    sql_Query=sql_Query[0:len(sql_Query)-3]
    sql_Query=sql_Query+")"
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp


#Recruiter approval sending Tto rec Mgr
@app.route('/sendtorecmgr',methods=['GET','POST'])
def sendtorecmgr():
    cid=request.args['cid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update tblcandidate_register set Statuss='RecMgr' where Candid='"+cid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Interview Scheduled"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


#Recruiter release rejected candidates
@app.route('/releasetoqueue',methods=['GET','POST'])
def releasetoqueue():
    cid=request.args['cid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "delete from tblapproved_candidates where CandidateId='"+cid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()

    
    sql_select_Query = "delete from tblinterview where Candid='"+cid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()

    
    sql_select_Query = "update tblcandidate_register set Statuss='Open' where Candid='"+cid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    msg="Candidate is released to candidate search pool"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


#Recruiter approval
@app.route('/recruiterapproval',methods=['GET','POST'])
def recruiterapproval():
    cid=request.args['cid']
    mgr=request.args['mgr']
    pname=request.args['pname']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    sql_select_Query = "update tblcandidate_register set Statuss='Approved' where Candid='"+cid+"'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit() 

    sql_select_Query = "insert into tblapproved_candidates values ("+cid+")"
    #print(sql_select_Query)    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()

    
    sql_select_Query = "insert into tblinterview(Candid,Interviewer,Process_requirements,Work_experience,Initiative,Language_fluency,Communication_skills,Personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,Rejection_reason,Pname) values ("+cid+",'"+mgr+"','','','','','','','','','','','"+pname+"')"
    #print(sql_select_Query)    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    msg="Candidate Approved"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


#############################################################
#obsolete
@app.route('/searchcsr', methods =  ['GET','POST'])
def searchcsr():
    csrtotal=request.args['totalcsr']
    csrquli=request.args['csrquli']
    csrexpe=request.args['csrexpe']
    csrshtis=request.args['csrshtis']
    csrlangs=request.args['csrlangs']
    csrgends=request.args['csrgends']
    print(csrtotal)
    languages= csrlangs.split(',')
    shifts=csrshtis.split(',')
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if csrgends=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+csrquli+"' and experience='"+csrexpe+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where (qualification = '"+csrquli+"' and experience='"+csrexpe+"'"
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp






#obsolete
@app.route('/searchsup', methods =  ['GET','POST'])
def searchsup():
    suptotl=request.args['suptotl']
    supquli=request.args['supquli']
    supexp=request.args['supexp']
    supsfti=request.args['supsfti']
    suplang=request.args['suplang']
    supgen=request.args['supgen']
    print(suptotl)
    languages= suplang.split(',')
    shifts=supsfti.split(',')
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if supgen=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+supquli+"' and experience='"+supexp+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+supquli+"' and experience='"+supexp+"'"
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp




#obsolete
@app.route('/searchtl', methods =  ['GET','POST'])
def searchtl():
    totaltl=request.args['totaltl']
    tlquli=request.args['tlquli']
    tlexp=request.args['tlexp']
    tlshti=request.args['tlshti']
    tllan=request.args['tllan']
    tlgen=request.args['tlgen']
    print(totaltl)
    languages= tllan.split(',')
    shifts=tlshti.split(',')
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if tlgen=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+tlquli+"' and experience='"+tlexp+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+tlquli+"' and experience='"+tlexp+"'"
        
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp


#obsolete
@app.route('/searchastmgr', methods =  ['GET','POST'])
def searchastmgr():
    totalastmgr=request.args['totalastmgr']
    astmgrquli=request.args['astmgrquli']
    astmgrexp=request.args['astmgrexp']
    astmgrshti=request.args['astmgrshti']
    astmgrlan=request.args['astmgrlan']
    astmgrgen=request.args['astmgrgen']
    print(totalastmgr)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if astmgrgen=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+astmgrquli+"' and experience='"+astmgrexp+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+astmgrquli+"' and experience='"+astmgrexp+"'"
        
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp   






#obsolete
@app.route('/searchmgr', methods =  ['GET','POST'])
def searchmgr():
    totalmgr=request.args['totalmgr']
    mgrquli=request.args['mgrquli']
    mgrexp=request.args['mgrexp']
    mgrshti=request.args['mgrshti']
    mgrlan=request.args['mgrlan']
    mgrgen=request.args['mgrgen']
    print(totalmgr)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if mgrgen=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+mgrquli+"' and experience='"+mgrexp+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+mgrquli+"' and experience='"+mgrexp+"'"
        
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp   



#obsolete
@app.route('/searchmis', methods =  ['GET','POST'])
def searchmis():
    totalmis=request.args['totalmis']
    misquli=request.args['misquli']
    misexp=request.args['misexp']
    misshti=request.args['misshti']
    mislan=request.args['mislan']
    misgen=request.args['misgen']
    print(totalmis)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query=""
    if misgen=='Any_Gender' or 'Any Gender':
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+misquli+"' and experience='"+misexp+"'"
        
    else:
        sql_Query =""
        print("---------------------------------------------------------------------------------------------------------")
        sql_Query = "SELECT * FROM `candidate_register` where qualification = '"+misquli+"' and experience='"+misexp+"'"
        
    print("final output")
    print(sql_Query)
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    resp = make_response(json.dumps(data))
    print(data, flush=True)
    return resp       



""" @app.route('/regdata', methods =  ['POST'])
def regdata():
    if request.method == 'POST':
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        fnames = request.form['fnames']
        print(fnames)
        lname = request.form['lname']
        print(lname)
        dob = request.form['dob']
        print(dob)
        age = request.form['age']
        print(age)
        gen = request.form['gen']
        print(gen)
        adders1 = request.form['adders1']
        print(adders1)
        adders2 = request.form['adders2']
        print(adders2)
        city = request.form['city']
        print(city)
        pin = request.form['pin']
        print(pin)
        state = request.form['state']
        print(state)
        email = request.form['email']
        print(email)
        phnum = request.form['phnum']
        print(phnum)
        addrnum= request.form['adhnum']
        print(addrnum)
        quali = request.form['quali']
        print(quali)
        exper = request.form['exper']
        print(exper)
        posi = request.form['posi']
        print(posi)
        walkin = request.form['walkin']
        print(walkin)
        shifttimeing = request.form['shifttimeing']
        print(shifttimeing)
        language = request.form['language']
        print(language)
        stdates = request.form['stdates']
        print(stdates)
        cvs = request.form['cvs']
        print(cvs)
        prod_mas = request.files['cvs']
        print(prod_mas)
        filename = secure_filename(prod_mas.filename)
        print(filename)
        prod_mas.save(os.path.join("E:\\Transact-Global-HRMS\\Flask-recruitmentmodel\\static\\resumes", filename))
        fn = os.path.join("E:\\Transact-Global-HRMS\\Flask-recruitmentmodel\\static\\resumes", filename)
        print(fn)
        coletts = request.form['coletts']
        print(coletts)
        cursor = connection.cursor()
        sql_Query = "insert into candidate_register values('"+fnames+"','"+lname+"','"+dob+"','"+age+"','"+gen+"','"+adders1+"','"+adders2+"','"+city+"','"+pin+"','"+state+"','"+email+"','"+phnum+"','"+addrnum+"','"+quali+"','"+exper+"','"+posi+"','"+walkin+"','"+shifttimeing+"','"+language+"','"+stdates+"','"+cvs+"','"+coletts+"')"
        print(sql_Query) 
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close() 
        return render_template('register.html') 

    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    fnames = request.args['fnames']
    lname = request.args['lname']
    dob = request.args['dob']
    age = request.args['age']
    gen = request.args['gen']
    adders1 = request.args['adders1']
    adders2 = request.args['adders2']
    city = request.args['city']
    pin = request.args['pin']
    state = request.args['state']
    email = request.args['email']
    phnum = request.args['phnum']
    addrnum= request.args['adhnum']
    quali = request.args['quali']
    exper = request.args['exper']
    posi = request.args['posi']
    walkin = request.args['walkin']
    shifttimeing = request.args['shifttimeing']
    language = request.args['language']
    stdates = request.args['stdates']
    cvs = request.args['cvs']
    print(cvs)
    prod_mas = request.files['cvs']
    print(prod_mas)
    filename = secure_filename(prod_mas.filename)
    print(filename)
    prod_mas.save(os.path.join("E:\\Transact-Global-HRMS\\Flask-recruitmentmodel\\static\\resumes", filename))
    fn = os.path.join("E:\\Transact-Global-HRMS\\Flask-recruitmentmodel\\static\\resumes", filename)
    print(fn)
    coletts = request.args['coletts']
    cursor = connection.cursor()
    sql_Query = "insert into candidate_register values('"+fnames+"','"+lname+"','"+dob+"','"+age+"','"+gen+"','"+adders1+"','"+adders2+"','"+city+"','"+pin+"','"+state+"','"+email+"','"+phnum+"','"+addrnum+"','"+quali+"','"+exper+"','"+posi+"','"+walkin+"','"+shifttimeing+"','"+language+"','"+stdates+"','"+cvs+"','"+coletts+"')"
    print(sql_Query) 
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp """

@app.route('/candidateviewcsr', methods =  ['GET','POST'])
def candidateviewcsr():

    adharnumber = request.args['adharnumber']
    global csradhar
    csradhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    return resp



@app.route('/candidateviewsup', methods =  ['GET','POST'])
def candidateviewsup():

    adharnumber = request.args['adharnumber']
    global supadhar
    supadhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    return resp


@app.route('/candidateviewtl', methods =  ['GET','POST'])
def candidateviewtl():

    adharnumber = request.args['adharnumber']
    global tladhar
    tladhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/candidateviewastmgr', methods =  ['GET','POST'])
def candidateviewastmgr():

    adharnumber = request.args['adharnumber']
    global astmgradhar
    astmgradhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/candidateviewmgr', methods =  ['GET','POST'])
def candidateviewmgr():

    adharnumber = request.args['adharnumber']
    global mgradhar
    mgradhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/candidateviewmis', methods =  ['GET','POST'])
def candidateviewmis():

    adharnumber = request.args['adharnumber']
    global misadhar
    misadhar=adharnumber
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp







@app.route('/candidateviewdetailscsr')
def candidateviewdetailscsr():
    global csradhar
    adhar=csradhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()

    return render_template('candidatereviewpage.html',data=data)

@app.route('/candidateviewdetailssup')
def candidateviewdetailssup():
    global supadhar
    adhar=supadhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    tladhar=""
    return render_template('candidatereviewpage.html',data=data)


@app.route('/candidateviewdetailstl')
def candidateviewdetailstl():
    global tladhar
    adhar=tladhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('candidatereviewpage.html',data=data)

@app.route('/candidateviewdetailsastmgr')
def candidateviewdetailsastmgr():
    global astmgradhar
    adhar=astmgradhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('candidatereviewpage.html',data=data)



@app.route('/candidateviewdetailsmgr')
def candidateviewdetailsmgr():
    global mgradhar
    adhar=mgradhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('candidatereviewpage.html',data=data)




@app.route('/candidateviewdetailsmis')
def candidateviewdetailsmis():
    global misadhar
    adhar=misadhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+adhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('candidatereviewpage.html',data=data)


@app.route('/recruitermanagerpage')
def recruitermanagerpage():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "SELECT * FROM `candidate_register` WHERE `recruiter_mgr_status`='Pending'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('recruitermanagerpage.html',data=data)

adharnumber=""

@app.route('/selectedcandidateview')
def selectedcandidateview():
    cname= request.args['cname']
    cadhar= request.args['cadhar']
    cqulific= request.args['cqulific']
    cexpri= request.args['cexpri']
    global adharnumber
    adharnumber=cadhar
    msg="Sent For Approval"
    resp=make_response(json.dumps(msg))
    return resp

@app.route('/selectedcandidateviewpage')
def selectedcandidateviewpage():
    global adharnumber
    cadhar=adharnumber
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "SELECT * FROM `candidate_register` where adhar_number='"+cadhar+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    sql_Query2 = "SELECT Process_id FROM `candidate_register` where adhar_number='"+cadhar+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_Query3 = "SELECT OPSManager FROM `proc_setup` where ProcessID='"+data2+"'"
    print(sql_Query3) 
    cursor.execute(sql_Query3)
    data3=cursor.fetchall()
    print(data3)
    datanew=data3[0][0]
    print(datanew)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('selectedcandidateviewpage.html',data=data,datanew=datanew)
 

@app.route('/opsinterview')
def opsinterview():
    aadhar_num = request.args['aadhar_num']
    global newprocessid
    processid=newprocessid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cur=connection.cursor()
    query="update candidate_register  set recruiter_mgr_status='Pending',Process_id='"+processid+"'  where   adhar_number='"+aadhar_num+"'" 
    print(query)
    cur.execute(query)
    connection.commit()
    cur.close()
    connection.close()
    msg="Sent For Approval"
    resp=make_response(json.dumps(msg))
    return resp




@app.route('/interviewedcandidatelist', methods =  ['GET','POST'])
def interviewedcandidatelist():
    aadharnum = request.args['aadharnum']
    global interviewadhar
    interviewadhar=aadharnum
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp



@app.route('/interviewedcandidate')
def viewinterviewedcandidate():
    global interviewadhar
    aadharnum=interviewadhar
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number="+aadharnum+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('interviewedcandidate.html',data=data)

@app.route('/opsmanager')
def opsmanager():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "select Ename from hrmsemployee where Eid='"+interviewer+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_Query = "select * from interviewed_candidate_list where='"+data2+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('opsmanager.html',data=data)



@app.route('/processingcandidate')
def processingcandidate():
    aadhar_num = request.args['aadhar_num']
    interviewername=request.args['interviewername']
    candidatename=request.args['candidatename']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "SELECT Process_id FROM `candidate_register`  where adhar_number='"+aadhar_num+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    data=data[0][0]
    sql_Query2 = "insert into interviewed_candidate_list(candidatename,candidateaadhaarnum,Interviewer,process_id) values('"+candidatename+"','"+aadhar_num+"','"+interviewername+"','"+data+"')"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/operationinterviewcandidate')
def operationinterviewcandidate():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    
    sql_Query = "select tblcandidate_register.Candid,tblcandidate_register.*,tblinterview.Interviewer from tblinterview,tblcandidate_register where tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Initiative=''"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('operationinterviewcandidate.html',data=data)


cadharofcandidate=""
processidops=""
interviewername=""
@app.route('/opscandidateinterview')
def opscandidateinterview():
    caadharid = request.args['caadharid']
    interviewer=request.args['interviewer']
    cname=request.args['cname']
    pid=request.args['pid']
    global cadharofcandidate
    cadharofcandidate=caadharid
    global processidops
    processidops=pid
    global interviewername
    interviewername=interviewer
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

#Operations Candidate OverView
@app.route('/opscandidateoverview')
def opscandidateoverview():
    global cadharofcandidate
    aadharnum=cadharofcandidate
    global interviewername
    datanew=interviewername
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    
    cid=request.args['cid']
    mgr=request.args['mgr']
    sql_Query = "select * from tblcandidate_register where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    
    sql_Query = "select * from tblinterview where Candid="+cid+" and Interviewer='"+mgr+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    interviewdata=cursor.fetchall()
    print(interviewdata)
    
    flagger=1
    if len(interviewdata)==0:
        flagger=0
    else:
        flagger=1



    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('opscandidateoverview.html',data=data,mgr=mgr,cid=cid,interviewdata=interviewdata,flagger=flagger)

#Recruiter Candidate OverView
@app.route('/reccandidateoverview1')
def reccandidateoverview1():
    global cadharofcandidate
    aadharnum=cadharofcandidate
    global interviewername
    datanew=interviewername
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    
    cid=request.args['cid']
    mgr=request.args['mgr']
    pname=request.args['pname']
    sql_Query = "select * from tblcandidate_register where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    sql_Query = "select * from tblinterview where Candid="+cid+" and Interviewer='"+mgr+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    interviewdata=cursor.fetchall()
    print(interviewdata)
    
    sql_Query = "select CSRMaxSal from tblproc_setup where ProcessName='"+str(interviewdata[0][3])+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sal=cursor.fetchall()
    print(sal)

    flagger=1
    if len(interviewdata)==0:
        flagger=0
    else:
        flagger=1


    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('reccandidateoverview1.html',data=data,mgr=mgr,cid=cid,interviewdata=interviewdata,flagger=flagger,pname=pname)

#Recruiter Candidate OverView as table
@app.route('/reccandidateoverview')
def reccandidateoverview():
    global cadharofcandidate
    aadharnum=cadharofcandidate
    global interviewername
    datanew=interviewername
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    
    cid=request.args['cid']
    mgr=request.args['mgr']
    sql_Query = "select * from tblcandidate_register where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    
    sql_Query = "select *, (CONVERT(Process_requirements,Decimal)+CONVERT(Work_experience,Decimal)+CONVERT(Initiative,Decimal)+CONVERT(Language_fluency,Decimal)+CONVERT(Communication_skills,Decimal)+CONVERT(Personality,Decimal)+CONVERT(Thinking_Strategy,Decimal)+CONVERT(Team_Player,Decimal)+CONVERT(Flexibility_for_shifts,Decimal)) AS Total from tblinterview where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    interviewdata=cursor.fetchall()
    print(interviewdata)

    
    
    sql_Query = "select CSRMaxSal from tblproc_setup where ProcessName='"+str(interviewdata[0][3])+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sal=cursor.fetchall()
    sal=sal[0][0]
    print(sal)


    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('reccandidateoverview.html',data=data,mgr=mgr,cid=cid,interviewdata=interviewdata,maxsal=sal)

#HR OPS Candidate OverView as table
@app.route('/hrcandidateoverview')
def hrcandidateoverview():
    global cadharofcandidate
    aadharnum=cadharofcandidate
    global interviewername
    datanew=interviewername
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    
    cid=request.args['cid']
    mgr=request.args['mgr']
    sql_Query = "select * from tblcandidate_register where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    
    sql_Query = "select *, (CONVERT(Process_requirements,Decimal)+CONVERT(Work_experience,Decimal)+CONVERT(Initiative,Decimal)+CONVERT(Language_fluency,Decimal)+CONVERT(Communication_skills,Decimal)+CONVERT(Personality,Decimal)+CONVERT(Thinking_Strategy,Decimal)+CONVERT(Team_Player,Decimal)+CONVERT(Flexibility_for_shifts,Decimal)) AS Total from tblinterview where Candid="+cid+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    interviewdata=cursor.fetchall()
    print(interviewdata)

    
    
    sql_Query = "select CSRMaxSal from tblproc_setup where ProcessName='"+str(interviewdata[0][3])+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sal=cursor.fetchall()
    sal=sal[0][0]
    print(sal)

    
    sql_Query = "select * from tblsalary_data where Pname='"+str(interviewdata[0][3])+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    saltbldata=cursor.fetchall()


    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('hrcandidateoverview.html',data=data,mgr=mgr,cid=cid,interviewdata=interviewdata,maxsal=sal,saltbldata=saltbldata)


@app.route('/statusupload')
def statusupload():
    adharnumb = request.args['adharnumb']
    interviewer=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    rejectcomments=request.args['rejectcomments']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "insert into assessment(candidateadharnum,interviewername,process_requirements,work_experience,Initiative,language_fluency,communication_skills,personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,status,comments_for_rejection) values('"+adharnumb+"','"+interviewer+"','"+Understanding+"','"+workexperience+"','"+initiative+"','"+language+"','"+Communicationskills+"','"+Personality+"','"+Strategically+"','"+teamplayer+"','"+shifts_flexibility+"','rejected','"+rejectcomments+"')"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sql_Query2 = "update interviewed_candidate_list set status='rejected' where candidateaadhaarnum='"+adharnumb+"' and Interviewer='"+interviewer+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp




@app.route('/proceedsendemail')
def proceedsendemail():
    email = request.args['email']
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp



@app.route('/statusuploadpass')
def statusuploadpass():
    adharnumb = request.args['adharnumb']
    interviewer=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "insert into assessment(candidateadharnum,interviewername,process_requirements,work_experience,Initiative,language_fluency,communication_skills,personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,status) values('"+adharnumb+"','"+interviewer+"','"+Understanding+"','"+workexperience+"','"+initiative+"','"+language+"','"+Communicationskills+"','"+Personality+"','"+Strategically+"','"+teamplayer+"','"+shifts_flexibility+"','Passed')"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sql_Query2 = "update interviewed_candidate_list set status='Passed' where candidateaadhaarnum='"+adharnumb+"' and Interviewer='"+interviewer+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

#Recruiter Candidate Assessment Select, Save
@app.route('/recstatusuploadsave')
def recstatusuploadsave():
    cid = request.args['cid']
    intname=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    comments=request.args['comments']
    status=request.args['status']
    pname=request.args['pname']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "insert into tblinterview(Candid,Interviewer,Process_requirements,Work_experience,Initiative,Language_fluency,Communication_skills,Personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,Statuss,Comments,Rejection_reason,Pname) values ("+cid+",'"+intname+"','"+Understanding+"','"+workexperience+"','"+initiative+"','"+language+"','"+Communicationskills+"','"+Personality+"','"+Strategically+"','"+teamplayer+"','"+shifts_flexibility+"','"+status+"','"+comments+"','','"+pname+"')"
    
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Assessment has been recorded"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

#Recruiter Candidate Reject
@app.route('/recstatusuploadsave1')
def recstatusuploadsave1():
    cid = request.args['cid']
    intname=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    comments=request.args['comments']
    status=request.args['status']
    pname=request.args['pname']
    rejectcomments=request.args['rejectcomments']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "insert into tblinterview(Candid,Interviewer,Process_requirements,Work_experience,Initiative,Language_fluency,Communication_skills,Personality,Thinking_Strategy,Team_Player,Flexibility_for_shifts,Statuss,Comments,Rejection_reason,Pname) values ("+cid+",'"+intname+"','"+Understanding+"','"+workexperience+"','"+initiative+"','"+language+"','"+Communicationskills+"','"+Personality+"','"+Strategically+"','"+teamplayer+"','"+shifts_flexibility+"','"+status+"','"+comments+"','"+rejectcomments+"','"+pname+"')"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Assessment has been recorded"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

#Candidate Select, Save
@app.route('/statusuploadsave')
def statusuploadsave():
    cid = request.args['cid']
    intname=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    comments=request.args['comments']
    status=request.args['status']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "update tblinterview set Process_requirements='"+Understanding+"',Work_experience='"+workexperience+"',Initiative='"+initiative+"',Language_fluency='"+language+"',Communication_skills='"+Communicationskills+"',Personality='"+Personality+"',Thinking_Strategy='"+Strategically+"',Team_Player='"+teamplayer+"',Flexibility_for_shifts='"+shifts_flexibility+"',Statuss='"+status+"',Comments='"+comments+"' where Candid="+cid+" and Interviewer='"+intname+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Assessment has been recorded"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


#Candidate Reject
@app.route('/statusuploadsave1')
def statusuploadsave1():
    cid = request.args['cid']
    intname=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    comments=request.args['comments']
    status=request.args['status']
    rejectcomments=request.args['rejectcomments']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "update tblinterview set Process_requirements='"+Understanding+"',Work_experience='"+workexperience+"',Initiative='"+initiative+"',Language_fluency='"+language+"',Communication_skills='"+Communicationskills+"',Personality='"+Personality+"',Thinking_Strategy='"+Strategically+"',Team_Player='"+teamplayer+"',Flexibility_for_shifts='"+shifts_flexibility+"',Statuss='"+status+"',Rejection_reason='"+rejectcomments+"',Comments='"+comments+"' where Candid="+cid+" and Interviewer='"+intname+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Assessment has been recorded"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


#Recruiter Saved Candidates List
@app.route('/savedcandidatesnew')
def savedcandidatesnew():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select distinct tblcandidate_register.Candid,tblcandidate_register.* from tblcandidate_register,tblapproved_candidates where  tblapproved_candidates.CandidateId=tblcandidate_register.Candid"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    sql_select_Query = "SELECT Eid,Ename FROM hrmsemployee where Type_Of_Users='Operations'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    mgrdata = cursor.fetchall()
    #print(qualification)

    connection.close()
    cursor.close()
    return render_template('savedcandidatesnew.html',candidateslist=data,mgrdata=mgrdata)



#Operations Saved candidates List
@app.route('/opsavedcandidates')
def opsavedcandidates():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "select Ename from hrmsemployee where Eid='"+str(interviewer)+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_Query = "select  distinct tblcandidate_register.Candid,tblcandidate_register.*,tblinterview.Interviewer from tblinterview,tblcandidate_register where  tblinterview.Statuss='Saved' and  tblcandidate_register.Candid=tblinterview.Candid"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('opsavedcandidates.html',data=data)

#Recruiter Shortlisted candidates List
@app.route('/recshortlistedcandidates')
def recshortlistedcandidates():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    #sql_Query = "select tblcandidate_register.*,Count(*),tblinterview.Interviewer from tblinterview,tblcandidate_register where tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Statuss='Shortlisted';"
    sql_Query="select tblcandidate_register.*,Count(tblinterview.Candid),tblinterview.Interviewer from tblinterview,tblcandidate_register where tblcandidate_register.Candid=tblinterview.Candid and tblinterview.Statuss='Shortlisted' group by tblinterview.Candid;"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('recshortlistedcandidates.html',data=data)



#Recruiter save salary data
@app.route('/savesalarydata')
def savesalarydata():
    global userid
    interviewer=userid    
    cid = request.args['cid']
    ctc = request.args['ctc']
    grosssal = request.args['grosssal']
    netsal = request.args['netsal']
    pname = request.args['pname']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "insert into tblsalary_data(CTC,Grosssal,Netsal,cid,Pname,Pid) values('"+ctc+"','"+grosssal+"', '"+netsal+"', '"+cid+"', '"+pname+"', '')"
    print(sql_Query) 
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Salary information has been updated"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/savedcandidates')
def savedcandidates():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query2 = "select Ename from hrmsemployee where Eid='"+str(interviewer)+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_Query = "select  distinct tblcandidate_register.Candid,tblcandidate_register.* from tblinterview,tblcandidate_register where  tblinterview.Statuss='Saved' and  tblcandidate_register.Candid=tblinterview.Candid"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('savedcandidates.html',data=data)


#Recruiter Rejected Candidates List
@app.route('/rejectedcandidates')
def rejectedcandidates():
    global userid
    interviewer=userid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select  distinct tblcandidate_register.Candid,tblcandidate_register.* from tblinterview,tblcandidate_register where  tblinterview.Statuss='Rejected' and  tblcandidate_register.Candid=tblinterview.Candid"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)

    sql_select_Query = "SELECT Eid,Ename FROM hrmsemployee where Type_Of_Users='Operations'"
    #print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    mgrdata = cursor.fetchall()
    #print(qualification)

    connection.close()
    cursor.close()
    return render_template('rejectedcandidates.html',candidateslist=data,mgrdata=mgrdata)



newadharnum=""
newinterviewer=""
newprocessid=""

@app.route('/viewsavedcandidates')
def viewsavedcandidates():
    cname = request.args['cname']
    caadharid=request.args['caadharid']
    interviewer=request.args['interviewer']
    pid=request.args['pid']
    global newadharnum
    newadharnum=caadharid
    global newinterviewer
    newinterviewer=interviewer
    global newprocessid
    newprocessid=pid
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp



@app.route('/viewsavedcandidatesnew')
def viewsavedcandidatesnew():
    cname = request.args['cname']
    caadharid=request.args['caadharid']
    interviewer=request.args['interviewer']
    pid=request.args['pid']
    global newadharnum
    newadharnum=caadharid
    global newinterviewer
    newinterviewer=interviewer
    global newprocessid
    newprocessid=pid
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/viewsavedcandidateslist')
def viewsavedcandidateslist():
    global newadharnum
    aadharnum=newadharnum
    global newinterviewer
    interviewer=newinterviewer
    global newprocessid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+aadharnum+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    sql_Query2 = "SELECT * FROM `assessment` where candidateadharnum='"+aadharnum+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    sql_Query3 = "SELECT Ename FROM `hrmsemployee`"
    print(sql_Query3) 
    cursor.execute(sql_Query3)
    data3=cursor.fetchall()
    print(data3)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('viewsavedcandidateslist.html',data=data,interviewer=interviewer,data2=data2,data3=data3)




@app.route('/viewsavedcandidateslistnew')
def viewsavedcandidateslistnew():
    global newadharnum
    aadharnum=newadharnum
    global newinterviewer
    interviewer=newinterviewer
    global newprocessid
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number='"+aadharnum+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    sql_Query2 = "SELECT * FROM `assessment` where candidateadharnum='"+aadharnum+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    sql_Query3 = "SELECT Ename FROM `hrmsemployee`"
    print(sql_Query3) 
    cursor.execute(sql_Query3)
    data3=cursor.fetchall()
    print(data3)
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('viewsavedcandidateslistnew.html',data=data,interviewer=interviewer,data2=data2,data3=data3)



@app.route('/rejectstatusupload')
def rejectstatusupload():
    adharnumb = request.args['adharnumb']
    interviewer=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    rejectcomments=request.args['rejectcomments']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "update  assessment set  status='rejected' where interviewername='"+interviewer+"' and candidateadharnum='"+adharnumb+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sql_Query2 = "update interviewed_candidate_list set status='rejected' where candidateaadhaarnum='"+adharnumb+"' and Interviewer='"+interviewer+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/alterstatusuploadpass')
def alterstatusuploadpass():
    adharnumb = request.args['adharnumb']
    interviewer=request.args['interviewer']
    Understanding=request.args['Understanding']
    workexperience=request.args['workexperience']
    initiative=request.args['initiative']
    language = request.args['language']
    Communicationskills=request.args['Communicationskills']
    Personality=request.args['Personality']
    Strategically=request.args['Strategically']
    teamplayer=request.args['teamplayer']
    shifts_flexibility=request.args['shifts_flexibility']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "update  assessment set  status='rejected' where interviewername='"+interviewer+"' and candidateadharnum='"+adharnumb+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    sql_Query2 = "update interviewed_candidate_list set status='Passed' where candidateaadhaarnum='"+adharnumb+"' and Interviewer='"+interviewer+"'"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/inserttothecandidatelist')
def inserttothecandidatelist():
    aadhar_num = request.args['aadhar_num']
    interviewer=request.args['interviewer']
    canme=request.args['canme']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "SELECT Process_id FROM `candidate_register` where adhar_number='"+aadhar_num+"' "
    print(sql_Query) 
    cursor.execute(sql_Query)
    data2=cursor.fetchall()
    print(data2)
    data2=data2[0][0]
    sql_Query2 = "insert into interviewed_candidate_list(candidatename,candidateaadhaarnum,Interviewer,process_id) values('"+canme+"','"+aadhar_num+"','"+interviewer+"','"+data2+"')"
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


rejectedcname=""
rejectedcaadhar=""
rejectedinterview=""
rejectedpid=""


@app.route('/viewrejectedcandidates')
def viewrejectedcandidates():
    cname = request.args['cname']
    caadharid=request.args['caadharid']
    interviewer=request.args['interviewer']
    pid=request.args['pid']
    global rejectedcname
    rejectedcname=cname
    global rejectedcaadhar
    rejectedcaadhar=caadharid
    global rejectedinterview
    rejectedinterview=interviewer
    global rejectedpid
    rejectedpid=pid
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/viewrejectedcandidateslist')
def viewrejectedcandidateslist():
    global rejectedcname
    cname=rejectedcname
    global rejectedcaadhar
    aadharnum=rejectedcaadhar
    global rejectedinterview
    datanew=rejectedinterview
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select * from candidate_register where adhar_number="+aadharnum+""
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    print(data)
    sql_Query2 = "SELECT * FROM `assessment` where candidateadharnum="+aadharnum+""
    print(sql_Query2) 
    cursor.execute(sql_Query2)
    data2=cursor.fetchall()
    print(data2)
    sql_Query3 = "SELECT Ename FROM `hrmsemployee`"
    print(sql_Query3) 
    cursor.execute(sql_Query3)
    data3=cursor.fetchall()
    print(data3)
    connection.commit() 
    connection.close()
    cursor.close()
    print(datanew)
    return render_template('viewrejectedcandidateslist.html',data=data,datanew=datanew,data2=data2,data3=data3)

@app.route('/moveprocess')
def moveprocess():
    adharnumb = request.args['adharnumb']
    interviewer=request.args['interviewer']
    fname=request.args['fname']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
    cursor = connection.cursor()
    sql_Query = "select Process_id from candidate_register where adhar_number='"+adharnumb+"'"
    print(sql_Query) 
    cursor.execute(sql_Query)
    data=cursor.fetchall()
    data=data[0][0]
    print(data)
    sql_Query = "insert into interviewed_candidate_list(candidatename,candidateaadhaarnum,Interviewer,process_id) values('"+fname+"','"+adharnumb+"','"+interviewer+"','"+data+"')"
    print(sql_Query) 
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp




    


#connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
