"use strict";

function query(pos) {
    let ul = document.querySelector('ul');
    ul.textContent = '';

    let month = form.elements['month'].value;

    let url = `/api/query?temp=${form.elements['temp'].value}&month=${month}`;
    if (pos) {
        url += `&latlong=${pos.latitude},${pos.longitude}`
    }
    fetch(url).then(response => response.json()).then(results => {
        document.body.classList.toggle('sonne-no-results', results.length === 0);
        for (let result of results) {
            console.log(result);
            let li = document.createElement('li');
            li.appendChild(document.importNode(document.querySelector('#sonne-city-template').content, true));
            li.querySelector('.sonne-city').textContent = result.name;
            li.querySelector('.sonne-temp').textContent = `${result.temps[month]} °C`;
            if (result.dist) {
                li.querySelector('.sonne-dist').textContent = `${Math.round(result.dist)} km`;
            }
            ul.appendChild(li);
        }
    });
}

let form = document.querySelector('form');
form.addEventListener('submit', event => {
    event.preventDefault();
    navigator.geolocation.getCurrentPosition(pos => {
        query(pos.coords);
    }, e => {
        query();
    });
});
