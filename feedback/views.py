from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback
from members.models import Member

@login_required
def feedback_list(request):
    member = get_object_or_404(Member, email=request.user.email)
    feedbacks = Feedback.objects.filter(member=member)
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    member = get_object_or_404(Member, email=request.user.email)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.member = member
            feedback.instructor = member.gym_instructor
            feedback.save()
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
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback.html', {'form': form})

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, member__email=request.user.email)
    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback_list')
    # ✅ render a delete confirmation template instead of feedback.html
    return render(request, 'feedback_confirm_delete.html', {'feedback': feedback})



