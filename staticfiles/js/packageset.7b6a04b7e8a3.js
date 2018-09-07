function createItemblock() {


    $('#add_item_form').append(itemblock);

}//end of create single item block

function createItemsetBlock() {
  var itemsetblock = document.createElement("div");
  itemsetblock.setAttribute("class", "w3-container w3-mobile");
  itemsetblock.setAttribute("id", "add_item_form");

  var itemsetheader = document.createElement("h3");
  itemsetheader.innerHTML="Add details of each item in the package:"
  itemsetblock.appendChild(itemsetheader)


  var itemblock = document.createElement("tr");
  itemblock.setAttribute("class", "w3-card-2 itemblock w3-panel w3-mobile");


  var ihblock = document.createElement("h3");
  ihblock.setAttribute("class", "item_header w3-container");
  ihblock.innerHTML = 'Item Detail: ';
  itemblock.appendChild(ihblock);

  var itnblock = document.createElement("div");
  itnblock.setAttribute("class", "w3-container");
  itnblock.innerHTML = 'Item Name: ';

  var itn = document.createElement("INPUT");
  itn.setAttribute("id", "id_item_set-0-item_name");
  itn.setAttribute("type", "text");
  itn.setAttribute("name", "item_set-0-item_name");
  itn.setAttribute("class", "w3-input w3-border");
  itn.setAttribute("placeholder", "Please enter your items name as detailed as possible");
  itn.required = true;
  itnblock.appendChild(itn);
  itemblock.appendChild(itnblock);


  var dtblock = document.createElement("div");
  dtblock.setAttribute("class", "w3-half w3-container");
  dtblock.innerHTML = 'Item Detail: ';

  var dt = document.createElement("INPUT");
  dt.setAttribute("id", "id_item_set-0-item_detail");
  dt.setAttribute("type", "text");
  dt.setAttribute("name", "item_set-0-item_detail");
  dt.setAttribute("class", "w3-input w3-border");
  dt.setAttribute("placeholder", "color/size.etc");
  dtblock.appendChild(dt);
  itemblock.appendChild(dtblock);

  var qtblock = document.createElement("div");
  qtblock.setAttribute("class", "w3-half w3-container");
  qtblock.innerHTML = 'Quantity: ';

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
  urlblock.innerHTML = 'Item URL: ';

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
  lvr.after("Minimize this item's volume");
  itemblock.appendChild(lvrblock);

  var notblock = document.createElement("div");
  notblock.setAttribute("class", "w3-container");
  notblock.innerHTML = 'Note: ';

  var not = document.createElement("INPUT");
  not.setAttribute("id", "id_item_set-0-item_memo");
  not.setAttribute("type", "textarea");
  not.setAttribute("name", "item_set-0-item_memo");
  not.setAttribute("class", "w3-input w3-border");
  not.setAttribute("placeholder", "tell us your needs");
  notblock.appendChild(not);
  itemblock.appendChild(notblock);


  var item_table = document.createElement("table");
  item_table.style.width="100%";
  item_table.appendChild(itemblock);

  itemsetblock.appendChild(item_table);

  if($('#add_item_form').length==0){
      $('#sub_btn_block').before(itemsetblock);
      $('#add_item_form').hide().slideDown(300);
      $('#add_item_btn').text("Delect all Items");
  }//end if #add_snapshot_form exists

  else{
      $('#add_item_form').slideUp(300, function(){
        $('#add_item_form').remove();
      });
      $('#add_item_btn').text("Add Items' Detail");
    }//end of DOES NOT #add_snapshot_form exists




  $('.itemblock').formset({
      addText: 'add Item',
      deleteText: 'delete item',
      prefix: 'item_set'
  });

}//end of create item set block

function AddSnapshotBlock(){
  var snblock = document.createElement("div");
  snblock.setAttribute("class", "w3-panel w3-container");
  snblock.setAttribute("id", "add_snapshot_form");

  var hd = document.createElement("h3");
  hd.innerHTML='Add Order Snapshot of the Package:';
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
      $('#add_item_btn_row').after(snblock);
      $('#add_snapshot_form').hide().slideDown(300);
      $('#add_snapshot_btn').text("Delete Snapshot");
  }//end if #add_snapshot_form exists

  else{
      $('#add_snapshot_form').slideUp(300, function(){
        $('#add_snapshot_form').remove();
      });
      $('#add_snapshot_btn').text("Add Snapshot");
    }//end of DOES NOT #add_snapshot_form exists

}//end of AddSnapshotBlock


function clearForm(){
  $('form').find("input[type=text], textarea").val("");
}
