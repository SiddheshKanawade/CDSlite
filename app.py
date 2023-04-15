import razorpay

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify, make_response
from src.helper import current_date, generate_uuid
from src.db import create_app
from src.helper import generate_uuid
from werkzeug.utils import secure_filename
import os
import time
import base64
import mysql.connector
from mysql.connector.conversion import MySQLConverter

app, mysql, razorpay_client = create_app()

# @app.route('/upload', methods=['POST'])
# def upload():
#   images = request.files.getlist('images[]')

#   for image in images:
#     filename = secure_filename(image.filename)
#     path = os.path.join('uploads', filename)
#     image.save(path)

#     print("in file upload")
#     # Insert the image path into the SQL database here

#   return 'Upload successful'
# HELPER FUNCTIONS
@app.route('/payment/<price>', methods=['GET', 'POST'])
def pay(price):
    # Get payment amount from the form
    # print("Entered")
    # print(price)
    amount = int(price)  # convert to paise
    currency = "INR"

    # Create a Razorpay order
    order = razorpay_client.order.create({
        'amount': amount,  # Razorpay requires amount in paise
        'currency': currency,
        'payment_capture': 1  # Automatically capture the payment when it is made
    })

    # Extract the order ID from the response
    order_id = order['id']
    # print(order)

    # Return the order ID to the client
    return order


def update_user(user_details, user_id):
    first_name = user_details['first-name']
    last_name = user_details["last-name"]
    email = user_details['email']
    mob_number = user_details['number']
    addressline = MySQLConverter().escape(user_details['addressline'])
    city = user_details['city']
    pincode = user_details['pincode']

    query = f"UPDATE User SET FirstName='{first_name}', LastName='{last_name}',Email_ID='{email}',MobileNo='{mob_number}',AddressLine='{addressline}',City='{city}',PinCode='{pincode}' WHERE UserID = '{user_id}'"
    print(query)
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    cur.close()


@app.route('/index', methods=['GET', 'POST'])
def index():
    print(session)
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    user_id = session['uid']
    if (user_id == None):
        user_id = '1'
    query = f"select * from VP_Products where Availability='Yes'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()
    if (vplist == None):
        flash("There are no products available for Bid")
    print(vplist)
    return render_template("index.html", vplist=vplist)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        user_id = None
        while True:
            user_id = generate_uuid()
            query = f"SELECT * from User WHERE User.UserID='{user_id}'"
            response = cur.execute(query)
            if response == 0:
                break
        cur.close()
        user_details = request.form
        first_name = user_details['first-name']
        last_name = user_details["last-name"]
        email = user_details['email']
        mob_number = user_details['number']
        # Add hashing for password
        password = user_details['password']
        confirm_password = user_details['confirm-password']
        if password == None or password == '':
            flash("Password can't be empty", 'danger')
            return render_template("register.html")

        if password != confirm_password:
            flash('Password and confirm password should be same', 'danger')
            return render_template("register.html")

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

        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"Unable to run query. Error: {e}")
        cur.close()

        flash('You are now registered and can login', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    """We create session in login route
    """
    if request.method == 'POST':
        user_details = request.form
        email_id = user_details['email']
        password = user_details['password']
        if email_id == None or email_id == "":
            flash("Email can't be empty", 'danger')
            return render_template("login.html")

        if password == None or password == "":
            flash("Password can't be empty", 'danger')
            render_template("login.html")

        query = "SELECT * from User WHERE User.Email_ID=%s and User.Password_=%s"
        values = (email_id, password)

        cur = mysql.connection.cursor()

        try:
            cur.execute(query, values)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        response = cur.fetchone()
        # User not found
        if response == None or response == 0:
            flash('Incorrect Login Credentials', 'danger')
            cur.close()
            return render_template("login.html")

        if (response['UserID'] == 'Admin_1'):
            return redirect(url_for('admin'))
        
        # Update session
        session['logged_in'] = True
        session['uid'] = response['UserID']
        session['session_name'] = response['FirstName']
        print(session)

        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/admin', methods = ['GET','POST'])
def admin():

    q = f"create view admin (Users, Sellers, Products, FPP, VPP, ULP) as select count(distinct(User.UserID)), count(distinct(Seller.SellerID)), count(distinct(Products.ProductID)), count(distinct(FP_Products.ProductID)), count(distinct(VP_Products.ProductID)), count(distinct(Unlisted_Products.ProductID)) from User, Seller, Products, FP_Products, VP_Products, Unlisted_Products"
    cur = mysql.connection.cursor()

    try:
        cur.execute(q)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    
    q = f"select* from admin"
    cur = mysql.connection.cursor()

    try:
        cur.execute(q)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    response = cur.fetchone()

    q = f"drop view admin"
    cur = mysql.connection.cursor()

    try:
        cur.execute(q)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    
    return render_template("admin.html", data = response)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'uid' in session:
        session.clear()
        flash('You are now logged out', 'success')
        return redirect(url_for('login'))
    return redirect(url_for('login'))

    # @app.route('/logout', methods=['GET', 'POST'])


@app.route('/read_user', methods=['GET', 'POST'])
def read_user():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))

    user_id = session['uid']
    if request.method == 'POST':
        user_details = request.form
        update_user(user_details, user_id)
        flash("Your profile has been updated", "success")
        return redirect(url_for('index'))
    else:
        query = f"SELECT * from User WHERE User.UserID={user_id}"
        cur = mysql.connection.cursor()

        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query: {query}. Error: {e}")

        response = cur.fetchone()
        return render_template("profile.html", data=response)


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))

    user_id = session['uid']
    query = f"DELETE FROM User WHERE UserID={user_id}"
    cur = mysql.connection.cursor()

    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    session.clear()
    flash('Your account has been deleted', 'success')
    return redirect(url_for('login'))


@app.route('/payment-callback')
def payment_success():
    payment_id = request.args.get('razorpay_payment_id')
    signature = request.args.get('razorpay_signature')

    # Verify the payment signature
    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
    except razorpay.errors.SignatureVerificationError:
        return jsonify({'status': 'error', 'message': 'Invalid payment signature'})

    # Payment successful
    return jsonify({'status': 'success', 'message': 'Payment successful'})


@app.route('/payment-cancel')
def payment_cancel():
    print("cancelled")
    return render_template("success.html", response="Cancelled")


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


@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    user_id = session['uid']
    if request.method == 'POST':
        form_details = request.form
        bank = form_details['bank']
        acc = form_details["Account"]
        ifsc = form_details["IFSC"]
        temp = None
        cur = mysql.connection.cursor()
        while True:
            temp = generate_uuid()
            gen_id = "SE" + str(temp)
            query = f"SELECT * from Seller WHERE Seller.SellerID='{gen_id}'"
            response = cur.execute(query)
            if response == 0:
                break
        seller_id = "SE" + str(temp)
        q = f"INSERT INTO Seller VALUES ('{seller_id}','{user_id}',0 ,'{bank}',{acc},'{ifsc}')"

        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        return redirect(url_for('product'))
    return render_template("acc_details.html")


@app.route('/product', methods=['GET', 'POST'])
def product():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    user_id = session['uid']
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
        return redirect(url_for('account'))

    else:
        print(r1)
        seller_id = r1['SellerID']

    try:
        cur.execute("SELECT * from Category")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    catlist = cur.fetchall()

    try:
        cur.execute("SELECT * from SubCategory")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    subcatlist = cur.fetchall()

    try:
        cur.execute("SELECT * from Constrained")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    constrainlist = cur.fetchall()

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        subcat_id = form_details.getlist("scat")
        creation_date = current_date()
        image = request.files['image'].read()
        encoded_image = base64.b64encode(image)
        
        # filename = secure_filename(image.filename)
        # print(filename)
        # path = os.path.join('Uploaded_Images', filename)
        # print(path)
        # image.save(path)
        # path ="C:/DBMS_Assignment/CDSlite-1/Uploaded_Images/" + filename

        # Correct method for assigning IDs
        product_id = None
        while True:
            product_id = generate_uuid()
            query = f"SELECT * from Products WHERE Products.ProductID='{product_id}'"
            response = cur.execute(query)
            if response == 0:
                break

        q = f"INSERT INTO Products VALUES ('{product_id}','{seller_id}')"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        q = "INSERT INTO Image VALUES (%s, %s)"
        params = (product_id,encoded_image)
        cur = mysql.connection.cursor()
        try:
            cur.execute(q,params)
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

        isMerchandise = form_details['Merch']
        if isMerchandise == "Yes":
            mrp = form_details["MRP"]
            quantity = form_details["Quantity"]

            q2 = f"INSERT INTO FP_Products VALUES ('{product_id}','{pdt_name}','{desc}','Yes',{mrp},{quantity},'{creation_date}','{creation_date}','{category_id}')"
            print(q2)
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
        flash("Product added successfully", 'success')
        return redirect(url_for('myproducts'))
    return render_template("addProduct.html", subcatlist=subcatlist, catlist=catlist,constrainlist=constrainlist)


@app.route('/account2/<user_id>/<pid>', methods=['GET', 'POST'])
def account2(user_id,pid):
    if request.method == 'POST':
        form_details = request.form
        bank = form_details['bank']
        acc = form_details["Account"]
        ifsc = form_details["IFSC"]
        temp = None
        cur = mysql.connection.cursor()
        while True:
            temp = generate_uuid()
            gen_id = "SE" + str(temp)
            query = f"SELECT * from Seller WHERE Seller.SellerID='{gen_id}'"
            response = cur.execute(query)
            if response == 0:
                break
        seller_id = "SE" + str(temp)
        q = f"INSERT INTO Seller VALUES ('{seller_id}','{user_id}',0 ,'{bank}',{acc},'{ifsc}')"

        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        return redirect(url_for('barterpage', id=pid))
    return render_template("acc_details.html")

@app.route('/get_image/<product_id>')
def get_image(product_id):
    # Retrieve image data from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT Img FROM Image WHERE ProductID = %s", [product_id])
    image_data = cur.fetchone()['Img']
    cur.close()

    # Convert image data to response object
    response = make_response(base64.b64decode(image_data))
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename='image.png')
    return response

@app.route('/Barter', methods=['GET', 'POST'])
def Barter():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        q1 = f"SELECT * from VP_Products WHERE isBarter = 'Yes' and Availability='Yes' "
        # print("Returning template")
        try:
            cur.execute(q1)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        brtlist = cur.fetchall()
        cur.close()
        return render_template("barterproduct.html", brtlist=brtlist)
    query = f"select * from VP_Products where isBarter='Yes'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()
    if (vplist == None):
        flash("There are no products available for Bid")
    print(vplist)
    return render_template("index.html", vplist=vplist)

@app.route('/Barter1/<product_id>', methods=['GET', 'POST'])
def Barter1(product_id):

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        q1 = f"SELECT * from VP_Products WHERE ProductID = '{product_id}' and Availability='Yes' "
        # print("Returning template")
        try:
            cur.execute(q1)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        brtlist = cur.fetchall()
        cur.close()
        return render_template("barterproduct.html", brtlist=brtlist)
    
    query = f"select * from VP_Products where isBarter='Yes'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()
    if (vplist == None):
        flash("There are no products available for Bid")
    print(vplist)
    return render_template("index.html", vplist=vplist)


@app.route('/barterpage/<id>', methods=['GET', 'POST'])
def barterpage(id):
    #print("here in barterpage")
    user_id = session['uid']

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        total_existing_products = cur.execute("SELECT * FROM Products")

        q3 = f"SELECT SellerID FROM Seller WHERE UserID='{user_id}'"

        cur.execute(q3)
        mysql.connection.commit()
        f = cur.fetchone()
        if (f == None):
            return redirect(url_for("account2", user_id=user_id, pid=id))
        seller_id = f['SellerID']

        product_id = str(total_existing_products+1)
        form_details = request.form
        prod_name = form_details["product-name"]
        desc = form_details["description"]
        creation_date = current_date()
        q1 = f"INSERT INTO Products VALUES ('{product_id}','{seller_id}')"

        try:
            cur.execute(q1)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        q = f"INSERT INTO Unlisted_Products VALUES ('{product_id}','{prod_name}','{desc}','{creation_date}')"

        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        while True:
            Barter_id = generate_uuid()
            query = f"SELECT * from Barter WHERE Barter.BarterID='{Barter_id}'"
            response = cur.execute(query)
            if response == 0:
                break

        q4 = f"INSERT INTO Barter (BarterID, P1ID, P2ID) VALUES ('{Barter_id}', '{id}', '{product_id}');"

        try:
            cur.execute(q4)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        return render_template("success.html")
    return render_template("barterpage.html")


@app.route('/myproducts')
def myproducts():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    user_id = session['uid']
    cur = mysql.connection.cursor()

    q1 = f"SELECT SellerID from Seller where Seller.UserID = '{user_id}'"
    try:
        cur.execute(q1)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"NOT A SELLER!!. Error: {e}")
    f = cur.fetchone()
    if (f == None):
        flash("You have not uploaded any products yet.", 'danger')
        return redirect(url_for('index'))

    seller_id = f['SellerID']
    # print(seller_id)

    q2 = f"select * from(select * from Products natural join FP_Products where Products.ProductID = FP_Products.ProductID) as P where P.sellerid = '{seller_id}'"
    try:
        cur.execute(q2)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    fplist = cur.fetchall()

    q3 = f"select * from(select * from Products natural join VP_Products where Products.ProductID = VP_Products.ProductID) as P where P.sellerid = '{seller_id}'"

    try:
        cur.execute(q3)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()

    if (len(fplist) == 0 and len(vplist) == 0):
        flash("There are no products left in your catalog.", 'danger')
        return redirect(url_for('index'))
    return render_template("myproducts.html", fplist=fplist, vplist=vplist)


@app.route('/dele/<param1>', methods=['GET', 'POST'])
def dele(param1='1'):
    cur = mysql.connection.cursor()
    print("Deleting", param1)
    q2 = f"Delete from Products where ProductID = '{param1}'"
    try:
        cur.execute(q2)
        mysql.connection.commit()
        print("deleted")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    return redirect(url_for('myproducts'))


@app.route('/vp_products/<id>', methods=["GET", "POST"])
def vp_products(id):
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    print("here in edit")
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
    print(id)
    vplist = None
    q2 = f"select * from VP_Products where Productid = '{id}'"
    print(q2)
    try:
        cur.execute(q2)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchone()
    #print(vplist)
    try:
        cur.execute("SELECT * from Constrained")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    constrainlist = cur.fetchall()

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        updation_date = current_date()
        base_price = form_details["BasePrice"]
        is_barter = form_details["isBarter"]
        subcat_id = form_details.getlist("scat")
        image = request.files['image'].read()
        encoded_image = base64.b64encode(image)

        q2 = f"UPDATE VP_Products SET ProductName = '{pdt_name}', Description_ = '{desc}', BasePrice = '{base_price}', CategoryID = '{category_id}',isBarter = '{is_barter}', UpdationDate = '{updation_date}' WHERE ProductID = '{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q2)
            mysql.connection.commit()
            print("Updated!")
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        q2 = f"DELETE FROM vphassubcat WHERE ProductID = '{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q2)
            mysql.connection.commit()
            #print("Updated!")
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        for i in subcat_id:
            q3 = f"INSERT INTO VPhasSubCat VALUES ('{id}','{i}')"
            try:
                cur.execute(q3)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
        
        q4 = f"Select * from Image where ProductID ='{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q4)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        IM = cur.fetchone()
        if(image ==  b''):
            return redirect(url_for('myproducts'))
        if(IM == None):
            q = "INSERT INTO Image VALUES (%s, %s)"
            params = (id,encoded_image)
        else:
            q = "UPDATE IMAGE SET Img = (%s) where ProductID= (%s)"
            params = (encoded_image,id)
        cur = mysql.connection.cursor()
        try:
            cur.execute(q,params)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
                
        return redirect(url_for('myproducts'))
    return render_template("edit_products_vp.html", subcatlist=subcatlist, catlist=catlist, vplist=vplist,constrainlist=constrainlist)


@app.route('/fp_products/<id>', methods=["GET", "POST"])
def fp_products(id):
    cur = mysql.connection.cursor()
    # print("here in edit")
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

    fplist = None
    q2 = f"select * from FP_Products where Productid = '{id}'"
    try:
        cur.execute(q2)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    fplist = cur.fetchone()

    try:
        cur.execute("SELECT * from Constrained")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    constrainlist = cur.fetchall()

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        updation_date = current_date()
        MRP = form_details["MRP"]
        Quantity = form_details["Quantity"]
        subcat_id = form_details.getlist("scat")
        image = request.files['image'].read()
        encoded_image = base64.b64encode(image)
        #print(id)

        q2 = f"UPDATE fp_products SET ProductName = '{pdt_name}', Description_ = '{desc}', MRP = {MRP}, Quantity = {Quantity}, CategoryID = '{category_id}', UpdationDate = '{updation_date}' WHERE ProductID = '{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q2)
            mysql.connection.commit()
            print("Updated!")
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        q2 = f"DELETE FROM vphassubcat WHERE ProductID = '{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q2)
            mysql.connection.commit()
            print("Updated!")
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        for i in subcat_id:
            q3 = f"INSERT INTO VPhasSubCat VALUES ('{id}','{i}')"
            try:
                cur.execute(q3)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            
        q4 = f"Select * from Image where ProductID ='{id}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q4)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        if(image ==  b''):
            return redirect(url_for('myproducts'))
        
        if(cur.fetchone() == None):
            q = "INSERT INTO Image VALUES (%s, %s)"
            params = (id,encoded_image)
        else:
            q = "UPDATE IMAGE SET Img = (%s) where ProductID= (%s)"
            params = (encoded_image,id)
        cur = mysql.connection.cursor()
        try:
            cur.execute(q,params)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        return redirect(url_for('myproducts'))
    return render_template("edit_products_fp.html", subcatlist=subcatlist, catlist=catlist, fplist=fplist,constrainlist=constrainlist)


@app.route('/bid_buyer/<id_>', methods=["GET", "POST"])
def bid_buyer(id_):
    if request.method == 'POST':
        q = f"LOCK Table BidTable Write"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        bid_id = None
        user_id = session['uid']
        cur = mysql.connection.cursor()
        while True:
            bid_id = generate_uuid()
            query = f"SELECT * from BidTable WHERE BidTable.BidID='{bid_id}'"
            response = cur.execute(query)
            if response == 0:
                break
        form_details = request.form
        bid_price = form_details["bid"]
        q = f"INSERT INTO BidTable VALUES ('{bid_id}','{id_}','{user_id}',DEFAULT,{bid_price},'Pending')"
        try:
            cur.execute(q)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        q = f"Unlock Tables"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        return redirect(url_for('index'))

    query = f"Select * from VP_Products where ProductID='{id_}'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    prod_list = cur.fetchone()
    return render_template("bid_buyer.html", plist=prod_list)
              
@app.route('/in_merch/<id_>', methods=["GET", "POST"])
def in_merch(id_):

    query = f"Select * from FP_Products where ProductID='{id_}'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    prod_list = cur.fetchone()
    return render_template("in_merchandise.html", plist=prod_list)

@app.route('/bid_page/<id_>', methods=["GET", "POST"])
def bid_page(id_):
    k = "Yes"
    query = f"Select * from (Select * from BidTable natural join VP_Products where VP_Products.ProductID=BidTable.ProductID) as P where P.ProductID='{id_}'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    bidarray = cur.fetchall()
    
    qr=f"SELECT VP_PID, VP_ProductName, BarterID, Buyer_PID, BarterStatus, BarterDate, ProductName, CreationDate FROM (SELECT VP_PID, VP_ProductName, BarterID, P2ID AS Buyer_PID, BarterStatus, BarterDate FROM (SELECT ProductID AS VP_PID, ProductName AS VP_ProductName FROM vp_products WHERE isBarter = 'Yes') AS temp LEFT OUTER JOIN barter ON temp.VP_PID = barter.P1ID) AS temp2 LEFT OUTER JOIN unlisted_products ON temp2.Buyer_PID = unlisted_products.productID WHERE temp2.VP_PID = '{id_}'"

    try:
        cur.execute(qr)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    
    barterlist = cur.fetchall()

    if len(barterlist)==0 and len(bidarray) == 0:
        flash("no product for barter or bid")

        return redirect(url_for('myproducts'))

    print("khvl ", barterlist)
    return render_template("bidpage.html",bidarray=bidarray,barterlist=barterlist)


@app.route('/buyer_barter/<barter_id_>')
def buyer_barter(barter_id_):
    cur=mysql.connection.cursor()
    print("gbid ", barter_id_)
    qr=f"SELECT ProductID, temp3.SellerID, BarterID, Seller_Name, Email_ID, MobileNo, ProductName, Description_, CreationDate  FROM ( SELECT ProductID, temp.SellerID, Seller_Name, Email_ID, MobileNo, ProductName, Description_, CreationDate  FROM (SELECT SellerID, FirstName AS Seller_Name, Email_ID, MobileNo FROM seller LEFT JOIN user ON seller.UserID = user.UserID) AS temp RIGHT OUTER JOIN ( SELECT products.ProductID, products.SellerID, ProductName, Description_, CreationDate  FROM unlisted_products LEFT OUTER JOIN products ON unlisted_products.ProductID = products.ProductID ) AS temp2 ON temp.SellerID = temp2.SellerID) AS temp3 LEFT OUTER JOIN Barter ON temp3.ProductID = Barter.P2ID WHERE BarterID = '{barter_id_}'"

    try:
        cur.execute(qr)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    
    res = cur.fetchone()
    print('akgia',res)
    return render_template("barter_buyer.html",res=res)

@app.route('/confirm_bid/<bid_id>')
def confirm_bid(bid_id):
    q = f"UPDATE BidTable SET BidStatus = 'Confirmed' where BidID='{bid_id}'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(q)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    q2 = f"Select ProductID from BidTable where BidID='{bid_id}'"
    try:
        cur.execute(q2)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    res = cur.fetchone()
    p_id = res['ProductID']
    q3 = f"UPDATE BidTable SET BidStatus = 'Declined' where ProductID = '{p_id}' and BidID != '{bid_id}'"
    try:
        cur.execute(q3)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    return redirect(url_for('myproducts'))
    
@app.route('/confirm_barter/<barter_id>/<pid>')
def confirm_barter(barter_id, pid):
    q = f"UPDATE barter SET BarterStatus = 'Accepted' WHERE BarterID = '{barter_id}' AND ProductID = '{pid}'"
    q2 = f"UPDATE barter SET BarterStatus = 'Declined' WHERE BarterID = '{barter_id}' AND BarterStatus = 'Pending'"
    cur = mysql.connection.cursor()
    try:
        cur.execute(q)
        cur.execute(q2)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    return barter_id

@app.route('/add_cart/<product_id>')
def add_shopping_cart(product_id):
    print("here in cart")
    user_id = session['uid']
    quantity = 1
    cur = mysql.connection.cursor()
    # Check if product already exists in cart
    query = f"SELECT * FROM ShoppingCart WHERE UserID = '{user_id}' and ProductID = '{product_id}'"
    cur.execute(query)
    response = cur.fetchone()
    if response != None:
        print("respionse: ", response)
        q = f"select * from fp_products where ProductID='{product_id}'"
        cur.execute(q)
        res = cur.fetchone()
        Q = res['Quantity']
        Q_dash = response['Quantity']
        if(Q < Q_dash+1):
            flash("Product quantity exceeded as per stock", 'danger')
            return redirect(url_for('read_shopping_cart'))
        else:
            quty = Q_dash + 1
            q = f"Update ShoppingCart Set Quantity = '{quty}' where UserID = '{user_id}' and ProductID = '{product_id}'"
            try:
                cur.execute(q)
                mysql.connection.commit()
            except Exception as e:
                raise Exception(f"UNable to run query. Error: {e}")
            return redirect(url_for('read_shopping_cart'))

    query = f"INSERT INTO ShoppingCart VALUES ('{user_id}','{product_id}','{quantity}',DEFAULT)"

    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    cur.close()
    flash('Your Product has been added to Cart', 'success')
    return redirect(url_for('read_shopping_cart'))


@app.route('/delete_cart/<product_id>')
def delete_shopping_cart(product_id):
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))

    user_id = session['uid']
    print("product_id", product_id)
    query = f"DELETE FROM ShoppingCart WHERE UserID = '{user_id}' and ProductID = '{product_id}'"
    flash("Product deleted from cart", 'success')
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")

    cur.close()
    return redirect(url_for('read_shopping_cart'))


@app.route('/index/shopping_cart', methods=['GET', 'POST'])
def read_shopping_cart():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    user_id = session['uid']
    query = f"SELECT * FROM ShoppingCart LEFT JOIN ( SELECT ProductID, ProductName, Price, Description_, CreationDate, UpdationDate, CategoryID FROM (SELECT BidTable.ProductID, ProductName, BidPrice AS Price, Description_, CreationDate, UpdationDate, CategoryID FROM BidTable LEFT JOIN VP_Products ON BidTable.productID = VP_Products.productID WHERE BidStatus = 'Confirmed') as temp UNION SELECT ProductID, ProductName, MRP AS Price, Description_, CreationDate, UpdationDate, CategoryID FROM FP_Products  ) AS temp2 ON ShoppingCart.ProductID = temp2.ProductID WHERE (UserID = {user_id});"
    cur = mysql.connection.cursor()

    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    response = cur.fetchall()
    total = 0
    items = 0
    for r in response:
        items += int(r["Quantity"])
        total += int(r["Price"]) * int(r["Quantity"])
    cur.close()
    return render_template("cart.html", data=response, total=total,items=items)


@app.route('/order/<product_id>', methods=['GET'])
def order_summary(product_id):
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    data = {}

    cur = mysql.connection.cursor()
    user_id = session['uid']
    query = f"SELECT * FROM User WHERE UserID = {user_id}"
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    response = cur.fetchone()
    data['User'] = response
    cur.close()

    cur = mysql.connection.cursor()
    query = f"SELECT * FROM ShoppingCart LEFT JOIN ( SELECT ProductID, ProductName, Price, Description_, CreationDate, UpdationDate, CategoryID FROM (SELECT BidTable.ProductID, ProductName, BidPrice AS Price, Description_, CreationDate, UpdationDate, CategoryID FROM BidTable LEFT JOIN VP_Products ON BidTable.ProductID = VP_Products.ProductID WHERE BidStatus = 'Confirmed') as temp UNION SELECT ProductID, ProductName, MRP AS Price, Description_, CreationDate, UpdationDate, CategoryID FROM FP_Products  ) AS temp2 ON ShoppingCart.ProductID = temp2.ProductID WHERE userID = {user_id} and temp2.ProductID={product_id} ;"
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    response = cur.fetchone()
    data['Product'] = response
    cur.close()
    print(data)
    # CREATE RAZORPAY ORDER
    quantity = response['Quantity']
    price = response['Price']
    data['Total'] = int(quantity) * int(price)
    order_details = pay(data['Total'])
    data['Order_Details'] = order_details
    print(order_details)
    return render_template("order.html", data=data)


@app.route('/order/cancel', methods=['GET', 'POST'])
def cancel_order():
    flash("Order cancelled")
    return redirect(url_for('index'))


@app.route('/merchandise/')
def merchandise():
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    
    query = f"SELECT * FROM FP_Products;"
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    response = cur.fetchall()
    return render_template('merchandise.html', plist=response)


if __name__ == '__main__':
    app.run(debug=True)
