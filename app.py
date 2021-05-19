import os
from flask import Flask,render_template,request,flash,redirect,url_for,session
from Databases import User,Person, Product, Cart
from flask_bcrypt import generate_password_hash,check_password_hash
from os import path
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "bnvsdnvsfvdvkvnjvdvdkbvdsc"



@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    user = Person.get(Person.id==id)
    if request.method == "POST":
        names = request.form["names"]
        age = request.form["age"]
        weight = request.form["weight"]
        user.names = names
        user.age = age
        user.weight = weight
        user.save()
        flash("User Updated Successfully")
        return redirect(url_for('show'))
    return render_template("update.html",user = user)


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    Person.delete().where(Person.id == id).execute()
    flash("Details Deleted Successfully")
    return redirect(url_for('show'))

#
# @app.route('/show')
# def show():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     id = session['id']
#     users = Person.select()
#     return render_template('show.html',users = users)

@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select()
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/cart')
def cart():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select()
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('cart.html',cartproducts = cartproducts,cartproductcount = cartproductcount)

#
# @app.route('/',methods=['GET','POST'])
# def index():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     if request.method == "POST":
#         names = request.form["names"]
#         age = request.form["age"]
#         weight = request.form["weight"]
#         id = session['id']
#         Person.create(owner = id,names = names, age = age, weight = weight)
#         flash("User Saved Successfully")
#         flash("User "+names)
#     return render_template("product.html")

@app.route('/',methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(path.dirname(path.realpath(__file__))+"/static/resources", filename))
        id = session['id']
        Product.create(name = name,price = price, description = description, image = file.filename)
        flash("Product posted Successfully")
        flash("Product "+name)
    return render_template("product.html")


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        names = request.form["names"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password)
        User.create(names = names, email = email, password = password)
        flash("Account Created Successfully")
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.get(User.email==email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Logged in Successfully")
                session['logged_in']=True
                session['names']=user.names
                session['id']=user.id
                return redirect(url_for('show'))
        except User.DoesNotExist:
            flash("Wrong Username or Password")
    return render_template("login.html")

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    products = Product.select().where(Product.id == id)
    for product in products:
        Cart.create(name=product.name, price=product.price, description=product.description, image=product.image)

    flash("Product added Successfully")
    return redirect(url_for('show'))

@app.route('/checkout')
def checkout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    Cart.delete().where(Cart.id > 0).execute()
    flash("Items Checked out Successfully")
    return redirect(url_for('show'))
@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop("logged_in",None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run()










