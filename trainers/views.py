from django.shortcuts import render
from .models import Trainer
from members.models import Training_history


def view_training_history(request):
    trainer = Trainer.objects.get(user=request.user)
    training_history = Training_history.objects.filter(trainer=trainer)
    context = {
        'trainer': trainer,
        'training_history': training_history,
    }
    return render(request, 'training_history.html', context)
