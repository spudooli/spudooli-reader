
function getfocus(a, b) {
    itemid = arguments[0];
    feedid = arguments[1];

    feedunread = document.getElementById(feedid).innerText - 1;
    document.getElementById(feedid).innerText = feedunread

    unreadcount = document.getElementById("unreadcount").innerText - 1;
    document.getElementById("unreadcount").innerText = unreadcount
    
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

setInterval(updatetitletag, 60000);

function updatetitletag() {
    console.log("running...");
    if (document.getElementById("unreadcount").innerText > 0) {
        $(document).prop('title', document.getElementById("unreadcount").innerText +' - Spudooli Feed Reader');
    }
}