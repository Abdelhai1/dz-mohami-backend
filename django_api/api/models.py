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
    activated = models.BooleanField(null=True)


    def __str__(self):
        return f"{self.name}"

class Comment(models.Model):
    text = models.TextField()
    user_name = models.CharField(max_length=255)
    rate = models.FloatField(default =0.5)
    def __str__(self):
        return f"{self.user_name}: {self.text}"

class LawyerComment(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lawyer.name} - {self.comment.user_name}'s comment"

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