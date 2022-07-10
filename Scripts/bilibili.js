const url = $request.url;
let body = JSON.parse($response.body);

try {
   //如果url不包含splash/list
    if (url.indexOf('splash\/list') != -1) {
        let i = body.data.items.length;
        while (i--) {
            if (body.data.list[i].is_ad == true) {
                body.data.list.splice(i, 1);
            }
        }
        i = body.data.show.length;
        while (i--) {
            body.data.show[i].stime = 0;
            body.data.show[i].etime = 1;
        }
    } else if (url.indexOf('feed\/index') != -1) {
        let i = body.data.items.length;
        while (i--) {
            if (body.data.items[i].card_goto.indexOf("ad") != -1 ||
                body.data.items[i].card_goto.indexOf("live") != -1) {
                body.data.items.splice(i, 1);
            } else if (body.data.items[i].card_goto.indexOf("banner") != -1) {
                let j = body.data.items[i].banner_item.length
                while (j--) {
                    if (body.data.items[i].banner_item[j].hasOwnProperty("is_ad") ||
                        (body.data.items[i].banner_item[j].hasOwnProperty("type") &&
                            body.data.items[i].banner_item[j].type.indexOf("ad") != -1)) {
                        body.data.items[i].banner_item.splice(j, 1);
                    }
                }
            }
        }
    }
} catch (e) {
    console.log('ERROR: bilibili_ad , ' + e)
}
body = JSON.stringify(body)
$done({
    body
