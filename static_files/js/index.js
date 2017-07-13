function two_digits(digit) {
    if (digit < 10)
        return '0' + digit;
    else
        return '' + digit;
}

$(document).ready(function () {
    let body = $('body');
    let last_log_id = -1,
        last_news_id = -1;
    let news_title = $('.news-container'),
        word_title = $('#word-title');

    function func() {

        let post = {
            last_log_id: last_log_id,
            last_news_id: last_news_id
        },
            json = encodedJSON(post);
        postJSON('/refresh', json, function (response) {
            /** @namespace response.body.newses */
            let newses = response.body.newses;
            /** @namespace response.body.logs */
            let logs = response.body.logs;
            last_news_id = response.body.last_news_id;
            last_log_id = response.body.last_log_id;


            // maimai改
            var result = [], hash = {};
            for (var i = 0; i<newses.length; i++) { //去重
                var elem = newses[i].time;
                if (!hash[elem]) {
                    result.push(newses[i]);
                    hash[elem] = true;
                }else{
                    for (var j = 0; j<result.length; j++) { //填数据
                        if(result[j].time == elem){
                            result[j].children.push({
                                title:newses[i].children[0].title,
                                source:newses[i].children[0].source,
                                url:newses[i].children[0].url,
                            })
                        }
                    }
                }
            }
            console.log(result)
            var listarr=['<div class="title" id="news-title">新闻列表</div>'];
            for (let i = 0; i < result.length; i++) {
                let item = newses[i];
                listarr.push(`<div class="time">———————— ${item.time} ————————</div>`);
                for(var k=0;k<item.children.length;k++){
                   listarr.push(`<div class="hot-item" onclick="window.open('${item.children[k].url}')">`
                    +`    <div class="news-title"><p class="source">${item.children[k].source}</p> | ${item.children[k].title} </div>`
                    +`</div>`);
                }
                    listarr.push('<hr />');
                news_title.html(listarr.join(""))
            }
            // maimai改 end
            for (let i = 0; i < logs.length; i++) {
                let item = logs[i];
                if (logs[i].great > 1) {
                    let audio = document.createElement('audio');
                    audio.src = '/static/res/boom2.mp3';
                    audio.play();
                }
                let html = `<div class="item ${item.tag}" onclick="window.open('/keyword/${item.kw}')">${item.kw}</div>`;
                word_title.after(html)
            }
        })
    }

    func();

    setInterval(func, 60000)
});