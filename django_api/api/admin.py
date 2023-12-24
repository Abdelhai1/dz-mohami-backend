from django.contrib import admin
from .models import User
from .models import Lawyer
from .models import Appointment
# Register your models here.

admin.site.register(User)


admin.site.register(Lawyer)

admin.site.register(Appointment)