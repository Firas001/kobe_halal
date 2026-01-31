from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)

    return render(request, 'restaurants/list.html', {
        'restaurants': restaurants,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})