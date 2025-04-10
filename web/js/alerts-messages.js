function mostrarAlerta({
    mensaje = "Operación realizada",
    tipo = "success", // success, danger, warning, info
    duracion = 30
} = {}) {
    let alerta = document.getElementById("alerta");

    // Si no existe, la crea
    if (!alerta) {
        alerta = document.createElement("div");
        alerta.id = "alerta";
        alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
        alerta.role = "alert";
        alerta.style = "display:none; position: fixed; top: 10px; right: 10px; z-index: 1050;";
        
        alerta.innerHTML = `
            <strong id="mensaje-alerta">${mensaje}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        `;
        
        document.body.appendChild(alerta);
    } else {
        // Reutiliza el contenedor, cambia contenido y clase
        alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
        document.getElementById("mensaje-alerta").textContent = mensaje;
    }

    // Mostrar la alerta
    alerta.style.display = "block";

    // Ocultar después de la duración especificada
    setTimeout(() => {
        alerta.style.display = "none";
    }, duracion*1000);
}

// mostrarAlerta({
//     mensaje: "Actualizado con éxito",
//     tipo: "success",
//     duracion: 5 // 5 segundos
// });

// mostrarAlerta({
//     mensaje: "Error al actualizar el registro",
//     tipo: "danger",
//     duracion: 10 // 10 segundos
// });

// mostrarAlerta({
//     mensaje: "Cuidado: estás por eliminar un elemento",
//     tipo: "warning",
//     duracion: 15
// });

console.log("alerts-messages.js cargado (versión con jQuery para UI).");
