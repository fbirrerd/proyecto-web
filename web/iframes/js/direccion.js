  // ========= Datos de ejemplo para regiones, provincias y comunas =========
  // Reemplaza estos datos y $.getJSON con tus endpoints reales si los tienes
  let regionesData = [];
  let provinciasData = [];
  let comunasData = [];

  const $region    = $('#region');
  const $provincia = $('#provincia');
  const $comuna    = $('#comuna');


  const urls = ['region', 'provincia', 'comuna'];

  fetchMultiple(urls,
    function (responses) {
      [regionesData, provinciasData, comunasData] = responses.map(r => r.respuesta ? r.data : []);
      cargarTabla();
    },
    function (err) {
      console.error("Fallo global:", err);
    }
  );

  function cargarTabla(){
    $region.html('<option value="">Seleccione región</option>');
    $.each(regionesData, function(_, r){
        $region.append(`<option value="${r.id}">${r.nombre}</option>`);
    });

  }


$(document).ready(() => {
--  // Cargar regiones

  // Cambiar región
  $region.on('change', function(){
    const rid = $(this).val();
    $provincia.html('<option value="">Seleccione provincia</option>');
    $comuna.html('<option value="">Seleccione comuna</option>');
    if (rid && provinciasData[rid]) {
      $.each(provinciasData[rid], function(_, p){
        $provincia.append(`<option value="${p.id}">${p.nombre}</option>`);
      });
    }
  });

  // Cambiar provincia
  $provincia.on('change', function(){
    const pid = $(this).val();
    $comuna.html('<option value="">Seleccione comuna</option>');
    if (pid && comunasData[pid]) {
      $.each(comunasData[pid], function(_, c){
        $comuna.append(`<option value="${c.id}">${c.nombre}</option>`);
      });
    }
  });

  // ========= Leaflet Mapa =========
  const defaultLat = -33.4489; // Santiago
  const defaultLng = -70.6693;
  const map = L.map('map').setView([defaultLat, defaultLng], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
  }).addTo(map);

  let marker = L.marker([defaultLat, defaultLng]).addTo(map);

  // Click en el mapa para seleccionar punto
  map.on('click', function(e){
    const lat = e.latlng.lat.toFixed(6);
    const lng = e.latlng.lng.toFixed(6);
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lng]).addTo(map);
    $('#latitud').val(lat);
    $('#longitud').val(lng);
  });

  // Geocodificar calle + número
  function geocode(){
    const calle = $('#calle').val().trim();
    const numero = $('#numero').val().trim();
    if(!calle) return;
    const query = encodeURIComponent(`${calle} ${numero}, Chile`);
    $.getJSON(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`, function(data){
      if (data && data.length > 0){
        const lat = parseFloat(data[0].lat).toFixed(6);
        const lon = parseFloat(data[0].lon).toFixed(6);
        if (marker) map.removeLayer(marker);
        marker = L.marker([lat, lon]).addTo(map);
        map.setView([lat, lon], 16);
        $('#latitud').val(lat);
        $('#longitud').val(lon);
      }
    });
  }

  $('#calle, #numero').on('blur', geocode);

  // ========= Envío del formulario =========
  $('#direccionForm').on('submit', function(e){
    e.preventDefault();
    const data = {
      calle:   $('#calle').val(),
      numero:  $('#numero').val(),
      region:  $region.val(),
      provincia: $provincia.val(),
      comuna:  $comuna.val(),
      latitud: $('#latitud').val(),
      longitud:$('#longitud').val()
    };
    console.log("Datos a guardar:", data);
    alert("Datos capturados. Reemplaza este alert con la llamada a tu API.\n" + JSON.stringify(data,null,2));
  });

});