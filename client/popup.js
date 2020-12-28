// document.addEventListener('DOMContentLoaded', function() {
//   var checkPageButton = document.getElementById('checkPage');
//   checkPageButton.addEventListener('click', function() {
//
//     chrome.tabs.getSelected(null, function(tab) {
//       d = document;
//
//       var f = d.createElement('form');
//       f.action = 'http://127.0.0.1:5000/connected';
//       f.method = 'post';
//       var i = d.createElement('input');
//       i.type = 'hidden';
//       i.name = 'url';
//       i.value = tab.url;
//       f.appendChild(i);
//       d.body.appendChild(f);
//       f.submit();
//     });
//   }, false);
// }, false);

$(document).ready(($) => {
  // $.post(
  //     "http://localhost:5000/connected",
  //     JSON.stringify({"Name": "Dmitry"}),
  //     function( data ) {
  //       console.log(data);
  // });

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/connected",
    data: JSON.stringify({Name: "Dmitry"}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){console.log(data);},
    failure: function(errMsg) {
        console.log(errMsg);
    }
  });
});