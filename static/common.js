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
            li.querySelector('.sonne-temp').textContent = `${result.temps[month]} °C`;
            if (result.dist) {
                li.querySelector('.sonne-dist').textContent = `${Math.round(result.dist)} km`;
            }
            ul.appendChild(li);

            sonneMap.addCity(result);
        }

    });
}

let form = document.querySelector('form');
form.addEventListener('submit', event => {
    event.preventDefault();
    form.classList.add('sonne-in-progress');
    new Promise(navigator.geolocation.getCurrentPosition).then(pos => {
        return query(pos.coords);
    }, e => {
        return query();
    }).then(() => {
        form.classList.remove('sonne-in-progress');
    });
});
