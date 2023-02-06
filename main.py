from flask import Flask,request,render_template,session
from create_table import *

@app.route("/", methods =['GET'])
def login_page():
    return render_template('login.html')

@app.route('/home_page')
def home_page():
    return render_template("home.html")

user_list=[]
@app.route('/user/registration', methods=['GET','POST'])
def user_registration():
    message=""
    if request.method == "POST":
        formdata = request.form
        emailid = formdata.get('emailid')
        dupli_email = User.query.filter_by(emailid=emailid).first()
        dupli_role = User.query.filter_by(role="Admin").first()
        if dupli_email:
            message = "Duplicate Emailid"
            return render_template('registration.html', result=message)

        if dupli_role:
            message = "Already we have Admin Account..Please Select as Guest Account..."
            return render_template('registration.html', result=message)

        if formdata.get('password') == formdata.get('confirm_password'):
            user = User(role=formdata.get("role"),
                            firstname=formdata.get("firstname"),
                            lastname=formdata.get("lastname"),
                            contact=formdata.get("contact"),
                            address=formdata.get("address"),
                            DOB=formdata.get("dob"),
                            emailid=formdata.get("emailid"),
                            password=formdata.get("password"),
                            conform_password=formdata.get("confirm_password"),
                            gender=formdata.get("gender"),
                            age=formdata.get("age"),
                            country=formdata.get("country"),
                            city=formdata.get("city"))
            db.session.add(user)
            db.session.commit()
            message = "User Registration Successfully...."
        else:
            message = "Password and Confirm Password not Matched"
    return render_template('registration.html', result=message)

@app.route('/login_page',methods=['POST'])
def validate_user():
    message=""
    if request.method == "POST":
        formdata = request.form
        emailid = formdata.get('emailid')
        password = formdata.get('password')
        role = formdata.get('role')
        account = User.query.filter(User.emailid == emailid, User.password == password,User.role == role).first()
        if account:
            session['firstname'] = account.firstname
            session['lastname'] =account.lastname
            session['role'] = account.role
            message = f'You have successfully logged in.. '
            message1= f'Welcome "{account.firstname} {account.lastname}", You are logined as "{account.role}"'
            return render_template('home.html',result=message,result1=message1)
        else:
            message = "Invalid Credentials!"
    return render_template('login.html', result=message)

@app.route('/add_product', methods=['GET','POST'])
def add_product():
    message=""
    if request.method == "POST":
        formdata= request.form
        id = int(formdata.get('id'))
        print(id)
        add_prod=Product.query.filter_by(product_id=id).first()
        if add_prod:
            message = "Duplicate Product Id"
            old_list = Product.query.all()
            return render_template('add_product.html', result=message,result1=old_list)
        else:
            prod = Product(product_id=formdata.get("id"),
                               name=formdata.get("name"),
                               price=formdata.get("price"),
                               quantity=formdata.get("quantity"),
                               vendor=formdata.get("vendor"),
                               category=formdata.get("Category"))
            db.session.add(prod)
            db.session.commit()
            message = "Product added Successfully"
    final_list = Product.query.all()
    return render_template('add_product.html',result=message,result1=final_list)

@app.route('/product_final_list', methods=['GET', 'POST'])
def product_final_list():
    final_list = Product.query.all()
    return render_template('product_final_list.html', result1=final_list)

@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    return render_template('search_product.html')

@app.route('/search_product_id', methods=['GET','POST'])
def search_product_id():
    message=""
    search_product = ""
    if request.method == 'POST':
        formdata = request.form
        id= formdata.get('id')
        search_product = Product.query.filter_by(product_id=id).all()
        if search_product:
            db.session.commit()
            message="Product is Present"
            return render_template('search_product_id.html', result=message, result1=search_product)
        else:
            message = "Product Id is Not Present"
    return render_template('search_product_id.html',result=message,result1=search_product )

@app.route('/search_product_name', methods=['GET','POST'])
def search_product_name():
    message=""
    search_product = ""
    if request.method == 'POST':
        formdata = request.form
        nd= formdata.get('name')
        search_product = Product.query.filter_by(name=nd).all()
        if search_product:
            db.session.commit()
            message="Product is Present"
            return render_template('search_product_name.html', result=message, result1=search_product)
        else:
            message = "Product Name is Not Present"
    return render_template('search_product_name.html',result=message,result1=search_product )

@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    return render_template('delete_product.html')

@app.route('/delete_product_id', methods=['GET', 'POST'])
def delete_product_id():
    message=""
    final_list =  Product.query.all()
    if request.method == 'POST'and session['role'] == 'Admin':
        formdata = request.form
        d_id = formdata.get('id')
        delete_list=Product.query.filter_by(product_id=d_id).first()
        if delete_list:
            db.session.delete(delete_list)
            delete_list = Product.query.all()
            message = "Product Deleted"
            db.session.commit()
            return render_template('delete_product_id.html', result=message,result1= delete_list)
        else:
            message="Product ID is Not Present"

        if request.method == 'POST' and session['role'] == 'Guest':
            message = 'You are not the Admin..So You Can Not Delete the Product'
            return render_template('delete_product_id.html', result=message,result1= final_list)

    return render_template('delete_product_id.html', result=message,result1= final_list)

@app.route('/delete_product_name', methods=['GET', 'POST'])
def delete_product_name():
    message = ""
    final_list = Product.query.all()
    if request.method == 'POST' and session['role'] == 'Admin':
        formdata = request.form
        n_id = formdata.get('name')
        delete_list_name=Product.query.filter_by(name=n_id).first()
        if delete_list_name:
            db.session.delete(delete_list_name)
            delete_list_name = Product.query.all()
            message = "Product Deleted"
            db.session.commit()
            return render_template('delete_product_name.html', result=message, result1=delete_list_name)
        else:
            message = "Product Name is Not Present"

        if request.method == 'POST' and session['role'] == 'Guest':
            message = 'You are not the Admin..So You Can Not Delete the Product'
            return render_template('delete_product_name.html', result=message,result1=final_list)

    return render_template('delete_product_name.html', result=message, result1=final_list)

@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    return render_template('update_product.html')

@app.route('/update_product_id', methods=['GET','POST'])
def update_product_id():
    message = ''
    final_list = Product.query.all()
    if request.method == 'POST' and session['role'] == 'Admin':
        formdata = request.form
        u_id = formdata.get('id')
        update_prod=Product.query.filter_by(product_id=u_id).first()
        if update_prod:
            update_prod.product_id = formdata.get("id")
            update_prod.name = formdata.get("name")
            update_prod.price = formdata.get("price")
            update_prod.quantity = formdata.get("quantity")
            update_prod.vendor = formdata.get("vendor")
            update_prod.category = formdata.get("category")
            message = "Update Successfully"
            db.session.commit()
            return render_template('update_product_id.html', result=message,result1=final_list)
        else:
            message="Product ID Not Present "

    if request.method == 'POST' and session['role'] == 'Guest':
        message='You are not the Admin..So You Can Not Update the Product'
    return render_template('update_product_id.html',result=message,result1=final_list)

@app.route('/update_product_name', methods=['GET','POST'])
def update_product_name():
    message = ''
    final_list = Product.query.all()
    if request.method == 'POST'and session['role'] == 'Admin':
        formdata = request.form
        n_id = formdata.get('name')
        update_prod=Product.query.filter_by(name=n_id).first()
        if update_prod:
            update_prod.product_id = formdata.get("id")
            update_prod.name = formdata.get("name")
            update_prod.price = formdata.get("price")
            update_prod.quantity = formdata.get("quantity")
            update_prod.vendor = formdata.get("vendor")
            update_prod.category = formdata.get("category")
            message = "Update Successfully"
            db.session.commit()
            return render_template('update_product_name.html', result=message,result1=final_list)
        else:
            message="Product Name Not Present "

    if request.method == 'POST' and session['role'] == 'Guest':
        message='You are not the Admin..So You Can Not Update the Product'
    return render_template('update_product_name.html',result=message,result1=final_list)


@app.route('/logout',methods=['GET','POST'])
def logout():
    result1=session['firstname']
    result2=session['lastname']
    message = f' You have Successfully Logout..'
    return render_template("login.html",result3=message,result1= result1,result2=result2)

if __name__ == "__main__":
    app.run(debug=True,port=5001)