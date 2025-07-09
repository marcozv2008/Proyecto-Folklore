// const eventos = {
//   "2025-06-20": [
//     { nombre: "Banda 1", hora: "18:00", integrantes: 3 },
//     { nombre: "Banda 2", hora: "20:00", integrantes: 5 },
//     { nombre:"Banda 3", hora:"19:00", integrantes: 5}
//   ],
//   "2025-06-21": [],

//   "2025-06-22": [
//     { nombre: "Banda 4", hora: "19:30", integrantes: 4 },
//     { nombre: "Banda 5", hora: "20:30", integrantes: 5 }
//   ],
//   "2025-06-23": [
//     { nombre:"Banda 6", hora: "21:30", integrantes: 3 }
//   ],
//   "2025-06-24": [
//     {nombre:"Banda 7", hora: "20:30", intengrantes: 3}
//   ]
// };

// const fechasContainer = document.getElementById("fechas");
// const panel = document.getElementById("panel-eventos");

// // Generar botones dinámicamente ordenados por fecha
// const fechasOrdenadas = Object.keys(eventos).sort();

// fechasOrdenadas.forEach(fecha => {
//   const boton = document.createElement("button");
//   boton.classList.add("fecha");
//   boton.dataset.dia = fecha;
  
//   // Mostrar fecha en formato dd/mm
//   const partes = fecha.split("-");
//   boton.textContent = `${partes[2]}/${partes[1]}`;
  
//   // Agregar evento click
//   boton.addEventListener("click", () => {
//     // Quitar clase activo de todos
//     document.querySelectorAll(".fecha").forEach(b => b.classList.remove("activo"));
//     boton.classList.add("activo");
//     mostrarEventos(fecha);
//   });

//   fechasContainer.appendChild(boton);
// });

// // Mostrar eventos para la primera fecha al cargar
// window.addEventListener("DOMContentLoaded", () => {
//   const primerBoton = document.querySelector(".fecha");
//   if (primerBoton) {
//     primerBoton.classList.add("activo");
//     mostrarEventos(primerBoton.dataset.dia);
//   }
// });

// function mostrarEventos(dia) {
//   const bandas = eventos[dia] || [];
//   panel.innerHTML = "";
//   panel.classList.remove("activo");

//   setTimeout(() => {
//     if (bandas.length > 0) {
//       bandas.forEach(banda => {
//         const div = document.createElement("div");
//         div.classList.add("banda");
//         div.dataset.integrantes = banda.integrantes;
//         div.innerHTML = `<strong title="${banda.nombre}">${banda.nombre}</strong><br><small>${banda.hora} hs</small>`;
//         panel.appendChild(div);
//       });
//     } else {
//       panel.innerHTML = `<p>Este día no hay eventos programados.</p>`;
//     }
//     panel.classList.add("activo");
//   }, 100);
// }
