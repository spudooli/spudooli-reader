function getfocus(a) {
    itemid = arguments[0]
    console.log(itemid);
    ele = "skiddly-" + itemid
    console.log(ele)
    var x = document.getElementById(ele);
    x.style.display = "none";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/read", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feedid: itemid
    }));
};