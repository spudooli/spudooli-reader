
// Reading cursor.
//
// Every article in the river gets a state:
//   'unread'   — visible, not yet marked read
//   'read'     — marked read on the server and hidden
//   'revealed' — marked read on the server but pulled back into view with `k`
//
// `cursor` is the index of the item currently at the top of the river, and
// `readHistory` is every item hidden this session, most recent last. j marks the
// current item read and moves down, k pulls the last hidden item back into
// view. Revealed items only live until the next page load — the server only
// ever sends unread items.

var items = [];
var state = [];
var readHistory = [];
var cursor = 0;

document.addEventListener('DOMContentLoaded', function () {
    items = Array.prototype.slice.call(document.querySelectorAll('.feed-item'));
    state = items.map(function () { return 'unread'; });
    readHistory = [];
    cursor = 0;
    updateUndoButton();
    document.addEventListener('keydown', onKeyDown);
});

function onKeyDown(e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;

    if (e.key === 'j') {
        e.preventDefault();
        readNext();
    } else if (e.key === 'k') {
        e.preventDefault();
        revealPrevious();
    }
}

// ── Cursor movement ──────────────────────────────────────────────

// j — mark the current item read, hide it, and move to the next one.
function readNext() {
    if (cursor >= 0 && cursor < items.length) {
        if (state[cursor] === 'unread') {
            markRead(cursor);
        }
        hide(cursor);
    }

    cursor = nextIndex();
    updateUndoButton();

    if (cursor < items.length) {
        scrollToItem(cursor);
    } else {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
}

// k — bring the last hidden item back into view. It stays read on the server,
// this is just so it can be looked at again before the next page load.
function revealPrevious() {
    if (!readHistory.length) return;
    var p = readHistory.pop();

    items[p].style.display = "";
    state[p] = 'revealed';
    // Never drag the cursor forwards — an item read out of order by clicking
    // simply rejoins the river and gets reached again on the way down.
    cursor = Math.min(cursor, p);
    updateUndoButton();
    scrollToItem(p);
}

function hide(i) {
    items[i].style.display = "none";
    state[i] = 'read';
    readHistory.push(i);
}

// The next item below the cursor that is on screen, skipping anything
// already read out of order by clicking.
function nextIndex() {
    for (var i = cursor + 1; i < items.length; i++) {
        if (state[i] === 'unread' || state[i] === 'revealed') return i;
    }
    return items.length;
}

function scrollToItem(i) {
    var header = document.querySelector('.site-header');
    var offset = header ? header.offsetHeight : 0;
    var top = items[i].getBoundingClientRect().top + window.pageYOffset - offset - 8;
    window.scrollTo({ top: Math.max(top, 0), behavior: 'smooth' });
}

// ── Marking read ─────────────────────────────────────────────────

// Click handler on the item body and date. Reads the item wherever it is in
// the river; k can always pull it straight back.
function getfocus(itemid, feedid) {
    var i = items.indexOf(document.getElementById("skiddly-" + itemid));
    if (i === -1) return;

    if (state[i] === 'unread') {
        markRead(i);
    }
    hide(i);

    // Clicking the item the cursor is sitting on moves it along, same as j.
    // Clicking further down the river leaves the cursor where it is, so j
    // still picks up from the top of what is left unread.
    if (i === cursor) {
        cursor = nextIndex();
    }
    updateUndoButton();
};

// Tell the server, and drop the sidebar counts by one.
function markRead(i) {
    var itemid = items[i].dataset.item;
    var feedid = items[i].dataset.feed;

    var feedCount = document.getElementById(feedid);
    if (feedCount) {
        var feedunread = parseInt(feedCount.innerText || 0) - 1;
        feedCount.innerText = feedunread;
        if (feedunread <= 0) {
            var feedrow = document.getElementById("feedrow-" + feedid);
            if (feedrow) feedrow.style.display = "none";
        }
    }

    var countEl = document.getElementById("unreadcount");
    if (countEl) {
        var unread = parseInt(countEl.innerText || 0) - 1;
        countEl.innerText = unread;
        document.title = unread + ' - Spudooli Feed Reader';
        if (unread <= 0) {
            countEl.style.display = "none";
            document.title = 'Spudooli Feed Reader';
        }
    }

    post("/read", itemid);
}

// ── Undo button ──────────────────────────────────────────────────

// The undo arrow is just `k` with a mouse — it can now step back
// through as many items as have been read this session.
function undoRead() {
    revealPrevious();
};

function updateUndoButton() {
    var btn = document.getElementById("undo-read-btn");
    if (btn) btn.style.display = readHistory.length ? "inline-block" : "none";
}

// ── Stars ────────────────────────────────────────────────────────

function setstar(itemid) {
    document.getElementById("star-" + itemid).setAttribute('name', 'star');
    post("/star", itemid);
};

function post(url, itemid) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    var csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        feed: itemid
    }));
}

setInterval("location.reload(true);", 300000);
