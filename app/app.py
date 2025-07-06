from flask import Flask, request, render_template, jsonify, redirect, url_for
import json
import os

def cargar_eventos():
    with open(os.path.join(os.path.dirname(__file__), 'eventos.json'), encoding='utf-8') as f:
        return json.load(f)

def save_eventos(eventos):
    with open(os.path.join(os.path.dirname(__file__), 'eventos.json'), 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/Login', methods=['POST'])
    def Login():
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "Marco" and password == "12345":
            return render_template('admin_general.html')
        elif username == 'Roberth' and password == '54321':
            return render_template('admin_pos.html')
        else:
            return "Ono viejo hubo un error!!!"

    @app.route('/cronograma')
    def Cronograma():
        eventos = cargar_eventos()
        fechas = sorted(eventos.keys())
    # Buscar la primera fecha con al menos un evento
        fecha_seleccionada = request.args.get('fecha')
        if not fecha_seleccionada:
            fecha_seleccionada = next((f for f in fechas if eventos[f]), fechas[0] if fechas else None)
        return render_template('cronograma.html', eventos=eventos, fecha_seleccionada=fecha_seleccionada)

    @app.route('/agregar_evento', methods=['POST'])
    def agregar_evento():
        eventos = cargar_eventos()
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        hora = request.form['hora']
        integrantes = int(request.form['integrantes'])
        if fecha not in eventos:
            eventos[fecha] = []
        eventos[fecha].append({
            "nombre": nombre,
            "hora": hora,
            "integrantes": integrantes
        })
        save_eventos(eventos)
        return redirect(url_for('ConfigCrono'))

    @app.route('/eliminar_evento', methods=['POST'])
    def eliminar_evento():
        eventos = cargar_eventos()
        fecha = request.form['fecha']
        index = int(request.form['index'])
        eventos[fecha].pop(index)
        if not eventos[fecha]:
            del eventos[fecha]
        save_eventos(eventos)
        return redirect(url_for('ConfigCrono'))

    @app.route('/editar_evento', methods=['POST'])
    def editar_evento():
        eventos = cargar_eventos()
        fecha_original = request.form['fecha_original']
        index = int(request.form['index'])
        # Eliminar el evento original
        eventos[fecha_original].pop(index)
        if not eventos[fecha_original]:
            del eventos[fecha_original]
        # Agregar el evento editado
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        hora = request.form['hora']
        integrantes = int(request.form['integrantes'])
        if fecha not in eventos:
            eventos[fecha] = []
        eventos[fecha].append({
            "nombre": nombre,
            "hora": hora,
            "integrantes": integrantes
        })
        save_eventos(eventos)
        return redirect(url_for('ConfigCrono'))

    @app.route('/config_crono')
    def ConfigCrono():
        eventos = cargar_eventos()
        return render_template('config_crono.html', eventos=eventos)

    return app