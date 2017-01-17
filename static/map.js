"use strict";

let map = L.map('map', {
	noWrap: true,
	center: [35, 0],
	zoom: 1
});

// create the tile layer with correct attribution
let osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
let osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
let osm = new L.TileLayer(osmUrl, {
	minZoom: 0,
	maxZoom: 5,
	noWrap: true,
	attribution: osmAttrib
});

map.addLayer(osm);

