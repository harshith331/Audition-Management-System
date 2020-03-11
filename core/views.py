from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, AppConfig
import json

round_details = {
    1: 'Pen and Paper Round',
    2: 'Task Round One',
    3: 'Task Round Two',
    4: 'Group Discussion Round',
    5: 'Final Personal Interview',
    6: 'Inducted'
}


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    students = Student.objects.all()
    for student in students:
        student.current_round = round_details[student.current_round]
    context_data = {
        'students': students,
    }
    return render(request, 'dashboard.html', context_data)


@login_required
def profile(request, id):
    student_details = Student.objects.filter(id=id).first()
    student_details.current_round = round_details[student_details.current_round]
    context_data = {
        'student_details': student_details,
    }
    return render(request, 'profile.html', context_data)


@login_required
def promote(request, id):
    if request.method == 'POST':
        student_details = Student.objects.filter(id=id).first()
        if student_details.current_round < 6:
            student_details.current_round = student_details.current_round + 1
            student_details.save()
            return redirect('/dashboard')
        else:
            messages.error(request, 'Already Inducted')
            return redirect('/profile/{}'.format(int(id)))


@login_required
def stop(request, id):
    if request.method == 'POST':
        student_details = Student.objects.filter(id=id).first()
        student_details.stopped = True
        student_details.save()
        return redirect('/dashboard')


@login_required
def resume(request, id):
    if request.method == 'POST':
        student_details = Student.objects.filter(id=id).first()
        student_details.stopped = False
        student_details.save()
        return redirect('/dashboard')


def results(request):
    students = Student.objects.all()
    config = AppConfig.objects.get(id=1)
    for student in students:
        student.current_round = round_details[student.current_round]
    context_data = {
        'students': students,
        'result_status': config.show_results,
    }
    return render(request, 'results.html', context_data)


@login_required
def set_result_status(request):
    config = AppConfig.objects.get(id=1)
    config.show_results = not config.show_results
    config.save()
    return redirect('/dashboard')

def all_stud_api(request):
    students=Student.objects.all()
    studs = list()
    for s in students:
        studs.append({
            'name':s.name,
            'year':str(s.year),
            'dept':s.dept,
            'stpd':s.stopped
        })
    print(studs)
    return JsonResponse(studs, safe=False)

def stud_deet_api(request,id):
    if request.method=="POST":
        stud=json.loads(request.body)
        name=stud['name']
        if name:
            student=Student.objects.get(name=name)
            print("request by name")
            print(student.year)
        else:
            student=Student.objects.get(id=id)
            print("request by id")
            print(student.year)
        return redirect('/')

    