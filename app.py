import os
from flask import Flask,render_template,request,flash,redirect,url_for,session
from Databases import User,Person, Product, Cart, Order
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

@app.route('/out_of_stock/<int:id>')
def out_of_stock(id):
    product = Product.get(Product.id==id)
    product.out_of_stock = 1
    product.save()
    flash("Product Updated Successfully")
    return redirect(url_for('master_product_view'))


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    Person.delete().where(Person.id == id).execute()
    flash("Details Deleted Successfully")
    return redirect(url_for('show'))


@app.route('/invoice/<int:id>')
def invoice(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    users = User.select().where(User.id==id)
    return render_template('invoice.html',users = users)


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    users = User.select()
    return render_template('show.html',users = users)

@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select()
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)
@app.route('/master_product_view')
def master_product_view():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select()
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('masterproducts.html',products = products,cartproductcount = cartproductcount)

@app.route('/laptops')
def laptops():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Laptop")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/televisions')
def televisions():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Television")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)
@app.route('/view_out_of_stock')
def view_out_of_stock():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.out_of_stock == 1)
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/woofers')
def woofers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Woofer")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/fridges')
def fridges():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Fridge")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/blenders')
def blenders():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Blender")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/microwaves')
def microwaves():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Microwave")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)

@app.route('/heaters')
def heaters():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Heater")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)\

@app.route('/cameras')
def cameras():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Product.select().where(Product.category == "Camera")
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('products.html',products = products,cartproductcount = cartproductcount)
@app.route('/orders')
def orders():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    products = Order.select().where(Order.delivered == 0)
    cartproducts = Cart.select()
    cartproductcount = len(cartproducts)
    return render_template('orders.html',products = products,cartproductcount = cartproductcount)

@app.route('/cart')
def cart():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    cartproducts = Cart.select()
    total_amount = 0
    for cartproduct in cartproducts:
        total_amount = total_amount+cartproduct.price
    cartproductcount = len(cartproducts)
    return render_template('cart.html',cartproducts = cartproducts,cartproductcount = cartproductcount,total_amount=total_amount)

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
        category = request.form["category"]
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(path.dirname(path.realpath(__file__))+"/static/resources", filename))
        id = session['id']
        Product.create(name = name,price = price, description = description, image = file.filename,category = category,out_of_stock=0)
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
        User.create(names = names, email = email, password = password,sum_purchase=0)
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
        user_id = session['id']
        user = User.get(User.id == user_id)
        user.sum_purchase = user.sum_purchase+product.price
        user.save()
        Cart.create(name=product.name, price=product.price, description=product.description, image=product.image)

    flash("Product added Successfully")
    return redirect(url_for('show'))

@app.route('/checkout')
def checkout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    cartproducts = Cart.select()
    for cartproduct in cartproducts:
        Order.create(name=cartproduct.name, price=cartproduct.price, description=cartproduct.description, image=cartproduct.image,delivered=0)
    Cart.delete().where(Cart.id > 0).execute()
    flash("Items Checked out Successfully")
    return redirect(url_for('show'))


@app.route('/deliver/<int:id>')
def deliver(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    myorder = Order.get(Order.id == id)
    myorder.delivered = 1
    myorder.save()
    flash("Product delivered Successfully")
    return redirect(url_for('orders'))


@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop("logged_in",None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run()










