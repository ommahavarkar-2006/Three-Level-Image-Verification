// SECUREVISION — Notifications JS (localStorage-based, NO database table)

const SV_NOTIF_KEY = 'securevision_notifications';

document.addEventListener('DOMContentLoaded', function() {
    renderNotifications();
    updateNotifCount();

    // Clear all button
    const clearBtn = document.getElementById('clearNotifs');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            localStorage.removeItem(SV_NOTIF_KEY);
            renderNotifications();
            updateNotifCount();
        });
    }

    // Add sample notifications on first dashboard visit
    if (window.location.pathname.includes('/dashboard')) {
        addNotification('Successful login detected', 'success');
    }
});

function getNotifications() {
    try {
        return JSON.parse(localStorage.getItem(SV_NOTIF_KEY)) || [];
    } catch(e) {
        return [];
    }
}

function addNotification(message, type) {
    const notifs = getNotifications();
    // Avoid duplicates
    const exists = notifs.find(n => n.message === message);
    if (exists) return;

    notifs.unshift({
        message: message,
        type: type || 'info',
        time: new Date().toISOString(),
        read: false
    });

    // Keep max 20
    if (notifs.length > 20) notifs.pop();
    localStorage.setItem(SV_NOTIF_KEY, JSON.stringify(notifs));
    renderNotifications();
    updateNotifCount();
}

function renderNotifications() {
    const list = document.getElementById('notifList');
    if (!list) return;

    const notifs = getNotifications();
    if (notifs.length === 0) {
        list.innerHTML = '<div class="text-center text-muted-sv py-3">No notifications</div>';
        return;
    }

    list.innerHTML = '';
    notifs.forEach(function(notif, idx) {
        const item = document.createElement('div');
        item.className = 'notif-item' + (notif.read ? '' : ' unread');
        const iconClass = notif.type === 'success' ? 'bi-check-circle-fill text-success' :
                          notif.type === 'danger' ? 'bi-x-circle-fill text-danger' :
                          'bi-info-circle-fill text-info';
        const timeStr = timeAgo(new Date(notif.time));
        item.innerHTML = '<div class="d-flex align-items-start gap-2">' +
            '<i class="bi ' + iconClass + ' mt-1"></i>' +
            '<div><div class="small">' + notif.message + '</div>' +
            '<small class="text-muted-sv">' + timeStr + '</small></div></div>';
        item.addEventListener('click', function() {
            markAsRead(idx);
        });
        list.appendChild(item);
    });
}

function markAsRead(idx) {
    const notifs = getNotifications();
    if (notifs[idx]) {
        notifs[idx].read = true;
        localStorage.setItem(SV_NOTIF_KEY, JSON.stringify(notifs));
        renderNotifications();
        updateNotifCount();
    }
}

function updateNotifCount() {
    const badge = document.getElementById('notifCount');
    if (!badge) return;
    const notifs = getNotifications();
    const unread = notifs.filter(n => !n.read).length;
    badge.textContent = unread;
    badge.style.display = unread > 0 ? 'flex' : 'none';
}

function timeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    if (seconds < 60) return 'Just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return minutes + 'm ago';
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return hours + 'h ago';
    const days = Math.floor(hours / 24);
    return days + 'd ago';
}
