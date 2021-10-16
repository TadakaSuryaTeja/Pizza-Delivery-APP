from django.contrib import admin
from django.urls import path
from .views import adminloginview, adminhomepageview, \
    authenticateadmin, logoutadmin, addpizza, deletepizza, \
    homepageview, signupuser, userloginview, customerwelcomeview, \
    userauthenticate, userlogout, placeorder, userorders, adminorder,\
    acceptorder, declineorder

urlpatterns = [
    path('', homepageview, name='homepage'),
    path('admin/', adminloginview, name='adminloginpage'),
    path('adminauthenticate/', authenticateadmin),
    path('admin/homepage/', adminhomepageview, name='adminhomepage'),
    path('adminlogout/', logoutadmin),
    path('addpizza/', addpizza),
    path('deletepizza/<int:pizzapk>/', deletepizza),
    path('signupuser/', signupuser),
    path('loginuser/', userloginview, name='userloginpage'),
    path('customer/welcome/', customerwelcomeview, name='customerpage'),
    path('customer/authentication/', userauthenticate),
    path('userlogout/', userlogout),
    path('placeorder/', placeorder),
    path('userorders/', userorders),
    path('adminorders/', adminorder),
    path('acceptorder/<int:orderpk>/', acceptorder),
    path('declineorder/<int:orderpk>/', declineorder)
]
