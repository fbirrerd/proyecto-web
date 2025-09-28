async function initDireccionForm(direccion) {
  const regionSelect = document.getElementById('region');
  const provSelect = document.getElementById('provincia');
  const comunaSelect = document.getElementById('comuna');

  async function loadProvincias(regionId, selected) {
    provSelect.innerHTML = "";
    if(!regionId) return;
    const res = await fetch(`/direccion/provincias/${regionId}`);
    const data = await res.json();
    provSelect.innerHTML = '<option value="">Seleccione provincia</option>';
    data.forEach(p => {
      provSelect.innerHTML += `<option value="${p.id}" ${selected==p.id?'selected':''}>${p.nombre}</option>`;
    });
  }
  async function loadComunas(provId, selected) {
    comunaSelect.innerHTML = "";
    if(!provId) return;
    const res = await fetch(`/direccion/comunas/${provId}`);
    const data = await res.json();
    comunaSelect.innerHTML = '<option value="">Seleccione comuna</option>';
    data.forEach(c => {
      comunaSelect.innerHTML += `<option value="${c.id}" ${selected==c.id?'selected':''}>${c.nombre}</option>`;
    });
  }

  regionSelect.addEventListener('change', e => loadProvincias(e.target.value));
  provSelect.addEventListener('change', e => loadComunas(e.target.value));

  // Inicializar selects si hay dirección
  if(direccion){
    await loadProvincias(direccion.id_region, direccion.id_provincia);
    await loadComunas(direccion.id_provincia, direccion.id_comuna);
  }

  // Inicializa mapa
  const map = L.map('map').setView([direccion?.latitud || -33.45, direccion?.longitud || -70.66], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OSM' }).addTo(map);
  let marker = null;
  if(direccion){
    marker = L.marker([direccion.latitud, direccion.longitud]).addTo(map);
  }

  // Click en mapa para actualizar lat/lon
  map.on('click', e => {
    if(marker) map.removeLayer(marker);
    marker = L.marker(e.latlng).addTo(map);
    document.getElementById('latitud').value = e.latlng.lat;
    document.getElementById('longitud').value = e.latlng.lng;
  });

  // Geocodificar cuando cambie calle o numero
  function geocode(){
    const calle = document.getElementById('calle').value;
    const numero = document.getElementById('numero').value;
    if(!calle) return;
    const q = encodeURIComponent(`${calle} ${numero || ''}, Chile`);
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${q}`)
      .then(r=>r.json())
      .then(res=>{
        if(res[0]){
          const {lat, lon} = res[0];
          map.setView([lat, lon], 16);
          if(marker) map.removeLayer(marker);
          marker = L.marker([lat, lon]).addTo(map);
          document.getElementById('latitud').value = lat;
          document.getElementById('longitud').value = lon;
        }
      });
  }
  document.getElementById('calle').addEventListener('blur', geocode);
  document.getElementById('numero').addEventListener('blur', geocode);

  // Guardar
  document.getElementById('direccionForm').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch('/direccion/guardar', { method: 'POST', body: formData });
    const json = await res.json();
    // comunicar al iframe padre
    if(window.parent){
      window.parent.postMessage({id_direccion: json.id_direccion}, '*');
    }
    alert("Dirección guardada. ID: " + json.id_direccion);
  });
}
