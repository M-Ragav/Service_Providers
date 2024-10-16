from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
data_storage =[]

# Initialize the database
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS details (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            services TEXT,
                            area TEXT,
                            phone TEXT,
                            fee TEXT,
                            subscription TEXT,
                            rating TEXT,
                            booking_option TEXT
                        )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name'].capitalize()
    services = request.form['services'].capitalize()
    area = request.form['area'].capitalize()
    phone = request.form['phone']
    fee = request.form['fee']
    subscription = request.form['subscription']
    rating = request.form['rating']
    booking_option = request.form['booking_option']

    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO details (name, services, area, phone, fee, subscription, rating, booking_option) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (name, services, area, phone, fee, subscription, rating, booking_option))
        conn.commit()
    
    # Store the details (you might want to store this in a database)
    details = {
        'name': name,
        'services': services,
        'area': area,
        'phone': phone,
        'fee': fee,
        'subscription': subscription,
        'rating': rating,
        'booking_option': booking_option
    }
    data_storage.append(details)

    return redirect(url_for('success', name=name))  # Redirect to the success page with name

@app.route('/success')
def success():
    # Get the name from query parameters if needed
    name = request.args.get('name')
    return render_template('success.html', name=name, detail=data_storage[-1])  # Display the last submitted detail


@app.route('/details')
def details_page():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM details")
        names = cursor.fetchall()
    return render_template('details.html', names=names)


@app.route('/display/<int:detail_id>')
def display_detail(detail_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM details WHERE id = ?', (detail_id,))
        detail = cursor.fetchone()
    return render_template('display.html', detail=detail)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
