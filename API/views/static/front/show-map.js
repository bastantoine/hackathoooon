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

var current_displayed_path = undefined;

$("#form_itinerary").submit((event) => {
    event.preventDefault();
    var start = $("input#start").val()
    var destination = $("input#destination").val()
    if(start !== "" && destination !== "") {
        $.getJSON({
            url: `${API_URL}/api/itinerary?start=${start}&destination=${destination}`,
            success: (data) => {
                var floor_to_use = data.features[0].properties.floor === "1" ? etage: rdc;
                if(current_displayed_path !== undefined && floor_to_use.hasLayer(current_displayed_path._leaflet_id)) {
                    floor_to_use.removeLayer(current_displayed_path._leaflet_id);
                }
                current_displayed_path = data
                floor_to_use.addLayer(L.geoJSON(data, {style: (_) => {return {color: '#ff0000'}}}));

                var coordinates = data.features[0].coordinates;
                floor_to_use.addLayer(L.marker(coordinates[0].reverse()));
                floor_to_use.addLayer(L.marker(coordinates[coordinates.length - 1].reverse()));
            },
            async: false
        });
    }
});
