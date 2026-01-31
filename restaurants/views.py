from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Category 
from django.contrib.auth import logout
from django.core.paginator import Paginator 

def restaurant_list(request):
    places_list = Place.objects.all().order_by('-created_at') 
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        places_list = places_list.filter(category_id=category_id)

    paginator = Paginator(places_list, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'restaurants/list.html', {
        'restaurants': page_obj, 
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def restaurant_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    
    return render(request, 'restaurants/detail.html', {
        'restaurant': place
    })

def custom_logout(request):
    logout(request)
    return redirect('list')