
function pass_package(csrf, url){
      let dt={'csrfmiddlewaretoken': csrf};

      $.ajax({
        type: "POST",
        url: url,
        data: dt,
        success: function(data){
            location.reload();
        },
        failure: function(data){
          console.log('failure');
        },
      });
}// end of pass package




function AddResponseForm(id, type){
    let content = '<div class="w3-row response_block" id="response_block_'+
    id+
    '">'+
    '<textarea class="w3-input w3-border" name="'+
    type+
    '" id="response_txt"/>'+
    '<button type="button" class="w3-right" onclick="submitForm('+
    id+
    ')">Save</button></div>'
    if($('.response_block').length>0){
        $('.response_block').remove();
    }
    if($('#response_block_'+id).length==0){
        $('#'+type+'_block_'+id).append(content);
        $('#response_block_'+id).hide().slideDown(500);
        $('.response_btn_'+id).hide();
    }
}






function submitForm(id){
    let response={'csrfmiddlewaretoken': '{{csrf_token}}',
                    'type':$('#response_txt').attr('name'),
                    'response_for': id,
                    'response':$('#response_txt').val(),
                  };
    $.ajax({
      type: "POST",
      url: '/collectionpoint/{{collector.pk}}/view',
      data: response,
      success: function(){
        location.reload();
      },
      failure: function(){
        location.reload();
      },
    });
  }



    $('#id_store').change( function(){
            if(!$(this).prop('checked')){
              $('#id_store_name').closest('.w3-row').slideUp(300, function(){
                  $('#id_store_name').closest('.w3-row').hide();
              });
              $('#id_license_type').closest('.w3-row').slideUp(300, function(){
                  $('#id_license_type').closest('.w3-row').hide();
              });
              $('#id_license_image').closest('.w3-row').slideUp(300, function(){
                  $('#id_license_image').closest('.w3-row').hide();
              });
            }else{
              $('#id_store_name').closest('.w3-row').hide().slideDown(300);
              $('#id_license_image').closest('.w3-row').hide().slideDown(300);
              $('#id_license_type').closest('.w3-row').hide().slideDown(300);
            }
        });

        function loadDoc(url) {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
              document.getElementById("term_block").innerHTML = this.responseText;
            }
          };
          xhttp.open("GET", url, true);
          xhttp.send();
        }



$(document).ready(function(){
      $('#id_store').change( function(){
            if (!$(this).is(':checked')) {
              $('#id_store_name').closest('.w3-row').slideUp(300, function(){
                  $('#id_store_name').closest('.w3-row').hide();
              });
              $('#id_license_type').closest('.w3-row').slideUp(300, function(){
                  $('#id_license_type').closest('.w3-row').hide();
              });
              $('#id_license_image').closest('.w3-row').slideUp(300, function(){
                  $('#id_license_image').closest('.w3-row').hide();
              });
            }else{
              $('#id_store_name').closest('.w3-row').hide().slideDown(300);
              $('#id_license_image').closest('.w3-row').hide().slideDown(300);
              $('#id_license_type').closest('.w3-row').hide().slideDown(300);
            }
        });

      $(".block_link").click(function(){
        if($('.response_block').length>=1){
          $('.response_block').remove();
        }
      });
      $("#id_message").click(function(){
        if($('.response_block').length>0){
            $('.response_block').remove();
        }
      });

      var url = '';
      if ('{{LANGUAGE_CODE}}'=="en-us"){
        url = "/static/information/collection_point_terms_en.txt";
      }else if('{{LANGUAGE_CODE}}'=="zh-hans"){
      url = "/static/information/collection_point_terms_cn.txt";
      }
      if(url!=''){
        loadDoc(url)
      }

      $('#id_collector_icon').change(function(){
            displayImages('#id_collector_icon');
      });
      $('#id_license_image').change(function(){
            displayImages('#id_license_image');
      });
      $('#id_id_image').change(function(){
            displayImages('#id_id_image');
      });
      $('#id_wechat_qrcode').change(function(){
            displayImages('#id_wechat_qrcode');
      });
});
