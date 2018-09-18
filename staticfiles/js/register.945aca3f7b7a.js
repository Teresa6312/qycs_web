var currentTab = 0;

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  //fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").style.display = "none";
    document.getElementById("submit_block").style.display = "inline";
  } else {
    document.getElementById("nextBtn").style.display = "inline";
    document.getElementById("submit_block").style.display = "none";
  }
  //run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
function validatePhone(phone) {
    var re =/^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;
    return re.test(String(phone));
}


function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) {
    if($('.errornote').length==0){
        var p = document.createElement('p');
        p.setAttribute('class','errornote');
        p.innerHTML = 'Please correct the error(s) below.';
        $('Form').before(p);
        $('.errornote').hide().slideDown(200);
    }
    return false;
  }else{
    $('.errornote').slideUp(200, function(){
      $('#errornote').remove();
    });
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    showTab(currentTab);
  }

}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i,j, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");

  if($('.WebFormSet').css('display')=="block"){
    let select=$('.select').each(function(){
        if($($(this)).find(":selected").text()=="---"){
          valid=false;
          $(this).find('select').css('background-color','#ffdddd');
        }
    });
  }

  for (i = 0; i < y.length; i++) {
    if (y[i].value == "" && y[i].required) {
      y[i].className += " invalid";
      valid = false;
    }
  }
  if (currentTab==0) {
    var email = document.getElementById('id_email')
    if(!validateEmail(email.value)){
      valid = false;
    }
  }
  if (currentTab==1) {
    var phone = document.getElementById('id_phone')
    if(phone.value!=''&&!validatePhone(phone.value)){
      valid = false;
    }
  }
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  x[n].className += " active";
}

$(document).ready(function(){

    showTab(currentTab);

    $(".cleanBtn").click(function(){
      $(this).closest('form').find("input[type=text], textarea").val("");
    });
    $('#id_email').change(function(){
      if(!validateEmail($(this).val())){
        $(this).addClass('invalid');
      }else{
        $(this).removeClass('invalid');
      }
    });
    $('#id_phone').change(function(){
      if(!validatePhone($(this).val())){
        $(this).addClass('invalid');
      }else{
        $(this).removeClass('invalid');
      }
    });

})
