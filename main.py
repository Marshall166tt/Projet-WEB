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

#Pages Accueil
@app.route('/')
def Accueil():
	return render_template('Accueil.html') # utilisation du template html accueil

#Pages Client
@app.route('/Client_Commande', methods=['GET', 'POST'])
def Client_Commande():
	return render_template('Client_Commande.html')

@app.route('/Client_Reception', methods=['GET', 'POST'])
def Client_Reception():
	return render_template('Client_Reception.html')

#Pages AgiLean
@app.route('/AgiLean_Matiere', methods=['GET', 'POST'])
def AgiLean_Matiere():
	return render_template('AgiLean_Matiere.html')

@app.route('/AgiLean_Information', methods=['GET', 'POST'])
def AgiLean_Information():
	return render_template('AgiLean_Information.html')

#Pages AgiLog
@app.route('/AgiLog_Matiere', methods=['GET', 'POST'])
def AgiLog_Matiere():
	return render_template('AgiLog_Matiere.html')

@app.route('/AgiLog_Information', methods=['GET', 'POST'])
def AgiLog_Information():
	return render_template('AgiLog_Information.html')

#Pages AgiParts
@app.route('/AgiParts', methods=['GET', 'POST'])
def AgiParts():
	return render_template('AgiParts.html')

#Pages En Savoir Plus
@app.route('/EnSavoirPlus', methods=['GET', 'POST'])
def SavoirPlus():
	return render_template('EnSavoirPlus.html')

# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
	
	
