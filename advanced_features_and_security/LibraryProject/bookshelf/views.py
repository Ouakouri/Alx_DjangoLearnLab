from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('app_name.can_edit', raise_exception=True)
def edit_book_list(request, pk):
 
    return render(request, 'edit_book_list.html', context)

@permission_required('app_name.can_create', raise_exception=True)
def create_books(request):

    return render(request, 'create_books.html', context)

# Create your views here.
