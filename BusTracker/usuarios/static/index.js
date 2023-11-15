let map;
function initpam(){
    const colCoords = {lat: 4.57, lng:-74.29};
    const map = new google.maps.Map(mapDiv, {
        center: colCoords,
        zoom: 6,
    });
    const marker = new google.maps.Marker({
        position: colCoords,
        map,
    });

    button2.addEventListener('click', ()=>{
        const coords2 = {
            lat: 6.200271,
            lng: -75.577620
        };
        map.setCenter(coords2);
        map.setZoom(15);
        marker.setPosition(coords2);
    })

    button3.addEventListener('click', ()=>{
        const coords3 = {
            lat: 6.225827,
            lng: -75.574980
        };
        map.setCenter(coords3);
        map.setZoom(15);
        marker.setPosition(coords3);
    })

    button.addEventListener('click', ()=>{
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(
                (position)=>{
                    const coords = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    console.log(coords);
                    map.setCenter(coords);
                    map.setZoom(15);
                    marker.setPosition(coords);

                    // Punto de partida y destino
                    var startPoint = new google.maps.LatLng(coords[0], coords[1]);
                    var endPoint1 = document.getElementById("destination").textContent;
                    
                }
            );
        }else{
            alert(
                "Tu navegador no dispone de la geolocalizacion, actualizalo para continuar"
            );
        }
    })
}
