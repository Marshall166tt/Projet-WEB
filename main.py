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



# crée la page web qui affiche la page d'accueil
@app.route('/')
def Accueil():
#	con = connection_bdd()
	return render_template('Accueil.html') # utilisation du template html accueil

@app.route('/')
def Client():
	return render_template('Client.html')

@app.route('/AgiLean')
def AgiLean():
	return render_template('AgiLean.html')

@app.route('/AgiLog')
def AgiLog():
	return render_template('AgiLog.html')

@app.route('/AgiParts')
def AgiParts():
	return render_template('AgiParts.html')


# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
	
	
