from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

from config import MYSQL_DATABASE, MYSQL_HOST, PASSWORD, MYSQL_USER
from helper import current_date

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
        return redirect(url_for('product'))
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

@app.route('/account/<user_id>',methods=['GET', 'POST'])
def account(user_id):
    user_id = 1
    if request.method == 'POST':
        form_details = request.form
        bank = form_details['bank']
        acc = form_details["Account"]
        ifsc = form_details["IFSC"]
        cur = mysql.connection.cursor()
        total_existing_sellers = cur.execute("SELECT * FROM Seller")
        seller_id = "SE" + str(total_existing_sellers+1)
        q = f"INSERT INTO Seller VALUES ('{seller_id}','{user_id}',0 ,'{bank}',{acc},'{ifsc}')"
        
        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        return redirect(url_for('product'))
    return render_template("acc_details.html")

@app.route('/product',methods=['GET', 'POST'])
def product():
    user_id = "1"
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * from SubCategory")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    subcatlist = cur.fetchall()
    try:
        cur.execute("SELECT * from Category")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    catlist = cur.fetchall()

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        subcat_id = form_details.getlist("scat")
        creation_date = current_date()
        query = f"SELECT SellerID from Seller WHERE Seller.UserID='{user_id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        r1 = cur.fetchone()
        seller_id = None
        if r1 == None:
            # MOdify this code, as this is not the right method
            return redirect(url_for('account',user_id=user_id))
            
        else:
            seller_id = r1[0]
            
        total_pdts = cur.execute("SELECT * FROM Products")
        product_id = str(total_pdts+1) 
        q = f"INSERT INTO Products VALUES ('{product_id}','{seller_id}')"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        # q1 = f"SELECT CategoryID from Category WHERE Category.catName='{category}'"
        # cur = mysql.connection.cursor()
        # try:
        #     cur.execute(q1)
        #     mysql.connection.commit()
        # except Exception as e:
        #     raise Exception(f"UNable to run query. Error: {e}")
        # r2 = cur.fetchone()
        # category_id = r2[0]

        isMerchandise= form_details['Merch']
        if isMerchandise == "Yes":
            mrp = form_details["MRP"]
            quantity = form_details["Quantity"]
            
            q2 = f"INSERT INTO FP_Products VALUES ('{product_id}','{pdt_name}','{desc}','Yes',{mrp},{quantity},'{creation_date}','{creation_date}','{category_id}')"
            cur = mysql.connection.cursor()
            try:
                cur.execute(q2)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            
            for i in subcat_id:
                q3 = f"INSERT INTO FPhasSubCat VALUES ('{product_id}','{i}')"
                try:
                    cur.execute(q3)
                    mysql.connection.commit()
                except Exception as e:
                    raise Exception(f"UNable to run query. Error: {e}")
                
        else:
            base_price = form_details["BasePrice"]
            is_barter = form_details["isBarter"]
            q2 = f"INSERT INTO VP_Products VALUES ('{product_id}','{pdt_name}','{desc}','Yes',{base_price},'{is_barter}','{creation_date}','{creation_date}','{category_id}')"
            cur = mysql.connection.cursor()
            try:
                cur.execute(q2)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            
            for i in subcat_id:
                q3 = f"INSERT INTO VPhasSubCat VALUES ('{product_id}','{i}')"
                try:
                    cur.execute(q3)
                    mysql.connection.commit()
                except Exception as e:
                    raise Exception(f"UNable to run query. Error: {e}")
                
        return render_template("success.html", response="done")
    return render_template("addProduct.html", subcatlist = subcatlist, catlist = catlist)

@app.route('/editproduct',methods=['GET', 'POST'])
def editproduct():
    user_id = "1"
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * from SubCategory")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    subcatlist = cur.fetchall()

    try:
        cur.execute("SELECT * from Category")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    catlist = cur.fetchall()

    try:
        cur.execute("Select * from (Select ProductID, ProductName, Description_,Availability,MRP, Quantity, CategoryID from Products natural join FP_Products where Products.ProductID = FP_Products.ProductID) as ")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    fplist = cur.fetchall()

    try:
        cur.execute("Select ProductID, ProductName, Description_,Availability,MRP, Quantity, CategoryID from Products natural join VP_Products where Products.ProductID = VP_Products.ProductID")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()

    # for i in fplist:
    #     pdt_name = i[1]
    #     desc = i[2]
    #     Available = i[3]
    #     MRP = i[4]
    #     Quant = i[5]
    #     category_id = i[6]
        

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        subcat_id = form_details.getlist("scat")
        creation_date = current_date()
        query = f"SELECT SellerID from Seller WHERE Seller.UserID='{user_id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        r1 = cur.fetchone()
        seller_id = None
        if r1 == None:
            # MOdify this code, as this is not the right method
            return redirect(url_for('account',user_id=user_id))
            
        else:
            seller_id = r1[0]
            
        total_pdts = cur.execute("SELECT * FROM Products")
        product_id = str(total_pdts+1) 
        q = f"INSERT INTO Products VALUES ('{product_id}','{seller_id}')"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        # q1 = f"SELECT CategoryID from Category WHERE Category.catName='{category}'"
        # cur = mysql.connection.cursor()
        # try:
        #     cur.execute(q1)
        #     mysql.connection.commit()
        # except Exception as e:
        #     raise Exception(f"UNable to run query. Error: {e}")
        # r2 = cur.fetchone()
        # category_id = r2[0]

        isMerchandise= form_details['Merch']
        if isMerchandise == "Yes":
            mrp = form_details["MRP"]
            quantity = form_details["Quantity"]
            
            q2 = f"INSERT INTO FP_Products VALUES ('{product_id}','{pdt_name}','{desc}','Yes',{mrp},{quantity},'{creation_date}','{creation_date}','{category_id}')"
            cur = mysql.connection.cursor()
            try:
                cur.execute(q2)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            
            for i in subcat_id:
                q3 = f"INSERT INTO FPhasSubCat VALUES ('{product_id}','{i}')"
                try:
                    cur.execute(q3)
                    mysql.connection.commit()
                except Exception as e:
                    raise Exception(f"UNable to run query. Error: {e}")
                
        else:
            base_price = form_details["BasePrice"]
            is_barter = form_details["isBarter"]
            q2 = f"INSERT INTO VP_Products VALUES ('{product_id}','{pdt_name}','{desc}','Yes',{base_price},'{is_barter}','{creation_date}','{creation_date}','{category_id}')"
            cur = mysql.connection.cursor()
            try:
                cur.execute(q2)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            
            for i in subcat_id:
                q3 = f"INSERT INTO VPhasSubCat VALUES ('{product_id}','{i}')"
                try:
                    cur.execute(q3)
                    mysql.connection.commit()
                except Exception as e:
                    raise Exception(f"UNable to run query. Error: {e}")
                
        return render_template("success.html", response="done")
    return render_template("addProduct.html", subcatlist = subcatlist, catlist = catlist)


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
