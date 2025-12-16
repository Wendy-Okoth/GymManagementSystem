from django.shortcuts import render, get_object_or_404
from .models import Instructor
from members.models import Member

def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'instructors/instructor_list.html', {'instructors': instructors})

def instructor_detail(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    return render(request, 'instructors/instructor_detail.html', {'instructor': instructor})

def instructor_dashboard(request):
    instructor_id = request.session.get('instructor_id')
    if not instructor_id:
        return redirect('login')
    instructor = Instructor.objects.get(id=instructor_id)
    return render(request, 'instructor_dashboard.html', {'instructor': instructor})

def instructor_profile(request):
    instructor_id = request.session.get('instructor_id')
    if not instructor_id:
        return redirect('login')
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructors/instructor_profile.html', {'instructor': instructor})

def instructor_members(request):
    instructor_id = request.session.get('instructor_id')
    if not instructor_id:
        return redirect('login')
    instructor = get_object_or_404(Instructor, id=instructor_id)
    members = Member.objects.filter(gym_instructor=instructor)
    return render(request, 'instructors/instructor_members.html', {'members': members})
