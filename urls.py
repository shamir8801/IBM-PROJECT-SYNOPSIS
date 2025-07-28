from django.urls import path
from MyApp import views

urlpatterns = [
    path('',views.fp,name='fp'),
    path('home',views.home,name='home'),
    path('login',views.login,name='login'),
    path('hospital_home',views.hospital_home,name='hospital_home'),
    path('hospital_home1',views.hospital_home1,name='hospital_home1'),
    path('hospital_home2',views.hospital_home2,name='hospital_home2'),
    path('ViewWards',views.ViewWards,name='ViewWards'),
    path('AddNewWard',views.AddNewWard,name='AddNewWard'),
    path('edit_ward/<id>',views.edit_ward,name='edit_ward'),
    path('ForecastProduct/<id>',views.ForecastProduct,name='ForecastProduct'),
    path('delete_ward/<id>',views.delete_ward,name='delete_ward'),

    path('ViewRooms/<id>',views.ViewRooms,name='ViewRooms'),
    path('add_new_room',views.add_new_room,name='add_new_room'),
    path('edit_room/<id>',views.edit_room,name='edit_room'),
    path('delete_room/<id>',views.delete_room,name='delete_room'),

    path('view_incharge', views.view_incharge, name='view_incharge'),
    path('add_new_incharge', views.add_new_incharge, name='add_new_incharge'),
    path('edit_incharge/<id>', views.edit_incharge, name='edit_incharge'),
    path('delete_incharge/<id>', views.delete_incharge, name='delete_incharge'),

    path('ViewManager',views.ViewManager,name='ViewManager'),
    path('add_new_manager',views.add_new_manager,name='add_new_manager'),
    path('edit_manager/<id>',views.edit_manager,name='edit_manager'),
    path('delete_manager/<id>',views.delete_manager,name='delete_manager'),
    path('ForecastProductdoc/<id>',views.ForecastProductdoc,name='ForecastProductdoc'),

    path('ViewDoctor',views.ViewDoctor,name='ViewDoctor'),
    path('add_new_doc',views.add_new_doc,name='add_new_doc'),
    path('delete_doc/<id>',views.delete_doc,name='delete_doc'),
    path('InchargeViewPatientInventry',views.InchargeViewPatientInventry,name='InchargeViewPatientInventry'),
    path('allocate_inventry_new',views.allocate_inventry_new,name='allocate_inventry_new'),
    path('send_request_inventry_user',views.send_request_inventry_user,name='send_request_inventry_user'),
    path('get_rooms',views.get_rooms,name='get_rooms'),
#------------------------------------------------------HOSPITAL---------------------------------------------------------

    path('inventory_manager_home',views.inventory_manager_home,name='inventory_manager_home'),
    path('inventory_manager_view_inventory',views.inventory_manager_view_inventory,name='inventory_manager_view_inventory'),
    path('add_inventory',views.add_inventory,name='add_inventory'),
    path('edit_inventory/<id>',views.edit_inventory,name='edit_inventory'),
    path('delete_inventory/<id>',views.delete_inventory,name='delete_inventory'),
    path('inventory_manager_view_inventory_request', views.inventory_manager_view_inventory_request,name='inventory_manager_view_inventory_request'),

    path('view_category',views.view_category,name='view_category'),
    path('add_new_category',views.add_new_category,name='add_new_category'),
    path('edit_category/<id>',views.edit_category,name='edit_category'),
    path('delete_category/<id>',views.delete_category,name='delete_category'),

    path('accept_request/<id>',views.accept_request,name='accept_request'),
    path('reject_request/<id>',views.reject_request,name='reject_request'),
    path('InchargeViewPatient/<id>',views.InchargeViewPatient,name='InchargeViewPatient'),

#--------------------------------------------------------Inventory Manager----------------------------------------------

    path('incharge_home', views.incharge_home, name='incharge_home'),
    path('view_rooms', views.view_rooms, name='view_rooms'),
    path('view_Inventory', views.view_Inventory, name='view_Inventory'),
    path('send_request', views.send_request, name='send_request'),
    path('view_request_status', views.view_request_status, name='view_request_status'),


    # ======================================================================DOCTOR====================
    path('doc_home', views.doc_home, name='doc_home'),
    path('ManagePatients', views.ManagePatients, name='ManagePatients'),
    path('addpatientdetails', views.addpatientdetails, name='addpatientdetails'),
    path('homehistory', views.homehistory, name='homehistory'),
    path('ViewPatientsDetails/<id>', views.ViewPatientsDetails, name='ViewPatientsDetails'),
    path('ViewPatientsDetails1/<id>', views.ViewPatientsDetails1, name='ViewPatientsDetails1'),
    path('dischargePatients/<id>', views.dischargePatients, name='dischargePatients'),
    path('get_rooms/', views.get_rooms, name='get_rooms'),









]