from django.shortcuts import render

from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from office.views import new_ads, new_invoice
import json



from dtr.views import worklogger, worklogger_out


from office.models import Customer, Adcategory, Ad, Invoice
from .models import User, Department, Position




def main(request):
    
    if request.user.is_authenticated:
        _uzer = request.user
             
        context = {'user': _uzer,
                    'position':_uzer.position,
                    'first_name': _uzer.first_name,
                    'last_name': _uzer.last_name,
                    'designation': [d.title for d in _uzer.designation.all()],
                    'logged': _uzer.is_logged,
                    
                }
        
 

        return render(request, 'mainapp/card/profiletab.html', context)            
    else:
        return HttpResponseRedirect(reverse('log'))


def worktab(request):
    if request.user.is_authenticated and request.user.is_logged:

        context = {
            'user':request.user,
            'logged':request.user.is_logged,
            'all_people': [person for person in User.objects.filter(is_superuser=False).all()],
            'customers': [customer for customer in Customer.objects.all()],
            'positions': [position for position in Position.objects.all()],
            'categories': [category for category in Adcategory.objects.all()],
            'invoices': [invoice for invoice in Invoice.objects.order_by('-invoice_no')],
            'ads': [ad for ad in Ad.objects.all()],
            'admin': False
        }
        if request.user.position is not None:

            if request.user.position.title == "manager":
                context['admin'] = True
            elif request.user.position.title == "traffic":
                context['admin'] = True
            elif request.user.position.title is None:
                context['admin'] = False
            else:
                context['admin'] = False
        else:
            context['admin'] = False

        return render(request, 'mainapp/card/worktab.html', context)
    else:
        return HttpResponseRedirect(reverse('main'))


def overview(request):
    
    if request.user.is_authenticated and request.user.is_logged:
        
        context = {
            'user':request.user,
            'logged':request.user.is_logged,
            'admin': False,

            'people':User.objects.filter(is_superuser=False),
            'positions':Position.objects.all(),
            'departments':Department.objects.all()

        }
        if request.user.position is not None:

            if request.user.position.title == "manager":
                context['admin'] = True
            elif request.user.position.title == "traffic":
                context['admin'] = True
            elif request.user.position.title is None:
                context['admin'] = False
            else:
                context['admin'] = False
        else:
            context['admin'] = False

        return render(request, 'mainapp/card/overview.html', context)
    else:
        return HttpResponseRedirect(reverse('main'))


def usr_api(request, username):
    if request.user.is_authenticated:
        _uzer = User.objects.get(username=username.lower())
        context = {'user': str(_uzer),
                    'position':str(_uzer.position).title(),
                    'first_name': _uzer.first_name.title(),
                    'last_name': _uzer.last_name.title(),
                    'email': _uzer.email.lower(),
                    'address': _uzer.address.title(),
                    'mobile': _uzer.mobile,
                    'telephone': _uzer.telephone,
                    'facebook': _uzer.facebook.lower(),

                    'logged': _uzer.is_logged,
                    'designation': [str(d.title) for d in _uzer.designation.all()],
                }
        return JsonResponse(context, status=201)
            
def department(request, department_name):
    context ={}

    departamento = Department.objects.get(title=department_name.lower())
    context["department"] = departamento
    context["logged"] = request.user.is_logged
    context["prospects"] = [prospects for prospects in User.objects.filter(is_superuser=False)]
    try:

        head = departamento.head.pk
        context["members_exclude_head"] = [meh for meh in departamento.users.exclude(pk=head)]
    except AttributeError:
        #if there's are no members yet
        context["members_exclude_head"] = [meh for meh in departamento.users.all()]
    
    
    
    return render(request, 'mainapp/card/department.html', context)


def login_view(request):
    return render(request, 'mainapp/login.html')


def login(request):
    if request.method == "POST":
        # Attempt to Login
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Verify User
        if user is not None:
            login_user(request, user)
            
            return HttpResponseRedirect(reverse('main'))
        else:
            return HttpResponse('WRONG PASSWORD OR USERNAME')
            #context={'login_notif': 'Invalid Username or Password!'}
            #return render(request, 'login.html', context)
    
    # Get request of Login 
    return HttpResponseRedirect(reverse('main'))


def logout(request):
    worklogger_out(f'{request.user}')
    request.user.is_logged = False
    request.user.save()
    logout_user(request)
    
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        # Getting the Details of the New User
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        address = request.POST["address"]
        mobile = request.POST["mobile"]
        telephone = request.POST["telephone"]
        facebook = request.POST["facebook"]
 

        # Check if Password Matched
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        pass

        if password != confirmation:
            return HttpResponse("The password you entered wont match each other...")

        # Save the Details to the Database
        print(request.POST)
        try:
            # & making sure the USERNAME and EMAIL are in lowerCase
            
            registration = User.objects.create_user(
                username.lower(),
                email.lower(),
                password,
                first_name=first_name.lower(),
                last_name=last_name.lower(),
                address=address.lower(),
                mobile=mobile,
                telephone=telephone,
                facebook=facebook.lower(),
            )
            registration.save()


            return HttpResponseRedirect(reverse('main'))
            
        except IntegrityError:
            return HttpResponse("Username already taken.")
            #context = {"registration_notif": "Username already taken."}
            #return render(request, "register.html", context)

    
   # return render(request, "mainapp/register.html")
    return HttpResponseRedirect(reverse('main'))



#BIOMETRICS IN
def clock_in(request):
    
    if request.user.is_logged:
        return JsonResponse({'message': 'USER ALREADY LOGGED FOR THE DAY LOG OUT FIRST'})
    else: 
        worklogger(f"{request.user}")
        request.user.is_logged = True
        request.user.save()
        return JsonResponse({'message': 'Logged'})

#EDIT PROFILE
@csrf_exempt
def save_profile(request):
    
    if request.method == "POST":
        
        context={}
        data = json.loads(request.body)  
        request.user.email = data["email"].lower()
        request.user.mobile = data["mobile"].lower()
        request.user.telephone = data["telephone"].lower()
        request.user.facebook = data["facebook"].lower()
        request.user.address = data["address"].lower()
        old_password = data["old_password"]
        new_password = data["new_password"]
        confirm_new_password = data["confirmation"]
        
        if data['change_pass_active']:
            #check if its valid password
            user = authenticate(request, username=request.user.username, password=old_password)
            context = {}
           
            if user is not None:
                if new_password == confirm_new_password:
                    request.user.password = make_password(new_password)
                    request.user.save()
                    
                else:
                    context['message'] = 'New Password Dont Match'
                    context['alert'] = 'danger'
                    context['error_fields'] = "new_fields"

            elif old_password == "":
                context['message'] = 'Empty Password'
                context['alert'] = 'danger'
                context['error_fields'] = "old_fields"
            else:
                context['message'] = 'Wrong Old Password'
                context['alert'] = 'danger'
                context['error_fields'] = "old_fields"
                
                
            return JsonResponse(context)


        request.user.save()  
                
        context['message'] = 'Details Changed Successfully'
        context['alert'] = 'success'
        return JsonResponse(context)
           
        return HttpResponseRedirect(reverse('main'))

    return HttpResponseRedirect(reverse('main'))



#APPOINT TO POSIION
@csrf_exempt
def appoint_to_position(request):
    data = json.loads(request.body)
    
    if data["position"] != "":
        try:
            _position =  Position.objects.get(title=data["position"].lower())
            _user = User.objects.get(username=data["user"])
            _user.position = _position
            _user.save()
            return JsonResponse({'message': 'SUCCESS'})

        except ObjectDoesNotExist:
            Position.objects.create(title=data["position"].lower())
            _position =  Position.objects.get(title=data["position"].lower())
            _user = User.objects.get(username=data["user"])
            _user.position = _position
            _user.save()

            return JsonResponse({'message': "CREATING NEW POSITION AND ADDING USER"})
    else:
        return JsonResponse({'message': "FAILED: Cant Create Empty Position"})

    

#FOR ADDING NEW DEPARTMENT/DESIGNATION/FIELD
def add_department(request):
    if request.method == "POST":
        dept_title = request.POST["dept_title"].lower()
        dept_description = request.POST["dept_description"].lower()
        _add = Department(title=dept_title,description=dept_description)
        _add.save()
        return HttpResponse(f'{dept_title} added to the departments')

#FO ASSIGNEMNT OF HEADS/IN-CHARGES
#FOR ASSIGNMENT OF WORKERS
@csrf_exempt
def designate_oic(request):
    data = json.loads(request.body)
    worker = data["person"].lower()
    department = data["department"].lower()
    _worker = User.objects.get(username=worker)
    _department = Department.objects.get(title=department.lower())
    context = {}
    if _department.head != _worker:
        if _worker not in _department.users.all():
            _worker.designation.add(_department)
        else:
            pass

        _department.head = _worker
        _department.save()

        _worker.in_charge_of.add(_department)
        _worker.save()#TO TRIGGER BOOLEAN OBJ (is_in_charge)

        context["message"] = f'SUCCESSFULLY APPOINTED AS IN-CHARGE FOR {_department}'
        return JsonResponse(context)
    else:
        context["message"] = f'{_worker} Is Currently In-Charge of {_department.title.title()} Department'
        return JsonResponse(context)

    
@csrf_exempt    
def designate(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        worker = data['person'].lower()
        department = data['department'].lower()
        context = {}
   
        try:
            _worker = User.objects.get(username=worker)
            _department = Department.objects.get(title=department.lower())
            _worker.designation.add(_department)
            context['message'] = f'{worker} assigned in {department} department'
            return JsonResponse(context)
        
        except ObjectDoesNotExist:
            context['message'] = f'{worker} or {department} does not exist in database'
            return JsonResponse(context)


def undesignate(request):
    if request.method == 'POST':
        try:
            worker = request.POST['worker_undesignate']
            department = request.POST['department_undesignate']

            _worker = User.objects.get(username=worker)
            _department = Department.objects.get(title=department)
            _worker.designation.remove(_department)

        except ObjectDoesNotExist:
            return HttpResponse(f'{worker} or {department} does not exist in database')




