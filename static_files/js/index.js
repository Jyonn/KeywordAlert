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
    let news_title = $('#news-title'),
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
            for (let i = 0; i < newses.length; i++) {
                let item = newses[i];
                let html =
                    `<div class="hot-item" onclick="window.open('${item.url}')">` +
                    `    <div class="news-title"><p class="source">${item.source}</p> | ${item.title}</div>` +
                    `    <hr>` +
                    `</div>`;
                news_title.after(html)
            }
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
            let crt_time = new Date(),
                crt_hour = two_digits(crt_time.getHours()),
                crt_minute = two_digits(crt_time.getMinutes()),
                // crt_second = crt_time.getSeconds(),
                html = `<div class="time">———————— ${crt_hour}:${crt_minute} ————————</div>`;
            if (newses.length > 0)
                news_title.after(html);
            if (logs.length > 0)
            word_title.after(html);
        })
    }

    func();

    setInterval(func, 60000)
});