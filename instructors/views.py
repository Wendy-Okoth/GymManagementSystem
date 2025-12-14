from django.shortcuts import render, get_object_or_404
from .models import Instructor

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

