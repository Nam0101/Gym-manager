from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from members.models import Member, Manager
from review.forms import addReviewForm
from review.models import Review


# Create your views here.
def add_review(request):
    if request.method == 'POST':
        form = addReviewForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('my_reviews')
    else:
        form = addReviewForm()
    context = {'form': form}
    return render(request, "add_review.html", context)


def view_reviews(request):
    current_user = request.user
    if current_user.is_superuser:
        reviews = Review.objects.all()
    else:
        manager = Manager.objects.get(user=current_user)
        reviews = Review.objects.filter(member__room__manager=manager)
    context = {'reviews': reviews}
    return render(request, 'view_review.html', context)


@login_required
def my_reviews(request):
    current_user = request.user
    member = Member.objects.get(user=current_user)
    reviews = Review.objects.filter(member=member)
    context = {'reviews': reviews}
    return render(request, 'my_reviews.html', context)