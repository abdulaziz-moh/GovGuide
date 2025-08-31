from django.shortcuts import render, redirect, get_object_or_404
from . models import Process
from reviews.forms import ReviewForm
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . forms import ProcessForm, StepFormSet
# Create your views here.

def process_list(request):
    # get all process objects, for consistent pagination
    list_of_processes = Process.objects.all().order_by('-created_at')
    # set the number of items per page
    items_per_page = 10
    #create a paginator instance 
    paginator = Paginator(list_of_processes, items_per_page)
    # get the current page number
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('HX-Request'): # then we will return a template(named partial ) with just the new items
        return render(request, 'processes/partials/process_items.html',{'page_obj':page_obj})
    
    # for initial page load, render the full page
    user = request.user
    return render(request, 'processes/list.html',{'page_obj':page_obj, 'user':user})


def process_detail(request, pk):
    process = get_object_or_404(Process, pk = pk)
    
    if request.user.is_authenticated:    # this uses to give a review form for authenticated and user who didn't rate before.
        try:
            Review.objects.get(user_id=request.user.id ,process_id=pk)
            
            form = None
        except Review.DoesNotExist:
            if request.method == "POST":
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    if request.user.is_authenticated:
                        review.user_id = request.user
                        review.process_id = process  # 👈 Corrected line
                    review.save()
                    review.process_id.average_rating(review.rating)
                    return redirect("process_list") 
            else:
                form = ReviewForm()
            
    else:
        form = None

    return render(request, 'processes/detail.html', {"process": process, "form": form})

@login_required
def create_process_steps(request):
    if request.method == 'POST':
        process_form = ProcessForm(request.POST)
        formset = StepFormSet(request.POST, prefix='steps')  # 👈 prefix

        if process_form.is_valid() and formset.is_valid():
            new_process = process_form.save(commit=False)
            new_process.created_by = request.user
            new_process.save()

            steps = formset.save(commit=False)
            for step in steps:
                step.process_id = new_process
                step.save()

            return redirect('success_page')
    else:
        process_form = ProcessForm()
        formset = StepFormSet(prefix='steps')  # 👈 prefix

    return render(request, 'processes/create_process.html', {
        'process_form': process_form,
        'formset': formset,
    })

def success_page(request):
    return render(request,"processes/success_page.html")
             

@login_required
def process_delete(request, pk):
    pass
def baseprocess(request):
    return render(request, 'processes/base_process.html')

@login_required
def personal_posts(request):
    user = request.user
    posts = user.processes.all()
    return render(request,"processes/personal_posts.html", {'user':user,'posts':posts})