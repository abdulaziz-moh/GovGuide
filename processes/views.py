from django.shortcuts import render, redirect, get_object_or_404
from . models import Process
from reviews.forms import ReviewForm
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . forms import ProcessForm, StepFormSet, AppCommentForm
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProcessSerializer

# Create your views here.

# def process_list(request):
#     # get all process objects, for consistent pagination
#     list_of_processes = Process.objects.all().order_by('-created_at')
#     # set the number of items per page
#     items_per_page = 10
#     #create a paginator instance 
#     paginator = Paginator(list_of_processes, items_per_page)
#     # get the current page number
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     if request.headers.get('HX-Request'): # then we will return a template(named partial ) with just the new items
#         return render(request, 'processes/partials/process_items.html',{'page_obj':page_obj})
    
#     # for initial page load, render the full page
#     commentform = AppCommentForm()
#     user = request.user
#     return render(request, 'processes/list.html',{'page_obj':page_obj, 'user':user,'commentform':commentform})

def process_list(request):
    query = request.GET.get("q", "")  # 👈 search query if exists

    # filter if searching, otherwise return all
    if query:
        list_of_processes = Process.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by("-created_at")
    else:
        list_of_processes = Process.objects.all().order_by("-created_at")

    # paginate
    items_per_page = 10
    paginator = Paginator(list_of_processes, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.headers.get("HX-Request"):  
        return render(request, "processes/partials/process_items.html", {
            "page_obj": page_obj,
            "query": query,
        })
    
    # full page load
    commentform = AppCommentForm()
    user = request.user
    return render(request, "processes/list.html", {
        "page_obj": page_obj,
        "user": user,
        "commentform": commentform,
        "query": query,  # 👈 keep the query in the template
    })


def process_detail(request, pk):
    process = get_object_or_404(Process, pk = pk)
    
    if request.user.is_authenticated:    # this uses to give a review form for authenticated and user who didn't rate before.
        try:
            Review.objects.get(user_id=request.user.id ,process_id=pk) # if their is no review it will raize an exception
            
            form = None
        except Review.DoesNotExist:
            if request.method == "POST":
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    if request.user.is_authenticated:
                        review.user_id = request.user
                        review.process_id = process  
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
            order = 1
            for step in steps:
                step.process_id = new_process
                step.order_number = order
                order += 1
                step.save()

            return redirect('success_page')
    else:
        process_form = ProcessForm()
        formset = StepFormSet(prefix='steps')  # 👈 prefix

    return render(request, 'processes/create_process.html', {
        'process_form': process_form,
        'formset': formset,
    })

@login_required
def process_update(request, pk):
    process = get_object_or_404(Process, id=pk)

    if request.method == 'POST':
        
        process_form = ProcessForm(request.POST, instance=process)
        formset = StepFormSet(request.POST, instance=process, prefix='steps')  # 👈 FIX

        if process_form.is_valid():
            print("process valid")
        if formset.is_valid():
            print("formset is valid")
        print("formset errors:", formset.errors)
        print("deleted forms:", [f.cleaned_data for f in formset.deleted_forms])

        if process_form.is_valid() and formset.is_valid():
            print("valid")
            updated_process = process_form.save(commit=False)
            updated_process.created_by = request.user
            updated_process.save()

            formset.instance = updated_process   # redundant but safe
            
            steps = formset.save(commit=False)

            # Delete steps marked for removal
            for obj in formset.deleted_objects:
                obj.delete()
            order = 1
            for step in steps:
                step.process = updated_process
                step.order_number = order
                order += 1
                step.save()
                
            # formset.save()                       # 👈 will now update/delete

            return redirect('process_update', pk=updated_process.id)
    else:
        process_form = ProcessForm(instance=process)
        formset = StepFormSet(instance=process, prefix='steps')  # 👈 FIX

    return render(request, 'processes/create_process.html', {
        'process_form': process_form,
        'formset': formset,
    })
 
def success_page(request):
    return render(request,"processes/success_page.html")
             

@login_required
def process_delete(request, pk):
    try:
        product = Process.objects.get(id=pk)
        product.delete()
        return redirect('personal_posts')
    except Process.DoesNotExist:
        return redirect('personal_posts')


def baseprocess(request):
    return render(request, 'processes/base_process.html')

@login_required
def personal_posts(request):
    user = request.user
    posts = user.processes.all()
    return render(request,"processes/personal_posts.html", {'user':user,'page_obj':posts})

def add_app_comment(request):
    if request.method == 'POST':
        commentform = AppCommentForm(request.POST)
        if commentform.is_valid():
            commentform.save()
            
            commentform = AppCommentForm()
            return render(request, 'processes/partials/comments.html', {
                'commentform': commentform,
                'success': True,   # so we can show a success message
            })
    commentform = AppCommentForm()
    return render(request, 'processes/partials/comments.html', {'commentform': commentform})
# ================================ API ====================================== #

@api_view(['GET'])
def process_share(request):
    processes = Process.objects.all()
    serializer = ProcessSerializer(processes, many=True)
    return Response(serializer.data)
