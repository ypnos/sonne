"use strict";

function query(pos) {

    let ul = document.querySelector('ul');

    let month = form.elements['month'].value;

    let url = `/api/query?temp=${form.elements['temp'].value}&month=${month}`;
    if (pos) {
        url += `&latlong=${pos.latitude},${pos.longitude}`
    }
    return fetch(url).then(response => response.json()).then(results => {
        document.body.classList.toggle('sonne-no-results', results.length === 0);
        ul.textContent = '';
        sonneMap.clearCities();
        for (let result of results) {
            console.log(result);
            let li = document.createElement('li');
            li.classList.add('list-group-item');
            li.appendChild(document.importNode(document.querySelector('#sonne-city-template').content, true));
            let a = li.querySelector('.sonne-city a');
            a.href = `https://www.google.com/maps/dir/Current+Location/${result.name},${result.country}`;
            a.textContent = result.name;
            li.querySelector('.sonne-city small').textContent = result.country;

            let updateLi = function (selector, text) {
                if (text) {
                    li.querySelector(selector + ' span:last-child').textContent = text;
                } else {
                    li.querySelector(selector).remove(); // no data, so don't display
                }
            }
            updateLi('.sonne-maxtemp', (result.maxtemps[month] !== null ? `${result.maxtemps[month]} °C` : null));
            updateLi('.sonne-mintemp', (result.mintemps[month] !== null ? `${result.mintemps[month]} °C` : null));
            updateLi('.sonne-raindays', (result.raindays[month] > -1 ? result.raindays[month] : null));
            updateLi('.sonne-dist', (result.dist ? `${Math.round(result.dist)} km` : null));
            ul.appendChild(li);

            sonneMap.addCity(result);
        }

    });
}

let form = document.querySelector('form');
form.addEventListener('submit', event => {
    event.preventDefault();
    form.classList.add('sonne-in-progress');
    new Promise(navigator.geolocation.getCurrentPosition.bind(navigator.geolocation)).then(pos => {
        return query(pos.coords);
    }, e => {
        return query();
    }).then(() => {
        form.classList.remove('sonne-in-progress');
    });
});
