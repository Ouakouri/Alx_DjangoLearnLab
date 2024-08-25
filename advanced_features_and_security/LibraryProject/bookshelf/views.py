from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('app_name.can_edit', raise_exception=True)
def edit_book_list(request, pk):
 
    return render(request, 'edit_book_list.html', context)

@permission_required('app_name.can_create', raise_exception=True)
def create_books(request):

    return render(request, 'create_books.html', context)

from .models import MyModel

def my_view(request):
    query = request.GET.get('query', '')
    results = MyModel.objects.filter(name__icontains=query)
    return render(request, 'my_template.html', {'results': results})
from django import forms
from .forms import ExampleForm"

class MyForm(forms.Form):
    query = forms.CharField(max_length=100)


# Create your views here.
