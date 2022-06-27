from django.contrib import admin
from .models import Ad, Customer, Adcategory, Invoice, InvoiceTransmittal
# Register your models here.

admin.site.register(Ad)
admin.site.register(Customer)
admin.site.register(Adcategory)
admin.site.register(Invoice)
admin.site.register(InvoiceTransmittal)