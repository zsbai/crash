const url = $request.url;
let newJavaScript = "<script>var n = document.evaluate('//*[@id="url"]/text()', document).iterateNext() && window.location.replace(n) <script/>"

var rBody = '</body>'
let body = $response.body
    .replace(rBody, newJavaScript);
$done({ body });
