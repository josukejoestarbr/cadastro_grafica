from flask import Flask, request, render_template,send_file,session,redirect,json , jsonify # Importa a biblioteca
import sqlite3
import time
import sqlite3
from waitress import serve
import pymysql
import credenciais
from datetime import date

Host=''
User=''
Password=''
Db=''
Charset=''
Port=0
Host,User,Password,Db,Charset,Port=credenciais.credencialbanco()
db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)

cursor = db1.cursor()
#colocando as tabelas
sql=''' 
CREATE TABLE IF NOT EXISTS produtos(item INT PRIMARY KEY AUTO_INCREMENT ,especificacao varchar (60),valor FLOAT,folha varchar (60)) 

'''
sql1=''' 
CREATE TABLE IF NOT EXISTS produtoshistorico(item varchar(5),especificacao varchar (60),valor FLOAT,data varchar (20)) 

'''
sql2=''' 
CREATE TABLE IF NOT EXISTS vendas(item INT PRIMARY KEY AUTO_INCREMENT ,cidade varchar (60),obra varchar(60),responsavel varchar(60),cnpj varchar(60),
cliente varchar(60),valor varchar(60), valortotal INT, cadastro varchar(60),data varchar(20),servico varchar(50)) 

'''
cursor.execute(sql)
cursor.execute(sql1)
cursor.execute(sql2)
db1.commit()
db1.close()
from datetime import date
import json


app = Flask(__name__) # Inicializa a aplicação

import os
app.secret_key = "senha_secreta"
import webbrowser
def pegadata():
    data = date.today()
    data=str(data)
    data= data.split('-')
    data=data[1]+'-'+data[2]+'-'+data[0]
    return data
@app.route('/vendas', methods=['GET','POST']) # Nova rota
def vendas():
    if request.args.get('puxavendas')=='sim':
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1 = "SELECT * FROM produtos"
        cursor.execute(sql1)
        retorno = cursor.fetchall()
        print (retorno)
        return jsonify (retorno)
    if request.args.get('cadastro')=='sim':
        cidade=request.args.get('cidade')
        obra=request.args.get('obra')
        responsavel=request.args.get('responsavel')
        cnpj=request.args.get('cnpj')
        cliente=request.args.get('cliente')
        valor=request.args.get('valor')
        valortotal=request.args.get('valortotal')
        cadastro=request.args.get('cadastro')
        enderecoobra=request.args.get('enderecoobra')
        servico=request.args.get('servico')
        data=pegadata()
        data=str(data)
        #print( cidade,obra,responsavel,cnpj,cliente,valor,valortotal,cadastro,data)
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1= """INSERT INTO vendas(cidade,obra,responsavel,cnpj,cliente,valor,valortotal,cadastro,data,servico) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql1, (cidade,obra,responsavel,cnpj,cliente,valor,valortotal,enderecoobra,data,servico))
        db1.commit()
        db1.close()
        return jsonify ("valores inseridos na tabela")

    
    return render_template('vendas.html')
@app.route('/historico', methods=['GET','POST']) # Nova rota
def historico():
    
    if request.args.get('puxarhistoricoproduto')=='sim':
        idi=request.args.get('idprodutos')
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1 = "SELECT * FROM produtoshistorico WHERE item=%s"
        cursor.execute(sql1,(idi,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if request.args.get('puxarhistoricovendas')=='sim'and request.args.get('puxarhistoricovendascomum')=='sim':
        filtro=request.args.get('filtro')
        inputar=request.args.get('input')
        print('entrou aqui')
        print (filtro,inputar)
        filtro=str(filtro)
        inputar=str(inputar)
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        #fazer analise combinatoria
        if filtro=='cidade':
            sql1 = "SELECT * FROM vendas WHERE cidade LIKE %s"
        if filtro=='obra':
            sql1 = "SELECT * FROM vendas WHERE obra LIKE %s"
        if filtro=='responsavel':
            sql1 = "SELECT * FROM vendas WHERE responsavel LIKE %s"
        if filtro=='cnpj':
            sql1 = "SELECT * FROM vendas WHERE cnpj LIKE %s"
        if filtro=='cliente':
            sql1 = "SELECT * FROM vendas WHERE cliente LIKE %s"
        if filtro=='valormais':
            #print('entrou no valor')
            sql1 = "SELECT * FROM vendas WHERE valortotal >= %s"
            cursor.execute(sql1,(inputar,))
            retorno = cursor.fetchall()
            #print(retorno)
            return jsonify (retorno)
        if filtro=='valormenos':
            #print('entrou no valor')
            sql1 = "SELECT * FROM vendas WHERE valortotal <= %s"
            cursor.execute(sql1,(inputar,))
            retorno = cursor.fetchall()
            #print(retorno)
            return jsonify (retorno)
        cursor.execute(sql1,(f"%{inputar}%",))
        #sql1 = "SELECT * FROM vendas "
        #cursor.execute(sql1)
        retorno = cursor.fetchall()
        print(retorno)
        return jsonify (retorno)
    if request.args.get('puxarhistoricovendas')=='sim'and request.args.get('pesquisadata')=='sim':
        data=request.args.get('data')
        dataordem=request.args.get('dataordem')
        print(data,dataordem,'entrou na pesquisa por data')
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        if dataordem=='mais':
            sql1 = "SELECT * FROM vendas WHERE data >= %s"
            cursor.execute(sql1,(data,))
            retorno = cursor.fetchall()
            #print(retorno)
            return jsonify (retorno)
        if dataordem=='menos':
            sql1 = "SELECT * FROM vendas WHERE data <= %s"
            cursor.execute(sql1,(data,))
            retorno = cursor.fetchall()
            #print(retorno)
            return jsonify (retorno)
        if dataordem=='igual':
            sql1 = "SELECT * FROM vendas WHERE data == %s"
            cursor.execute(sql1,(data,))
            retorno = cursor.fetchall()
            #print(retorno)
            return jsonify (retorno)
    if request.args.get('deletarhistoricoproduto')=='sim':
        idihistorico=request.args.get('idhistorico')
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        cursor.execute('DELETE FROM vendas WHERE item=%s ',(idihistorico,))
        db1.commit()
        db1.close()
        retorno ="dados deletados"
        return jsonify (retorno)
        

    
    return render_template('historico.html')
@app.route('/', methods=['GET']) # Nova rota
def index():
    
    return render_template('index.html')
@app.route('/cadastro', methods=['GET','POST']) # Nova rota
def cadastro():
    if request.args.get('busca')=='sim':
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1 = "SELECT * FROM produtos"
        cursor.execute(sql1)
        retorno = cursor.fetchall()
        return jsonify (retorno)
    
    return render_template('cadastro.html')
@app.route('/inserir', methods=['GET','POST']) # Nova rota
def inserir():
    retorno=''
    if request.args.get('informacao')=='simmuda':
        indexador=request.args.get('index')
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1 = "SELECT * FROM produtos WHERE item=%s"
        cursor.execute(sql1,(indexador,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if request.args.get('informacao')=='sim':
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        sql1 = "SELECT * FROM produtos"
        cursor.execute(sql1)
        retorno = cursor.fetchall()
        return jsonify (retorno)
        

    if request.method=='POST':
        if request.form['deletar']=='sim':
            indexador=request.form['indexador']
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            cursor.execute('DELETE FROM produtos WHERE item=%s ',(indexador,))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM produtos"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            return jsonify (retorno)
        if request.form['substituir']=='sim':
            indexadoraltera=request.form['indexadoraltera']
            especificacaoaltera=request.form['especificacaoaltera']
            valoraltera=request.form['valoraltera']
            folhaaltera=request.form['folhaaltera']
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            if len(folhaaltera)>=1:
                cursor.execute("""UPDATE produtos SET especificacao =%s, valor=%s, folha=%s  WHERE item=%s """, (especificacaoaltera,valoraltera,folhaaltera,indexadoraltera))
            else:
                cursor.execute("""UPDATE produtos SET especificacao =%s, valor=%s  WHERE item=%s """, (especificacaoaltera,valoraltera,indexadoraltera))
            data=pegadata()
            sql2= """INSERT INTO produtoshistorico(especificacao,valor,data,item) VALUES (%s,%s,%s)"""
            cursor.execute(sql2, (especificacaoaltera,valoraltera,data,indexadoraltera))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM produtos"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            return jsonify (retorno)
        if request.form['folha']=='sim':
            especificacao=request.form['especificacao']
            valor=request.form['valor']
            folha=request.form['tipo']
            data=pegadata()
            data=str(data)
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1= """INSERT INTO produtos(especificacao,valor,folha) VALUES (%s,%s,%s)"""
            cursor.execute(sql1, (especificacao,valor,folha))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM produtos"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            item=retorno[0][0]
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            print(item,especificacao,valor,data)
            sql2= """INSERT INTO produtoshistorico(item,especificacao,valor,data) VALUES (%s,%s,%s,%s)"""
            cursor.execute(sql2, (item,especificacao,valor,data))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM produtos"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            return jsonify (retorno)
        if request.form['folha']=='nao':
            especificacao=request.form['especificacao']
            valor=request.form['valor']
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1= """INSERT INTO produtos(especificacao,valor) VALUES (%s,%s)"""
            cursor.execute(sql1, (especificacao,valor))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM produtos"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            return jsonify (retorno)
        
    return render_template('inserir.html')

if __name__ == '__main__':
  #serve(app, host='10.75.243.115', port=5000)
  app.run(debug=True) # Executa a aplicação
  #app.run( host='10.75.243.115', port=5000)