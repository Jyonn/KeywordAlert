$(document).ready(function () {
    let body = $('body');
    let last_id = -1;
    let title = $('.title');
    setInterval(function () {
        let post = {
            last_id: last_id
        },
            json = encodedJSON(post);
        postJSON('/refresh', json, function (response) {
            /** @namespace response.body.logs */
            let logs = response.body.logs;
            last_id = response.body.last_id;
            for (let i = 0; i < logs.length; i++) {
                let html =
                    `<div class="hot-item item-normal">` +
                    `    <div class="kw">${logs[i].kw}</div>` +
                    `    <div class="web-count"><i class="fa fa-globe"></i> ${logs[i].web_count}</div>` +
                    `   <div class="count"><i class="fa fa-search"></i> ${logs[i].count}</div>` +
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