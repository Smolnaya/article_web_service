window.onload = function init() {
    // getDataFilterFromServer();
}

function updateArticle() {
    let params = getData();
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "updateArticle/");
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(params));

    xhr.onload = (e) => {
        const resp = JSON.parse(e.target.response);
        if (resp.resp === 'true') {
            window.location.reload();
        } else {
            window.alert('Ошибка при создании статьи: ' + resp.err);
        }
    };
}

function deleteArticle() {
    let params = getData();
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "deleteArticle/");
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(params));

    xhr.onload = (e) => {
        const resp = JSON.parse(e.target.response);
        if (resp.resp === 'true') {
            goHomePage();
        } else {
            window.alert('Ошибка при удалении статьи: ' + resp.err);
        }
    };
}

function unblockForm() {
    document.getElementById('articleHeader').removeAttribute("disabled");
    document.getElementById('articleDate').removeAttribute("disabled");
    document.getElementById('articleAuthor').removeAttribute("disabled");
    document.getElementById('articleText').removeAttribute("disabled");
    document.getElementById('articleTags').removeAttribute("disabled");
    document.getElementById('articleSource').removeAttribute("disabled");
    document.getElementById('btnApply').removeAttribute("disabled");
    document.getElementById("btnEdit").setAttribute("disabled", "disabled");
}

function getData() {
    let title = document.getElementById("articleHeader").value;
    let date = document.getElementById("articleDate").value;
    let author = document.getElementById("articleAuthor").value;
    let text = document.getElementById("articleText").value;
    let tags = document.getElementById("articleTags").value;
    let source = document.getElementById("articleSource").value;

    if ((title !== "") && (date !== "") && (author !== "") && (text !== "")) {
        let params = {
            "title": title,
            "date": date,
            "author": author,
            "text": text,
            "tags": tags,
            "source": source
        }
        return (params);
    } else {
        window.alert("Поля заголовок, дата, автор и текст обязательны для заполнения");
    }
}

function goHomePage() {
    window.location.href = '/';
}

function getDataFilterFromServer() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "getDataView/");
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(null);
    xhr.onload = (e) => {
        const data = JSON.parse(e.target.response);
        setDataToFilter(data);
        alert('data');
    }
}

function setDataToFilter(data) {
    for (let a of data.author) {
        $('#selectAuthor').append("<option>" + a + "</option>")
    }
    for (let a of data.source) {
        $('#selectSource').append("<option>" + a + "</option>")
    }
    for (let a of data.tags) {
        $('#selectTags').append("<option>" + a + "</option>")
    }
}