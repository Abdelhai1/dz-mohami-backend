from django.db import models

# models

class User(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
    name = models.CharField(max_length=30,null=False,blank=False)
    email = models.CharField(max_length=30,null=False,blank=False)
    password = models.CharField(max_length=12,null=False,blank=False)
    address = models.CharField(max_length=60,null=False,blank=False)
    def __str__(self):
        return f"{self.name}"
    
class Lawyer(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    rating = models.IntegerField()
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    def __str__(self):
        return f"{self.user.name}- Lawyer"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    details = models.TextField()

    def __str__(self):
        return f"Appointment with {self.lawyer.user.name} {self.lawyer.user.name} on {self.date} at {self.time}"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    details = models.TextField()

    def __str__(self):
        return f"Reservation for {self.user.name} with {self.lawyer.user.name} on {self.date} at {self.time}"