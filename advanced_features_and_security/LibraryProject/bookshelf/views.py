from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('app_name.can_edit', raise_exception=True)
def edit_my_model(request, pk):
 
    return render(request, 'edit_my_model.html', context)

@permission_required('app_name.can_create', raise_exception=True)
def create_my_model(request):

    return render(request, 'create_my_model.html', context)

# Create your views here.
