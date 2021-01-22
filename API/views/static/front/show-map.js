var map = L.map('map').setView([48.358457, -4.570544], 21);

// Do not show the map, otherwise we won't be able to zoo much into the building
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
//     maxZoom: 19 // https://wiki.openstreetmap.org/wiki/Zoom_levels
// }).addTo(map);

$.getJSON({
    url: `${API_URL}/geometry/contour`,
    success: (data) => {
        L.geoJSON(data, {style: (_) => {return {color: '#000', fill: false}}}).addTo(map);
    },
    // async: false
});

var features_rdc = []
var features_etage = []

$.getJSON({
    url: `${API_URL}/geometry/floor0`,
    success: (data) => {
        features_rdc.push(
            L.geoJSON(data, {filter: (feature) => feature.properties.type !== 'corridor'})
                .bindTooltip((layer) => layer.feature.properties.salle)
        );
    },
    async: false
});

$.getJSON({
    url: `${API_URL}/geometry/floor1`,
    success: (data) => {
        features_etage.push(
            L.geoJSON(data, {filter: (feature) => feature.properties.type !== 'corridor'})
                .bindTooltip((layer) => layer.feature.properties.salle)
        );
    },
    async: false
});

var rdc = L.layerGroup(features_rdc).addTo(map);
var etage = L.layerGroup(features_etage);

L.control.layers({
    "RDC": rdc,
    "Etage": etage
}).addTo(map);
