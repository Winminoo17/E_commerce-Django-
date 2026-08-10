from Eco_Website.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
    
    def db_add(self, product, quantity ):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            current_user.update(old_cart=carty)
    
    def add(self, product, quantity ):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            current_user.update(old_cart=carty)
            
        
    def __len__(self):
        return len(self.cart)

    def prods_cart(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def prods_qty(self):
        prod_qty = self.cart
        return prod_qty
    
    def update_qty(self, product, qty ):
        product_id = str(product)
        product_qty = int(qty)
        currentCart = self.cart
        currentCart[product_id] = product_qty
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            current_user.update(old_cart=carty)
        
        thing = self.cart
        return thing
    
    def cart_delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            current_user.update(old_cart=carty)
    
    def get_total_price(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        total = 0
        for key, value in self.cart.items():
            product = Product.objects.get(id=key)
            if product.is_sale:
                total += float(product.sale_price) * value
            else:
                total += float(product.price) * value
        return total
    
    def clear(self):
    # empty the session cart
        self.session['session_key'] = {}
        self.session.modified = True

        # also wipe the saved copy so it doesn't get reloaded on next login
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            current_user.update(old_cart=None)
        
    
    
    