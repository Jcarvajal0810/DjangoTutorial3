from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect 
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from .models import Product
from pages.utils import ImageLocalStorage

# Create your views here.
#def homePageView(request):
    # return HttpResponse('Hello, World!')
    #return render(request, 'pages/home.html')

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About Us - Online Store",
            "subtitle": "About Us",
            "description": "This is an about page...",
            "author": "Develop by: Jose Manuel Carvajal Aristizabal"
        })

        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Contact Us",
            "description": "This is a contact page...",
            "author": "Develop by: Jose Mnauel Carvajal",
            "email": "info@example.com",
            "address": "123 Main St, City, State, 12345",
            "phone": "555-555-5555",
        })

        return context

"""class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1000},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1500},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 2000},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 500},
    ]"""

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (IndexError, ValueError):  # Para cuando el indice no es valido
            return HttpResponseRedirect('/')  # Lo redirige al home
        
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm):
    #name = forms.CharField(required=True)
    #price = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Agregue un precio mayor a 0")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_created')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            return render(request, self.template_name, viewData)

class ProductCreatedView(TemplateView):
        template_name = 'products/product_created.html'

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through "products" in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}

        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)
    
    
    def post(self, request, product_id):
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')
    
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    
    return ImageView 

class ImageViewNoDI(View):
    template_name = 'imagesnotdi/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('imagenotdi_index')
