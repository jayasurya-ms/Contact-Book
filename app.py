# from flask import Flask, render_template, request, redirect, url_for, flash
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import os

# app = Flask(__name__)
# app.secret_key = "contact_book_secret_key"

# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['contact_book']
# contacts = db['contacts']

# @app.route('/')
# def index():
#     all_contacts = list(contacts.find())
#     return render_template('index.html', contacts=all_contacts)

# @app.route('/add_contact', methods=['GET', 'POST'])
# def add_contact():
#     if request.method == 'POST':
#         # Required fields
#         name = request.form.get('name')
#         phone_number = request.form.get('phone_number')
        
#         # Optional fields
#         email = request.form.get('email', '')
#         address = request.form.get('address', '')
#         alternative_mobile_number = request.form.get('alternative_mobile_number', '')
        
#         # Validation for required fields
#         if not name or not phone_number:
#             flash('Name and Phone Number are required!', 'danger')
#             return redirect(url_for('add_contact'))
        
#         # Create contact document
#         contact = {
#             'name': name,
#             'phone_number': phone_number,
#             'email': email,
#             'address': address,
#             'alternative_mobile_number': alternative_mobile_number
#         }
        
#         # Insert into MongoDB
#         contacts.insert_one(contact)
#         flash('Contact added successfully!', 'success')
#         return redirect(url_for('index'))
    
#     return render_template('add_contact.html')

# # edit

# @app.route('/edit_contact/<id>', methods=['GET', 'POST'])
# def edit_contact(id):
#     contact = contacts.find_one({'_id': ObjectId(id)})
    
#     if request.method == 'POST':
#         # Required fields
#         name = request.form.get('name')
#         phone_number = request.form.get('phone_number')
        
#         # Optional fields
#         email = request.form.get('email', '')
#         address = request.form.get('address', '')
#         alternative_mobile_number = request.form.get('alternative_mobile_number', '')
        
#         # Validation for required fields
#         if not name or not phone_number:
#             flash('Name and Phone Number are required!', 'danger')
#             return redirect(url_for('edit_contact', id=id))
        
#         # Update contact document
#         updated_contact = {
#             'name': name,
#             'phone_number': phone_number,
#             'email': email,
#             'address': address,
#             'alternative_mobile_number': alternative_mobile_number
#         }
        
#         # Update in MongoDB
#         contacts.update_one({'_id': ObjectId(id)}, {'$set': updated_contact})
#         flash('Contact updated successfully!', 'success')
#         return redirect(url_for('index'))
    
#     return render_template('edit_contact.html', contact=contact)

# @app.route('/delete_contact/<id>')
# def delete_contact(id):
#     contacts.delete_one({'_id': ObjectId(id)})
#     flash('Contact deleted successfully!', 'success')
#     return redirect(url_for('index'))

# @app.route('/view_contact/<id>')
# def view_contact(id):
#     contact = contacts.find_one({'_id': ObjectId(id)})
#     return render_template('view_contact.html', contact=contact)

# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('query', '')
#     if query:
#         # Search in name, phone number, or email
#         search_results = list(contacts.find({
#             '$or': [
#                 {'name': {'$regex': query, '$options': 'i'}},
#                 {'phone_number': {'$regex': query, '$options': 'i'}},
#                 {'email': {'$regex': query, '$options': 'i'}}
#             ]
#         }))
#         return render_template('index.html', contacts=search_results, search_query=query)
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = "contact_book_secret_key"

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['contact_book']
contacts = db['contacts']

@app.route('/')
def index():
    all_contacts = list(contacts.find())
    return render_template('index.html', contacts=all_contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        # Required fields
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        # Optional fields
        email = request.form.get('email')
        address = request.form.get('address')
        alternative_mobile_number = request.form.get('alternative_mobile_number')

        # Validation for required fields
        if not name or not phone_number:
            flash('Name and Phone Number are required!', 'danger')
            return redirect(url_for('add_contact'))

        # Create contact document dynamically
        contact = {
            'name': name,
            'phone_number': phone_number
        }

        if email:
            contact['email'] = email
        if address:
            contact['address'] = address
        if alternative_mobile_number:
            contact['alternative_mobile_number'] = alternative_mobile_number

        # Insert into MongoDB
        contacts.insert_one(contact)
        flash('Contact added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_contact.html')

@app.route('/edit_contact/<id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = contacts.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        # Required fields
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        # Optional fields
        email = request.form.get('email')
        address = request.form.get('address')
        alternative_mobile_number = request.form.get('alternative_mobile_number')

        # Validation for required fields
        if not name or not phone_number:
            flash('Name and Phone Number are required!', 'danger')
            return redirect(url_for('edit_contact', id=id))

        # Prepare update query
        update_query = {'$set': {
            'name': name,
            'phone_number': phone_number
        }}

        unset_fields = {}
        if email:
            update_query['$set']['email'] = email
        else:
            unset_fields['email'] = ""

        if address:
            update_query['$set']['address'] = address
        else:
            unset_fields['address'] = ""

        if alternative_mobile_number:
            update_query['$set']['alternative_mobile_number'] = alternative_mobile_number
        else:
            unset_fields['alternative_mobile_number'] = ""

        if unset_fields:
            update_query['$unset'] = unset_fields

        # Update in MongoDB
        contacts.update_one({'_id': ObjectId(id)}, update_query)
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_contact.html', contact=contact)

@app.route('/delete_contact/<id>')
def delete_contact(id):
    contacts.delete_one({'_id': ObjectId(id)})
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/view_contact/<id>')
def view_contact(id):
    contact = contacts.find_one({'_id': ObjectId(id)})
    return render_template('view_contact.html', contact=contact)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        # Search in name, phone number, or email
        search_results = list(contacts.find({
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'phone_number': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}}
            ]
        }))
        return render_template('index.html', contacts=search_results, search_query=query)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
