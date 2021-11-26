

//Login
$("#btn_login").click(function(){
		
			debugger;
			var name=document.getElementById('eid').value;
			var pass=document.getElementById('pass').value;
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
		window.location="recruitermanagerhomepage";
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
		 
		 
		 
		 

//Approve Process
$("#btn_procapprove").click(function(){
		
			debugger;
			var pid=document.getElementById('pid').value;
			var totcsr=document.getElementById('tot_csr').value;
			var totsup=document.getElementById('tot_sup').value;
			var tottl=document.getElementById('tot_tl').value;
			var totmgr=document.getElementById('tot_mgr').value;
			var totamgr=document.getElementById('tot_amgr').value;
			var totmis=document.getElementById('tot_mis').value;
			
			 $.ajax({
                type: 'GET',
                url: '/approveprocess',
                
            contentType: 'application/json;charset=UTF-8',
                data: {
                
                'pid':pid,
                'totcsr':totcsr,
                'totsup':totsup,
                'tottl':tottl,
                'totmgr':totmgr,
                'totamgr':totamgr,
                'totmis':totmis
            },
                
            dataType:"json",
                success: function(data) {
                  alert("Approved Successfully");
                    window.location='ceopage'
                },
                 error: function(data) {
                   
                }
            }); 

});


	 

//Reject Process
$("#btn_procreject").click(function(){
		
			debugger;
			var name=document.getElementById('eid').value;
			var pass=document.getElementById('pass').value;
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



//Search Candidates
$(".btnSearchCand").click(function(){
	debugger;
    var $row = $(this).closest("tr");    // Find the row
    var $tds=  $row.find("td");  // Find the text
	
	
	/*
    $.each($tds, function() {               // Visits every single <td> element
    console.log($(this).text());        // Prints out the text within the <td>
});
    */
			debugger;
			var qual=$tds[5].innerText;
			var exp=$tds[6].innerText;
			var shift=$tds[8].innerText;
			var lang=$tds[9].innerText;
			var gen=$tds[10].innerText;
			  $.ajax({
                                        type: 'GET',
                                        url: '/searchcand',
                                        
                                    contentType: 'application/json;charset=UTF-8',
                                        data: {
                                        'qual': qual,
                                        'exp':exp,
                                        'shift':shift,
                                        'lang':lang,
                                        'gen':gen

                                    },
                                        
                                    dataType:"json",
                                        success: function(data) {
                                            //alert(data);
                                            details=data
                                           // alert(details);





					var mydiv=document.getElementById("table_driver_history");
						mydiv.innerHTML ="";
						var body="";
						var header="<h4 class='mt-4 text-center'>Matched Candidates List</h4><table style='border:solid black; width: 100%;'><thead style='background-color:black;border:solid;'><tr><th> Candidate Id </th><th> First Name </th><th> Last Name </th><th> Phone number </th><th> Aadhar Number  </th><th>  Qualification </th><th> Experience </th><th> Languages  </th><th>       </th> <th>       </th> </tr></thead><tbody>";
						for (var i=0; i<details.length; i++){
								  body+="<tr><td>" + details[i][0] + "</td><td>" + details[i][1] + "</td><td>" +details[i][2] + "</td><td>" + details[i][12]+ "</td><td>" + details[i][13]+ "</td><td>" + details[i][14]+ "</td><td>" + details[i][15]+ "</td><td>" + details[i][18]+"</td><td><button class='btn btn-primary allocateinterview' id='allocateinterview' onclick='datafetcher("+details[i][0]+")'>Approval </button></td><td><button class='btn btn-primary allocateinterview' id='allocateinterview' onclick='datapproval("+details[i][0]+")'>Submit </button></td></tr>";
					  }
					  mydiv.innerHTML=header+body+"</tbody></table>";
						//tablebuilder(newdata);	
                                             
                                        },
                                         error: function(data) {

                                           
                                        }
                                    });  

});


//Candidate Register
$("#btn_candreg").click(function()
{
	debugger;
   var form_data = new FormData($('#datatransfer')[0]);
   //alert(form_data);
        $.ajax({
            type: 'POST',
            url: '/registerss',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
				candreg(data);
            },
        });
}); 

function candreg(data)
{
	console.log('Success!');
	alert('Candidate data has been stored');
	window.location='register';
}


//Allocate Interview
function datafetcher(data)
{
	debugger;
	$.ajax({
           type: 'GET',
           url: '/sendtorecmgr',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'cid': data
       },
           
       dataType:"json",
           success: function(logindata) {
			   alert(logindata);
				window.location='recruiterpage';
			   
      
           },
       });
}

function datapproval(data)
{
	debugger;
	$.ajax({
           type: 'GET',
           url: '/recruiterapproval',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'cid': data,
		   'mgr':'Bopanna C K'
       },
           
       dataType:"json",
           success: function(logindata) {
			   alert(logindata);
				window.location='recruiterpage';
			   
      
           },
       });
}


//Rec Mgr Approve
function RecMgrApprove(data)
{
	debugger;
	$.ajax({
           type: 'GET',
           url: '/recmgrapproval',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'cid': data
       },
           
       dataType:"json",
           success: function(logindata) {
			   alert("Candidate Approved");
				window.location='recruitermanagerhomepage';
			   
      
           },
       });
}



//Interview Allocation
function IntrvwAllocation(Cid,Mgr)
{
	debugger;
	$.ajax({
           type: 'GET',
           url: '/interviewalloc',
     
       contentType: 'application/json;charset=UTF-8',
           data: {           
           'cid': Cid,
		   'mgr':Mgr
       },
           
       dataType:"json",
           success: function(logindata) {
			   alert("Candidate has been allocated for interview");
				window.location='savedcandidatenew';
			   
      
           },
       });
}
	