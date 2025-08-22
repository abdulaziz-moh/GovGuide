from django.shortcuts import render, redirect, get_object_or_404
from . models import Process
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def process_list(request):
    # get all process objects, for consistent pagination
    processes_list = Process.objects.all().order_by('-created_at')
    # set the number of items per page
    items_per_page = 20
    #create a paginator instance 
    paginator = Paginator(process_list, items_per_page)
    
    # get the current page number
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.headers.get('HX-Request'): # then we will return a template(named partial ) with just the new items
        return render(request, 'processes/partials/process_items.html',{'page_obj':page_obj})
    
    # for initial page load, render the full page
    return render(request, 'processes/list.html',{'page_obj':page_obj})


def process_detail(request, pk):
    pass

@login_required
def process_create(request):
    pass

@login_required
def process_delete(request, pk):
    pass