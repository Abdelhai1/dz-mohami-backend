from django.db import models

# models

class User(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
    email = models.CharField(max_length=30,null=False,blank=False)
    activated = models.BooleanField(null=True)
    def __str__(self):
        return f"{self.email}"
    
class Lawyer(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
    name = models.CharField(max_length=30,null=False,blank=False)
    fname = models.CharField(max_length=30,null=False,blank=False)
    email = models.CharField(max_length=30,null=False,blank=False,unique=True)
    password = models.CharField(max_length=12,null=False,blank=False)
    address = models.CharField(max_length=60,null=True,blank=False)
    phone = models.CharField(max_length=30,null=True,blank=False)
    description = models.CharField(max_length=30,null=True,blank=False)
    avocat_image = models.CharField(max_length=500,null=True,blank=False)
    social = models.CharField(max_length=150,null=True,blank=False)
    wilaya = models.CharField(max_length=50,null=True,blank=False)
    rating = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    latitude = models.FloatField(null = True)
    experience_years = models.IntegerField(null = True)
    activated = models.BooleanField(null=True,default = False)


    def __str__(self):
        return f"{self.name}"

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rate = models.FloatField(default =0.5)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user_name}: {self.text}"



class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LawyerCategoryAssignment(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey (Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lawyer.name} - {self.category.name}"
    
class Schedule(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title

class LawyerSchedule(models.Model):
    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lawyer.name} - {self.schedule.title}"
    
class Appointment(models.Model):
    user = models.ForeignKey(User, null = True,on_delete=models.SET_NULL)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    date = models.CharField(max_length = 100)
    time = models.CharField(max_length = 100)
    details = models.TextField(max_length = 100)

    def __str__(self):
        return f"Appointment with {self.lawyer.name} {self.user} on {self.date} at {self.time}"
    def update_user_id(self, new_user_id):
        self.user_id = new_user_id
        self.save()
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete = models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return f"Reservation for {self.user} with {self.lawyer.name} on {self.appointment.date} at {self.appointment.time}"