from multiprocessing import context
import re
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from .models import Ad, Customer, Adcategory
from mainapp.models import Position, User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Ad, Customer, Invoice
from .helper import create_invoice, collection_append
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.conf import settings

import qrcode


@csrf_exempt
def new_ads(request):
    print(request)
    if request.method == "POST":
        
        data = json.loads(request.body)   

        _amount = data['amount'] 
        amount = float(re.sub('[\D_]+', '', _amount))#To Remove any Symbols in Number

        title = data['title']
        code = data['code']
        
        customer = data['customer']
        customer_address = data['customer_address']
        category = data['category']
        
        
        broadcast_start = data['broadcast_start']
        broadcast_end = data['broadcast_end']
        spots_per_day = int(data['spots_per_day'])
        material_duration = int(data['material_duration'])
        sponsorship_taglines = int(data['sponsorship_taglines'])
        specific_time_schedule = data['specific_time_schedule']
        remarks = data['remarks']

        #set AE
        
        if data['account_executive'] == "":
            account_executive = None
        else:
            account_executive = User.objects.get(username=data['account_executive'])


        running = True
        valid_customer = None
        valid_category = None

        #VALIDATE CUSTOMER
        try:
            valid_customer = Customer.objects.get(company=customer.lower())

        except ObjectDoesNotExist:
            
            Customer.objects.create(company=customer.lower(), address=customer_address)

            valid_customer = Customer.objects.get(company=customer.lower())

        
        #VALIDATE CATEGORY
        try:
            valid_category = Adcategory.objects.get(title=category.lower())

        except ObjectDoesNotExist:
            Adcategory.objects.create(title=category.lower())
            valid_category = Adcategory.objects.get(title=category.lower())

        #THEN CREATE AD INSTANCE:
        try:
            Ad.objects.create(title = title,
                                code = code,
                                amount = amount,
                                customer = valid_customer,
                                customer_address = customer_address,
                                category = valid_category,
                                running = running,
                                account_executive = account_executive,
                                broadcast_start = datetime.strptime(broadcast_start, "%Y-%m-%d"),
                                broadcast_end = datetime.strptime(broadcast_end, "%Y-%m-%d"),
                                spots_per_day = spots_per_day,
                                material_duration = material_duration,
                                sponsorship_taglines = sponsorship_taglines,
                                specific_time_schedule = specific_time_schedule,
                                remarks = remarks)
            print('SUCCESS: New Contract Created!')
        except IntegrityError:
            print('FAILED: Something wrong with either title or the code -- check if it already existed!')
            return JsonResponse({'message': 'Something wrong with either title or the code -- check if it already existed!'})

        
        valid_customer.address = customer_address
        valid_customer.save()
        valid_customer.ads.add(Ad.objects.get(code=code))
        valid_customer.save()
        valid_category.ads.add(Ad.objects.get(code=code))
        valid_category.save()

        img = qrcode.make(f'https://{settings.LOCAL_IP}/contract/{code}')
        qrcode.image.pil.PilImage
        img.save(f"office/static/contracts/qr/{code}.png")
        

        return JsonResponse({'message': 'SUCCESS'})


@csrf_exempt
def new_invoice(request):
    data =json.loads(request.body)
    print(data)
    if request.method == "POST":
        
        contract = data["contract"]
        invoice_no = data["invoice_no"]
        invoice_from = data["from"]
        invoice_till = data["till"]

        
        try:#CHECK IF INVOICE IS ALRAEDY THERE
            Invoice.objects.get(invoice_no=invoice_no)
            print(f'invoice:{invoice_no} already exist')
            return JsonResponse({'message': f'invoice:{invoice_no} already exist'})

        except ObjectDoesNotExist:#IF NOT FOUND, CONTINUE!

            try:#CONTINUE
                create_invoice(contract, invoice_no, invoice_from, invoice_till)
                print('SUCCESS')
                return JsonResponse({'message': 'SUCCESS'})

            except ObjectDoesNotExist:#IF CONTRACT NOW FOUND, RETURN
                print(f'contract:{contract} dont exist')
                return JsonResponse({'message': f'contract:{contract} dont exist'})


def populate_new_payment(request, invoice_no):
    if request.method == "GET":
        context = {}
        
        try:
            contract_no = Invoice.objects.get(invoice_no=invoice_no).from_contract
            ad = Ad.objects.get(code=contract_no)
            context["advertiser"] = ad.customer.company.title()
            context["ad_amount"] = ad.amount
            context["valid"] = True

            return JsonResponse(context)
        except ObjectDoesNotExist:
            context["advertiser"] = 'NOT FOUND'
            context["ad_amount"] = 'None'
            context["valid"] = False
            return JsonResponse(context)





@csrf_exempt
def input_payment(request):
    data = json.loads(request.body)

    if request.method == "PUT":

        invoice_no = data["invoice"]
        _or_date = data["or_date"]
        _invoice = Invoice.objects.get(invoice_no=invoice_no)
        advertiser = _invoice.advertiser.company.title()

        if not _invoice.paid:
            or_date = datetime.strptime(_or_date, "%Y-%m-%d")
            or_number = data["or_num"]
            
            _ad = Ad.objects.get(code=_invoice.from_contract)
            
            _invoice.or_date = or_date
            _invoice.or_number = or_number
            _invoice.paid = True
            _invoice.received = float(_ad.amount)
            _invoice.save()

            _ad.running = True
            _ad.save()

            collection_append(invoice_no)

            return JsonResponse({'message': ' Success', 'succeed':True, 'advertiser': advertiser})
        
        else:
            date = naturalday(_invoice.or_date)
            return JsonResponse({'message': f' Already Paid {date.title()} with OR: {_invoice.or_number}', 'succeed':False, 'advertiser': advertiser})

@csrf_exempt
def populate_collections(request):
    if request.method == "POST":
        data = json.loads(request.body)
        _data = datetime.strptime(data["month_year"], "%Y-%m")

        month = _data.strftime('%m')
        year = _data.strftime('%Y')
        context = {}
        filtered_invoices = []
        for i in Invoice.objects.filter(invoice_date__month = month, invoice_date__year=year):
            _from = i.applicable_month_from.strftime('%b %d %Y')
            _to = i.applicable_month_to.strftime('%b %d %Y')
            filtered_invoices.append({'invoice_no': i.invoice_no,
                                        'advertiser': i.advertiser.company.title(),
                                        'paid': i.paid,
                                        'amount': i.received,
                                        'invoice_date': i.invoice_date.strftime('%B %d, %Y'),
                                        'particular': f'{_from} to {_to}',
                                        })
        context["filtered_invoices"] = filtered_invoices
        return JsonResponse(context)

@csrf_exempt
def new_position(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            title = data["title"].lower()
            level1_salary = data["level1_salary"]
            level2_salary = data["level2_salary"]
            level3_salary = data["level3_salary"]
            level4_salary = data["level4_salary"]
            level5_salary = data["level5_salary"]

            Position.objects.create(
                title=title,
                salary_1=level1_salary,
                salary_2=level2_salary,
                salary_3=level3_salary,
                salary_4=level4_salary,
                salary_5=level5_salary
            )

            return JsonResponse({'message': 'SUCCESS', 'success': True})
        except IntegrityError:
            return JsonResponse({'message': 'Already exists', 'success': False})

def edit_position(request, position):
    _position = Position.objects.get(pk=int(position))
    context = {}

    context["title"] = _position.title
    context["salary1"] = _position.salary_1
    context["salary2"] = _position.salary_2
    context["salary3"] = _position.salary_3
    context["salary4"] = _position.salary_4
    context["salary5"] = _position.salary_5

    return JsonResponse(context)

@csrf_exempt
def save_position(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        _position = Position.objects.get(pk=int(data["position_id"]))
        salary1 = data["salary1"]
        salary2 = data["salary2"]
        salary3 = data["salary3"]
        salary4 = data["salary4"]
        salary5 = data["salary5"]


        _position.salary_1 = salary1
        _position.salary_2 = salary2
        _position.salary_3 = salary3
        _position.salary_4 = salary4
        _position.salary_5 = salary5

        _position.save()

        context = {}

        context["position_title"] = _position.title.title()
        context["pk"] = _position.pk
        context["salary1"] = salary1
        context["salary2"] = salary2
        context["salary3"] = salary3
        context["salary4"] = salary4
        context["salary5"] = salary5

        return JsonResponse(context)
#
def contractapi(request, code):
    if request.method == "GET":
        contract_object = Ad.objects.get(code=code)
        context = {}

        context["title"] = contract_object.title.title()
        context["amount"] = contract_object.amount
        context["customer"] = contract_object.customer.company.title()
        context["customer_address"] = contract_object.customer_address
        context["category"] = contract_object.category.title
        context["running"] = contract_object.running
        context["account_executive"] = f"{contract_object.account_executive.first_name.title()} {contract_object.account_executive.last_name.title()}"
        context["broadcast_start"] = contract_object.broadcast_start.strftime('%b %d %Y')
        context["broadcast_end"] = contract_object.broadcast_end.strftime('%b %d %Y')
        context["spots_per_day"] = contract_object.spots_per_day
        context["material_duration"] = contract_object.material_duration
        context["sponsorship_taglines"] = contract_object.sponsorship_taglines
        context["remarks"] = contract_object.remarks
        context["specific_time_schedule"] = [contract_object.specific_time_schedule.split(",")]
        context["added"] = contract_object.broadcast_end.strftime('%b %d %Y')
        print(context)
        return JsonResponse(context)

def contract(request, code):
    if request.method == "GET":
        context = {}
        context["contract_object"] = Ad.objects.get(code=code)
        context["specific_time_schedule"] = [x for x in Ad.objects.get(code=code).specific_time_schedule.split(",") if x]
        
        context["logged"] = request.user.is_logged
        try:
            context["invoices"] = [y for y in Invoice.objects.filter(from_contract=code)]
            context["unpaid_invoice"] = len(Invoice.objects.filter(from_contract=code, paid=False))
        except ObjectDoesNotExist:
            context["invoices"] = []
        return render(request, 'office/solo/contract.html', context)

     
     
    
    
    
    
    
    
    
    
    
    
    
