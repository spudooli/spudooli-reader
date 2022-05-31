
function getfocus(a, b) {
    itemid = arguments[0];
    feedid = arguments[1];

    // Decrement the feed unread count and remove the count and feed if 0
    feedunread = document.getElementById(feedid).innerText - 1;
    document.getElementById(feedid).innerText = feedunread
    if (document.getElementById(feedid).innerText == 0) {
        document.getElementById(feedid).style.display = "none";
        //document.getElementById("feedname-" + feedid).style.display = "none"
        document.getElementById("feedname-" + feedid).remove

    }

    // Decrement the total unread count and remove the count if 0 and update title tag
    unreadcount = document.getElementById("unreadcount").innerText - 1;
    document.getElementById("unreadcount").innerText = unreadcount
    $(document).prop('title', document.getElementById("unreadcount").innerText + ' - Spudooli Feed Reader');
    if (document.getElementById("unreadcount").innerText == 0) {
        document.getElementById("unreadcount").style.display = "none";
        $(document).prop('title', 'Spudooli Feed Reader');
    }

    // Hide the post when clicked
    ele = "skiddly-" + itemid;
    var x = document.getElementById(ele);
    x.style.display = "none";

    // Mark the post as read
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/read", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feed: itemid
    }));
};

setTimeout("location.reload(true);", 900000);