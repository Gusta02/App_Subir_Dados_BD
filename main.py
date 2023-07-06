from flask import Flask, render_template, request
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database'
db = SQLAlchemy(app)

class TableData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column1 = db.Column(db.String)
    column2 = db.Column(db.String)
   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global df
    file = request.files['file']
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        return "Tipo de arquivo inválido. Apenas arquivos .xlsx ou .csv são permitidos."

    return render_template('table.html', table=df)

@app.route('/edit', methods=['POST'])
def edit():
    global df
    row = int(request.form['row'])
    column = request.form['column']
    value = request.form['value']
    df.loc[row, column] = value
    return render_template('table.html', table=df)

@app.route('/save', methods=['POST'])
def save():
    global df
    df.to_csv('output.csv', index=False)
    return render_template('saved.html', table=df)

@app.route('/upload_db', methods=['POST'])
def upload_db():
    global df
    file_name = f'upload_{date.today()}.csv'
    file_path = os.path.join('uploads', file_name)
    df.to_csv(file_path, index=False)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df.to_sql('table_data', engine, if_exists='replace', index=False)
    
    return "Dados enviados para o banco de dados com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
