const url = $request.url;
let body = JSON.parse($response.body);

try {
    if (url.indexOf('feed\/index') != -1) {
        let i = body.data.items.length;
        while (i--) {
            if (body.data.items[i].card_goto.indexOf('banner') != -1 ) {
                body.data.items.splice(i,1);
            } else if (body.data.items[i].title.indexOf('C') != -1 ||
            body.data.items[i].title.indexOf('pi') != -1 ||
            body.data.items[i].title.indexOf('奶茶') != -1 ||
            body.data.items[i].title.indexOf('小由') != -1) {
                body.data.items.splice(i,1);
                console.log(body.data.items[i].title)

            }
        }

    }
} catch (e) {
    console.log("bilibili_test , " + e)
    
}
body = JSON.stringify(body)
$done({
    body
})
