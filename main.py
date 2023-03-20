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

def connection_bdd():
	
	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	
	return con

@app.route('/Accueil')
def Accueil():
	con = connection_bdd()
	
	
	
	
# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
	
	
