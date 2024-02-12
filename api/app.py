from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy(app)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sides = db.Column(db.Integer)
    rolls = db.Column(db.String)

# Cria o banco de dados (será um arquivo 'results.db' na mesma pasta do script)
with app.app_context():
    db.create_all()

# Função para ler os resultados do banco de dados
def read_results():
    results = Result.query.all()
    return results

# Função para escrever um novo resultado no banco de dados
def write_result(sides, rolls):
    result = Result(sides=sides, rolls=','.join(map(str, rolls)))
    db.session.add(result)
    db.session.commit()

# Função para excluir o último resultado do banco de dados
def delete_last_result():
    last_result = Result.query.order_by(Result.id.desc()).first()
    if last_result:
        db.session.delete(last_result)
        db.session.commit()

# Função para rolar um dado de RPG
def roll_rpg_dice(sides, quantity):
    rolls = [random.randint(1, sides) for _ in range(quantity)]
    return rolls

# Rota principal
@app.route('/')
def index():
    # Exibir os resultados na tela ao iniciar a aplicação
    results = read_results()
    print("Results on start:", results)  # Adicionei este print para verificar no console
    return render_template('index.html', results=results)

# Rota para rolar os dados
@app.route('/roll_dice/<int:sides>/<int:quantity>')
def roll_dice(sides, quantity):
    # Lógica para rolar os dados
    rolls = roll_rpg_dice(sides, quantity)
    
    # Escrever o resultado no banco de dados
    write_result(sides, rolls)
    
    result = {"sides": sides, "rolls": rolls}
    return jsonify(result)

# Rota para excluir o último resultado
@app.route('/delete_last_result')
def delete_last_result_route():
    delete_last_result()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
