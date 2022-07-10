const url = $request.url;
let newJavaScript = "<script>
let newurl = document.evaluate('//*[@id="url"]/text()', document).iterateNext();
window.location.replace(newurl.textContent)
  </script>"

var rBody = '</body>'
let body = $response.body
    .replace(rBody, newJavaScript);
$done({ body });
