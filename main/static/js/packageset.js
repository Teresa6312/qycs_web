function createItemblock() {


    $('#add_item_form').append(itemblock);

}//end of create single item block

function createItemsetBlock() {
  var itemsetblock = document.createElement("div");
  itemsetblock.setAttribute("class", "w3-container w3-mobile");
  itemsetblock.setAttribute("id", "add_item_form");

  var itemsetheader = document.createElement("div");
  itemsetheader.setAttribute("class", "text-large");

  itemsetheader.innerHTML=gettext("Add details of each item in the package: ")
  itemsetblock.appendChild(itemsetheader)


  var itemblock = document.createElement("tr");
  itemblock.setAttribute("class", "w3-card-2 itemblock w3-panel w3-mobile");


  var ihblock = document.createElement("div");
  ihblock.setAttribute("class", "text-large");
  ihblock.setAttribute("class", "item_header w3-container");
  ihblock.innerHTML = gettext('Item Detail: ');
  itemblock.appendChild(ihblock);

  var itnblock = document.createElement("div");
  itnblock.setAttribute("class", "w3-container");
  itnblock.innerHTML = gettext('Item Name: ');

  var itn = document.createElement("INPUT");
  itn.setAttribute("id", "id_item_set-0-item_name");
  itn.setAttribute("type", "text");
  itn.setAttribute("name", "item_set-0-item_name");
  itn.setAttribute("class", "w3-input w3-border");
  itn.setAttribute("placeholder", gettext("Please enter your items name as detailed as possible"));
  itn.required = true;
  itnblock.appendChild(itn);
  itemblock.appendChild(itnblock);


  var dtblock = document.createElement("div");
  dtblock.setAttribute("class", "w3-half w3-container");
  dtblock.innerHTML = gettext('Item Detail: ');

  var dt = document.createElement("INPUT");
  dt.setAttribute("id", "id_item_set-0-item_detail");
  dt.setAttribute("type", "text");
  dt.setAttribute("name", "item_set-0-item_detail");
  dt.setAttribute("class", "w3-input w3-border");
  dt.setAttribute("placeholder", gettext("color/size.etc"));
  dtblock.appendChild(dt);
  itemblock.appendChild(dtblock);

  var qtblock = document.createElement("div");
  qtblock.setAttribute("class", "w3-half w3-container");
  qtblock.innerHTML = gettext('Quantity: ');

  var qt = document.createElement("INPUT");
  qt.setAttribute("id", "id_item_set-0-item_quantity");
  qt.setAttribute("type", "number");
  qt.setAttribute("name", "item_set-0-item_quantity");
  qt.setAttribute("class", "w3-input w3-border");
  qt.setAttribute("value", "1");
  qt.required = true;
  qtblock.appendChild(qt);
  itemblock.appendChild(qtblock);


  var urlblock = document.createElement("div");
  urlblock.setAttribute("class", "w3-container");
  urlblock.innerHTML = gettext('Item URL: ');

  var url = document.createElement("INPUT");
  url.setAttribute("id", "id_item_set-0-item_url");
  url.setAttribute("type", "text");
  url.setAttribute("name", "item_set-0-item_url");
  url.setAttribute("class", "w3-input w3-border");
  url.setAttribute("placeholder", "https://...");
  urlblock.appendChild(url);
  itemblock.appendChild(urlblock);

  var lvrblock = document.createElement("div");
  lvrblock.setAttribute("class", "w3-container");


  var lvr = document.createElement("INPUT");
  lvr.setAttribute("id", "id_item_set-0-low_volume_request");
  lvr.setAttribute("type", "checkbox");
  lvr.setAttribute("name", "item_set-0-low_volume_request");
  lvr.setAttribute("class", "w3-border");
  lvrblock.appendChild(lvr);
  lvr.after(gettext("Minimize this item's volume"));
  itemblock.appendChild(lvrblock);

  var notblock = document.createElement("div");
  notblock.setAttribute("class", "w3-container");
  notblock.innerHTML = gettext('Note: ');

  var not = document.createElement("INPUT");
  not.setAttribute("id", "id_item_set-0-item_memo");
  not.setAttribute("type", "textarea");
  not.setAttribute("name", "item_set-0-item_memo");
  not.setAttribute("class", "w3-input w3-border");
  not.setAttribute("placeholder", gettext("tell us your needs"));
  notblock.appendChild(not);
  itemblock.appendChild(notblock);


  var item_table = document.createElement("table");
  item_table.style.width="100%";
  item_table.appendChild(itemblock);

  itemsetblock.appendChild(item_table);

  if($('#add_item_form').length==0){
      $('#item_information_block').append(itemsetblock);
      $('#add_item_form').hide().slideDown(300);
      $('#add_item_btn').text(gettext("Delect all Items"));
  }//end if #add_snapshot_form exists

  else{
      $('#add_item_form').slideUp(300, function(){
        $('#add_item_form').remove();
      });
      $('#add_item_btn').text(gettext("Add Items' Detail"));
    }//end of DOES NOT #add_snapshot_form exists




  $('.itemblock').formset({
      addText: gettext('add Item'),
      deleteText: gettext('delete item'),
      prefix: 'item_set'
  });

}//end of create item set block

function AddSnapshotBlock(){
  var snblock = document.createElement("div");
  snblock.setAttribute("class", "w3-panel w3-container");
  snblock.setAttribute("id", "add_snapshot_form");

  var hd = document.createElement("div");
  hd.setAttribute("class", "text-large");
  hd.innerHTML=gettext('Add Order Snapshot of the Package:');
  snblock.appendChild(hd);

  var im = document.createElement("input");
  im.setAttribute("type", "file");
  im.setAttribute("name", "image");
  im.setAttribute("id", "id_image");
  im.setAttribute("class", "w3-input w3-border");
  im.multiple=true;
  im.required=true;
  snblock.appendChild(im);

  if($('#add_snapshot_form').length==0){
      $('#item_information_block').append(snblock);
      $('#add_snapshot_form').hide().slideDown(300);
      $('#add_snapshot_btn').text(gettext("Delete Snapshot"));
  }//end if #add_snapshot_form exists

  else{
      $('#add_snapshot_form').slideUp(300, function(){
        $('#add_snapshot_form').remove();
      });
      $('#add_snapshot_btn').text(gettext("Add Snapshot"));
    }//end of DOES NOT #add_snapshot_form exists

}//end of AddSnapshotBlock


function clearForm(){
  $('form').find("input[type=text], textarea").val("");
}


// ----------------------------------------------multistepform----------------------------------------------------

var currentTab = 0;

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";


  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").style.display = "none";
    document.getElementById("submit_block").style.display = "inline";
  } else {
    document.getElementById("nextBtn").style.display = "inline";
    document.getElementById("submit_block").style.display = "none";
  }
  //run a function that displays the correct step indicator:
}


function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) {
    if($('.errornote').length==0){
        var p = document.createElement('p');
        p.setAttribute('class','errornote');
        p.innerHTML = gettext('Please correct the error(s) below.');
        $('#message_block').append(p);
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
  var x, y, i, j, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input", "textarea");

  for (i = 0; i < y.length; i++) {
    if (y[i].value == "" && y[i].required) {
      y[i].className += " invalid";
      valid = false;
    }

  }
  var selects = x[currentTab].getElementsByTagName("select");
  for (j = 0; j < selects.length; j++) {
    var index = selects[j].selectedIndex
    if (selects[j].options[index].value == "" && selects[j].required) {
      selects[j].className += " invalid";
      valid = false;
    }
  }


  return valid; // return the valid status
}



$(document).ready(function(){
    showTab(currentTab);
    $("#prevBtn").click(function(){
        if(currentTab==0){
          window.location.href='javascript:history.back()';
        }else{
          nextPrev(-1);
        }
    });
    $("#nextBtn").click(function(){
        nextPrev(1);
    });
})
