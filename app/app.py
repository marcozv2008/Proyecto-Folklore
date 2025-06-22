from flask import Flask, request, render_template

def create_app(): 
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/Login', methods=['POST'])
    def Login():
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "Marco" and password == "12345" :
            return render_template('admin_general.html')
        elif username == 'Roberth' and password == '54321':
            return render_template('admin_pos.html')
        else:
            return "Ono viejo hubo un error!!!"
    
    @app.route('/cronograma')
    def Cronograma():
        return render_template('cronograma.html')
    
    @app.route('/config_crono')
    def ConfigCrono():
        return render_template('config_crono.html')
    
    return app
