$(document).ready(function () {
    let body = $('body');
    let last_log_id = -1,
        last_news_id = -1;
    let title = $('.title');
    setInterval(function () {
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
                title.after(html)
            }
            let crt_time = new Date(),
                crt_hour = crt_time.getHours(),
                crt_minute = crt_time.getMinutes(),
                // crt_second = crt_time.getSeconds(),
                html = `<div class="time">———————— ${crt_hour}:${crt_minute} ————————</div>`;
            title.after(html)
        })
    }, 60000)
});