from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

from config import MYSQL_DATABASE, MYSQL_HOST, PASSWORD, MYSQL_USER

app = Flask(__name__)

#lm = LoginManager(app)


# Configure db
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = MYSQL_DATABASE

#mysql:://username:password@server/db"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:9413079486@localhost/CDSlite'
# db = SQLAlchemy(app)


#bc = Bcrypt (app)

mysql = MySQL(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Returning template")
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        total_existing_users = cur.execute("SELECT * FROM User")
        cur.close()

        user_id = total_existing_users+1
        user_details = request.form
        first_name = user_details['first-name']
        last_name = user_details["last-name"]
        email = user_details['email']
        mob_number = user_details['number']
        # Add hashing for password
        password = user_details['password']
        if password == None or password == '':
            raise Exception("Password can't be empty")
        dob = user_details['dob']
        gender = user_details['gender']
        if gender == 'male':
            gender = 'M'
        else:
            gender = 'F'
        address_line = user_details['addressline']
        city = user_details['city']
        pincode = user_details['pincode']

        query = f"INSERT INTO User VALUES ({user_id},'{first_name}','{last_name}', '{email}',{mob_number},'{password}','{dob}','{gender}', '{address_line}', '{city}', {pincode})"
        print(query)
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"Unable to run query. Error: {e}")
        cur.close()
        return render_template("success.html", response="success")

    return render_template("register.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_details = request.form
        email_id = user_details['email']
        password = user_details['password']
        if password == None or password == "":
            raise Exception("Password can't be empty")
        query = f"SELECT * from User WHERE User.Email_ID='{email_id}' and User.Password_='{password}'"

        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        response = cur.fetchone()
        if response == None:
            return redirect(url_for('register'))
        return render_template("success.html", response=response)
    return render_template("login.html")


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        print("Entered")
        user_details = request.form

        user_id = "generate"
        print("")
        print(user_details)
        print("")
        first_name = user_details['first-name']
        print(first_name)
        return render_template("success.html")
    else:
        return render_template("error.html")


@app.route('/signup')
def signup():
    pass


@app.route('/product',methods=['GET', 'POST'])
def product():
    user_id = 1
    if request.method == 'POST':
        form_details = request.form
        bank = form_details['bank']
        acc = form_details["Account"]
        ifsc = form_details["IFSC"]
        query = f"SELECT SellerID,SoldProducts from Seller WHERE Seller.UserID='{user_id}'"

        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        response = cur.fetchone()
        if response == None:
            # MOdify this code, as this is not the right method
            total_existing_sellers = cur.execute("SELECT * FROM Seller")
            seller_id = "SE" + str(total_existing_sellers+1)
            query = f"INSERT INTO Seller VALUES ({seller_id},'{user_id}', ,'{bank}',{acc},'{ifsc})"
            
        else:
            seller_id = response['SellerID']
        total_pdts = cur.execute("SELECT * FROM Products")
        product_id = str(total_pdts+1) 

        return render_template("success.html", response=response)
    return render_template("addProduct.html")



@app.route('/cart')
def shopping_cart():
    pass


@app.route('/barter')
def barter():
    pass


@app.route('/order')
def order_confirmation():
    pass


if __name__ == '__main__':
    app.run(debug=True)
