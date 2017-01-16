"use strict";

var sonneMap = sonneMap || {};

sonneMap.init = function () {
	this.markers = [];
	this.map = L.map('map', {
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

	this.map.addLayer(osm);
};

sonneMap.clearCities = function () {
	for (let marker of this.markers) {
		this.map.removeLayer(marker);
	}
	this.markes = [];
};

sonneMap.addCity = function (city) {
	let marker = L.marker(city.latlong);
	marker.bindPopup(city.name).openPopup();
	marker.addTo(this.map);
	this.markers.push(marker);
};

sonneMap.init();
