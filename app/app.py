from flask import Flask, request, render_template, redirect, url_for
import json
import os

def cargar_eventos():
    path = os.path.join(os.path.dirname(__file__), 'eventos.json')
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({}, f)
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def guardar_eventos(eventos):
    path = os.path.join(os.path.dirname(__file__), 'eventos.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

def create_app():
    app = Flask(__name__)

 
    @app.route('/Login', methods=['POST'])
    def Login():
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "Marco" and password == "12345" :
            return render_template('admin_general.html')
        elif username == 'Roberth' and password == '54321':
            return render_template('admin_pos.html')
        else:
            return """
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
    <script>
        alert('Hubo un error en el inicio de sesión. Por favor ingrese las credenciales correctas');
        window.location.href = '/'; 
    </script>
</head>
<body></body>
</html>
"""


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/cronograma')
    def Cronograma():
        eventos = cargar_eventos()
        fecha_seleccionada = request.args.get('fecha')
        return render_template('cronograma.html', eventos=eventos, fecha_seleccionada=fecha_seleccionada)

    @app.route('/config_crono', methods=['GET', 'POST'])
    def ConfigCrono():
        eventos = cargar_eventos()
        mensaje = ""
        fecha_noche = request.args.get("fecha_noche")
        eventos_noche = []

        # --- NUEVO: Variables para edición de banda ---
        banda_a_editar = None
        idx_banda_editar = None

        if request.method == "POST":
            # Eliminar noche
            if 'eliminar_noche' in request.form:
                noche_a_eliminar = request.form['eliminar_noche']
                if noche_a_eliminar in eventos:
                    eventos.pop(noche_a_eliminar)
                    guardar_eventos(eventos)
                    mensaje = f"Noche {noche_a_eliminar} eliminada."
            # Eliminar banda
            elif 'eliminar_banda' in request.form:
                fecha = request.form['fecha_banda']
                idx = int(request.form['eliminar_banda'])
                if fecha in eventos and 0 <= idx < len(eventos[fecha]):
                    eventos[fecha].pop(idx)
                    guardar_eventos(eventos)
                    mensaje = "Banda eliminada correctamente."
                fecha_noche = fecha  # Para que siga mostrando la noche actual
            # Guardar banda modificada
            elif 'modificar_banda' in request.form:
                fecha = request.form['fecha_banda']
                idx = int(request.form['modificar_banda'])
                nombre = request.form['nombre']
                hora_inicio = request.form['hora_inicio_banda']
                hora_fin = request.form['hora_fin']
                if fecha in eventos and 0 <= idx < len(eventos[fecha]):
                    eventos[fecha][idx] = {
                        "nombre": nombre,
                        "hora": hora_inicio,
                        "hora_fin": hora_fin
                    }
                    guardar_eventos(eventos)
                    mensaje = "Banda modificada correctamente."
                fecha_noche = fecha
            # Agregar nueva banda
            elif all(k in request.form for k in ['nombre', 'hora_inicio_banda', 'hora_fin', 'fecha_banda']):
                fecha = request.form['fecha_banda']
                nombre = request.form['nombre']
                hora_inicio = request.form['hora_inicio_banda']
                hora_fin = request.form['hora_fin']

                # Validar duración
                from datetime import datetime
                fmt = "%H:%M"
                duracion = (datetime.strptime(hora_fin, fmt) - datetime.strptime(hora_inicio, fmt)).seconds // 60
                if duracion > 150:
                    mensaje = "Una banda no puede tocar más de 150 minutos."
                elif fecha not in eventos:
                    mensaje = "Primero debes crear la noche."
                else:
                    eventos[fecha].append({
                        "nombre": nombre,
                        "hora": hora_inicio,
                        "hora_fin": hora_fin
                    })
                    guardar_eventos(eventos)
                    mensaje = "Banda agregada correctamente."

        # --- NUEVO: Cargar datos para editar banda ---
        if request.method == "GET" and "editar_banda" in request.args and "fecha_noche" in request.args:
            fecha_noche = request.args["fecha_noche"]
            idx_banda_editar = int(request.args["editar_banda"])
            if fecha_noche in eventos and 0 <= idx_banda_editar < len(eventos[fecha_noche]):
                banda_a_editar = eventos[fecha_noche][idx_banda_editar]

        noches = sorted(eventos.keys())
        if fecha_noche and fecha_noche in eventos:
            eventos_noche = sorted(
                [
                    dict(banda, idx=i)
                    for i, banda in enumerate(eventos[fecha_noche])
                ],
                key=lambda x: x['hora']
            )

        return render_template("config_crono.html",
                               noches=noches,
                               eventos=eventos_noche,
                               fecha_seleccionada=fecha_noche,
                               mensaje=mensaje,
                               banda_a_editar=banda_a_editar,
                               idx_banda_editar=idx_banda_editar)

    return app
