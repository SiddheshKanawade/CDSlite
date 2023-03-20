import razorpay

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from src.helper import current_date, generate_uuid
from src.db import create_app
from src.helper import generate_uuid

app, mysql, razorpay_client = create_app()

# HELPER FUNCTIONS


def update_user(user_details, user_id):
    first_name = user_details['first-name']
    last_name = user_details["last-name"]
    email = user_details['email']
    mob_number = user_details['number']
    addressline = user_details['addressline']
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
    return render_template("index.html", uid=user_id)


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

        query = f"SELECT * from User WHERE User.Email_ID='{email_id}' and User.Password_='{password}'"

        cur = mysql.connection.cursor()

        try:
            cur.execute(query)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")

        response = cur.fetchone()
        # User not found
        if response == None or response == 0:
            flash('Incorrect Login Credentials', 'danger')
            cur.close()
            return render_template("login.html")

        # Update session
        session['logged_in'] = True
        session['uid'] = response['UserID']
        session['session_name'] = response['FirstName']
        print(session)

        return redirect(url_for('index'))
    return render_template("login.html")


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

    query = f"SELECT * from User WHERE User.UserID={user_id}"
    cur = mysql.connection.cursor()

    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query: {query}. Error: {e}")

    response = cur.fetchone()
    return render_template("profile.html", data=response)


@app.route('/delete_user', methods=['POST'])
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


@app.route('/payment/<price>', methods=['GET', 'POST'])
def pay(price):
    if 'uid' not in session:
        flash("Please login to continue", 'danger')
        return redirect(url_for('login'))
    # Get payment amount from the form
    print("Entered")
    print(price)
    amount = int(price) * 100  # convert to paise
    currency = "INR"

    # Create a Razorpay order
    order = razorpay_client.order.create({
        'amount': amount * 100,  # Razorpay requires amount in paise
        'currency': currency,
        'payment_capture': 1  # Automatically capture the payment when it is made
    })

    # Extract the order ID from the response
    order_id = order['id']
    print(order)

    # Return the order ID to the client
    return render_template("confirm_payment.html", payment=order)


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

        return redirect(url_for('myproducts'))
    return render_template("addProduct.html", subcatlist=subcatlist, catlist=catlist)

@app.route('/Barter',methods=['GET', 'POST'])
def Barter():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        q1 = f"SELECT * from VP_Products WHERE VP_Products.isBarter='Yes'"
        # print("Returning template")
        try:
            cur.execute(q1)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        
        brtlist=cur.fetchall()
        cur.close()
        return render_template("barterproduct.html", brtlist = brtlist)
    return render_template("index.html")


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
    except Exception as e:
        raise Exception(f"NOT A SELLER!!. Error: {e}")
    f = cur.fetchone()
    if (f == None):
        flash("You have not uploaded any products yet.", 'danger')
        return render_template("index.html")

    seller_id = f['SellerID']
    # print(seller_id)

    q2 = f"select * from(select * from Products natural join FP_Products where Products.ProductID = FP_Products.ProductID) as P where P.sellerid = '{seller_id}'"
    try:
        cur.execute(q2)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    fplist = cur.fetchall()

    q3 = f"select * from(select * from Products natural join VP_Products where Products.ProductID = VP_Products.ProductID) as P where P.sellerid = '{seller_id}'"

    try:
        cur.execute(q3)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    vplist = cur.fetchall()

    q4=f"SELECT * from VP_Products WHERE VP_Products.isBarter='Yes'"
    try:
        cur.execute(q4)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    brtlist = cur.fetchall()

    if (len(fplist) == 0 and len(vplist) == 0):
        flash("There are no products left in your catalog.", 'danger')
        return render_template("index.html")
    return render_template("myproducts.html", fplist=fplist, vplist=vplist)

@app.route('/dele/<param1>', methods=['GET', 'POST'])
def dele(param1='1'):
    cur = mysql.connection.cursor()
    print( "Deleting", param1)
    q2 = f"Delete from Products where ProductID = '{param1}'"
    try:
        cur.execute(q2)
        mysql.connection.commit()
        print("deleted")
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    return redirect(url_for('myproducts'))

@app.route('/vp_products/<id>', methods = ["GET", "POST"])
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
    print(vplist)
    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        updation_date = current_date()
        base_price = form_details["BasePrice"]
        is_barter = form_details["isBarter"]
        subcat_id = form_details.getlist("scat")
        
        q2 = f"UPDATE vp_products SET ProductName = '{pdt_name}', Description_ = '{desc}', BasePrice = '{base_price}', CategoryID = '{category_id}',isBarter = '{is_barter}', UpdationDate = '{updation_date}' WHERE ProductID = '{id}'"
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
        
        return redirect(url_for('myproducts'))
    return render_template("edit_products_vp.html", subcatlist=subcatlist, catlist = catlist, vplist=vplist)

@app.route('/fp_products/<id>', methods = ["GET", "POST"])
def fp_products(id):
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

    fplist = None
    q2 = f"select * from FP_Products where Productid = '{id}'"
    try:
        cur.execute(q2)
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    fplist = cur.fetchone()

    if request.method == 'POST':
        form_details = request.form
        pdt_name = form_details["product-name"]
        desc = form_details["description"]
        category_id = form_details["cat"]
        updation_date = current_date()
        MRP = form_details["MRP"]
        Quantity = form_details["Quantity"]
        subcat_id = form_details.getlist("scat")
        print(id)
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
        
        return redirect(url_for('myproducts'))
    return render_template("edit_products_fp.html", subcatlist=subcatlist, catlist = catlist, fplist=fplist)

@app.route('/bid_buyer', methods = ["GET", "POST"])
def bid_buyer():
    print("ekfgwho")
    return render_template("bid_buyer.html")

@app.route('/bid_page', methods = ["GET", "POST"])
def bid_page():
    print("ekfgwho")
    return render_template("bidpage.html")


@app.route('/add_cart/<product_id>')
def add_shopping_cart(product_id):
    user_id = session['uid']
    creation_date = current_date()
    quantity = 1
    cur = mysql.connection.cursor()
    # Check if product already exists in cart
    query = f"SELECT * FROM ShoppingCart WHERE UserID = '{user_id}' and ProductID = '{product_id}'"
    response = cur.execute(query)
    if response != 0:
        flash("Product already exists in cart", 'danger')
        return redirect(url_for('index'))

    query = f"INSERT INTO ShoppingCart VALUES ('{user_id}','{product_id}','{quantity}','{creation_date}')"

    try:
        cur.execute(query)
        mysql.connection.commit()
    except Exception as e:
        raise Exception(f"UNable to run query. Error: {e}")
    cur.close()
    flash('Your Product has been added to Cart', 'success')
    return redirect(url_for('index'))


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
    cur.close()
    return render_template("cart.html", data=response)


@app.route('/order')
def order_confirmation():
    pass


if __name__ == '__main__':
    app.run(debug=True)
