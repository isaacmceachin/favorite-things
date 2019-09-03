from django.http import HttpResponse, JsonResponse, Http404
# Create your views here.
from django.core import serializers

from django.views.generic import TemplateView
from django.views import View

from django.db.models import Count
from .models import Category, FavoriteThing

from rest_framework.response import Response
from rest_framework import status

from django.middleware.csrf import get_token
from django.views.decorators.csrf import requires_csrf_token

from django.http import QueryDict

import json

class TextView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class CategoriesView(View):

    def get(self, request, *args, **kwargs):
        #cat = request.GET.get('','')
        #print("Cat", cat)
        #print("args", args)
        #print("kwargs", kwargs)

        try:
            results = Category.objects.annotate(subthings=Count('favoritethings')).order_by('-created_on')
            if results.count() >= 1:
                return JsonResponse({'data': list(results.values())})
            else:
                return JsonResponse({'error': "no-data"})
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
            return None

    def post(self, request, *args, **kwargs):
        category_title = request.POST.get('categoryTitle', '')
        res = Category.objects.create(title=category_title)
        print(res)
        return JsonResponse({'data': {}})

class CategoryView(View):

    def get(self, request, *args, **kwargs):
        #csrf_token = get_token(request)
        #print("my", csrf_token)

        #cat = request.GET.get('','')
        #print("Cat", cat)
        #print("args", args)
        #print("kwargs", kwargs)

        #return JsonResponse({'data': kwargs})

        try:
            results = Category.objects.get(uuid=kwargs['category_uuid']).favoritethings.all().order_by('ranking')
            #print(results)

            if results.count() >= 1:
                return JsonResponse({'data': list(results.values())})
            else:
                return JsonResponse({'error': "no-data"})
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
            return None

    def post(self, request, *args, **kwargs):
        #print("req", request)
        #print("args", args)
        #print("kwargs", kwargs)

        category_title = request.POST.get('categoryTitle', '')
        description = request.POST.get('description', '')
        ranking = request.POST.get('ranking', 1)
        meta_data = request.POST.get('meta_data', {})
        category = request.POST.get('category', '')

        print(category_title, description, ranking, meta_data, category)

        #print("category_title", category_title)
        #print("GET", request.GET)
        #print("POST", request.POST)

        cat = Category.objects.get(uuid=category)

        if len(category_title) > 0 :
            res = FavoriteThing.objects.create(title=category_title, description=description, ranking=ranking, meta_data=meta_data, category=cat);
            print(res)

            results = Category.objects.annotate(subthings=Count('favoritethings')).order_by('-created_on')
            if results.count() >= 1:
                return JsonResponse({'data': list(results.values())})
            else:
                return JsonResponse({'error': "no-data"})
        else:
            raise Http404("Unable to create blank category")
            return None

    def delete(self, request, *args, **kwargs):

        cat = Category.objects.filter(uuid=kwargs['category_uuid']).delete()
        print(cat)

        return JsonResponse({'data': cat})


class IndexView(View):

    def get(self, request):
        #a = request.POST.get('section','') # => [39]
        #b = request.POST.get('MAINS','') # => [137]
        c = request.GET.get('c','') # => [39]
        d = request.GET.get('d','') # => [137]

        print("C", c, "D", d)

        results = FavoriteThing.objects.all().values()#.values('uuid', 'title')
        return JsonResponse({'data': list(results)})

    def post(self, request):
        # Code block for POST request
        return HttpResponse('Hello, World!')
