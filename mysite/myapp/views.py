from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required


def index(request):
    items = Product.objects.all()
    context = {
        'items': items
    }
    return render(request, "myapp/index.html", context)


def indexItem(request, my_id):
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, "myapp/detail.html", context)

@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        # получаем кто добавил товар
        seller = request.user
        item = Product(name=name, price=price, description=description, image=image, seller=seller)
        item.save()
    return render(request, "myapp/add_item.html")


def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        # перезаписываем данные в базе данных на новые
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.image = request.FILES.get('upload', item.image)
        item.save()
        return redirect('/myapp/')
    context = {
        'item': item
    }

    return render(request, "myapp/update_item.html", context)


def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect('/myapp/')
    context = {
        'item': item
    }

    return render(request, "myapp/delete_item.html", context)


