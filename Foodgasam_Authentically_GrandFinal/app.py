import configparser
import io 
from PIL import Image
from multiprocessing import connection
from typing import ItemsView
from flask import Flask, Response, redirect, jsonify, render_template,session, request, url_for, flash

import sqlite3
app = Flask(__name__)
app.secret_key = "foodgasam"



@app.route("/")
def home():
   return render_template("index.html")

@app.route("/index/")
def index():
    return render_template("index.html")



@app.route("/aboutus/")
def aboutus():
    return render_template("aboutus.html")


@app.route("/Menu/")
def Menu():
     with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM items order by category")
        rows = cur.fetchall()
        return render_template('Menu.html', rows=rows)
 

@app.route('/signup')
def signin():
    # code to execute when the /signin endpoint is accessed
    return render_template('signup.html')

@app.route('/login')
def login():
    # code to execute when the /login endpoint is accessed
    return render_template('login.html')

@app.route('/Popular')
def Popular():
    # code to execute when the /login endpoint is accessed
    return render_template('Data_Analytics.html')


#---------- Specials----
@app.route('/Dosa')
def Dosa():
    return render_template('Dosa.html')

@app.route('/Paneer_Tikka')
def paneer_tikka():
    return render_template('Paneer_Tikka.html')

@app.route('/king_fisher')
def king_fisher():
    return render_template('king_fish_Fry.html')

@app.route('/fish_curry_thali')
def fish_curry_thali():
    return render_template('fish_curry_thali.html')

@app.route('/biriyani')
def biriyani():
    return render_template('biriyani.html')
    
@app.route('/prawns')
def prawns():
    return render_template('prawns.html')

#------------SignUp----
@app.route('/signup')
def signup():
    return render_template('signup.html')

#------------add_item--
@app.route('/itemadd')
def itemadd():
    return render_template('item.html')

@app.route('/updateitem')
def updateitem():
    return render_template('update_item.html')


#-------sql-----

import sqlite3


"""conn.execute('DROP TABLE IF EXISTS items')
conn.commit()"""
'''conn.execute('DROP TABLE IF EXISTS users')
conn.commit()'''
conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS items 
             (id INTEGER PRIMARY KEY,
             category TEXT not null,
             item_name TEXT not null,
             price REAL not null);''')
print("Table created successfully")

conn.execute('CREATE TABLE  IF NOT EXISTS users(first_name TEXT, last_name TEXT,number Varchar,age Integer, email VARCHAR, password VARCHAR,repassword VARCHAR)')
print('Table Users created successfully', flush=True)
conn.close()



# SIGNUP FUNCTIONALITY

@app.route('/addrec', methods=['POST'])
def addrec():
    try:
        # get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        number = request.form['number']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']

        # insert data into database
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (first_name, last_name, number, age, email, password,repassword) VALUES (?, ?, ?, ?, ?, ?,?)",
                        (first_name, last_name, number, age, email, password,repassword))
            con.commit()

            # set success message and flag
            success = True
            msg = "Record successfully added"
            return render_template("login.html", msg=msg, success=success)

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        msg = "Error in insert operation"
        success = False

    except KeyError as e:
        print("Missing form field:", e)
        msg = "Please fill out all required fields"
        success = False

    except Exception as e:
        print("An unexpected error occurred:", e)
        msg = "Error in insert operation"
        success = False

# LOGIN FUNCTIONALITY 

@app.route('/login_post', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    
    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Execute a SELECT query to check if the email and password match the user table
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    
    # Close the database connection
    conn.close()
    
    # If the user is found, set the email and user object in session and redirect to the home page
    if user:
        session['email'] = email
        session['user'] = user
        
        # Check if the logged-in user is an admin
        if email == 'admin@gmail.com':
            return redirect(url_for('add_item_page'))
        else:
            session['username']=user[0]
            session['mesg']="what do you want to order today?"
            firstname = get_user_firstname(email)
            return render_template('index.html', firstname=firstname)
    else:
        # If the email and password do not match, show an error message
        error = 'Invalid email or password. Please try again.'
        return render_template('login.html', error=error)

@app.route('/add_item_page')
def add_item_page():
    # Check if the user is logged in and is an admin
    if 'email' in session and session['email'] == 'admin@gmail.com':
        return render_template('item.html')
    else:
        # If the user is not logged in or is not an admin, redirect them to the login page
        return redirect(url_for('login'))


@app.route('/get_user_firstname/<email>')
def get_user_firstname(email):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Execute a parameterized SELECT query to retrieve the user's first name
    cursor.execute("SELECT first_name FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    
    # Close the database connection
    cursor.close()
    conn.close()
    
    return user[0] if user else ''



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ADMIN FUNCTIONALITIES

@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select first_name,last_name,number,age,email from users")

    rows = cur.fetchall(); 
    return render_template("signuplist.html",rows = rows)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            category = request.form['category']
            item_name = request.form['item_name']
            price = request.form['price']
           
            
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (category, item_name, price) VALUES (?, ?, ?)", 
                            (category, item_name, price))
                
                con.commit()
                msg = "New Item has been successfully added to the menu"
                
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return render_template("item.html", msg=msg)

@app.route('/update_item_price', methods=['POST'])
def update_item_price():
    item_name = request.form['item_name']
    new_price = request.form['new_price']
    
    # Update the item price in the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE items SET price = ? WHERE item_name = ?", (new_price, item_name))
    conn.commit()
    msg1 = "Price has been updated"
    
    # Redirect to the item entry page or any other page you want to display after updating the price
    return render_template("update_item.html", msg1=msg1)




# EXTRA TRIALS 
# @app.route('/home1')
# def home1():
#     # Check if the email is set in session
#     if 'email' in session:
#         return render_template('index_custom.html')
#     else:
#         # If the email is not set in session, redirect to the login page
#         return redirect(url_for('login'))

# # Route to log out the user
# @app.route('/logout')
# def logout():
#     # Remove the email from session
#     session.pop('email', None)
#     return redirect(url_for('login'))



#DELETING EXTRA COLUMNS
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# c.execute("DELETE FROM items WHERE id in (11,12,13,14,15,16,17)")
# print('deleted successfully', flush=True)
# conn.commit()
# conn.close() 

"""@app.route('/view_items_by_category', methods=['GET', 'POST'])
def view_items_by_category():
    if request.method == 'POST':
        selected_category = request.form.get('category')
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT item_name, price FROM items WHERE category = ?", (selected_category,))
            rows = cur.fetchall()
            return render_template('view_items_by_category.html', rows=rows, selected_category=selected_category)
    else:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT DISTINCT category FROM items")
            categories = cur.fetchall()
        return render_template('select_category.html', categories=categories)"""




"""@app.route('/view_items_by_category', methods=['GET'])
def view_items_by_category():
    ##category = request.args.get('category')
   # with sqlite3.connect('database.db') as con:
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT item_name, priceFROM items") 
  

        ##cur.execute("SELECT item_name, price FROM items WHERE category = ?", (category,))
    rows = cur.fetchall();
    return render_template('view_items_by_category.html', rows = rows)"""


"""@app.route('/view_items_by_category', methods=['GET'])
def view_items_by_category():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT item_name, price, item_image FROM items")
    rows = cur.fetchall()
    
    for row in rows:
        image_data = row['item_image']
        image = Image.open(io.BytesIO(image_data))
        row['item_image'] = image
    
    return render_template('view_items_by_category.html', rows=rows)"""""


#------to delete the db--------------   
"""import os
import sqlite3

# Close any open connections to the database
conn = sqlite3.connect('database.db')
conn.close()

# Drop the items table
conn = sqlite3.connect('database.db')
conn.execute("DROP TABLE items")
conn.close()

# Delete the database file
os.remove('database.db')"""
