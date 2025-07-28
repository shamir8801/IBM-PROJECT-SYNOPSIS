from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .sample import forecast_inventory

def fp(request):
    # from openpyxl import load_workbook
    #
    # # Load the workbook and select a worksheet
    # workbook = load_workbook(
    #     r"C:\Users\ShAmiR\OneDrive\Desktop\Patient.csv.xlsx")
    # sheet = workbook.active  # Or workbook['SheetName']
    #
    # # Access cell values
    # i = 0
    # for row in sheet.iter_rows(values_only=True):
    #     if i != 0:
    #         print(row)
    #         ob = Patients()
    #         ob.DOCTOR = Doctor.objects.order_by('?').first()
    #         ob.ROOM = Room.objects.order_by('?').first()
    #         ob.date = str(row[2]).split(' ')[0]
    #         ob.status = 'discharged'
    #         ob.ddate = str(row[-2]).split(' ')[0]
    #         ob.name = row[1]
    #         ob.number = row[5]
    #         ob.gender = 'Male'
    #         ob.dob = row[3]
    #         ob.address = row[4]
    #         ob.save()
    #     i = i + 1
    return render(request, 'fpfp.html')

def home(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        a = Login.objects.filter(username=username, password=password)
        if a.exists():
            a1 = Login.objects.get(username=username, password=password)
            request.session['lid'] = a1.id
            if a1.type == 'hospital':
                return HttpResponse('''<script>alert('hospital Login success'); window.location = '/hospital_home';</script>''')
            elif a1.type == 'incharge':
                obi=Incharge.objects.get(LOGIN__id=a1.id)
                request.session['lwid']=obi.WARD.id
                request.session['luid']=obi.id
                return HttpResponse('''<script>alert('Incharge Login success'); window.location = '/incharge_home';</script>''')
            elif a1.type == 'inventory_manager':
                return HttpResponse('''<script>alert('Inventory Login success'); window.location = '/inventory_manager_home';</script>''')
            elif a1.type == 'doctor':
                return HttpResponse('''<script>alert('Doctor Login success'); window.location = '/doc_home';</script>''')
            else:
                return HttpResponse('''<script>alert('Invalid'); window.location = '/login';</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid'); window.location = '/login';</script>''')
    return render(request, 'login.html')

from datetime import datetime
def hospital_home(request):
    ob=Inventory.objects.all()
    obw=Ward.objects.all()
    obp=Patients.objects.filter(status='Admitted')

    ilist = []
    dlist=[]

    for i in range(1, 13):
        y=datetime.now().strftime("%Y")
        m=datetime.now().strftime("%m")
        print(y,type(y),m,type(m),"year===================")
        if i>int(m):
            y=int(y)-1
        obin = InventoryRequest.objects.filter(
            date__year=str(y),
            date__month=i,status='accepted')
        listsum = 0
        for j in obin:
            listsum += j.quantity
        ilist.append(listsum)
        if i<10:
            dlist.append(datetime.now().strftime("%Y")+"-0"+str(i))
        else:
            dlist.append(datetime.now().strftime("%Y")+"-"+str(i))
    flist=forecast_inventory(dlist,ilist)
    wards = Ward.objects.all()
    ward_data = []

    for ward in wards:
        rooms = Room.objects.filter(WARD=ward)
        total_rooms = rooms.count()
        available_rooms = rooms.filter(status='available').count()
        occupied_rooms = total_rooms - available_rooms
        avp,nap=0,0
        if total_rooms>0:
            avp=round((available_rooms/total_rooms)*100,2)
            nap=round((occupied_rooms/total_rooms)*100,2)
        ward_data.append({
            'ward': ward,
            'total': total_rooms,
            'available': available_rooms,
            'occupied': occupied_rooms,
            'rooms': rooms,
            "avp":avp,
            "nap":nap,
        })
    print(ward_data)
    # return render(request, 'ward_availability.html', {'ward_data': ward_data})

    return render(request, 'hospital/index.html',{"inv":len(ob),"pa":len(obp),"wa":len(obw),"expl":flist,'ilist':ilist,'ward_data': ward_data})

def hospital_home1(request):
    ob=Inventory.objects.all()
    obw=Ward.objects.all()
    obp=Patients.objects.filter(status='Admitted')

    ilist = []
    dlist=[]

    for i in range(1, 13):
        obin = InventoryRequest.objects.filter(
            date__year=datetime.now().strftime("%Y"),
            date__month=i,status='accepted')
        listsum = 0
        for j in obin:
            listsum += j.quantity
        ilist.append(listsum)
        if i<10:
            dlist.append(datetime.now().strftime("%Y")+"-0"+str(i))
        else:
            dlist.append(datetime.now().strftime("%Y")+"-"+str(i))
    print(dlist,ilist)
    flist=forecast_inventory(dlist,ilist)

    oblist=Inventory.objects.all()
    result=[]
    for i in oblist:
        obin = InventoryRequest.objects.filter(status='accepted',PRODUCT__id=i.id)
        if len(obin)>0:
            tc=0
            for j in obin:
                tc+=j.quantity
            i.tp=tc
            result.append(i)

    return render(request, 'hospital/report.html',{"inv":len(ob),"pa":len(obp),"wa":len(obw),"expl":flist,'ilist':ilist,"res":result})





def get_dates_from(start_date_str, date_format="%Y-%m-%d"):
    from datetime import datetime, timedelta
    # Parse the input date string
    start_date = datetime.strptime(start_date_str, date_format).date()
    today = datetime.today().date()

    # Generate all dates from start_date to today
    delta = (today - start_date).days
    date_list = [str(start_date + timedelta(days=i)) for i in range(delta + 1)]

    return date_list
from django.db.models import Q
def hospital_home2(request):

    obp=Patients.objects.all().order_by("date")
    fd=obp[0].date
    dlist=get_dates_from(str(fd))

    plist=[]

    for i in dlist:
        obin = Patients.objects.filter( Q(date__lte=i,ddate__gte=i) | Q(status='Admitted'))

        plist.append(len(obin))

    print(dlist,plist)
    # flist=forecast_inventory(dlist,plist)
    # print("+++)))))))))))))((((((((((((((((((((")
    # print(flist)

    ob=Doctor.objects.all()
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print(plist)
    print(dlist)

    return render(request, 'hospital/report2.html',{"inv":len(ob),"pa":len(obp),"expl":dlist,'ilist':plist,"res":ob})

def ForecastProductdoc(request,id):

    obp=Patients.objects.filter(DOCTOR__id=id).order_by("date")
    fd=obp[0].date
    dlist=get_dates_from(str(fd))

    plist=[]

    for i in dlist:
        obin = Patients.objects.filter( Q(date__lte=i,ddate__gte=i,DOCTOR__id=id) | Q(status='Admitted',DOCTOR__id=id))

        plist.append(len(obin))

    print(dlist,plist)
    # flist=forecast_inventory(dlist,plist)
    # print("+++)))))))))))))((((((((((((((((((((")
    # print(flist)

    ob=Doctor.objects.filter(id=id)
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print(plist)
    print(dlist)
    fdet = get_inventory_combinations_for_doctor(id)
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++")
    print(fdet)
    res = []
    output = [(tuple(row.itemsets), row.support) for _, row in fdet.iterrows()]
    print("output", output)

    res = []
    print(len(output))
    pids=[]
    for i in range(0, len(output)):
        print(i)
        print(output[i])
        if output[i][0][0] not in pids:
            pids.append(output[i][0][0])
            obin = Inventory.objects.get(id=output[i][0][0])
            r = {"inv": obin.name, "img": obin.photo.url, "cat": obin.CATEGORY.name, "con": round(output[i][1] * 100, 2)}
            res.append(r)
    print(")))))))))))))))))))))))))))))))))")
    print(res)

    return render(request, 'hospital/report3.html',
                  {"inv": len(ob), "pa": len(obp), "expl": dlist, 'ilist': plist, "res": ob, "invd": res})


def ForecastProduct(request,id):
    ob=Inventory.objects.all()
    obw=Ward.objects.all()
    obp=Patients.objects.filter(status='Admitted')

    ilist = []
    dlist=[]

    for i in range(1, 13):
        y = datetime.now().strftime("%Y")
        m = datetime.now().strftime("%m")
        print(y, type(y), m, type(m), "year===================")
        if i > int(m):
            y = int(y) - 1
        obin = InventoryRequest.objects.filter(
            date__year=str(y),
            date__month=i,status='accepted',PRODUCT__id=id)
        listsum = 0
        for j in obin:
            listsum += j.quantity
        ilist.append(listsum)
        if i<10:
            dlist.append(datetime.now().strftime("%Y")+"-0"+str(i))
        else:
            dlist.append(datetime.now().strftime("%Y")+"-"+str(i))
    flist=forecast_inventory(dlist,ilist)

    oblist=Inventory.objects.all()
    result=[]
    for i in oblist:
        obin = InventoryRequest.objects.filter(status='accepted',PRODUCT__id=i.id)
        if len(obin)>0:
            tc=0
            for j in obin:
                tc+=j.quantity
            i.tp=tc
            result.append(i)

    return render(request, 'hospital/report.html',{"inv":len(ob),"pa":len(obp),"wa":len(obw),"expl":flist,'ilist':ilist,"res":result})

def ViewWards(request):
    wards = Ward.objects.all()
    return render(request, 'hospital/wards.html',{'wards':wards})

def AddNewWard(request):
    if request.method == 'POST':
        ward_number = request.POST['ward_number']
        capacity = request.POST['capacity']
        details = request.POST['details']
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)

        ward = Ward(
            ward_number=ward_number,
            capacity=capacity,
            details=details,
            photo=fp
        )
        ward.save()
        return HttpResponse('''<script>alert('Ward Added Successfully'); window.location = '/ViewWards';</script>''')
    return render(request, 'hospital/add_new_ward.html')

def edit_ward(request,id):
    ward = Ward.objects.get(id=id)
    if request.method == 'POST':
        ward.ward_number = request.POST['ward_number']
        ward.capacity = request.POST['capacity']
        ward.details = request.POST['details']
        if 'photo' in request.FILES:
            ward.photo = request.FILES['photo']
            ward.save()
        ward.save()
        return HttpResponse('''<script>alert('Ward Edited Successfully'); window.location = '/ViewWards';</script>''')
    return render(request, 'hospital/edit_ward.html',{'ward':ward})

def delete_ward(request,id):
    ward = Ward.objects.get(id=id)
    ward.delete()
    return HttpResponse('''<script>alert('Ward Deleted Successfully'); window.location = '/ViewWards';</script>''')


def ViewRooms(request,id):
    request.session['wid']=id
    rooms = Room.objects.filter(WARD__id=id)
    return render(request, 'hospital/view_rooms.html',{'rooms':rooms})

def add_new_room(request):
    if request.method == 'POST':
        room_number = request.POST['room_number']
        fn = request.FILES['fn']

        capacity = request.POST['capacity']

        room = Room(
            room_number=room_number,
            capacity=capacity,
            image=fn,
            price=request.POST['r'],
            details=request.POST['rd'],
            status='Available',
            WARD_id=request.session['wid']
        )
        room.save()
        return HttpResponse('''<script>alert('Room Added Successfully'); window.location = "/ViewRooms/'''+str(request.session['wid'])+'''";</script>''')
    ob=Ward.objects.all()
    return render(request, 'hospital/add_new_room.html',{"val":ob})

def edit_room(request,id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.room_number = request.POST['room_number']
        room.capacity = request.POST['capacity']
        room.save()
        return HttpResponse('''<script>alert('Room Edited Successfully'); window.location = '/ViewRooms';</script>''')
    return render(request, 'hospital/edit_room.html',{'room':room})


def delete_room(request,id):
    room = Room.objects.get(id=id)
    room.delete()
    return HttpResponse('''<script>alert('Room Deleted Successfully'); window.location = "/ViewRooms/'''+str(request.session['wid'])+'''";</script>''')

def view_incharge(request):
    incharge = Incharge.objects.all()
    return render(request, 'hospital/view_incharge.html',{'incharge':incharge})

def add_new_incharge(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        photo = request.FILES['photo']
        gender = request.POST['gender']
        dob = request.POST['dob']
        email = request.POST['email']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']
        ward = request.POST['ward']

        if Login.objects.filter(username=email).exists():
            return HttpResponse('''<script>alert('Email Already Exists'); window.location = '/view_incharge';</script>''')

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)


        log_details = Login(
            username=email,
            password=number,
            type='incharge'
        )
        log_details.save()

        profile = Incharge(
            LOGIN = log_details,
            name = name,
            number=number,
            gender=gender,
            dob=dob,
            place=place,
            post=post,
            pin=pin,
            email=email,
            WARD_id=ward,
            photo=fp
        )
        profile.save()
        return HttpResponse('''<script>alert('Incharge Added Successfully'); window.location = '/view_incharge';</script>''')
    ob=Ward.objects.all()
    return render(request, 'hospital/add_new_incharge.html',{"val":ob})

def edit_incharge(request,id):
    incharge = Incharge.objects.get(id=id)
    if request.method == 'POST':
        incharge.name = request.POST['name']
        incharge.number = request.POST['number']
        if 'photo' in request.FILES:
            incharge.photo = request.FILES['photo']
            incharge.save()
        incharge.gender = request.POST['gender']
        incharge.dob = request.POST['dob']
        incharge.email = request.POST['email']
        incharge.place = request.POST['place']
        incharge.post = request.POST['post']
        incharge.pin = request.POST['pin']
        incharge.save()
        return HttpResponse('''<script>alert('Incharge Edited Successfully'); window.location = '/view_incharge';</script>''')
    return render(request, 'hospital/edit_incharge.html',{'incharge':incharge})

def delete_incharge(request,id):
    incharge = Incharge.objects.get(id=id)
    incharge.delete()
    return HttpResponse('''<script>alert('Incharge Deleted Successfully'); window.location = '/view_incharge';</script>''')

def delete_doc(request,id):
    incharge = Doctor.objects.get(id=id)
    incharge.delete()
    return HttpResponse('''<script>alert('Doctor Deleted Successfully'); window.location = '/ViewDoctor';</script>''')


def ViewManager(request):
    managers = InventoryManager.objects.all()
    return render(request, 'hospital/view_managers.html',{'managers':managers})


def ViewDoctor(request):
    managers = Doctor.objects.all()
    return render(request, 'hospital/view_doc.html',{'doc':managers})

def add_new_manager(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        photo = request.FILES['photo']
        gender = request.POST['gender']
        dob = request.POST['dob']
        email = request.POST['email']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']

        if Login.objects.filter(username=email).exists():
            return HttpResponse('''<script>alert('Email Already Exists'); window.location = '/ViewManager';</script>''')

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)

        log = Login(username=email,password=number,type='inventory_manager')
        log.save()

        profile = InventoryManager(
            LOGIN=log,
            name=name,
            number=number,
            gender=gender,
            dob=dob,
            email=email,
            place=place,
            post=post,
            pin=pin,
            photo=fp
        )
        profile.save()
        return HttpResponse('''<script>alert('Manager Added Successfully'); window.location = '/ViewManager';</script>''')
    return render(request, 'hospital/add_new_manager.html')

def add_new_doc(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        photo = request.FILES['photo']
        gender = request.POST['gender']
        dob = request.POST['dob']
        email = request.POST['email']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']
        qua = request.POST['qu']
        dep = request.POST['dep']

        if Login.objects.filter(username=email).exists():
            return HttpResponse('''<script>alert('Email Already Exists'); window.location = '/ViewManager';</script>''')

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)

        log = Login(username=email,password=number,type='doctor')
        log.save()

        profile = Doctor(
            LOGIN=log,
            name=name,
            number=number,
            gender=gender,
            dob=dob,
            email=email,
            place=place,
            post=post,
            pin=pin,
            qualification=qua,
            department=dep,
            photo=fp
        )
        profile.save()
        return HttpResponse('''<script>alert('Manager Added Successfully'); window.location = '/ViewDoctor';</script>''')
    return render(request, 'hospital/add_new_doc.html')


def edit_manager(request,id):
    manager = InventoryManager.objects.get(id=id)
    if request.method == 'POST':
        manager.name = request.POST['name']
        manager.number  =request.POST['number']
        if 'photo' in request.FILES:
            manager.photo  =request.FILES['photo']
            manager.save()
        manager.gender  =request.POST['gender']
        manager.dob  =request.POST['dob']
        manager.email  =request.POST['email']
        manager.place  =request.POST['place']
        manager.post  =request.POST['post']
        manager.pin  =request.POST['pin']
        manager.save()
        return HttpResponse('''<script>alert('Manager Edited Successfully'); window.location = '/ViewManager';</script>''')
    return render(request, 'hospital/edit_manager.html',{'manager':manager})

def delete_manager(request,id):
    manager = InventoryManager.objects.get(id=id)
    manager.delete()
    return HttpResponse('''<script>alert('Manager Deleted Successfully'); window.location = '/ViewManager';</script>''')

#---------------------------------------------------HOSPITAL------------------------------------------------------------

def inventory_manager_home(request):
    # inventory = Inventory.objects.all()
    # return render(request, 'Inventory_Manager/view_inventory.html', {'inventory': inventory})

    return render(request, 'Inventory_Manager/inventory_manager_home.html')

def inventory_manager_view_inventory(request):
    inventory = Inventory.objects.all()
    return render(request, 'Inventory_Manager/view_inventory.html',{'inventory':inventory})

def view_category(request):
    category = InventoryCategory.objects.all()
    return render(request, 'Inventory_Manager/view_category.html',{'category':category})

def add_new_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        InventoryCategory.objects.create(name=name)
        return HttpResponse('''<script>alert('Category Added Successfully'); window.location = '/view_category';</script>''')
    return render(request, 'Inventory_Manager/add_new_category.html')

def edit_category(request,id):
    category = InventoryCategory.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return HttpResponse('''<script>alert('Category Edited Successfully'); window.location = '/view_category';</script>''')
    return render(request, 'Inventory_Manager/edit_category.html',{'category':category})

def delete_category(request,id):
    category = InventoryCategory.objects.get(id=id)
    category.delete()
    return HttpResponse('''<script>alert('Category Deleted Successfully'); window.location = '/view_category';</script>''')

def add_inventory(request):
    category = InventoryCategory.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        fp = fs.save(photo.name,photo)

        manager = InventoryManager.objects.get(LOGIN=request.session['lid'])
        cat = InventoryCategory.objects.get(id=request.POST['category'])
        Inventory.objects.create(
            ADDED_BY=manager,
            CATEGORY=cat,
            name=name,
            quantity=quantity,
            photo=fp
        )
        return HttpResponse('''<script>alert('Inventory Added Successfully'); window.location = '/inventory_manager_view_inventory';</script>''')
    return render(request, 'Inventory_Manager/add_inventory.html',{'category':category})

def edit_inventory(request,id):
    inventory = Inventory.objects.get(id=id)
    category = InventoryCategory.objects.all()
    if request.method == 'POST':
        inventory.CATEGORY_id = request.POST['category']
        inventory.name = request.POST['name']
        inventory.quantity = request.POST['quantity']
        if 'photo' in request.FILES:
            inventory.photo = request.POST['photo']
            inventory.save()
        inventory.save()
        return HttpResponse('''<script>alert('Inventory Edited Successfully'); window.location = '/inventory_manager_view_inventory';</script>''')
    return render(request, 'Inventory_Manager/edit_inventory.html',{'inventory':inventory,'category':category})

def delete_inventory(request,id):
    inventory = Inventory.objects.get(id=id)
    inventory.delete()
    return HttpResponse('''<script>alert('Inventory Deleted Successfully'); window.location = '/inventory_manager_view_inventory';</script>''')


def inventory_manager_view_inventory_request(request):
    inventory_request = InventoryRequest.objects.filter(PRODUCT__ADDED_BY__LOGIN=request.session['lid'],status='pending').order_by('-id')
    return render(request, 'Inventory_Manager/inventory_request.html',{'inventory_request':inventory_request})

def accept_request(request,id):
    inventory_request = InventoryRequest.objects.get(id=id)
    product = inventory_request.PRODUCT
    if product.quantity >= inventory_request.quantity:


        wob=inventory_request.SENDER.WARD.id
        obis=InventoryStock.objects.filter(WARD__id=wob,PRODUCT__id=inventory_request.PRODUCT.id)
        if len(obis)==0:
            obis=InventoryStock()
            obis.PRODUCT = Inventory.objects.get(id=inventory_request.PRODUCT.id)
            obis.WARD = Ward.objects.get(id=wob)

            obis.quantity =inventory_request.quantity
            obis.save()
        else:
            obis=obis[0]
            obis.quantity+=int(inventory_request.quantity)
            obis.save()
        inventory_request.status = 'accepted'
        product.quantity -= inventory_request.quantity
        product.save()
        inventory_request.save()
    return HttpResponse('''<script>alert('Request Accepted'); window.location = '/inventory_manager_view_inventory_request';</script>''')

def reject_request(request,id):
    inventory_request = InventoryRequest.objects.get(id=id)
    inventory_request.status = 'rejected'
    inventory_request.save()
    return HttpResponse('''<script>alert('Request Rejected'); window.location = '/inventory_manager_view_inventory_request';</script>''')


#----------------------------------------------------------Inventory Manager--------------------------------------------

def incharge_home(request):
    inventory = InventoryStock.objects.filter(WARD__id=request.session['lwid']).order_by("-id")
    print(inventory)

    return render(request, 'Incharge/home.html',{'inventory':inventory[:9]})

def view_rooms(request):


    rooms = Room.objects.filter(WARD__id=request.session['lwid'])
    return render(request, 'Incharge/view_rooms.html',{'rooms':rooms})

def view_Inventory(request):
    inventory = Inventory.objects.all()
    return render(request, 'Incharge/view_inventory.html',{'inventory':inventory})


def send_request(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        quantity = request.POST.get('quantity')

        inventory = Inventory.objects.get(id=inventory_id)
        sender_login = request.session['lid']
        sender = Incharge.objects.get(LOGIN=sender_login)

        InventoryRequest.objects.create(
            PRODUCT=inventory,
            SENDER=sender,
            quantity=quantity
        )
        return HttpResponse('''<script>alert('Request Sent Successfully'); window.location = '/view_request_status';</script>''')
    return redirect('/view_Inventory')

def send_request_inventry_user(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        quantity = request.POST.get('quantity')

        inventory = Inventory.objects.get(id=inventory_id)
        sender_login = request.session['lid']
        ob=InventoryAllocation()
        ob.PRODUCT = inventory
        ob.PATIENT = Patients.objects.get(id=request.session['pid'])
        ob.quantity = quantity
        ob.date=datetime.today()
        ob.save()


        obin=InventoryStock.objects.get(PRODUCT__id=inventory_id,WARD__id=request.session['lwid'])
        obin.quantity-=int(quantity)
        obin.save()

        return HttpResponse('''<script>alert('Request Sent Successfully'); window.location = '/InchargeViewPatientInventry';</script>''')


def view_request_status(request):
    status_list = InventoryRequest.objects.filter(SENDER__LOGIN=request.session['lid']).order_by("-id")
    paginator = Paginator(status_list, 6)  # Show 6 requests per page (3 cards per row, 2 rows)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Incharge/view_request_status.html', {'page_obj': page_obj})




def doc_home(request):

    ob=Patients.objects.filter(DOCTOR__LOGIN__id=request.session['lid'],status='Admitted')
    print(ob)
    return render(request, 'doctor/home.html',{"inventory":ob})



def homehistory(request):

    ob=Patients.objects.filter(DOCTOR__LOGIN__id=request.session['lid']).exclude(status='Admitted')
    return render(request, 'doctor/homehistory.html',{"inventory":ob})


# def ManagePatients(request):
#     k=Ward.objects.all()
#
#     return render(request, 'doctor/add_patient.html',{"ward":k})
#
#
#
#
# def get_rooms(request):
#     ward_id = request.GET.get('ward_id')
#     rooms = Room.objects.filter(ward_id=ward_id, status='Available')
#     data = {'rooms': [{'id': r.id, 'room_number': r.room_number, 'details': r.details} for r in rooms]}
#     return JsonResponse(data)



# def ManagePatients(request):
#     wards = Ward.objects.all()
#     return render(request, 'doctor/add_patient.html', {'ward': wards})
#
# def get_rooms(request):
#     ward_id = request.GET.get('ward_id')
#     rooms = Room.objects.filter(WARD__id=ward_id, status='Available')
#     print (rooms,"jjjjjjjjjjjjjjjjjjjjjj")
#     data = {'rooms': [{'id': r.id, 'room_number': r.room_number, 'details': r.details} for r in rooms]}
#     return JsonResponse(data)


#
#
# def ManagePatients(request):
#     wards = Ward.objects.all()
#     return render(request, 'doctor/add_patient.html', {'ward': wards})
# #
# # def get_rooms(request):
# #     ward_id = request.GET.get('ward_id')
# #     rooms = Room.objects.filter(WARD__id=ward_id, status='Available')
# #     data = {
# #         'rooms': [
# #             {'id': r.id, 'room_number': r.room_number, 'details': r.details}
# #             for r in rooms
# #         ]
# #     }
# #     return JsonResponse(data)
#
# from django.http import JsonResponse
# from django.http import JsonResponse
# from .models import Room
#
# def get_rooms(request):
#     ward_id = request.GET.get('ward_id')
#     rooms = Room.objects.filter(WARD__id=ward_id, status='Available')
#     data = {
#         'rooms': [
#             {
#                 'id': room.id,
#                 'room_number': room.room_number,
#                 'details': room.details
#             } for room in rooms
#         ]
#     }
#     print(data)
#     return JsonResponse(data)
from django.shortcuts import render
from django.http import JsonResponse
from .models import Ward, Room

def ManagePatients(request):
    wards = Ward.objects.all()

    if request.method == 'POST':
        obr = Room.objects.get(id=request.POST['room'])
        obr.status = 'Na'
        obr.save()
        manager = Patients()
        manager.DOCTOR = Doctor.objects.get(LOGIN__id=request.session['lid'])
        manager.ROOM = Room.objects.get(id=request.POST['room'])

        manager.name = request.POST['name']
        manager.number = request.POST['mob']
        manager.gender = request.POST['gen']
        manager.dob = request.POST['dob']
        manager.address = request.POST['address']
        manager.save()
        return HttpResponse(
            '''<script>alert('Success'); window.location = '/doc_home';</script>''')

    return render(request, 'doctor/add_patient.html', {'wards': wards})

def get_rooms(request):
    ward_id = request.GET.get('ward_id')
    rooms = Room.objects.filter(WARD__id=ward_id, status='Available')
    data = {
        'rooms': [
            {
                'id': room.id,
                'room_number': room.room_number,
                'details': room.details
            } for room in rooms
        ]
    }
    print (data,'ddddddddddddd')
    return JsonResponse(data)





def ViewPatientsDetails(request,id):
    request.session['pid']=id
    pd=PatientsDetails.objects.filter(PATIENT__id=id)

    return render(request, 'doctor/view_patient.html',{"pd":pd})
def InchargeViewPatient(request,id):

    request.session['rid']=id
    obpd=Patients.objects.get(ROOM__id=id,status='Admitted')
    request.session['pid'] = obpd.id

    pd=PatientsDetails.objects.filter(PATIENT__id=obpd.id)

    return render(request, 'Incharge/view_patient.html',{"pd":pd,"pob":obpd})

def InchargeViewPatientInventry(request):

    id=request.session['pid']

    pd=InventoryAllocation.objects.filter(PATIENT__id=id).order_by("-date")

    return render(request, 'Incharge/view_patientinventry.html',{"pd":pd})

def allocate_inventry_new(request):

    id=request.session['pid']

    pd= InventoryStock.objects.filter(WARD__id=request.session['lwid'])

    return render(request, 'Incharge/view_inventory1.html',{"pd":pd})



def ViewPatientsDetails1(request,id):
    request.session['pid']=id
    pd=PatientsDetails.objects.filter(PATIENT__id=id)

    return render(request, 'doctor/view_patient1.html',{"pd":pd})




def dischargePatients(request,id):
    request.session['pid']=id
    pd=Patients.objects.get(id=id)
    obr=Room.objects.get(id=pd.ROOM.id)
    obr.status='Available'
    obr.save()
    pd.status='discharged'
    pd.ddate=datetime.today()
    pd.save()

    return HttpResponse(
        '''<script>alert('Success'); window.location = '/doc_home';</script>''')


def addpatientdetails(request):
    id=request.session['pid']
    if request.method == 'POST':

        manager=PatientsDetails()
        manager.PATIENT = Patients.objects.get(id=id)

        manager.pstatus = request.POST['s']
        manager.medicines = request.POST['med']
        manager.plan = request.POST['plan']
        manager.status = 'pending'

        manager.save()
        return HttpResponse(
            '''<script>alert('Success'); window.location = "/ViewPatientsDetails/'''+str(id)+'''";</script>''')

    return render(request, 'doctor/add_patient_details.html')


from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

from collections import defaultdict
import pandas as pd
def get_inventory_combinations_for_doctor(doctor_id, min_support=0.2):
    # Get all patients under the doctor
    patients = Patients.objects.filter(DOCTOR_id=doctor_id)
    patient_ids = patients.values_list('id', flat=True)

    # Fetch inventory allocations for those patients
    allocations = InventoryAllocation.objects.filter(PATIENT_id__in=patient_ids).select_related('PRODUCT')

    # Build transactions: one transaction per patient (a set of inventory item names)
    patient_inventory_map = defaultdict(set)
    for alloc in allocations:
        patient_inventory_map[alloc.PATIENT_id].add(str(alloc.PRODUCT.id))

    transactions = list(patient_inventory_map.values())

    if not transactions:
        return pd.DataFrame()  # return empty DataFrame if no data

    # Encode the transactions for the Apriori algorithm
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_array, columns=te.columns_)

    # Run the Apriori algorithm with min_support
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    print(frequent_itemsets,"==========================")

    # Filter only combinations with at least 2 inventory items
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    result = frequent_itemsets[frequent_itemsets['length'] >= 1].sort_values(by='support', ascending=False)

    return result[['itemsets', 'support']]








