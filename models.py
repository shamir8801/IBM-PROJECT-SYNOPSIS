from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=30)

class Ward(models.Model):
    ward_number = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    details = models.CharField(max_length=500)

    photo = models.FileField()

class Hospital(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=40)
    place = models.CharField(max_length=40)
    post = models.CharField(max_length=40)
    pin = models.PositiveIntegerField()
    photo = models.FileField()

class Incharge(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    WARD = models.ForeignKey(Ward, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number = models.PositiveBigIntegerField()
    photo = models.FileField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    email = models.EmailField(max_length=50)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()

class InventoryManager(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number = models.PositiveBigIntegerField()
    photo = models.FileField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    email = models.EmailField(max_length=50)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()

class Doctor(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number = models.PositiveBigIntegerField()
    photo = models.FileField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    email = models.EmailField(max_length=50)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()

class InventoryCategory(models.Model):
    name = models.CharField(max_length=40)

class Inventory(models.Model):
    ADDED_BY = models.ForeignKey(InventoryManager, on_delete=models.CASCADE)
    CATEGORY = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    photo = models.FileField(null=True,blank=True)


class Room(models.Model):
    WARD=models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    details = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    image = models.FileField()

class InventoryRequest(models.Model):
    PRODUCT = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    SENDER = models.ForeignKey(Incharge,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30,default='pending')

class InventoryStock(models.Model):
    PRODUCT = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    WARD = models.ForeignKey(Ward,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()




class Patients(models.Model):
    DOCTOR = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    ROOM = models.ForeignKey(Room, on_delete=models.CASCADE)
    # date = models.DateField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30,default='Admitted')
    ddate=models.DateField(auto_now_add=True)
    # ddate=models.DateField()
    name = models.CharField(max_length=50)
    number = models.PositiveBigIntegerField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.TextField()

class InventoryAllocation(models.Model):
    PRODUCT = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    PATIENT = models.ForeignKey(Patients,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    date=models.DateField()

class PatientsDetails(models.Model):
    PATIENT = models.ForeignKey(Patients, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    pstatus = models.TextField()
    plan=models.TextField()
    medicines=models.TextField()
    status=models.CharField(max_length=20)



