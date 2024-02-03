from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)  # erstellen von einer neuer Flask projekt
app.config['SECRET_KEY'] = 'geheimeschluessel'

benutzerdaten = {'benutzername': 'demo', 'passwort': 'geheim'}


def connect_db():  # datenbankverbindung wird damit erstellt.
    return sqlite3.connect('DB_Lieferspatz.db')


@app.route('/')  # startpfad
def landing_page():
    return render_template('landingPage.html')


@app.route('/login', methods=['POST'])
def kundenLogin():
    benutzername = request.form.get('benutzername')
    passwort = request.form.get('passwort')

    if benutzername == benutzerdaten['benutzername'] and passwort == benutzerdaten['passwort']:
        return redirect(url_for('ansicht_kunde'))
    else:
        return redirect(url_for('landing_page'))


@app.route('/login', methods=['POST'])
def restaurantLogin():
    benutzername = request.form.get('benutzername')
    passwort = request.form.get('passwort')

    if benutzername == benutzerdaten['benutzername'] and passwort == benutzerdaten['passwort']:
        return redirect(url_for('ansichtRestaurant'))
    else:
        return redirect(url_for('landing_page'))


@app.route('/registrieren', methods=['POST'])
def registrierenKunde():
    Passwort = request.form.get('Passwort')
    Name = request.form.get('Name')
    Email = request.form.get('Email')
    Telefonnummer = request.form.get('Telefonnummer')
    Strasse = request.form.get('Strasse')
    PLZID = request.form.get('PLZID')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kunde(Name,Passwort,Telefonnummer,Strasse,PLZID) VALUES(?,?,?,?,?,?)",
                   (Name, Passwort,Email, Telefonnummer, Strasse, PLZID))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))

@app.route('/registrieren', methods=['POST'])
def registrierenRestaurant():

    Restaurantname = request.form.get('Restaurantname')
    Passwort = request.form.get('Passwort')
    Email = request.form.get('Email')
    Telefonnummer = request.form.get('Telefonnummer')
    Strasse = request.form.get('Strasse')
    PLZID = request.form.get('PLZID')
    Beschreibung = request.form.get('Beschreibung')
    Oeffnungszeit = request.form.get('Oeffnungszeit')
    Schliesszeit = request.form.get('Schliesszeit')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Restaurant(Restaurantname,Passwort,Email,Telefonnummer,Strasse,PLZID,Beschreibung,Oeffnungszeit,Schliesszeit) VALUES(?,?,?,?,?,?,?,?,?)",
                   (Restaurantname, Passwort,Email, Telefonnummer, Strasse, PLZID,Beschreibung,Oeffnungszeit,Schliesszeit))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))
def get_all_restaurant(): #alle Restaurants werden von der Datenbank aufgerufen. Dadurch bekommen wir alle Restaurants in restaurants zugewiesen.
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Restaurant")
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

@app.route('/Ansicht Kunde', methods=['POST'])  #Kunden können einen Ausblick auf alle Restaurants haben.
def ansicht_kunde():
    restaurants = get_all_restaurant()
    return render_template('AnsichtKunde.html', restaurants=restaurants)

@app.route('/suche', methods=['POST'])
def suche():  # damit wir Suchfeld auf der Webanwendung richtig aufrufen und Ergebnisse geben können
    if request.method == 'POST':
        search_term = request.form['Suchen'].lower()

        conn = connect_db()
        cursor = conn.cursor()

        #Restaurantsnamen werden nach dem Suchbegriff gefiltert.
        cursor.execute("SELECT * FROM Restaurant WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))
        search_results = cursor.fetchall()
        conn.close()
        return render_template('suchergebnisse.html', search_results=search_results)

def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item")
    items = cursor.fetchall()
    conn.close()
    return items

@app.route('/Detailansicht Kunde')
def detailAnsicht():
    item = get_all_items()
    return render_template('detailAnsichtKunde.html', item=item)

def get_item_by_id(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item WHERE ID=?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

@app.route('/Warenkorb Kunde',methods=['GET','POST'])
def warenkorb():
    if 'warenkorb' not in session:
        session['warenkorb'] = []

    if request.method == 'POST':
        itemID = request.form.get('itemID')
        menge = int(request.form.get('menge'))
        kommentar =request.form.get('kommentar')

        #um das Produkt mit der Menge zum Warenkorb hinzuzufügen
        item = get_item_by_id(itemID)
        session['warenkorb'].append({'item': itemID, 'menge': menge,'kommentar': kommentar})

    return render_template('warenkorbKunde.html', warenkorb=session['warenkorb'])

@app.route('/warenkorb/löschen/<int:item_id>', methods=['POST'])
def warenkorb_loeschen(item_id):
    if 'warenkorb' in session:
        warenkorb = session['warenkorb']

        # Durchsuche den Warenkorb nach dem zu löschenden Artikel anhand der item_id
        for position in warenkorb:
            if position['item']['id'] == item_id:
                warenkorb.remove(position)
                break

        # Aktualisiere den Warenkorb in der Session
        session['warenkorb'] = warenkorb

    return redirect(url_for('warenkorb'))


@app.route('/Bezahlvorgang Kunde',methods=['POST'])
def bezahlVorgang():
    if request.method == 'POST':

        # Beispiel: Zahlungsinformationen aus dem Formular abrufen
        name = request.form.get('Vor- und Nachname')
        adresse = request.form.get('Adresse')
        adresszusatz = request.form.get('Adresszusatz')
        optionfeld1= request.form.get('Optionfeld1')
        optionfeld2= request.form.get('Optionfeld2')
        optionfeld3 = request.form.get('Optiondeld3')

    return render_template('bezahlvorgangKunde.html')

def get_orders_by_customer_with_status(customer_id, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bestellstatus WHERE Namekunde=? AND Namerestaurant=? ORDER BY Sortierung", (customer_id, status))
    orders = cursor.fetchall()
    conn.close()
    return orders


@app.route('/Bestellung abgeschlossen Kunde')
def bestellhistorie():
    # Annahme: KundenID ist in der Session gespeichert (nach erfolgreicher Anmeldung)
    customer_id = session.get('KundenID')

    if customer_id:
        # Abrufen aller laufenden Bestellungen (Status: "laufend")
        new_orders = get_orders_by_customer_with_status(customer_id, 'neu')
        running_orders = get_orders_by_customer_with_status(customer_id, 'laufend')
        # Abrufen aller abgeschlossenen und stornierten Bestellungen
        completed_orders = get_orders_by_customer_with_status(customer_id, 'abgeschlossen')
        canceled_orders = get_orders_by_customer_with_status(customer_id, 'storniert')

        return render_template('bestellhistorie.html',
                               running_orders=running_orders,
                               new_orders=new_orders,
                               completed_orders=completed_orders,
                               canceled_orders=canceled_orders)
    else:
        # Falls keine KundenID in der Session vorhanden ist, den Benutzer zum Login weiterleiten
        return redirect(url_for('login'))
def get_orders_for_restaurant(restaurant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bestellung_Item WHERE BestellungID=? ORDER BY BestellungID DESC", (restaurant_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

@app.route('/Ansicht Restaurant/Geschäft')
def ansichtRestaurant():
    #RestaurantID wird aus der Anfrage oder Session erhalten
    restaurant_id = 1  #die entsprechende Restaurant-ID basierend auf der Anfrage oder Session erhalten

    if 'kundenID' in session:
        # Annahme: KundenID ist in der Session gespeichert (nach erfolgreicher Anmeldung)
        customer_id = session.get('kundenID')

        # Annahme: Bestellungen für das ausgewählte Restaurant abrufen
        restaurant_orders = get_orders_for_restaurant(restaurant_id)

        return render_template('ansichtRestaurant.html', restaurant_orders=restaurant_orders)
    else:
        # Falls keine KundenID in der Session vorhanden ist, den Benutzer zum Login weiterleiten
        return redirect(url_for('login'))

def get_order_history_for_restaurant(restaurant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bestellungen WHERE RestaurantID=? ORDER BY Eingangstag_uhrzeit DESC",(restaurant_id,))
    order_history = cursor.fetchall()
    conn.close()
    return order_history

@app.route('/Bestellhistorie')
def bestellHistorie():
    # Annahme: Restaurant-ID wird aus der Anfrage oder Session erhalten
    restaurant_id = 1  # Hier müsstest du die entsprechende Restaurant-ID basierend auf der Anfrage oder Session erhalten

    if 'kundenID' in session:
        # Annahme: KundenID ist in der Session gespeichert (nach erfolgreicher Anmeldung)
        customer_id = session.get('kundenID')

        # Annahme: Bestellhistorie für das ausgewählte Restaurant abrufen
        order_history = get_order_history_for_restaurant(restaurant_id)

        return render_template('bestellhistorie_restaurant.html', order_history=order_history)
    else:
        # Falls keine KundenID in der Session vorhanden ist, den Benutzer zum Login weiterleiten
        return redirect(url_for('login'))

def get_menu_for_restaurant(restaurant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item WHERE RestaurantID=?", (restaurant_id,))
    menu = cursor.fetchall()
    conn.close()
    return menu

@app.route('/Speisekarte Ansicht')
def speisekarteAnsicht():
    # Annahme: Restaurant-ID wird aus der Anfrage oder Session erhalten
    restaurant_id = 1  # Hier müsstest du die entsprechende Restaurant-ID basierend auf der Anfrage oder Session erhalten

    # Annahme: Menü für das ausgewählte Restaurant abrufen
    menu = get_menu_for_restaurant(restaurant_id)

    return render_template('speisekarteAnsicht.html', menu=menu)


if __name__ == "__main__":  # starten der App
    app.run(debug=True)

