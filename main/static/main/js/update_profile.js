function submitForm(csrf, submit_url){
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
                      'is_popup':"True"};

      $.ajax({
        type: "POST",
        url: submit_url,
        data: addobject,
        success: function(data){
          $('#id-new-address-modalBody').append($(data).find('#id-new-address-modal').find('#newAddressForm'));
          $('#id-new-address-modal').append($(data).find('#id-new-address-modal').find('script'));

          if($(data).find('#id-new-address-modal').find('.messagelist').children().length == 0){
            $('#id-new-address-modal').hide();
            $('#default_address_card').remove();
            $('#newAddressForm_js').remove();
            $('#remove_default_add_btn').parent('div').before($(data).find('#default_address_card'));
          }
          else{
            $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
            $('.messagelist').hide().slideDown(500);
          }
        },
        failure: function(data){
          $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
          $('.messagelist').hide().slideDown(500);
        },
      });
    }
}//end of submitForm


function createAddForm(user,csrf, submit_url) {
    var addform = document.createElement("FORM");
    addform.setAttribute("id", "newAddressForm_js");

    var formblock = document.createElement("div");
    formblock.setAttribute("class", "w3-row");

    var fuiblock = document.createElement("div");
    fuiblock.setAttribute("id", "id_follow_user_infor_block");

    var fui = document.createElement("button");
    fui.setAttribute("type", "button");
    fui.setAttribute("id", "id_follow_user_infor");
    fui.append("Follow User Information");
    fui.innerHTML = 'Follow User Information';
    fui.onclick = function(){
      fn.value = user.first_name;
      ln.value = user.last_name;
      ph.value = user.phone;
    };

    fuiblock.appendChild(fui);
    formblock.appendChild(fuiblock);

    var fnblock = document.createElement("div");
    fnblock.setAttribute("class", "w3-half w3-container");
    fnblock.append('First Name:');

    var fn = document.createElement("INPUT");
    fn.setAttribute("id", "id_first_name");
    fn.setAttribute("type", "text");
    fn.setAttribute("name", "first_name");
    fn.setAttribute("class", "w3-input w3-border");
    fn.required = true;
    fnblock.appendChild(fn);
    formblock.appendChild(fnblock);

    var lnblock = document.createElement("div");
    lnblock.setAttribute("class", "w3-half w3-container");
    lnblock.append('Last Name:');

    var ln = document.createElement("INPUT");
    ln.setAttribute("id", "id_last_name");
    ln.setAttribute("type", "text");
    ln.setAttribute("name", "last_name");
    ln.setAttribute("class", "w3-input w3-border");
    ln.required = true;
    lnblock.appendChild(ln);
    formblock.appendChild(lnblock);



    var row_block = document.createElement("div");
    row_block.setAttribute("class", "w3-row");

    var phblock = document.createElement("div");
    phblock.setAttribute("class", "w3-half w3-container");
    phblock.append('Phone:');

    var ph = document.createElement("INPUT");
    ph.setAttribute("id", "id_phone");
    ph.setAttribute("type", "text");
    ph.setAttribute("name", "phone");
    ph.setAttribute("class", "w3-input w3-border");
    ph.required = true;
    phblock.appendChild(ph);
    row_block.appendChild(phblock)
    formblock.appendChild(row_block);


    var coblock = document.createElement("div");
    coblock.setAttribute("class", "w3-half w3-container");
    coblock.append('Country:');

    var co = document.createElement("INPUT");
    co.setAttribute("id", "id_country");
    co.setAttribute("type", "text");
    co.setAttribute("name", "country");
    co.setAttribute("class", "w3-input w3-border");
    co.required = true;
    coblock.appendChild(co);
    formblock.appendChild(coblock);



    var stblock = document.createElement("div");
    stblock.setAttribute("class", "w3-half w3-container");
    stblock.append('State:');

    var st = document.createElement("INPUT");
    st.setAttribute("id", "id_state");
    st.setAttribute("type", "text");
    st.setAttribute("name", "state");
    st.setAttribute("class", "w3-input w3-border");
    st.required = true;
    stblock.appendChild(st);
    formblock.appendChild(stblock);


    var ctblock = document.createElement("div");
    ctblock.setAttribute("class", "w3-half w3-container");
    ctblock.append('City:');

    var ct = document.createElement("INPUT");
    ct.setAttribute("id", "id_city");
    ct.setAttribute("type", "text");
    ct.setAttribute("name", "city");
    ct.setAttribute("class", "w3-input w3-border");
    ct.required = true;
    ctblock.appendChild(ct);
    formblock.appendChild(ctblock);

    var zpblock = document.createElement("div");
    zpblock.setAttribute("class", "w3-half w3-container");
    zpblock.append('Zip Code:');

    var zp = document.createElement("INPUT");
    zp.setAttribute("id", "id_zipcode");
    zp.setAttribute("type", "text");
    zp.setAttribute("name", "zipcode");
    zp.setAttribute("class", "w3-input w3-border");
    zp.required = true;
    zpblock.appendChild(zp);
    formblock.appendChild(zpblock);

    var adblock = document.createElement("div");
    adblock.setAttribute("class", " w3-container");

    adblock.append('Address:');
    var ad = document.createElement("INPUT");
    ad.setAttribute("id", "id_address");
    ad.setAttribute("type", "text");
    ad.setAttribute("name", "address");
    ad.setAttribute("class", "w3-input w3-border");
    ad.required = true;
    adblock.appendChild(ad);

    adblock.append('Address2/Apartment:');
    var ap = document.createElement("INPUT");
    ap.setAttribute("id", "id_apt");
    ap.setAttribute("type", "text");
    ap.setAttribute("name", "apt");
    ap.setAttribute("class", "w3-input w3-border");
    adblock.appendChild(ap);

    formblock.appendChild(adblock);


    var btblock = document.createElement("div");
    btblock.setAttribute("class", "w3-right");

    var ca = document.createElement("button");
    ca.setAttribute("type", "button");
    ca.setAttribute("class", "cancel-modal");
    ca.innerHTML = 'Cancel';
    ca.onclick = function(){
     $('#id-new-address-modal').hide();
    };
    btblock.appendChild(ca);

    var sv = document.createElement("button");
    sv.setAttribute("type", "button");
    sv.setAttribute("id", "newAddressSubmitBtn");
    sv.setAttribute("onclick", "submitForm()");
    sv.innerHTML = 'Save';
    sv.onclick = function(){
      if($('.addform-errors').length>0){
        $('.addform-errors').remove();
      }
      submitForm(csrf, submit_url);
    };
    btblock.appendChild(sv);


    formblock.appendChild(btblock);

    addform.appendChild(formblock);
    if($('#newAddressForm_js').length==0){
        $('#id-new-address-content').append(addform);
   }
   $('#id-new-address-modal').show();

}//end of create address form


$(document).ready(function(){

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

      if($('#default_address_card').length>=1){
        $('#default_address_card').remove();
      }

      $('#id-select-address-modal').hide();

      let element=$(this).clone();
      element.addClass("w3-half")
      element.removeClass("addchoice")
      $('#remove_default_add_btn').parent('div').before(element);
      $('#default_address_block').find('.w3-card-2').attr('id','default_address_card');
      $('#default_address_card').append('<input type="hidden" id="id_default_address" name="default_address" value='+$(this).attr("id")+' />');
        $('#remove_default_add_btn').show();
      $(this).addClass("w3-pale-green");
    });
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
        element.addClass("w3-half")
        element.removeClass("colchoice")
        $('#remove_default_col_btn').parent('div').before(element);
        $('#default_col_block').find('.w3-card-2').attr('id','default_col_card');
        $('#default_col_card').append('<input type="hidden" id="id_default_col" name="default_col" value='+$(this).attr("id")+' />');
        $('#remove_default_col_btn').show();
        $(this).addClass("w3-pale-green");
    });

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
