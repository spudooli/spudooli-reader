
var lastRead = null;

function getfocus(a, b) {
    itemid = arguments[0];
    feedid = arguments[1];

    // Decrement the feed unread count and remove the count and feed if 0
    feedunread = document.getElementById(feedid).innerText - 1;
    document.getElementById(feedid).innerText = feedunread
    if (document.getElementById(feedid).innerText == 0) {
        document.getElementById(feedid).style.display = "none";
        document.getElementById("feedname-" + feedid).style.display = "none"
    }

    // Decrement the total unread count and remove the count if 0 and update title tag
    unreadcount = document.getElementById("unreadcount").innerText - 1;
    document.getElementById("unreadcount").innerText = unreadcount
    document.title = document.getElementById("unreadcount").innerText + ' - Spudooli Feed Reader';
    if (document.getElementById("unreadcount").innerText == 0) {
        document.getElementById("unreadcount").style.display = "none";
        document.title = 'Spudooli Feed Reader';
    }

    // Hide the post when clicked
    ele = "skiddly-" + itemid;
    var x = document.getElementById(ele);
    x.style.display = "none";

    // Remember this read action so it can be undone
    lastRead = { itemid: itemid, feedid: feedid };
    document.getElementById("undo-read-btn").style.display = "inline-block";

    // Mark the post as read
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/read", true);
    var csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feed: itemid
    }));
};

function undoRead() {
    if (!lastRead) return;
    var itemid = lastRead.itemid;
    var feedid = lastRead.feedid;
    lastRead = null;

    document.getElementById("undo-read-btn").style.display = "none";

    // Show the post again
    document.getElementById("skiddly-" + itemid).style.display = "";

    // Restore feed unread count
    var feedEl = document.getElementById(feedid);
    feedEl.style.display = "";
    document.getElementById("feedname-" + feedid).style.display = "";
    feedEl.innerText = parseInt(feedEl.innerText || 0) + 1;

    // Restore total unread count
    var countEl = document.getElementById("unreadcount");
    countEl.style.display = "";
    countEl.innerText = parseInt(countEl.innerText || 0) + 1;
    document.title = countEl.innerText + ' - Spudooli Feed Reader';
};

function setstar(a) {
    itemid = arguments[0];

    document.getElementById("star-" + itemid).setAttribute('name', 'star');
    // Mark the post as Starred
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/star", true);
    var csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feed: itemid
    }));
};


setInterval("location.reload(true);", 300000);
