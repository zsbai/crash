const url = $request.url;
let body = $response.body

let newJavaScript = '<script type="text/javascript" async="async" src="https://raw.githubusercontent.com/zsbai/crash/master/Scripts/anti_qq.js"></script>'

var rBody = '</body>'
try {
     .replace(rBody, newJavaScript);
} catch (e) {
concole.log(e)
}
$done({ body });
