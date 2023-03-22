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

# connecte à la BDD, affecte le mode dictionnaire aux résultats de requêtes et renvoie un curseur
def connection_bdd():
	
	con = lite.connect('BDD.db')
	con.row_factory = lite.Row
	
	return con

#à copier et à modifier pour chaque connexion à la BDD et pour récuperer les données
# connecte à la BDD et renvoie toutes les lignes de la table personne
def selection_personnes():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT nom, prenom, role FROM personnes")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes

# crée la page web qui affiche la page d'accueil
@app.route('/Accueil')
def Accueil():
	con = connection_bdd()
	
	return render_template('Accueil.html') # utilisation du template html accueil

def reset_bdd():
	con = lite.connect('BDD.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("DELETE FROM COMMANDE") #remet à zéro la table
	con.commit()
	cur.execute("UPDATE PIECES SET stock='' ") #remet à jour la table
	con.commit()
	lignes = cur.fetchall()
	con.close()

reset_bdd()

# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
	
	
