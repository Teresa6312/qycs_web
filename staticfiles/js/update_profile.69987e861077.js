function submitForm(csrf, submit_url, add_field_name){
  let formpass=true;
  let inputs = document.forms["newAddressForm_js"].getElementsByTagName("input");
  for(var i = 0, a; a = inputs[i++];){
    if(a.required && a.value==''){
        a.style.background = "#ffdddd";
        formpass=false;
    }
  }

  if(formpass){
      let addobject={'csrfmiddlewaretoken': csrf,
                      'addform':$('#newAddressForm_js').serialize(),
                      'add_field_name': add_field_name};

      $.ajax({
        type: "POST",
        url: submit_url,
        data: addobject,
        success: function(data){
          $('#id-new-address-modal').find('.messagelist').remove();
          $('#id-new-address-modal').find('.errorlist').remove();
          $('#id-new-address-modal').find('.errornote').remove();
          if($(data).find('#main_address_form').length == 0){
              $('#newAddressForm_js').remove();
              $('#default_address_card').remove();
              if($('#remove_default_add_btn').length > 0){
                  $('#remove_default_add_btn').parent('div').before($(data).find('#default_address_card'));
              }else{
                $('#default_address_block').append($(data).find('#default_address_card'));
              }
              $('#id-new-address-modal').hide();
          }else{
            $('#id-new-address-content').before($(data).find('.messagelist'));
            $('.messagelist').hide().slideDown(500);
            $(data).find('.errorlist').each(function(){
                var input = $(this ).parent('div').find('input');
                $('#id-new-address-content').find('#'+input.prop("id")).before($(this));
            });
            $('.errorlist').hide().slideDown(500);
            $('#id-new-address-content').before($(data).find('.errornote'));
            $('.errornote').hide().slideDown(500);
          }
        },
        failure: function(data){
          console.log('failure');
        },
      });
    }
}//end of submitForm

function getAddForm(user,csrf, submit_url, add_field_name){
  $.ajax({
    url: submit_url,
    success: function(data){
      if($(data).find('#main_address_form').length > 0){
          $(data).find('#button_row').remove();
          $('#id-new-address-content').addClass('w3-container');
          if($('#id-new-address-content').find('form').length == 0){
            $('#id-new-address-content').append($(data).find('#main_address_form form'));
            $('#id-new-address-content form').prop('id', 'newAddressForm_js');

            $('#id-new-address-content #button_row').remove();


            if($('#id-new-address-content').find('#button_block').length == 0){
              var btblock = document.createElement("div");
              btblock.setAttribute("class", "w3-right");
              btblock.setAttribute("id", "button_block");

              var ca = document.createElement("button");
              ca.setAttribute("type", "button");
              ca.setAttribute("class", "logo-red");
              ca.innerHTML = 'Cancel';
              ca.onclick = function(){
               $('#id-new-address-modal').hide();
               $('#id-new-address-content #form').remove();
               $('#id-new-address-content script').remove();
              };
              btblock.appendChild(ca);

              var sv = document.createElement("button");
              sv.setAttribute("type", "button");
              sv.setAttribute("class", "logo-blue");
              sv.setAttribute("id", "newAddressSubmitBtn");
              sv.innerHTML = 'Save';
              sv.onclick = function(){
                if($('.addform-errors').length>0){
                  $('.addform-errors').remove();
                }
                submitForm(csrf, submit_url, add_field_name);
              };
              btblock.appendChild(sv);
              $('#id-new-address-content').append(btblock);
            }
            $("#id-new-address-content input[required]").before('<span class="required_stick">*</span>');

            $('#id-new-address-content').append($(data).find('script'));

          }
          $('#id-new-address-modal').show();
      }
      else{
        createAddForm(user_obj, "{{ csrf_token }}", "{% url 'useraddress' %}", '{{add_field_name}}');
      }
    },
    failure: function(data){
        createAddForm(user_obj, "{{ csrf_token }}", "{% url 'useraddress' %}", '{{add_field_name}}');
    },
  });


}

function createAddForm(user,csrf, submit_url, add_field_name) {
    var addform = document.createElement("FORM");
    addform.setAttribute("id", "newAddressForm_js");


    var formblock = document.createElement("div");

    var fuiblock = document.createElement("div");
    fuiblock.setAttribute("id", "id_follow_user_infor_block");

    var fui = document.createElement("button");
    fui.setAttribute("class", "logo-blue");
    fui.setAttribute("type", "button");
    fui.setAttribute("id", "id_follow_user_infor");
    fui.append("Follow User Information");
    fui.innerHTML = 'Follow User Information';
    fui.onclick = function(){
      fn.value = user.first_name;
      ln.value = user.last_name;
      ph.value = user.phone;
      co.value = user.country;
    };

    fuiblock.appendChild(fui);
    formblock.appendChild(fuiblock);

    var fnblock = document.createElement("div");
    fnblock.setAttribute("class", "w3-half w3-container");

    var fn_l = document.createElement("label");
    fn_l.setAttribute('for', 'id_first_name')
    fn_l.append('First Name:');

    fnblock.append(fn_l);

    var fn = document.createElement("INPUT");
    fn.setAttribute("id", "id_first_name");
    fn.setAttribute("type", "text");
    fn.setAttribute("name", "first_name");
    fn.setAttribute("class", "w3-input w3-border");
    fn.required = true;
    fnblock.appendChild(fn);


    var lnblock = document.createElement("div");
    lnblock.setAttribute("class", "w3-half w3-container");

    var ln_l = document.createElement("label");
    ln_l.setAttribute('for', 'id_last_name')
    ln_l.append('Last Name:');

    lnblock.append(ln_l);

    var ln = document.createElement("INPUT");
    ln.setAttribute("id", "id_last_name");
    ln.setAttribute("type", "text");
    ln.setAttribute("name", "last_name");
    ln.setAttribute("class", "w3-input w3-border");
    ln.required = true;

    lnblock.appendChild(ln);

    var phrow = document.createElement("div");
    phrow.setAttribute("class", "w3-row");

    var phblock = document.createElement("div");
    phblock.setAttribute("class", "w3-half w3-container");

    var ph_l = document.createElement("label");
    ph_l.setAttribute('for', 'id_phone')
    ph_l.append('Phone:');

    phblock.append(ph_l);

    var ph = document.createElement("INPUT");
    ph.setAttribute("id", "id_phone");
    ph.setAttribute("type", "text");
    ph.setAttribute("name", "phone");
    ph.setAttribute("class", "w3-input w3-border");

    ph.required = true;
    phblock.appendChild(ph);
    phrow.appendChild(phblock);


    var coblock = document.createElement("div");
    coblock.setAttribute("class", "w3-third w3-container");


    var co_l = document.createElement("label");
    co_l.setAttribute('for', 'id_country')
    co_l.append('Country:');

    coblock.append(co_l);

    var co = document.createElement("INPUT");
    co.setAttribute("id", "id_country");
    co.setAttribute("type", "text");
    co.setAttribute("name", "country");
    co.setAttribute("class", "w3-input w3-border");

    co.required = true;
    coblock.appendChild(co);


    var stblock = document.createElement("div");
    stblock.setAttribute("class", "w3-third w3-container");

    var st_l = document.createElement("label");
    st_l.setAttribute('for', 'id_state')
    st_l.append('State:');

    stblock.append(st_l);

    var st = document.createElement("INPUT");
    st.setAttribute("id", "id_state");
    st.setAttribute("type", "text");
    st.setAttribute("name", "state");
    st.setAttribute("class", "w3-input w3-border");

    st.required = true;
    stblock.appendChild(st);


    var ctblock = document.createElement("div");
    ctblock.setAttribute("class", "w3-third w3-container");

    var ct_l = document.createElement("label");
    ct_l.setAttribute('for', 'id_city')
    ct_l.append('City:');

    ctblock.append(ct_l);

    var ct = document.createElement("INPUT");
    ct.setAttribute("id", "id_city");
    ct.setAttribute("type", "text");
    ct.setAttribute("name", "city");
    ct.setAttribute("class", "w3-input w3-border");
    ct.required = true;
    ctblock.appendChild(ct);

    var zprow = document.createElement("div");
    zprow.setAttribute("class", "w3-row w3-container");

    var zpblock = document.createElement("div");
    zpblock.setAttribute("class", "w3-quarter w3-right");


    var zp_l = document.createElement("label");
    zp_l.setAttribute('for', 'id_zipcode')
    zp_l.append('Zip Code:');

    zpblock.append(zp_l);


    var zp = document.createElement("INPUT");
    zp.setAttribute("id", "id_zipcode");
    zp.setAttribute("type", "text");
    zp.setAttribute("name", "zipcode");
    zp.setAttribute("class", "w3-input w3-border");
    zp.required = true;
    zpblock.appendChild(zp);
    zprow.appendChild(zpblock);

    var adblock = document.createElement("div");
    adblock.setAttribute("class", "w3-container");

    var ad_l = document.createElement("label");
    ad_l.setAttribute('for', 'id_address')
    ad_l.append('Address:');

    adblock.append(ad_l);

    var ad = document.createElement("INPUT");
    ad.setAttribute("id", "id_address");
    ad.setAttribute("type", "text");
    ad.setAttribute("name", "address");
    ad.setAttribute("class", "w3-input w3-border");
    ad.required = true;
    adblock.appendChild(ad);



    var apblock = document.createElement("div");
    apblock.setAttribute("class", "w3-container");

    var ap_l = document.createElement("label");
    ap_l.setAttribute('for', 'id_apt')
    ap_l.append('Address2/Apartment:');

    apblock.append(ap_l);

    var ap = document.createElement("INPUT");
    ap.setAttribute("id", "id_apt");
    ap.setAttribute("type", "text");
    ap.setAttribute("name", "apt");
    ap.setAttribute("class", "w3-input w3-border");
    apblock.appendChild(ap);

    formblock.appendChild(fnblock);
    formblock.appendChild(lnblock);
    formblock.appendChild(phrow);
    formblock.appendChild(coblock);
    formblock.appendChild(stblock);
    formblock.appendChild(ctblock);
    formblock.appendChild(adblock);
    formblock.appendChild(apblock);
    formblock.appendChild(zprow);

    var btblock = document.createElement("div");
    btblock.setAttribute("class", "w3-right");

    var ca = document.createElement("button");
    ca.setAttribute("type", "button");
    ca.setAttribute("class", "logo-red");
    ca.innerHTML = 'Cancel';
    ca.onclick = function(){
     $('#id-new-address-modal').hide();
     addform.remove();
    };
    btblock.appendChild(ca);

    var sv = document.createElement("button");
    sv.setAttribute("type", "button");
    sv.setAttribute("class", "logo-blue");
    sv.setAttribute("id", "newAddressSubmitBtn");
    sv.innerHTML = 'Save';
    sv.onclick = function(){
      if($('.addform-errors').length>0){
        $('.addform-errors').remove();
      }
      submitForm(csrf, submit_url, add_field_name);
    };
    btblock.appendChild(sv);


    formblock.appendChild(btblock);

    addform.appendChild(formblock);
    if($('#newAddressForm_js').length==0){
        $('#id-new-address-content').append(addform);
   }
   $("input[required]").before('<span class="required_stick">*</span>');
   $('#id-new-address-modal').show();
}//end of create address form


$(document).ready(function(){

  $('#id-new-address-modal .close-modal').click(function(){
    $('#newAddressForm_js').remove();
  });

  $("#select_address_btn").click(function(){
       $('#id-select-address-modal').show();
  });
  $("#remove_default_add_btn").click(function(){
    $('#default_address_card').slideUp(300, function(){
      $('#default_address_card').remove();
    });
    $(this).hide()
  });
  if($('#default_address_card').length>=1){
    $('#remove_default_add_btn').show();
  };

  // select address
  $('.addchoice').click(function(){
      $('.addchoice').each(function(){
        $(this ).removeClass("w3-pale-green")
      })

      let element=$(this).children().clone();

      if($('#default_address_card').length == 0){
        var add_card = document.createElement('div');
        add_card.setAttribute('id', 'default_address_card');
        add_card.setAttribute('class', 'w3-card-2 w3-round w3-container w3-mobile w3-half');
        add_card.style.maxWidth = "30vw";
        var add_fields = document.createElement('div');
        add_fields.setAttribute('id', 'default_address_card_fields');
        add_card.append(add_fields);

        var add_id = document.createElement('input');
        add_id.setAttribute('type', 'hidden');

        if($('body').find('#id_cust_tracking_num').length == 0){
          add_id.setAttribute('id', 'id_default_address');
          add_id.setAttribute('name', 'default_address');
        }else{
          add_id.setAttribute('id', 'id_ship_to_add');
          add_id.setAttribute('name', 'ship_to_add');
        }
        add_card.append(add_id);
        $('#select_address_btn').parent('div').after(add_card);
      }

      $( "#default_address_card_fields").find('.add_fields').remove();
      $( "#default_address_card_fields").append(element);
      $('#default_address_card').find('input[type="hidden"]').val($(this).attr("id"));
      $('#remove_default_add_btn').show();

      $('#id-select-address-modal').hide();
      $(this).addClass("w3-pale-green");

    });  // END OF select address


// select collection point
    $('.colchoice').click(function(){
        $('.colchoice').each(function(){
          $(this ).removeClass("w3-pale-green")
        })

        if($('#default_col_card').length>=1){
          $('#default_col_card').remove();
        }

        $('#id-select-col-modal').hide();

        let element=$(this).clone();
        let id = element.attr("id");
        element.removeClass("colchoice")
        element.attr('id','default_col_card');

        $('#remove_default_col_btn').parent('div').before(element);
        $('#default_col_card').append('<input type="hidden" id="id_default_col" name="default_col" value='+id+' />');
        $('#remove_default_col_btn').show();
        $(this).addClass("w3-pale-green");
    });// END OF select collection point



    $("#select_col_btn").click(function(){
         $('#id-select-col-modal').show();
    });
    $("#remove_default_col_btn").click(function(){
      $('#default_col_card').slideUp(300, function(){
        $('#default_col_card').remove();
      });
      $(this).hide()
    });
    if($('#default_col_card').length>=1){
      $('#select_col_btn').text("Change");
      $('#remove_default_col_btn').show();
    }else {
      $('#select_col_btn').text("Select a Collection Point");
      $('#remove_default_col_btn').hide();
    }

});
