from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
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


@login_required
def view_reviews(request):
    current_user = request.user
    if not current_user.is_active:
        raise Http404
    if current_user.is_superuser:
        reviews = Review.objects.all()
    else:
        manager = get_object_or_404(Manager, user=current_user)
        try:
            reviews = Review.objects.filter(member__room__manager=manager)
        except Review.DoesNotExist:
            raise Http404
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'reviews': page_obj}
    return render(request, 'view_review.html', context)


@login_required
def my_reviews(request):
    try:
        current_user = request.user
        member = Member.objects.get(user=current_user)
        reviews = Review.objects.filter(member=member)
        context = {'reviews': reviews}
    except Member.DoesNotExist:
        raise Http404
    return render(request, 'my_reviews.html', context)