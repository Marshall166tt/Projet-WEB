# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite 

# ------------------
# Application Flask
# ------------------

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')

# ------------------
# Les différentes pages
# ------------------

#Remise à zéro base de données
con = lite.connect('BDD.db')
con.row_factory = lite.Row
cur = con.cursor()
cur.execute("DELETE FROM COMMANDES") #remet à zéro la table commande
con.commit()
cur.execute("UPDATE PIECES SET stock='' ") #remet à jour le stock à 0
con.commit()
con.close()

#commandes
def BDD(command):
	con = lite.connect('BDD.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute(command)
	lignes = cur.fetchall()
	con.close()
	return lignes
	
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
	if not request.method == 'POST':
		render_template('Client_Reception.html')
	else:
		modele = request.form.get('modele')
		option1 = request.form.get('Option1')
		option2 = request.form.get('Option2')
		option3 = request.form.get('Option3')
		print(modele, option1, option2, option3)

		if (modele != None and option1 != None and option2 != None and option3 != None):
			con = lite.connect('BDD.db')
			con.row_factory = lite.Row
			cur = con.cursor()
			cur.execute("INSERT INTO COMMANDES('Modèle', 'Option') VALUES (?,?)", (modele,""+option1+option2+option3))
			con.commit()
			con.close()
			return redirect(url_for('Client_Reception.html'))
		else:
			return render_template('Client_Reception.html')

	lignes = BDD("SELECT id, Date, Modèle, Option, Etat_Lean, Etat_Client FROM COMMANDES")
	#print(lignes)
	return render_template('Client_Reception.html', commandes = lignes)

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
	