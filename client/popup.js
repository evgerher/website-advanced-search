function post_msg(url, data, func_sucess) {
  $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: func_sucess,
    failure: (errMsg) => {
        console.error(errMsg);
    }
  });
}

$(document).ready(($) => {
  post_msg("http://localhost:5000/connected", JSON.stringify({Name: "Dmitry"}), () => {})

  $('#submit').on('click', () => {
    chrome.tabs.getSelected(null, function(tab) {
      let data = $('#input-text').val();
      let url = tab.url;
      console.log(`Sending data: ${data}`)
      $p = `<p class="user">User: ${data}</p>`;
      $msgs = $('#messages')
      $msgs.append($p);

      if (data[data.length - 1] != '?') {
        post_msg("http://localhost:5000/phase1", {question: data}, (data) => {
            console.log(`Received: ${data}`);
            $p = `<p class="system">System: I would like to suggest you next recipes:</p>`;
            $msgs.append($p);
            $msgs.append('<ul>');
            for (i = 0; i < data.length; i++) {
              let item = data[i];
              $li = `<li class="system"><a href="${item.url}">${item.title}</a></li>`
              $msgs.append($li);
            }
            $msgs.append('</ul>');
        });
      } else {
        post_msg("http://localhost:5000/phase2", {question: data, url: url}, (data) => {
            console.log(`Received: ${data}`);
            $p = `<p class="system">System: The answer is "${data.answer}".</p>`;
            $msgs.append($p);
          });
      }

      $('#input-text').val('');
    });
  })

});