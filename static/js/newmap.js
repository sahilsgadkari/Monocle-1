var PokemonIcon = L.Icon.extend({
    options: {
        iconSize: [30, 30],
        popupAnchor: [0, -16]
    }
});
var FortIcon = L.Icon.extend({
    options: {
        iconSize: [20, 20],
        popupAnchor: [0, -10],
        className: 'fort-icon'
    }
});
var WorkerIcon = L.Icon.extend({
    options: {
        iconSize: [20, 20],
        className: 'worker-icon',
        iconUrl: '/static/img/pokeball.png'
    }
});
var NotificationIcon = L.Icon.extend({
    options: {
        iconSize: [35, 35],
        className: 'notification-icon',
        iconUrl: '/static/img/masterball.png'
    }
});
var PokestopIcon = L.Icon.extend({
    options: {
        iconSize: [20, 20],
        className: 'pokestop-icon',
        iconUrl: '/static/img/pokestop.png'
    }
}); 
var SpawnIcon = L.Icon.extend({
    options: {
        iconSize: [5, 5],
        className: 'spawn-icon',
        iconUrl: '/static/img/masterball.png'
    }
});

function getMarkers () {
    return new Promise(function (resolve, reject) {
        $.get('/data', function (response) {
            resolve(response);
        });
    });
}

var markers = {};
var overlays = {
    Pokemon: L.layerGroup([]),
    Trash: L.layerGroup([]),
    Gyms: L.layerGroup([]),
    Pokestops: L.layerGroup([]),
    Workers: L.layerGroup([]),
    Spawns: L.layerGroup([])
};

function getPopupContent (item) {
    var diff = (item.expires_at - new Date().getTime() / 1000);
    var minutes = parseInt(diff / 60);
    var seconds = parseInt(diff - (minutes * 60));
    var expires_at = minutes + 'm ' + seconds + 's';
    return '<b>#' + item.pokemon_id + ' ' + item.name + '</b> ' + expires_at;
}

function getOpacity (item) {
    var diff = (item.expires_at - new Date().getTime() / 1000);
    if (diff > 600) {
        return 1;
    }
    return 0.5 + diff / 600;
}

function PokemonMarker (raw) {
    var icon = new PokemonIcon({iconUrl: '/static/icons/' + raw.pokemon_id + '.png'});
    var marker = L.marker([raw.lat, raw.lon], {icon: icon, opacity: 1});
    marker.raw = raw;
    markers[raw.id] = marker;
    marker.on('popupopen',function popupopen (event) {
        event.popup.setContent(getPopupContent(event.target.raw));
        event.target.popupInterval = setInterval(function () {
            event.popup.setContent(getPopupContent(event.target.raw));
        }, 1000);
    });
    marker.on('popupclose', function (event) {
        clearInterval(event.target.popupInterval);
    });
    marker.setOpacity(getOpacity(marker.raw));
    marker.opacityInterval = setInterval(function () {
        var diff = marker.raw.expires_at - new Date().getTime() / 1000;
        if (diff > 0) {
            marker.setOpacity(getOpacity(marker.raw));
        } else {
            if (marker.raw.trash) {
                marker.removeFrom(overlays.Trash);
            } else {
                marker.removeFrom(overlays.Pokemons);
            }
            marker.removeFrom(map);
            markers[marker.raw.id] = undefined;
            clearInterval(marker.opacityInterval);
        }
    }, 1000);
    marker.bindPopup();
    return marker;
}

function FortMarker (raw) {
    var icon = new FortIcon({iconUrl: '/static/forts/' + raw.team + '.png'});
    var marker = L.marker([raw.lat, raw.lon], {icon: icon, opacity: 1});
    marker.raw = raw;
    markers[raw.id] = marker;
    marker.on('popupopen',function popupopen (event) {
        var pokemonName;
        if (raw.team === 0) {
            event.popup.setContent('An empty Gym!');
        } else {
            event.popup.setContent('Prestige: <b>' + raw.prestige + '</b><br>Guarding Pokemon:<br><b>' + '#' + raw.pokemon_id + ' ' + raw.pokemon_name + '</b>');
        }
    });
    marker.bindPopup();
    return marker;
}

function WorkerMarker (raw) {
    if (raw.sent_notification === true) {
        var icon = new NotificationIcon();
    } else {
        var icon = new WorkerIcon();
    }
    var marker = L.marker([raw.lat, raw.lon], {icon: icon});
    marker.raw = raw;
    markers[raw.worker_no] = marker;
    marker.bindPopup('<b>Worker ' + raw.worker_no + '</b><br>time: ' + raw.time + '<br>speed: ' + raw.speed + '<br>total seen: ' + raw.total_seen + '<br>visits: ' + raw.visits + '<br>seen here: ' + raw.seen_here);
    return marker;
}

function addMarkersToMap (data, map) {
    // Pokemons
    data.forEach(function (item) {
        var marker = null;
        if (item.type === 'pokemon') {
            // Already placed? No need to do anything, then
            if (item.id in markers) {
                return;
            }
            marker = PokemonMarker(item);
            if (item.trash) {
                marker.addTo(overlays.Trash);
            } else {
                marker.addTo(overlays.Pokemon);
            }
        } else if (item.type === 'fort') {
            // No change since last time? Then don't do anything
            var existing = markers[item.id];
            if (typeof existing !== 'undefined') {
                if (existing.raw.sighting_id === item.sighting_id) {
                    return;
                }
                existing.removeFrom(overlays.Gyms);
                markers[item.id] = undefined;
            }
            marker = FortMarker(item);
            marker.addTo(overlays.Gyms);
        } else if (item.type === 'worker') {
            var existing = markers[item.worker_no];
            if (typeof existing !== 'undefined') {
                existing.removeFrom(overlays.Workers);
                markers[item.worker_no + 'c'].removeFrom(overlays.Workers);
            }
            circle = L.circle([item.lat, item.lon], 70, {weight: 2})
            markers[item.worker_no + 'c'] = circle;
            marker = WorkerMarker(item);
            marker.addTo(overlays.Workers);
            circle.addTo(overlays.Workers);
        } else if (item.type === 'pokestop') {
            var icon = new PokestopIcon();
            var marker = L.marker([item.lat, item.lon], {icon: icon});
            marker.raw = item;
            marker.bindPopup('<b>Pokestop ' + item.external_id + '</b>');
            marker.addTo(overlays.Pokestops);
        } else if (item.type === 'spawn') {
            var circle = L.circle([item.lat, item.lon], 5, {weight: 2});
            var popup = '<b>Spawn ' + item.spawn_id + '</b><br/>time: ';
            var time = '??';
            if (item.despawn_time != null) {
                time = item.despawn_time;
            }
            else {
                circle.setStyle({color: '#f03'})
            }
            popup += time + '<br/>duration: ';
            popup += item.duration == null ? '30mn' : item.duration + 'mn';
            circle.bindPopup(popup);
            circle.addTo(overlays.Spawns);
        }
    });
}

function refresh () {
    getMarkers().then(function (data) {
        addMarkersToMap(data, map);
    });
}

function getSpawnPoints() {
    new Promise(function (resolve, reject) {
        $.get('/spawnpoints', function (response) {
            resolve(response);
        });
    }).then(function (data) {
        addMarkersToMap(data, map);
    });
}

function getPokestops() {
    new Promise(function (resolve, reject) {
        $.get('/pokestops', function (response) {
            resolve(response);
        });
    }).then(function (data) {
        addMarkersToMap(data, map);
    });
}

var map = L.map('main-map').setView([{{ map_center[0] }}, {{ map_center[1] }}], 13);
overlays.Pokemon.addTo(map);
var control = L.control.layers(null, overlays).addTo(map);
L.tileLayer('{{ map_provider_url }}', {
    opacity: 0.55,
    attribution: '{{ map_provider_attribution|safe }}'
}).addTo(map);
map.whenReady(function () {
    $('.my-location').on('click', function () {
        map.locate({ enableHighAccurracy: true, setView: true });
    });

    setInterval(refresh, 5000);
    refresh();
    getSpawnPoints();
    getPokestops();
});