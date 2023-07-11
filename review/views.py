from django.shortcuts import render, redirect

from review.forms import addReviewForm


# Create your views here.
def add_review(request):
    if request.method == 'POST':
        form = addReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_review')
    else:
        form = addReviewForm()
    context = {'form': form}
    return render(request, "add_review.html", context)


def view_review(request):
    return None