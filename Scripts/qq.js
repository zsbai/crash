const url = $request.url;
let newJavaScript = '<script type="text/javascript" async="async" src="https://raw.githubusercontent.com/zsbai/crash/master/Scripts/anti_qq.js"></script>'

var rBody = '</body>'
try {
  let body = $response.body
     .replace(rBody, newJavaScript);
} catch (e) {
concole.log(e)
}
$done({ body });
