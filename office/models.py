from django.db import models
from django.dispatch import receiver

# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)
    code = models.CharField(max_length=50, unique=True, blank=False)
    bo_number = models.CharField(max_length=50, unique=False, blank=True)
    amount = models.FloatField(blank=False)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)
    customer_address = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey('Adcategory', on_delete=models.SET_NULL, blank=True, null=True)
    running = models.BooleanField(default=True)
    account_executive = models.ForeignKey('mainapp.User', on_delete=models.SET_NULL, blank=True, null=True)

    broadcast_start = models.DateField(null=True, blank=True)
    broadcast_end = models.DateField(null=True, blank=True)

    spots_per_day = models.IntegerField(blank=False)
    material_duration = models.IntegerField(blank=False)
    sponsorship_taglines = models.IntegerField(blank=False)

    remarks = models.TextField(max_length=500, blank=True)
    specific_time_schedule = models.TextField(max_length=500, blank=True)

    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    company = models.CharField(max_length=50, blank=False, unique=True)
    address = models.CharField(max_length=100, blank=True)
    ads = models.ManyToManyField(Ad, blank=True, related_name="ads_owned")
    owner = models.CharField(max_length=50, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company


class Adcategory(models.Model):
    title = models.CharField(max_length=50, unique=True)
    ads = models.ManyToManyField(Ad, blank=True, related_name="ads_under")

    def __str__(self):
        return self.title



class Invoice(models.Model):
    advertiser = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    from_contract = models.CharField(max_length=100, blank=False)
    account_executive = models.ForeignKey('mainapp.User', on_delete=models.SET_NULL, null=True)
    for_ads = models.ManyToManyField(Ad, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_no = models.IntegerField(blank=False)
    
    paid = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    received = models.FloatField(blank=True, null=True)

    or_date = models.DateField(null=True, blank=True)
    or_number = models.IntegerField(blank=True, null=True)
    applicable_month_from = models.DateField(null=True, blank=True)
    applicable_month_to = models.DateField(null=True, blank=True)
    excel_file = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.invoice_date}|{self.from_contract}'


class InvoiceTransmittal(models.Model):
    month = models.CharField(max_length=100, blank=False)
    year = models.CharField(max_length=5, blank=False)
    invoices = models.ManyToManyField(Invoice, blank=True)

    def __str__(self):
        return self.month
