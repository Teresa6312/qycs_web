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
    $("#send_email_btn").click(function(){
        send_email('id-email-modal');

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
    $('container').find('input').each(function(){
      console.log($(this));
      if($(this).readonly){
        console.log($(this));
        $(this).addClass('w3-light-gray');
      }
    });
    $(".cleanBtn").click(function(){
      $(this).closest('form').find("input[type=text], textarea").val("");
    });
})

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

function send_email(id){
  let formpass=true;
  let inputs = document.forms[id].getElementsByTagName("input");
  // need to add textarea

  for(var i = 0, a; a = inputs[i++];){
    if(a.required && a.value==''){
        a.style.background = "#ffb2b2";
        formpass=false;
    }
  }

  if(formpass){
    // modify this part
      let addobject={'csrfmiddlewaretoken': '{{csrf_token}}',
                      'addform':$('#'+id).serialize(),
                      'is_popup':"True"};

      $.ajax({
        type: "POST",
        url: submit_url,
        data: addobject,
        success: function(data){
          $('#newAddressFormModalBody').append($(data).find('#newAddressFormModal').find('#newAddressForm'));
          $('#newAddressFormModal').append($(data).find('#newAddressFormModal').find('script'));

          if($(data).find('#newAddressFormModal').find('.messagelist').children().length == 0){
            $('#newAddressFormModal').modal('hide');
            $('#default_address_card').remove();
            $('#newAddressForm_js').remove();
            $('#default_address_block').append($(data).find('#default_address_card'));
          }
          else{
            $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
            $('#.messagelist').hide().slideDown(500);
          }
        },
        failure: function(data){
          $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
          $('#.messagelist').hide().slideDown(500);
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
