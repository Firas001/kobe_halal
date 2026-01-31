from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Category 
from django.contrib.auth import logout

def restaurant_list(request):
    places = Place.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        places = places.filter(category_id=category_id)

    return render(request, 'restaurants/list.html', {
        'restaurants': places,
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