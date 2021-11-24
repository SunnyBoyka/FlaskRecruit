

//Login
$("#btn_login").click(function(){
		
			debugger;
			var name=document.getElementById('eid').value;
			var pass=document.getElementById('pass').value;
			
			//alert('Request Exceeds Trial Limit.');
			/*
			if(name=="admin"&&pass=="admin")
			{
				window.location='masters'

			}
			else
			{
				window.location='loginverify?name='+name+'&pass='+pass;				
				
			}
			*/
			
			
			$.ajax({
           type: 'GET',
           url: '/loginverify',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'name': name,
           'pass': pass
       },
           
       dataType:"json",
           success: function(logindata) {
			   logindatacheck(logindata);
			   
      
           },
       });

});


function logindatacheck(ldata)
{
	debugger;
	if(ldata=="CEO")
	{
		window.location="ceopage";
	}
	else if(ldata=="Operations")
	{
		window.location="operations";
	}
	else if(ldata=="Recruiter")
	{
		window.location="recruiterhomepage";
	}
	else if(ldata=="Recruiter Manager")
	{
		window.location="ceopage";
	}
	else if(ldata=="Quality")
	{
		window.location="ceopage";
	}
	else if(ldata=="HR Head")
	{
		window.location="hrheadpage";
	}
	else if(ldata=="HR")
	{
		window.location="hrhomepage";
	}
}


//New Process Creation
$("#btn_proccreate").click(function(){
           
 debugger;
 

 var pname=document.getElementById('process_name').value;
 var opsmgr=document.getElementById('ops_manager').value;
 var targetdate=document.getElementById('target_date').value;
 if(process_name=="" || opsmgr=="" || targetdate=="")
 {
	 alert("Please fill all details");
	 return false;
 }
 
 var salarybudget=document.getElementById('salary_budget').value;
var tot_csr=document.getElementById('CSR').value;
 var tot_sup=document.getElementById('Supervisor').value;
 var tot_tl=document.getElementById('tl').value;
 var tot_astmgr=document.getElementById('astmgr').value;
 var tot_mgr=document.getElementById('mgr').value;
 var tot_mis=document.getElementById('mis').value;
 var csr_max=document.getElementById('csrmaximum_salary').value;
 var tl_max=document.getElementById('tlmaximum_salary').value;
 var sup_max=document.getElementById('supmaximum_salary').value;				 
 var ast_max=document.getElementById('astmgrmaximum_salary').value;
 var mgr_max=document.getElementById('mgrmaximum_salary').value;
 var mis_max=document.getElementById('MISmaximum_salary').value;
 
 
 
 var csr_min=document.getElementById('csrminimum_salary').value;
 var tl_min=document.getElementById('tlminimum_salary').value;
 var sup_min=document.getElementById('supminimum_salary').value;				 
 var ast_min=document.getElementById('astmgrminimum_salary').value;
 var mgr_min=document.getElementById('mgrminimum_salary').value;
var mis_min=document.getElementById('MISminimum_salary').value;
var regular=document.getElementById('regular').value;
var buffer=document.getElementById('buffer').value;
 

var newval=(tot_csr*csr_max)*12;
var newval2=(tot_sup*sup_max)*12;
var newval3=(tot_tl*tl_max)*12;
var newval4=(tot_astmgr*ast_max)*12;
var newval5=(tot_mgr*mgr_max)*12;
var newval6=(tot_mis*mis_max)*12;
var newvals=newval+newval2+newval3+newval4+newval5+newval6;
/*

    if ( 
       document.getElementById('CSR').value =='' || document.getElementById('Supervisor').value =='' ||
       document.getElementById('tl').value =='' ||
       document.getElementById('astmgr').value =='' ||
       document.getElementById('mgr').value =='' ||
       document.getElementById('mis').value =='' || csr_max=='' || tl_max=='' || sup_max=='' || ast_max=='' || mgr_max=='' || mis_max=='' || csr_min=='' || tl_min=='' || sup_min=='' || ast_min=='' || mgr_min=='' || mis_min=='' || regular=='' || buffer=='')

         {
             alert('Please Fill All Fields');
             return false;
         } 
         
*/

         salarybudget=newvals
 $.ajax({
           type: 'GET',
           url: '/createnewprocess',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'pname': pname,
           'opsmgr': opsmgr,
           'targetdate': targetdate,
           'salarybudget': salarybudget,
           'tot_csr':tot_csr,
           'regular':regular,
           'buffer':buffer,
           'csr_min':csr_min,
           'csr_max':csr_max,
           'tot_sup':tot_sup,
           'sup_min':sup_min,
           'sup_max':sup_max,
           'tot_tl':tot_tl,
           'tl_min':tl_min,
           'tl_max':tl_max,
           'tot_astmgr':tot_astmgr,
           'ast_max':ast_max,
           'ast_min':ast_min,
           'tot_mgr':tot_mgr,
           'mgr_min':mgr_min,
           'mgr_max':mgr_max,
           'tot_mis':tot_mis,
           'mis_min':mis_min,
           'mis_max':mis_max
       },
           
       dataType:"json",
           success: function(data) {
      alert('Process created  Successfully');
      
       window.location='process';
             // window.location='register';
           },
       });
	 });
		 