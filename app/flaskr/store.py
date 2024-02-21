"""
Flask blueprint for browsing items.
"""
from flask import (
    Blueprint, 
    render_template, 
    request, 
    session, 
    g, 
    flash, 
    redirect, 
    url_for
)

from flaskr.db import (
    get_some_products, 
    count_products, 
    get_one_product, 
    update_cart as update_cart_in_db,
    get_amount_in_cart,
    get_cart
)

bp = Blueprint("store", __name__)
LIMIT = 12 #TODO: move magic constants somewhere else

@bp.route("/")
def index():
    try:
        page = int(request.args.get('page', 1))
        page = page if page > 0 else 1
    except TypeError:
        page = 1
    except ValueError:
        page = 1
    products = get_some_products(LIMIT, (page-1)*LIMIT)
    total_product_count = count_products()
    return render_template("store/index.html", products=products, page=page, limit=LIMIT, tot_prod=total_product_count)

@bp.route("/cart", methods=['GET'])
def cart():
    if g.user is not None:
        cart, cart_id = get_cart(g.user['id'])
        return render_template("store/cart.html", cart=cart, cart_id=cart_id)
    return redirect(url_for('store.index'))

@bp.route("/cart", methods=['POST'])
def update_cart():
    if g.user is not None:
        cart, cart_id = get_cart(g.user['id'])
        for form in request.form:
            # TODO
            pass
        return render_template("store/cart.html", cart=cart, cart_id=cart_id)
    return redirect(url_for('store.index'))

@bp.route("/product", methods=["GET"])
def product_info():
    try:
        product_id = int(request.args.get('id', 1))
    except TypeError:
        product_id = 1
    except ValueError:
        product_id = 1

    if g.user is None: # This updates the text below the greyed out "add to cart" button
        flash("You must be logged in to add to cart.")
    product = get_one_product(product_id)
    return render_template("store/product.html", id=product_id, product=product)

@bp.route("/product", methods=["POST"])
def add_to_cart():
    try:
        product_id = int(request.args.get('id', 1))
    except TypeError:
        product_id = 1
    except ValueError:
        product_id = 1

    product = get_one_product(product_id)
    quantity = int(request.form.get('quantity'))

    if g.user is not None:
        in_cart_amount = get_amount_in_cart(g.user['id'], product_id)
        update_cart_in_db(g.user['id'], product, quantity+in_cart_amount)

    return render_template("store/product.html", id=product_id, product=product)