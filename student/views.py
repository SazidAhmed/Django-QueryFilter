from django.shortcuts import render
from .models import Student, Teacher

#sql queries
from django.db import connection
from django.db.models import Q


# OR Queries
#################################################################

def student_list_(request):
    data = Student.objects.all()
    print(data)
    print(data.query)
    print(connection.queries)
    return render(request, 'output.html',{'data':data})

def student_list_(request):
    data = Student.objects.filter(surname__startswith='austin') | Student.objects.filter(surname__startswith='baldwin')
    return render(request, 'output.html',{'data':data})

def student_list_(request):
    data = Student.objects.filter(Q(surname__startswith='austin') | ~Q (surname__startswith='baldwin') | Q (surname__startswith='avery-parker'))
    return render(request, 'output.html',{'data':data})


# AND Queries
#################################################################

def student_list_(request):
    data = Student.objects.filter(classroom=3) & Student.objects.filter(firstname__startswith='lakisha')
    print(connection.queries)
    return render(request, 'output.html',{'data':data})

def student_list_(request):
    data = Student.objects.exclude(classroom=3) & Student.objects.filter(firstname__startswith='lakisha')
    print(connection.queries)
    return render(request, 'output.html',{'data':data})


def student_list(request):
    data = Student.objects.filter(Q(surname__startswith='baldwin')&Q(firstname__startswith='lakisha'))
    print(connection.queries)
    return render(request, 'output.html',{'data':data})


# UNION Queries
#################################################################

def student_list_(request):
    #return list
    datax = Student.objects.all().values_list("firstname").union(Teacher.objects.all().values_list("firstname"))
    #return dictionary
    data = Student.objects.all().values("firstname").union(Teacher.objects.all().values("firstname"))
    print(connection.queries)
    return render(request,'output.html',{'data': data})

# NOT Queries (WHERE NOT)
#################################################################

# Simple EXCLUDE
def student_list_(request):

    data = Student.objects.exclude(age=20)
    datax = Student.objects.exclude(age=20) & Student.objects.exclude(firstname__startswith='lakisha')
    print(connection.queries)
    return render(request,'output.html',{'data': data})

#extended operations
def student_list_(request):
    # = Equal 
    # =! Not Equal 
    # > Greater than (gt)
    datax = Student.objects.exclude(age__gt=20)
     # >= Greater than or qual to (gte)
    datax = Student.objects.exclude(age__gte=21)
    # < Less than (lt)
    datax = Student.objects.exclude(age__lt=21)
    # <= Less than or equal to (lte)
    datax = Student.objects.exclude(age__lte=20)

    print(connection.queries)
    return render(request,'output.html',{'data': data})

# ~Q mean not equal
def student_list_(request):
    #return not age greater then 20
    datax = Student.objects.filter(~Q(age__gt=20))
    #return not age greater then 20 AND NOT surname = baldwin
    data = Student.objects.filter(~Q(age__gt=20) &~Q(surname__startswith='baldwin'))

    print(connection.queries)
    return render(request,'output.html',{'data': data})

# Select individual fields
#################################################################
def student_list_(request):
    #return only firstname of classroom 1
    data = Student.objects.filter(classroom=1).only('firstname', 'age')

    print(data)
    print(connection.queries)
    return render(request,'output.html',{'data': data})

# RAW SQL queries
#################################################################
def student_list_(request):
    sql = "SELECT * FROM student_student"
    sqlx = "SELECT * FROM student_student WHERE age>=21"
    datax = Student.objects.raw(sql)
    data = Student.objects.raw(sql)[:2]

    # looping
    for s in Student.objects.raw("SELECT * FROM student_student"):
        print(s.age)

    # mapping
    student_mapping = {'fname':'firstname', 'sname':'surname'}
    objs = Student.objects.raw("SELECT * FROM student_student",translations = student_mapping)
    student = objs[0].firstname
    print(student)
    print(connection.queries)

    return render(request,'output.html',{'data': data})

# RAW SQL queries without the ORM
#################################################################
def student_list_(request):
    cursor = connection.cursor()
    # cursor.execute("SELECT count (*) FROM student_student")
    # datax = cursor.fetchone()
    cursor.execute("SELECT * FROM student_student")
    data = cursor.fetchall()
    print(data)
    print(connection.queries)

    return render(request,'output.html',{'data': data})

#using dictionary
def dictfetchall(cursor):
    desc = cursor.description
    return[
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def student_list(request):
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM student_student")
    cursor.execute("SELECT * FROM student_student WHERE age > 20")
    data = dictfetchall(cursor)
    print(data)
    print(connection.queries)

    return render(request,'output.html',{'data': data})

# Model Inheritance Options
#################################################################
def student_list_(request):
    cursor = connection.cursor()
    # cursor.execute("SELECT count (*) FROM student_student")
    # datax = cursor.fetchone()
    cursor.execute("SELECT * FROM student_student")
    data = cursor.fetchall()
    print(data)
    print(connection.queries)

    return render(request,'output.html',{'data': data})