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


  $.ajax({
    type: "POST",
    url: "http://localhost:5000/connected",
    data: JSON.stringify({Name: "Dmitry"}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: (data) => {
      console.log(data);
    },
    failure: (errMsg) => {
        console.log(errMsg);
    }
  });


  var state = 0;

  $('#submit').on('click', () => {
    chrome.tabs.getSelected(null, function(tab) {
      let data = $('#input-text').val();
      let url = tab.url;
      console.log(`Sending data: ${data}`)
      $p = `<p class="user">User: ${data}</p>`;
      $msgs = $('#messages')
      $msgs.append($p);

      if (data[data.length - 1] != '?') {
        $.ajax({
          type: "POST",
          url: "http://localhost:5000/phase1",
          data: JSON.stringify({question: data}),
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          success: (data) => {
            console.log(data);
            $p = `<p class="system">System: I would like to suggest you next recipes:</p>`;
            $msgs.append($p);
            $msgs.append('<ul>');
            for (i = 0; i < data.length; i++) {
              let item = data[i];
              $li = `<li class="system"><a href="${item.url}">${item.title}</a></li>`
              $msgs.append($li);
            }
            $msgs.append('</ul>');
            state = 1;
          }
        });
      } else {
        $.ajax({
          type: "POST",
          url: "http://localhost:5000/phase2",
          data: JSON.stringify({question: data, url: url}),
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          success: (data) => {
            console.log(data);
            $p = `<p class="system">System: The answer is "${data.answer}".</p>`;
            $msgs.append($p);
            // add here fields
            state = 1;
          }
        });
      }

      $('#input-text').val('');
    });
  })

});