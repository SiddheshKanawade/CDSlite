function busel_login() {
    document.querySelector('.details_logsign').className = "details_logsign login_detailing_active";  
    document.querySelector('.login_details').style.display = "block";
    document.querySelector('.signup_detail').style.opacity = "0";               
  
    setTimeout(function(){  document.querySelector('.login_details').style.opacity = "1"; },400);  
        
    setTimeout(function(){    
    document.querySelector('.signup_detail').style.display = "none";
    },200);  
    }
  
function busel_sign_up(at) {
    document.querySelector('.details_logsign').className = "details_logsign signup_detailing_active";
    document.querySelector('.signup_detail').style.display = "block";
    document.querySelector('.login_details').style.opacity = "0";
    
    setTimeout(function()
    {  
        document.querySelector('.signup_detail').style.opacity = "1";
    },100);  
  
    setTimeout(function(){   
        document.querySelector('.login_details').style.display = "none";
    },400);  
  
}      
function busel_login_sign_up() {
  
  document.querySelector('.details_logsign').className = "details_logsign";  
  document.querySelector('.signup_detail').style.opacity = "0";               
  document.querySelector('.login_details').style.opacity = "0"; 
  
  setTimeout(function(){
  document.querySelector('.signup_detail').style.display = "none";
  document.querySelector('.login_details').style.display = "none";
  },500);  
    
}