from flask import render_template,session, request,redirect,url_for,flash,current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import app, db, photos, search, bcrypt, login_manager
from .models import Category,Brand,Addproduct
from shop.customers.model import Register
from .forms import Addproducts
from ..customers.forms import CustomerLoginFrom, CustomerRegisterForm
import os
import secrets


#################### Functions to Add to STORE page ####################
def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return single_page(id)

def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)    
    except Exception as e:
        print(e) 
    finally:
        return redirect(request.referrer)

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list): 
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

def grandtotal ():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('store'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        grandtotal = float("%.2f" % (1.06 * subtotal)) 
    return grandtotal 

#################### Functions to Add to STORE page ####################
@app.route('/',methods =['GET' , 'POST'])
@app.route('/landing',methods =['GET' , 'POST'])
def landing():

    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    products = Addproduct.query.filter(Addproduct.stock > 0)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(1)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store'))  

    return render_template('landing.html', title='layout',  grandtotal=grandtotal(), products=products, brands=brands(), product=product, filterd_resultr=filterd_resultr, vi_product=vi_product, categories=categories(), form_R=form_R, form=form)


@app.route('/footer')
def footer():
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    product = Addproduct.query.get_or_404(6)
    p_id = 3
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    allresult = Addproduct.query.all()
    return render_template('footer.html' ,products=products, product=product, allresult=allresult, filterd_resultr=filterd_resultr)




@app.route('/my_account')
def my_account():
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    product = Addproduct.query.get_or_404(6)
    p_id = 3
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    allresult = Addproduct.query.all()
    return render_template('my_account.html' ,products=products, product=product, allresult=allresult, filterd_resultr=filterd_resultr)

@app.route('/order_history')
def order_history():
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    product = Addproduct.query.get_or_404(6)
    p_id = 3
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    allresult = Addproduct.query.all()
    return render_template('order_history.html' ,products=products, product=product, allresult=allresult, filterd_resultr=filterd_resultr)

@app.route('/settings')
def settings():
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    product = Addproduct.query.get_or_404(6)
    p_id = 3
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    allresult = Addproduct.query.all()
    return render_template('settings.html' ,products=products, product=product, allresult=allresult, filterd_resultr=filterd_resultr)
	
@app.route('/test')
def test():
    product = Addproduct.query.get_or_404(6)
    p_id = 3
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    allresult = Addproduct.query.all()
    return render_template('test.html' , product=product, allresult=allresult, filterd_resultr=filterd_resultr)

 
@app.route('/layout',methods =['GET' , 'POST'])
def layout():
    product = Addproduct.query.get_or_404(6)
    return render_template('layout.html', title='layout', product=product)

@app.route('/layout_store',methods =['GET' , 'POST'])
def layout_store():
    filterd_resultr="filterd_resultr"
    product = Addproduct.query.get_or_404(6)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    return render_template('layout_store.html', title='layout', product=product, filterd_resultr=filterd_resultr, products= products)

@app.route('/store',methods =['GET' , 'POST'])
def store():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=16)
    product = Addproduct.query.get_or_404(1)
    sizes = Addproduct.query.filter(Addproduct.size)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(4)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store'))  

    return render_template('store.html', title='layout',sizes=sizes, grandtotal=grandtotal(), products=products, brands=brands(), product=product, filterd_resultr=filterd_resultr, vi_product=vi_product, categories=categories(), form_R=form_R, form=form)

@app.route('/home')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    product = Addproduct.query.get_or_404(1)

    return render_template('products/index.html', products=products,brands=brands(),categories=categories(), product=product)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6).all()
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    products = Addproduct.query.filter(Addproduct.stock > 0)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(id)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store'))

    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories(),grandtotal=grandtotal(), products=products, filterd_resultr=filterd_resultr, vi_product=vi_product, form=form, form_R=form_R)


@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=16)
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(1)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store')) 

    return render_template('store.html',brand=brand,brands=brands(), categories=categories(),get_brand=get_brand,grandtotal=grandtotal(), filterd_resultr=filterd_resultr, vi_product=vi_product, form_R=form_R, form=form)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=16)
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(1)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store')) 
        
    return render_template('store.html',get_cat_prod=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat, grandtotal=grandtotal(), filterd_resultr=filterd_resultr, vi_product=vi_product, form_R=form_R, form=form)

@app.route('/Discount')
def get_Discount():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0, Addproduct.discount).order_by(Addproduct.id.desc()).paginate(page=page, per_page=16)
    product = Addproduct.query.get_or_404(1)

    p_id = "1"
    filterd_resultr=Addproduct.query.filter_by(id=p_id).first()
    product = Addproduct.query.get_or_404(1)
    vi_product=filterd_resultr

    #Customer Login Logic 
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('store'))

    #Customer Register Logic
    form_R = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('store'))  

    return render_template('store.html', title='layout', grandtotal=grandtotal(), products=products, brands=brands(), product=product, filterd_resultr=filterd_resultr, vi_product=vi_product, categories=categories(), form_R=form_R, form=form)

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Add brand',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/addbrand.html', title='Udate brand',brands='brands',updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The brand {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title='Add category')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update cat',updatecat=updatecat)



@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method=="POST"and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        size = form.size.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addproduct = Addproduct(name=name,price=price,size=size,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)




@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.size = form.size.data
        product.colors = form.colors.data
        product.desc = form.discription.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.size.data = product.size
    form.colors.data = product.colors
    form.discription.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
