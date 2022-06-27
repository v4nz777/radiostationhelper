from turtle import clear
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, pre_save


#CLASSES
#CLASSES

class User(AbstractUser):
    position = models.ForeignKey('Position', on_delete=models.CASCADE, blank=True, null=True, related_name="pos")
    designation = models.ManyToManyField('Department', blank=True, related_name="departments_assigned")
    address = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    is_in_charge = models.BooleanField(default=False)
    in_charge_of = models.ManyToManyField('Department', blank=True, related_name="departments_headed")
    is_logged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # IF ALREADY CREATED
        if self.pk != None:
            if self.in_charge_of.all().count() >= 1:
                self.is_in_charge = True
                super(User, self).save(*args, **kwargs)
            else:
                self.is_in_charge = False
                super(User, self).save(*args, **kwargs)
        # FOR NEWLY REGISTERED
        else:
            super(User, self).save(*args, **kwargs)
        
          

class Department(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=300, blank=True)
    head = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="in_charge")
    users = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.title

class Position(models.Model):
    title = models.CharField(max_length=30, blank=False, unique=True)
    salary_1 = models.IntegerField(blank=True, null=True)
    salary_2 = models.IntegerField(blank=True, null=True)
    salary_3 = models.IntegerField(blank=True, null=True)
    salary_4 = models.IntegerField(blank=True, null=True)
    salary_5 = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.title



#END CLASSES
#END CLASSES




#IF DEPARTMENT IS DESIGNATED TO USER, ADD USER TO THE DEPARTMENT
#IF DEPARTMENT IS UNDESIGNATED TO USER, REMOVE USER TO THE DEPARTMENT
@receiver(m2m_changed, sender=User.designation.through)
def department_designate(sender, instance, action, **kwargs):
    if action == 'post_add':
        _department = instance.designation.all()
        for i in _department:
            i.users.add(instance)

    if action == 'pre_remove':
        _department = instance.designation.all()
        for i in _department:
            i.users.remove(instance)

   





    
