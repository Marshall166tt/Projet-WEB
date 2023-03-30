# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

# ------------------
# Application Flask
# ------------------

app = Flask(__name__)

# ------------------
# Les différentes pages
# ------------------

#Remise à zéro base de données
con = lite.connect('BDD.db')
con.row_factory = lite.Row
cur = con.cursor()
cur.execute("DELETE FROM COMMANDE") #remet à zéro la table
con.commit()
cur.execute("UPDATE PIECES SET stock='' ") #remet à jour la table
con.commit()
lignes = cur.fetchall()
con.close()

#Pages Accueil
@app.route('/')
def Accueil():
	con = lite.connect('BDD.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	con.close()
	return render_template('Accueil.html') # utilisation du template html accueil

#Pages Client
@app.route('/Client_Commande', methods=['GET'])
def Client_Commande():
	return render_template('Client_Commande.html')

@app.route('/Client_Reception', methods=['GET'])
def Client_Reception():
	return render_template('Client_Reception.html')

#Pages AgiLean
@app.route('/AgiLean_Matiere', methods=['GET'])
def AgiLean_Matiere():
	return render_template('AgiLean_Matiere.html')

@app.route('/AgiLean_Information', methods=['GET'])
def AgiLean_Information():
	return render_template('AgiLean_Information.html')

#Pages AgiLog
@app.route('/AgiLog_Matiere', methods=['GET'])
def AgiLog_Matiere():
	return render_template('AgiLog_Matiere.html')

@app.route('/AgiLog_Information', methods=['GET'])
def AgiLog_Information():
	return render_template('AgiLog_Information.html')

#Pages AgiParts
@app.route('/AgiParts', methods=['GET'])
def AgiParts():
	return render_template('AgiParts.html')

#Pages En Savoir Plus
@app.route('/EnSavoirPlus', methods=['GET'])
def SavoirPlus():
	return render_template('EnSavoirPlus.html')

# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
	
	
