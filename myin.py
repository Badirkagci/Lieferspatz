from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)  # erstellen von einer neuer Flask projekt
app.config['SECRET_KEY'] = 'geheimeschluessel'

benutzerdaten = {'benutzername': 'demo', 'passwort': 'geheim'}


def connect_db():  # datenbankverbindung wird damit erstellt.
    return sqlite3.connect('db.db')


def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item")
    items = cursor.fetchall()
    conn.close()
    return items


def get_all_restaurant():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Restaurant")
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants


@app.route('/')  # startpfad
def landing_page():
    return render_template('landingPage.html')


@app.route('/login', methods=['POST'])
def login():
    benutzername = request.form.get('benutzername')
    passwort = request.form.get('passwort')

    if benutzername == benutzerdaten['benutzername'] and passwort == benutzerdaten['passwort']:
        return redirect(url_for('ansicht_kunde'))
    else:
        return redirect(url_for('landing_page'))


@app.route('/registrieren', methods=['POST'])
def registrieren():
    Passwort = request.form.get('Passwort')
    Name = request.form.get('Name')
    Email = request.form.get('Email')
    Telefonnummer = request.form.get('Telefonnummer')
    Strasse = request.form.get('Strasse')
    PLZID = request.form.get('PLZID')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kunde(Name,Passwort,Telefonnummer,Strasse,PLZID) VALUES(?,?,?,?,?)",
                   (Name, Passwort, Telefonnummer, Strasse, PLZID))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))


@app.route('/Ansicht Kunde', methods=[
    'POST'])  # Bestellung wird hier verarbeitet POST wird gebraucht damit wir informationen abfangen können
def ansicht_kunde():
    restaurants = get_all_restaurant()
    return render_template('AnsichtKunde.html', restaurants=restaurants)


@app.route('/suche', methods=['POST'])
def suche():  # damit wir Suchfeld auf der Webanwendung richtig aufrufen und Ergebnisse geben können
    if request.method == 'POST':
        search_term = request.form['Suchen'].lower()

        conn = connect_db()
        cursor = conn.cursor()

        # Beispiel: Produkte filtern nach dem Suchbegriff
        cursor.execute("SELECT * FROM Restaurant WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))
        search_results = cursor.fetchall()
        conn.close()
        return render_template('suchergebnisse.html', search_results=search_results)


@app.route('/Detailansicht Kunde')
def detailAnsicht():
    item = get_all_items()
    return render_template('detailAnsichtKunde.html', items=item)


@app.route('/Warenkorb Kunde')
def warenkorb():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('warenkorbKunde.html')


@app.route('/Bezahlvorgang Kunde')
def bezahlVorgang():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('bezahlvorgangKunde.html')


@app.route('/Bestellung abgeschlossen Kunde')
def bestellung_abgeschlossen():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('bestellungAbgeschlossenKunde.html')


@app.route('/Ansicht Restaurant/Geschäft')
def ansichtRestaurant():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('ansichtRestaurant.html')


@app.route('/Bestellhistorie')
def bestellhistorie():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('bestellunghistorie.html')


@app.route('/Speisekarte Ansicht')
def speisekarteAnsicht():
    # hier kann man daten aus der Datenbank abrufen und auf der Bestätigungsseite anzeigen
    return render_template('speisekarteAnsicht.html')


if __name__ == "__main__":  # starten der App
    app.run(debug=True)

