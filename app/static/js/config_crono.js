// // Cargamos los eventos desde localStorage.
// // Si no hay datos guardados, usamos una lista por defecto de ejemplo.
// let eventos = JSON.parse(localStorage.getItem("eventos")) || {
//   "2025-06-20": [
//     { nombre: "Los Calientes", hora: "18:00", integrantes: 3 },
//     { nombre: "La Patrulla Espacial", hora: "20:00", integrantes: 5 }
//   ],
//   "2025-06-22": [
//     { nombre: "Viva el Ruido", hora: "19:30", integrantes: 4 },
//     { nombre: "Metalhero 2323", hora: "20:30", integrantes: 5 }
//   ]
// };

// // Obtenemos referencias a los elementos del HTML que vamos a manipular.
// const contenedorEventos = document.getElementById("contenedor-eventos");
// const form = document.getElementById("form-evento");
// const cancelarBtn = document.getElementById("cancelar-edicion");

// // Esta variable la usamos para saber si estamos editando un evento existente.
// let editando = null;

// /* 
//   Función que guarda el estado actual de los eventos en el navegador.
//   Se usa para que, si el usuario cierra o recarga la página, no se pierdan los datos.
// */
// function guardarEventos() {
//   localStorage.setItem("eventos", JSON.stringify(eventos));
// }

// /*
//   Esta función se encarga de mostrar en pantalla todos los eventos guardados.
//   Recorre cada fecha y por cada evento crea un div con los datos y los botones de editar/eliminar.
// */
// function renderizarEventos() {
//   contenedorEventos.innerHTML = ""; // Limpiamos todo antes de volver a mostrar
//   const fechas = Object.keys(eventos).sort(); // Ordenamos las fechas cronológicamente

//   fechas.forEach(fecha => {
//     eventos[fecha].forEach((evento, i) => {
//       const div = document.createElement("div");
//       div.className = "evento-item";
//       div.innerHTML = `
//         <span><strong>Fecha:</strong> ${fecha}</span>
//         <span><strong>Hora:</strong> ${evento.hora}</span>
//         <span><strong>Banda:</strong> ${evento.nombre}</span>
//         <span><strong>Integrantes:</strong> ${evento.integrantes}</span>
//         <div class="botones-evento">
//           <button onclick="editarEvento('${fecha}', ${i})">Editar</button>
//           <button onclick="eliminarEvento('${fecha}', ${i})">Eliminar</button>
//         </div>
//       `;
//       contenedorEventos.appendChild(div); // Agregamos el evento al contenedor
//     });
//   });
// }

// /*
//   Evento que se dispara cuando se envía el formulario.
//   Sirve tanto para crear como para actualizar un evento.
// */
// form.addEventListener("submit", e => {
//   e.preventDefault(); // Prevenimos el comportamiento normal del formulario

//   // Tomamos los valores que el usuario completó
//   const fecha = document.getElementById("fecha").value;
//   const hora = document.getElementById("hora").value;
//   const nombre = document.getElementById("nombre").value;
//   const integrantes = parseInt(document.getElementById("integrantes").value);

//   // Si no hay eventos para esa fecha aún, creamos un arreglo vacío
//   if (!eventos[fecha]) eventos[fecha] = [];

//   /*
//     Si estamos editando, eliminamos el evento original antes de agregar el nuevo.
//     Esto es necesario porque el usuario puede cambiar la fecha, y por lo tanto
//     el evento podría ir en otro día.
//   */
//   if (editando) {
//     const { fechaOriginal, index } = editando;
//     eventos[fechaOriginal].splice(index, 1); // Eliminamos el viejo
//     editando = null; // Terminamos la edición
//   }

//   // Agregamos el evento nuevo al arreglo correspondiente
//   eventos[fecha].push({ nombre, hora, integrantes });

//   form.reset();       // Limpiamos el formulario
//   guardarEventos();   // Guardamos los cambios en localStorage
//   renderizarEventos(); // Volvemos a mostrar todo actualizado
// });

// // Botón para cancelar la edición actual y limpiar el formulario
// cancelarBtn.addEventListener("click", () => {
//   form.reset();
//   editando = null;
// });

// /*
//   Esta función se llama cuando el usuario hace clic en "Editar".
//   Carga los datos del evento en el formulario para que puedan ser modificados.
// */
// window.editarEvento = (fecha, index) => {
//   const evento = eventos[fecha][index];
//   document.getElementById("fecha").value = fecha;
//   document.getElementById("hora").value = evento.hora;
//   document.getElementById("nombre").value = evento.nombre;
//   document.getElementById("integrantes").value = evento.integrantes;

//   // Guardamos qué evento estamos editando
//   editando = { fechaOriginal: fecha, index };
// };

// /*
//   Esta función elimina un evento si el usuario lo confirma.
//   Si luego de borrar no quedan eventos en esa fecha, también borramos la fecha entera.
// */
// window.eliminarEvento = (fecha, index) => {
//   if (confirm("¿Estás seguro de que querés eliminar este evento?")) {
//     eventos[fecha].splice(index, 1);
//     if (eventos[fecha].length === 0) delete eventos[fecha]; // Borramos la fecha si está vacía
//     guardarEventos();
//     renderizarEventos();
//   }
// };

// // Cuando se carga la página, renderizamos los eventos guardados
// window.addEventListener("DOMContentLoaded", () => {
//   renderizarEventos();
// });