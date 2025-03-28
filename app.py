from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")
db = client['contact_book']
users = db['users']
contacts = db['contacts']

# --------------------- Registration Route ---------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if users.find_one({'email': email}):
            flash('Email already exists. Please login.', 'error')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        users.insert_one({'name': name, 'email': email, 'password': hashed_password})
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# --------------------- Login Route ---------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger') 

    return render_template('login.html')

# --------------------- Logout Route ---------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# --------------------- Display, Search & Filter Contacts ---------------------
@app.route('/index', methods=['GET'])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))

    query = {}
    
    search_term = request.args.get('search', '')
    filter_by = request.args.get('filter_by', '')

    # Search and Filter logic
    if search_term:
        if filter_by == 'name':
            query['name'] = {'$regex': search_term, '$options': 'i'}
        elif filter_by == 'phone':
            query['phone'] = {'$regex': search_term, '$options': 'i'}
        elif filter_by == 'email':
            query['email'] = {'$regex': search_term, '$options': 'i'}
        elif filter_by == 'address':
            query['address'] = {'$regex': search_term, '$options': 'i'}

    all_contacts = list(contacts.find(query))

    return render_template('index.html', contacts=all_contacts, search_term=search_term, filter_by=filter_by)

# --------------------- Add Contact  ---------------------
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        contacts.insert_one({
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        })

        flash('Contact added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_contact.html')

# --------------------- Edit Contact ---------------------
@app.route('/edit/<contact_id>', methods=['GET', 'POST'])
def edit(contact_id):
    contact = contacts.find_one({'_id': ObjectId(contact_id)})

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        contacts.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'name': name, 'phone': phone, 'email': email, 'address': address}}
        )

        flash('Contact updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', contact=contact)

# --------------------- Delete Contact ---------------------
@app.route('/delete/<contact_id>')
def delete(contact_id):
    contacts.delete_one({'_id': ObjectId(contact_id)})
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
