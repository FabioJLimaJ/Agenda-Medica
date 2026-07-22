import json
import requests
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def carregar_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('agenda'))

    if request.method == 'POST':
        user = request.form.get('login_input')
        senha_digitada = request.form.get('senha')

        user_encontrado = Usuario.query.filter(
            (Usuario.nome == user) | (Usuario.email == user)
        ).first()

        if user_encontrado and check_password_hash(user_encontrado.senha, senha_digitada):
            login_user(user_encontrado)

            return redirect(url_for('agenda'))
        else:
            flash("Usuário/E-mail ou senha inválidos.")

    return render_template("login.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada")
    return redirect(url_for('login'))

@app.route("/api/agendamentos", methods=['GET'])
def api_agendamentos():
    dados_mockados = [
        {
            "paciente": "Ana Silva",
            "cpf": "123.456.789-00",
            "medico": "Dr. Roberto Carlos",
            "especialidade": "Cardiologia",
            "data": "25/07/2026",
            "horario": "09:00",
            "convenio": "Unimed",
            "status": "Confirmado"
        },
        {
            "paciente": "Carlos Eduardo",
            "cpf": "987.654.321-11",
            "medico": "Dra. Maria Fernanda",
            "especialidade": "Dermatologia",
            "data": "25/07/2026",
            "horario": "10:30",
            "convenio": "Bradesco Saúde",
            "status": "Pendente"
        },
        {
            "paciente": "Juliana Mendes",
            "cpf": "456.789.123-22",
            "medico": "Dr. Lucas Souza",
            "especialidade": "Ortopedia",
            "data": "26/07/2026",
            "horario": "14:00",
            "convenio": "Particular",
            "status": "Cancelado"
        }
    ]
    return jsonify(dados_mockados)

@app.route("/agenda")
@login_required
def agenda():
    agendamentos_validos = []

    try:
        response = requests.get("http://127.0.0.1:5000/api/agendamentos", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            campos_obrigatorios = ["paciente", "cpf", "medico", "especialidade", "data", "horario", "convenio", "status"]

            for item in dados:
                if isinstance(item, dict) and all(k in item for k in campos_obrigatorios):
                    agendamentos_validos.append(item)
                else:
                    flash("Aviso: Dados incompletos recebidos da API foram ignorados.")
        else:
            flash("Resposta inválida da API ao buscar agendamentos.")

    except requests.exceptions.Timeout:
        flash("Indisponibilidade temporária: A API demorou para responder.")
    except requests.exceptions.RequestException:
        flash("Erro de conexão: Não foi possível conectar à API de agendamentos.")


    return render_template("agenda.html", agendamentos_json=json.dumps(agendamentos_validos))

if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)