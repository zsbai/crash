const url = $request.url;
let newJavaScript = "<script>
let newurl = document.evaluate('//*[@id="url"]/text()', document).iterateNext();
window.location.replace(newurl.textContent)
  </script>"

var rBody = '</body>'
try {
  let body = $response.body
     .replace(rBody, newJavaScript);
} catch (e) {
concole.log(e)
}
$done({ body });
