
function getfocus(a, b) {
    itemid = arguments[0];
    feedid = arguments[1];
    
    feedunread = document.getElementById(feedid).innerText - 1;
    document.getElementById(feedid).innerText = feedunread
    
    ele = "skiddly-" + itemid;
    var x = document.getElementById(ele);
    x.style.display = "none";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/read", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feedid: itemid
    }));
};

setTimeout("location.reload(true);", 900000);