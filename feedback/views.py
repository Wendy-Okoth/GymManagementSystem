from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import datetime

from .forms import FeedbackForm
from .models import Feedback
from members.models import Member

@login_required
def feedback_list(request):
    member = get_object_or_404(Member, email=request.user.email)
    feedbacks = Feedback.objects.filter(member=member).order_by('-date')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    member = get_object_or_404(Member, email=request.user.email)
    today = timezone.localdate()

    # ✅ Rule 1: Only one feedback per day
    if Feedback.objects.filter(member=member, date=today).exists():
        messages.error(request, "You have already submitted feedback for today.")
        return redirect('feedback_list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.member = member
            feedback.instructor = member.gym_instructor
            feedback.save()
            messages.success(request, "Feedback submitted successfully.")
            return redirect('feedback_list')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})

@login_required
def feedback_edit(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, member__email=request.user.email)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully.")
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback.html', {'form': form})

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, member__email=request.user.email)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
        return redirect('feedback_list')
    return render(request, 'feedback_confirm_delete.html', {'feedback': feedback})




