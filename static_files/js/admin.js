function login() {
    var post = {
        username: $('#login-username').val(),
        password: $('#login-password').val()
    },
        json = encodedJSON(post);
    postJSON('/admin/login', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    });
}

function logout() {
    postJSON('/admin/logout', '', function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    })
}

function add_kw(add_btn_raw) {
    var kw_item = $(add_btn_raw).parent();
    var post = {
        kw: kw_item.find('.keyword').val(),
        count: kw_item.find('.count').val(),
        web_count: kw_item.find('.web-count').val()
    },
        json = encodedJSON(post);
    postJSON('/add-kw', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    })
}

function update_kw(update_btn_raw) {
    var kw_item = $(update_btn_raw).parent();
    var post = {
        id: kw_item.attr('data-id'),
        kw: kw_item.find('.keyword').val(),
        count: kw_item.find('.count').val(),
        web_count: kw_item.find('.web-count').val()
    },
        json = encodedJSON(post);
    postJSON('/update-kw', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    })
}

function delete_kw(update_btn_raw) {
    var kw_item = $(update_btn_raw).parent();
    var post = {
        id: kw_item.attr('data-id')
    },
        json = encodedJSON(post);
    postJSON('/delete-kw', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    })
}

function update_lasting() {
    var post = {
        lasting: $('#lasting').val()
    },
        json = encodedJSON(post);
    postJSON('/update-lasting', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    });
}

function update_interval() {
    var post = {
        interval: $('#interval').val()
    },
        json = encodedJSON(post);
    postJSON('/update-interval', json, function (response) {
        if (response.code === 0)
            window.location.reload();
        else
            alert(response.msg)
    });
}