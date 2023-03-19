from flask import Flask, render_template, request, url_for, redirect, session, flash
from src.helper import current_date, generate_uuid
from src.db import create_app


app, mysql = create_app()


@app.route('/index', methods=['GET', 'POST'])
def index():
    print(session)
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


def delete_user():
    pass


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
    user_id = session['uid']
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


@app.route('/product', methods=['GET', 'POST'])
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
            return redirect(url_for('account'))

        else:
            print(r1)
            seller_id = r1['SellerID']

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


@app.route('/myproducts')
def myproducts():
    user_id = session['uid']
    cur = mysql.connection.cursor()

    q1 = f"SELECT SellerID from Seller where Seller.UserID = '{user_id}'"
    try:
        cur.execute(q1)
    except Exception as e:
        raise Exception(f"NOT A SELLER!!. Error: {e}")
    f = cur.fetchone()
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

    return render_template("myproducts.html", fplist=fplist, vplist=vplist)


@app.route('/edit/<param1>/<param2>', methods=['GET', 'POST'])
def edit(param1='1', param2='vp'):
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

    vplist = None
    fplist = None

    if (param2 == 'vp'):
        cur = mysql.connection.cursor()
        q2 = f"select * from VP_Products where Productid = '{param1}'"
        try:
            cur.execute(q2)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        vplist = cur.fetchall()
        print("bhk ", vplist)
        return render_template("edit_products_vp.html", vplist=vplist, catlist=catlist, subcatlist=subcatlist)
    else:
        q2 = f"select * from FP_Products where Productid = '{param1}'"
        cur = mysql.connection.cursor()
        try:
            cur.execute(q2)
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        fplist = cur.fetchall()
        return render_template("edit_products_fp.html", fplist=fplist, catlist=catlist, subcatlist=subcatlist)


@app.route('/dele/<param1>/<param2>', methods=['GET', 'POST'])
def dele(param1='1',param2='vp'):
    user_id = '1'
    cur = mysql.connection.cursor()
    print("here in delete")

    if(param2 == 'vp'):
        cur = mysql.connection.cursor()
        q2 = f"Delete from VP_Products where Productid = '{param1}'"
        try:
            cur.execute(q2)
            mysql.connection.commit()
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        return render_template("myproducts.html",user_id = user_id)
    else:
        cur = mysql.connection.cursor()
        print(param1)
        q2 = f"Delete from FP_Products where ProductID = '{param1}'"
        try:
            cur.execute(q2)
            mysql.connection.commit()
            print("deleted")
        except Exception as e:
            raise Exception(f"UNable to run query. Error: {e}")
        return redirect(url_for('myproducts'))

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
