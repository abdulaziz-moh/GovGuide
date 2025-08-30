from django.shortcuts import render, redirect
from .forms import ReviewForm

# Create your views here.

def submit_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            # make status variable and if reviewed give it another veiw like thanks!
            return redirect("reviews_list")  # redirect after POST
    else:
        form = ReviewForm()

    return render(request, "processes/detail.html", {"form": form})
