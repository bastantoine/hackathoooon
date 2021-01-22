var map = L.map('map').setView([48.358457, -4.570544], 21);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19 // https://wiki.openstreetmap.org/wiki/Zoom_levels
}).addTo(map);
