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

        if request.method == "POST":
            # Eliminar noche
            if 'eliminar_noche' in request.form:
                noche_a_eliminar = request.form['eliminar_noche']
                if noche_a_eliminar in eventos:
                    eventos.pop(noche_a_eliminar)
                    guardar_eventos(eventos)
                    mensaje = f"Noche {noche_a_eliminar} eliminada."
    # Agregar nueva noche
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

        noches = sorted(eventos.keys())
        if fecha_noche and fecha_noche in eventos:
            eventos_noche = sorted(eventos[fecha_noche], key=lambda x: x['hora'])

        return render_template("config_crono.html",
                               noches=noches,
                               eventos=eventos_noche,
                               fecha_seleccionada=fecha_noche,
                               mensaje=mensaje)

    return app
