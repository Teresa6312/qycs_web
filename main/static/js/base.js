$(document).ready(function(){
    $(".wechat").click(function(){
        $('#id-wechat-modal').show();
    });
    $(".email").click(function(){
        $('#id-email-modal').show();
    });

    $(".close-modal").click(function(){
      $(this).parents('.w3-modal').hide();
    });
    $(".cancel-modal").click(function(){
      $(this).parents('.w3-modal').hide();
    });
    $('#id-email').change(function(){
      if(!validateEmail($(this).val())){
        $(this).css('background-color','#ffdddd');
      }else{
        $(this).css('background-color','#fff');
      }
    });
    $(".contentCSS input[required]").before('<span class="required_stick">*</span>');
    $("select[required]").before('<span class="required_stick">*</span>');
    $('#id_email').change(function(){
      if(!validateEmail($(this).val())){
        $(this).css('background-color','#ffdddd');
      }else{
        $(this).css('background-color','#fff');
      }
    });
    $('#id_phone').change(function(){
      if(!validatePhone($(this).val())){
        $(this).css('background-color','#ffdddd');
      }else{
        $(this).css('background-color','#fff');
      }
    });
    $(".cleanBtn").click(function(){
      $(this).closest('form').find("input[type=text], textarea").val("");
    });
    $("#footer h5").click(function(){
      $(this).parents('.w3-col').find('.footer_links').show();
    });
});

function getPackageNumber(url,id){
    $.ajax({
        url: url,
        success: function(data){
          if (parseFloat(data)>0){
            $('#'+id).text(data);
            $('#package_num').show();
          }
        }
      });
}//end of getPackageNumber

function displayImages(id){
    $('#images_view'+id).remove();
    var files = $(id).prop('files');
    if(files.length > 0){
      var viewblock = document.createElement("div");
      viewblock.setAttribute("id", "images_view"+id);
      $(id).after(viewblock);

      for (i = 0; i < files.length; i++) {
          var type = files[i].type.split('/')[0];

          var size = Math.round(files[i].size / 1024 / 1024);
          if (type !='image') {
              alert(gettext('Images only, please try again.'));
              return;
          }
          if (size > 3) {
              alert(gettext('The maxium size of each image is 3M, please try again.'));
              return;
          };
          var reader = new FileReader();//creat FileReader for each images
          reader.readAsDataURL(files[i]);
                reader.onload=function(e){
                var img = document.createElement("img");
                img.setAttribute("width", "70");
                img.setAttribute("height", "70");
                      img.setAttribute("src", e.target.result);
                viewblock.append(img);
                }
      }

      }
} //display upload images

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
function validatePhone(phone) {
    var re =/^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;
    return re.test(String(phone));
}

function validateForm(block) {
  let valid=true;
  block.find('input').each(function(){
      if($(this).val()==''&& $(this).required){
        $(this).css('background-color','#ffdddd');
        valid=false;
      }
  });
  return valid;
}

function send_email(id,csrf){
    var formpass = false
    var form = $('#'+id).parents('form');
    var email = form.find('#id-email');
    var subj = form.find('#id-subject');
    var cc = form.find('#id-cc');
    var cont = form.find('#id-content')
    var email_data = {'csrfmiddlewaretoken': csrf,
                'email': email.val(),
                'subject': subj.val(),
                'content': cont.val(),
                'cc': cc.prop('checked')
                }
    if( validateEmail(email.val())){
      if(subj.val()!=''){
          if(cont.val().trim()!==''){
              formpass=true
          }else{
            alert(gettext('Please enter the content'));
          }
      }else{
        alert(gettext('Please enter the subject'));
      }
    }else{
      alert(gettext('Please enter a valid Email'));
    }
   if(formpass){
     $.ajax({
       type: "POST",
       url: '/contact-us/',
       data: email_data,
       success: function(data){
         alert(gettext('The email was sent successfully!'));
         form.find("input[type=text], textarea").val("");
         form.parents('.w3-modal').hide();

       },
       failure: function(data){
         alert(gettext('Failure, please try again.'));
     },
   });
   }

}//end of submitForm



function createmodal(id){
    var modal = document.createElement("div");
    modal.setAttribute("class", "w3-modal");
    modal.setAttribute("id", "id");

    var modal_content = document.createElement("div");
    modal_content.setAttribute("class", "w3-modal-content w3-container");


    var close = document.createElement("div");
    close.setAttribute("class", "w3-row w3-right");
    close.append('&times;')
    close.onclick = function(){
       modal.remove();
    };

    var content = document.createElement("div");
    content.setAttribute("class", "w3-container");
    content.setAttribute("id", "content_block");
    content.append(id)

    modal_content.append(content);

    modal_content.appendChild(close);

    modal.appendChild(modal_content);

    modal.style.display="block";

    var container = document.getElementById('container');
    container.appendChild(modal);
}


function openBlock(evt, blockName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("message_block");
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
     tablinks[i].className = tablinks[i].className.replace(" w3-border-red", "");
  }
  document.getElementById(blockName).style.display = "block";
  evt.currentTarget.firstElementChild.className += " w3-border-red";
}
