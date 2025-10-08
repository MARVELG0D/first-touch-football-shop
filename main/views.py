from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

@login_required(login_url='/login')
def show_main(request):
    context = {
        'npm' : '2406421346',
        'name': request.user.username,
        'class': 'PBP C',
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

# AJAX endpoint to get products as JSON
@login_required(login_url='/login')
def get_products_json(request):
    filter_type = request.GET.get("filter", "all")
    
    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    
    return HttpResponse(serializers.serialize('json', products), content_type="application/json")

# AJAX endpoint to create product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def create_product_ajax(request):
    try:
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        thumbnail = request.POST.get("thumbnail")
        stock = request.POST.get("stock")
        brand = request.POST.get("brand")
        is_featured = request.POST.get("is_featured") == "on"
        
        new_product = Product.objects.create(
            user=request.user,
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            stock=stock,
            brand=brand,
            is_featured=is_featured
        )
        
        return JsonResponse({
            "status": "success",
            "message": "Product created successfully!",
            "product": {
                "id": str(new_product.id),
                "name": new_product.name,
                "price": new_product.price
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX endpoint to update product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        
        if request.user != product.user:
            return JsonResponse({
                "status": "error",
                "message": "You are not authorized to edit this product."
            }, status=403)
        
        product.name = request.POST.get("name", product.name)
        product.price = request.POST.get("price", product.price)
        product.description = request.POST.get("description", product.description)
        product.category = request.POST.get("category", product.category)
        product.thumbnail = request.POST.get("thumbnail", product.thumbnail)
        product.stock = request.POST.get("stock", product.stock)
        product.brand = request.POST.get("brand", product.brand)
        product.is_featured = request.POST.get("is_featured") == "on"
        
        product.save()
        
        return JsonResponse({
            "status": "success",
            "message": f"Product '{product.name}' updated successfully!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX endpoint to delete product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        
        if request.user != product.user:
            return JsonResponse({
                "status": "error",
                "message": "You are not authorized to delete this product."
            }, status=403)
        
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            "status": "success",
            "message": f"Product '{product_name}' deleted successfully!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX login
@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": "success",
                "message": "Login successful!",
                "username": user.username
            }, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "message": "Invalid username or password."
            }, status=401)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)

# AJAX register
@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return JsonResponse({
                "status": "error",
                "message": "Passwords do not match."
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": "error",
                "message": "Username already exists."
            }, status=400)
        
        try:
            user = User.objects.create_user(username=username, password=password1)
            return JsonResponse({
                "status": "success",
                "message": "Registration successful! You can now login."
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)

# Keep old views for backward compatibility
@login_required(login_url='/login')
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login/')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.user != product.user:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('main:show_main')

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, f"Product '{product.name}' has been updated successfully!")
        return redirect('main:show_main')

    context = {
        'form': form,
        'product': product,
    }

    return render(request, "edit_product.html", context)

@login_required(login_url='/login/')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.user == product.user:
        product.delete()
        messages.success(request, f"Product '{product.name}' has been deleted.")
    else:
        messages.error(request, "You are not authorized to delete this product.")
        
    return HttpResponseRedirect(reverse('main:show_main'))