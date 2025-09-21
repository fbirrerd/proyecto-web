// Variables
let currentImage = null;

// Obtiene los parámetros de la carpeta y ID
const folder = $('#folder').val();
const fileId = $('#fileId').val();

// Al cargar el formulario, consulta si la imagen existe
$(document).ready(function() {
    fetchImageStatus(folder, fileId);

    // Evento para el click en el área de carga de archivos
    $('#uploadArea').on('click', function() {
        $('#fileInput').click();
    });

    // Evento para el cambio de archivo (cuando se selecciona un archivo)
    $('#fileInput').on('change', function() {
        const file = this.files[0];
        handleFile(file);
    });

    // Evento de arrastre y soltado (drag-and-drop)
    $('#uploadArea').on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
    });

    $('#uploadArea').on('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const file = e.originalEvent.dataTransfer.files[0];
        handleFile(file);
    });

    // Evento para el botón de guardar
    $('#saveBtn').on('click', saveImage);

    // Evento para el botón de eliminar
    $('#deleteBtn').on('click', deleteImage);
});

// Función para consultar si la imagen existe en la base de datos
function fetchImageStatus(folder, id) {
    $.ajax({
        url: `/consultarImagen?folder=${folder}&id=${id}`,
        method: 'GET',
        success: function(data) {
            if (data.imageExists) {
                currentImage = data.imageName;
                $('#imagePreviewImg').attr('src', `/uploads/${folder}/${currentImage}`).removeClass('hidden');
                $('#uploadArea').addClass('hidden');
                $('#buttons').removeClass('hidden');
            } else {
                $('#uploadArea').removeClass('hidden');
            }
        },
        error: function() {
            showAlert('Error al consultar imagen', 'danger');
        }
    });
}

// Función que maneja la carga de la imagen
function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        displayImage(file);
    } else {
        showAlert('Por favor, selecciona un archivo de imagen válido.', 'warning');
    }
}

// Muestra la imagen cargada
function displayImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        $('#imagePreviewImg').attr('src', e.target.result).removeClass('hidden');
        $('#uploadArea').addClass('hidden');
        $('#buttons').removeClass('hidden');
        currentImage = file.name; // Guarda el nombre del archivo
    };
    reader.readAsDataURL(file);
}

// Función para guardar la imagen
function saveImage() {
    const formData = new FormData();
    const fileInput = $('#fileInput')[0];
    if (fileInput.files.length > 0) {
        formData.append('image', fileInput.files[0]);
    }

    formData.append('folder', folder);
    formData.append('id', fileId);

    $.ajax({
        url: '/guardarImagen',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success) {
                showAlert('Imagen guardada con éxito', 'success');
                currentImage = data.imageName; // Guarda el nombre de la imagen
                fetchImageStatus(folder, fileId); // Actualiza la vista
            } else {
                showAlert('Error al guardar la imagen', 'danger');
            }
        },
        error: function() {
            showAlert('Error al guardar la imagen', 'danger');
        }
    });
}

// Función para eliminar la imagen
function deleteImage() {
    $.ajax({
        url: `/eliminarImagen?folder=${folder}&id=${fileId}`,
        method: 'GET',
        success: function(data) {
            if (data.success) {
                showAlert('Imagen eliminada con éxito', 'success');
                currentImage = null;
                fetchImageStatus(folder, fileId); // Actualiza la vista
            } else {
                showAlert('Error al eliminar la imagen', 'danger');
            }
        },
        error: function() {
            showAlert('Error al eliminar la imagen', 'danger');
        }
    });
}

// Función para mostrar alertas con Bootstrap
function showAlert(message, type) {
    const alertContainer = $('#alertContainer');
    const alert = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
                     ${message} 
                     <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                   </div>`;
    alertContainer.html(alert); // Limpia cualquier alerta previa
    setTimeout(function() {
        alertContainer.find('.alert').alert('close');
    }, 5000); // Elimina la alerta después de 5 segundos
}
