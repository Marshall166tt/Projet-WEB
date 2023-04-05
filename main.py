# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite 
import time

# ------------------
# Application Flask
# ------------------

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')

# ------------------
# Les différentes pages
# ------------------

#Remise à zéro base de données
conn = lite.connect('BDD.db')
conn.row_factory = lite.Row
cur = conn.cursor()
cur.execute("DELETE FROM COMMANDES") #remet à zéro la table commande
conn.commit()
cur.execute("UPDATE PIECES SET stock='' ") #remet à jour le stock à 0
conn.commit()
conn.close()
t = time.time()

#commandes
def BDD(command):
	conn = lite.connect('BDD.db')
	conn.row_factory = lite.Row
	cur = conn.cursor()
	cur.execute(command)
	conn.commit()
	lignes = cur.fetchall()
	conn.close()
	return lignes

def format_num(num):
	num = str(num)
	if num == "0":
		return "Sans option"
	if len(num) == 1:
		return "00"+num
	if len(num) == 2:
		return "0"+num
	else:
		return num
	
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
		return render_template('Client_Reception.html')
	else:
		modele = request.form.get('modele', '')
		option1 = request.form.get('Option1')
		option2 = request.form.get('Option2')
		option3 = request.form.get('Option3')
		#print(modele, option1, option2, option3, str(option1)+str(option2)+str(option3))
		nbr = 0
		if option3:
			nbr += 100
		if option2:
			nbr += 10
		if option1:
			nbr += 1

		option = format_num(nbr)
		print(option)

		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		cur.execute("INSERT INTO COMMANDES('Date', 'Modèle', 'Option', 'Etat_Lean', 'Etat_Log', 'Etat_Client') VALUES (?,?,?,?,?,?)", (int((time.time()-t)*100)/100, modele, str(option), "Commande passée", "En cours", "Yeey"))
		conn.commit()
		conn.close()
		redirect(url_for('Client_Reception'))
		lignes = BDD("SELECT id, Date, Modèle, Option, Etat_Lean, Etat_Client FROM COMMANDES")
		render_template('Client_Reception.html', commandes = lignes)

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
	app.run(debug = True)
	