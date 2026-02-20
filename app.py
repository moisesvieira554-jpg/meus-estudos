import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados (SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'estudos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco
class Estudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(100), nullable=False)
    subtopico = db.Column(db.String(200), nullable=False)
    data_revisao = db.Column(db.String(10), nullable=False)
    feito = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/api/estudos', methods=['GET', 'POST'])
def gerenciar_estudos():
    if request.method == 'GET':
        estudos = Estudo.query.all()
        return jsonify([{'id':e.id, 'materia':e.materia, 'subtopico':e.subtopico, 'data':e.data_revisao, 'feito':e.feito} for e in estudos])
    
    data = request.json
    novo = Estudo(materia=data['materia'], subtopico=data['subtopico'], data_revisao=data['data'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'id': novo.id})

@app.route('/api/estudos/<int:id>', methods=['PUT', 'DELETE'])
def acao_estudo(id):
    estudo = Estudo.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(estudo)
    else:
        data = request.json
        if 'feito' in data: estudo.feito = data['feito']
    db.session.commit()
    return jsonify({'status': 'sucesso'})

if __name__ == '__main__':
    app.run(debug=True)