from django.shortcuts import render
import requests
import json


def products_view(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    min_reviews = request.GET.get('min_reviews')

    filters = {}
    if min_price:
        filters['min_price'] = min_price
    if max_price:
        filters['max_price'] = max_price
    if min_rating:
        filters['min_rating'] = min_rating
    if min_reviews:
        filters['min_reviews'] = min_reviews

    # запрос к эндпоинту
    api_url = "http://localhost:8000/api/products/"
    try:
        response = requests.get(api_url, params=filters)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        charts_data = data.get("charts_data", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        products = []
        charts_data = {}


    # передача данных
    return render(request, 'frontend/products.html', {
        'products': products,
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'min_rating': min_rating,
            'min_reviews': min_reviews,
        },
        'charts_data': json.dumps(charts_data)
    })