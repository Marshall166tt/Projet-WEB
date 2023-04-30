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
cur.execute("DELETE FROM COMMANDE_CLIENT") #remet à zéro la table commande
cur.execute("DELETE FROM COMMANDE_AGILEAN")
cur.execute("DELETE FROM COMMANDE_AGILOG")
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
	elif len(num) == 1:
		return "00"+num
	elif len(num) == 2:
		return "0"+num
	else:
		return str(num)

#Pages Accueil
@app.route('/')
def Accueil():

	return render_template('Accueil.html') # utilisation du template html accueil

#Pages Client
@app.route('/Client', methods=['GET', 'POST'])
def Client():
	if not request.method == 'POST':
		return render_template('Client.html', commande_client=BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_CLIENT"))
		
	modele = request.form.get('modele', '')	
	option1 = request.form.get('Option1')
	option2 = request.form.get('Option2')
	option3 = request.form.get('Option3')
	num = request.form.get('valide', '')
	if modele != '' :

		#print(modele, option1, option2, option3, str(option1)+str(option2)+str(option3))
		nbr = 0
		if option3:
			nbr += 100
		if option2:
			nbr += 10
		if option1:
			nbr += 1
		option = format_num(nbr)
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		cur.execute("INSERT INTO COMMANDE_CLIENT('Date', 'Modèle', 'Option', 'Etat') VALUES (?,?,?,?)", (int((time.time()-t)*100)/100, modele, option, "en attente",))
		conn.commit()
		conn.close()

	if num != '' :
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		cur.execute("SELECT Etat FROM COMMANDE_CLIENT WHERE id=?", (num,))
		row = cur.fetchone()
		etat = row["Etat"]
		if etat == "envoyée" : 
			cur.execute("UPDATE COMMANDE_CLIENT SET Etat = 'validée' WHERE id = ?", (num,))
		conn.commit()
		conn.close()
	return render_template('Client.html', commande_client = BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_CLIENT"))

#Pages AgiLean

@app.route('/AgiLean', methods=['GET', 'POST'])
def AgiLean():
	if not request.method == 'POST':
		return render_template('AgiLean.html', commande_client=BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_CLIENT"), commande_agilean=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILEAN"))
	num = request.form.get('envoye', '')
	id = request.form.get('commande', '')

	if num is not None and num != '' :
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		num = request.form.get('envoye', '')
		cur.execute("SELECT Etat FROM COMMANDE_AGILEAN WHERE id=?", (num,))
		row = cur.fetchone()
		print(row)
		etat = row["Etat"]
		if etat == "envoyée" and etat!= None : 
			cur.execute("UPDATE COMMANDE_CLIENT SET Etat = 'envoyée' WHERE id = ?", (num,))
		conn.commit()
		conn.close()

	if id is not None and id != '' :
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		id = request.form.get('commande', '')
		id = int(id)
		cur.execute("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_CLIENT WHERE id=?", (id,))
		row = cur.fetchone()
		id = row["id"]
		date = row["Date"]
		modele = row["Modèle"]
		option = row["Option"]
		etat = "en attente"

		kit = ""
		for i in range(1,15) : 
			kit_name = request.form.get(str(i))
			if kit_name == 'True' : 
				kit+= str(i)+ ", "
		kit = kit[:-2]

		cur.execute("INSERT INTO COMMANDE_AGILEAN('id','Date', 'Modèle', 'Option', 'Kit', 'Etat') VALUES (?,?,?,?,?,?)", (id,date, modele, option, kit, etat))
		conn.commit()
		conn.close()
		
	return render_template('AgiLean.html', commande_client=BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_CLIENT"), commande_agilean=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILEAN"))

#Pages AgiLog

@app.route('/AgiLog', methods=['GET', 'POST'])
def AgiLog():
	if not request.method == 'POST':
		return render_template('AgiLog.html', commande_agilean=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILEAN"), commande_agilog=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILOG"))
	
	num = request.form.get('envoye', '')
	id = request.form.get('commande', '')
	print("num",num,"id",id)

	if num is not None and num != '' :
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		num = request.form.get('envoye', '')
		cur.execute("UPDATE COMMANDE_AGILEAN SET Etat = 'envoyée' WHERE id = ?", (num,))
		conn.commit()
		conn.close()
		return render_template('AgiLog.html', commande_agilean=BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_AGILEAN"), commande_agilog=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILOG"))

	if  id != '' :
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		id = request.form.get('commande', '')
		id = int(id)
		cur.execute("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILEAN WHERE id=?", (id,))
		row = cur.fetchone()
		id = row["id"]
		date = row["Date"]
		modele = row["Modèle"]
		option = row["Option"]
		kit = row["Kit"]
		etat = row["Etat"]
		cur.execute("INSERT INTO COMMANDE_AGILOG('id','Date', 'Modèle', 'Option', 'Kit', 'Etat') VALUES (?,?,?,?,?,?)", (id, date, modele, option, kit, etat))
		conn.commit()
		conn.close()
		
		return render_template('AgiLog.html', commande_agilean=BDD("SELECT id, Date, Modèle, Option, Etat FROM COMMANDE_AGILEAN"), commande_agilog=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILOG"))

#Pages AgiParts
@app.route('/AgiParts', methods=['GET', 'POST'])
def AgiParts():
	if not request.method == 'POST':
		return render_template('AgiParts.html', commande_agilog=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILOG"))
	else:
		conn = lite.connect('BDD.db')
		conn.row_factory = lite.Row
		cur = conn.cursor()
		num = request.form.get('envoye', '')
		cur.execute("UPDATE COMMANDE_AGILOG SET Etat = 'envoyée' WHERE id = ?", (num,))
		conn.commit()
		conn.close()
		return render_template('AgiParts.html', commande_agilog=BDD("SELECT id, Date, Modèle, Option, Kit, Etat FROM COMMANDE_AGILOG"))

#Pages En Savoir Plus
@app.route('/EnSavoirPlus', methods=['GET', 'POST'])
def SavoirPlus():
	return render_template('EnSavoirPlus.html')

# ---------------------------------------
# Lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug = True)
	