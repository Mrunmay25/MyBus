from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from bus.models import Bus ,Book
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def home(request):
   return render(request,'base.html')

def user_login(request):
    data = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admins")
        else:
            return redirect("/mybus")


    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == "" or password == "":
            data['error_msg'] = "Fields can't be empty"
            return render(request, 'user/login.html', context=data)
        elif not User.objects.filter(username=username).exists():
            data['error_msg'] = f"{username} user does not exist"
            return render(request, 'user/login.html', context=data)
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                data['error_msg'] = "Wrong password"
            else:
                login(request, user)
                if user.is_superuser:
                    return redirect("/admins")
                else:
                    return redirect("/mybus")
    
    return render(request, 'user/login.html', context=data)

def user_register(request):
   data={}

   if request.method=="POST":
      username=request.POST['username']
      email=request.POST['email']
      password=request.POST['password']
      password2=request.POST['password2']
     
      if (username=="" or password=="" or password2==""):
         data['error_msg']="Fields cant be empty"
         return render(request,'user/register.html',context=data)
      elif(password!=password2):
         data['error_msg']="Password Does not matched"
         return render(request,'user/register.html',context=data)
      elif(User.objects.filter(username=username).exists()):
         data['error_msg']=username + " already exist"
         return render(request,'user/register.html',context=data)
      else:
         user=User.objects.create(username=username,email=email)
         user.set_password(password)
         user.save()
         return redirect("/login")
   return render(request,'user/register.html',context=data)


def user_logout(request):
   logout(request)
   return redirect('/mybus')

def admin_panel(request):
   if request.user.is_authenticated:
      if not request.user.is_superuser:
         return redirect("/mybus")

   return render(request,'admin/admin.html')

# from user.models import Cart_Table,User_info,Pets
# from products.models import Order_history,Payment_history
# from appointments.models import User_App
# from sib_api_v3_sdk import Configuration, ApiClient
# from sib_api_v3_sdk.api.smtp_api import SMTPApi
# from sib_api_v3_sdk.models.send_smtp_email import SendSmtpEmail
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import random
import logging


otp = None

logger = logging.getLogger(__name__)

def forgot_password(request):
    if request.method == "POST":
        uname = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=uname, email=email).exists():
            user = User.objects.get(username=uname, email=email)
            global otp
            otp = random.randint(1111, 9999)
            try:
                send_mail(
                    "OTP for Password Change - MyBus",
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                logger.info("Email sent successfully to %s", user.email)
            except Exception as e:
                logger.error("Error sending email: %s", e)
                return render(request, "user/forgotpassword.html", {"error": "Error sending email. Please try again."})
            return redirect(f"/forgotpassword/update/{user.username}")
        else:
            return render(request, "user/forgotpassword.html", {"error": "Invalid username or email"})
    return render(request, "user/forgotpassword.html")


def passotp(request, uname):
    user = User.objects.get(username=uname)
    data = {}
    if request.method == "POST":
        uotp = int(request.POST['otp'])
        password = request.POST['password']
        confpass = request.POST['confpass']
        global otp
        if uotp != otp:
            data['error'] = "OTP does not match"
        elif password != confpass:
            data['error'] = "Passwords do not match"
        elif uotp == otp and password == confpass:
            user.set_password(password)
            user.save()
            otp = None
            return redirect("/login")
    return render(request, "user/changepass.html", context=data)


# def find(request):   
#    data={}
#    if request.method=="POST":
#       source_r=request.POST.get('source')
#       destination_r=request.POST.get('destination')
#       date_r=request.POST.get('date')
#       bus=Bus.objects.filter(source=source_r, destination=destination_r, date=date_r)
      
#       if (source_r=="" or destination_r=="" or date_r==""):
#          data['error_msg']="Fields cant be empty"
#          return render(request, 'home/find.html', context=data)
#       elif (bus.exists()):
#          data = {}
#          q1=Q(source=source_r)
#          q2=Q(destination=destination_r)
#          q3=Q(date=date_r)
#          buses = Bus.objects.filter(q1 & q2 & q3)  
#          data['buses'] = buses
#          return render(request, 'home/list.html',context=data)
#       else:
#          data["error_msg"] = "Sorry no bus availiable"
#          return render(request, 'home/find.html', context=data)
#    else:   
#       return render(request,'home/find.html')
#    return render(request,'home/find.html')

# def find(request):
#     data = {}
#     if request.method == "POST":
#         source_r = request.POST.get('source')
#         destination_r = request.POST.get('destination')
#         date_r = request.POST.get('date')
#         bus = Bus.objects.filter(source=source_r, destination=destination_r, date=date_r)
        
#         if source_r == "" or destination_r == "" or date_r == "":
#             data['error_msg'] = "Fields can't be empty"
#             return render(request, 'home/find.html', context=data)
#         elif bus.exists():
#             q1 = Q(source=source_r)
#             q2 = Q(destination=destination_r)
#             q3 = Q(date=date_r)
#             buses = Bus.objects.filter(q1 & q2 & q3)
#             data['buses'] = buses
#             return render(request, 'home/list.html', context=data)
#         else:
#             data["error_msg"] = "Sorry, no bus available"
#             return render(request, 'home/find.html', context=data)
#     else:
#         return render(request, 'home/find.html')
#     return render(request, 'home/find.html')


# def find(request):
#     if request.method == "POST":
#         source_r = request.POST.get('source')
#         destination_r = request.POST.get('destination')
        
#         if source_r == "" or destination_r == "" :
#             return render(request, 'home/find.html', {'error_msg': "Fields can't be empty"})
        
#         now = timezone.now()
        
#         bus = Bus.objects.filter(source=source_r, destination=destination_r, date__gte=now.date()).exclude(date=now.date(), time__lte=now.time())
        
#         if bus.exists():
#             return redirect('bus_list')
#         else:
#             return render(request, 'home/find.html', {'error_msg': "Sorry, no bus available"})
#     else:
#         return render(request, 'home/find.html')

def bus_list(request, source, destination):
    now = timezone.now()
    q1 = Q(source=source)
    q2 = Q(destination=destination)
    q3 = Q(date__gte=now.date())
    q4 = ~Q(date=now.date(), time__lte=now.time())
    buses = Bus.objects.filter(q1 & q2 & q3 & q4)
    
    return render(request, 'home/list.html', {'buses': buses})

from django.utils import timezone
def find(request): 
    data = {}
    if request.method == "POST":
        source_r = request.POST.get('source')
        destination_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        
        # Check if any of the fields are empty
        if source_r == "" or destination_r == "" or date_r == "":
            data['error_msg'] = "Fields can't be empty"
            return render(request, 'home/find.html', context=data)
        
        # Get the current date and time
        now = timezone.now()
        
        # Filter buses based on the source, destination, date, and ensure they are after the current date and time
        bus = Bus.objects.filter(source=source_r, destination=destination_r, date__gte=now.date()).exclude(date=now.date(), time__lte=now.time())
        
        if bus.exists():
            q1 = Q(source=source_r)
            q2 = Q(destination=destination_r)
            q3 = Q(date__gte=now.date())
            q4 = ~Q(date=now.date(), time__lte=now.time())
            buses = Bus.objects.filter(q1 & q2 & q3 & q4)
            data['buses'] = buses
            return render(request, 'home/list.html', context=data)
        else:
            data["error_msg"] = "Sorry, no bus available"
            return render(request, 'home/find.html', context=data)
    else:
        return render(request, 'home/find.html')


def bus_seats(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        if bus_id:
            bus = Bus.objects.get(id=bus_id)
            booked_seats = bus.get_booked_seats()
            seats_layout = {
                'left_column1': ['1WD', '5WD', '9WD'],
                'left_column2': ['2S', '6S', '10S'],
                'right_column1': ['3S', '7S', '11S'],
                'right_column2': ['4WD', '8WD', '12WD']
            }
            return render(request, 'home/bus_seats.html', {
                'bus': bus,
                'booked_seats': booked_seats,
                'seats_layout': seats_layout
            })
    return redirect('/find')

# def book(request):
#     if request.method == 'POST':
#         user = request.user  
#         bus_id = request.POST.get('bus_id')
#         selected_seats = request.POST.get('num_of_seats').split(',')

#         bus = Bus.objects.get(id=bus_id)
#         num_of_seats_to_book = len(selected_seats)

#         if num_of_seats_to_book > bus.num_of_seats_rem:
#             return render(request, 'home/error.html', {'message': 'Not enough available seats'})

#         for seat in selected_seats:
#             Book.objects.create(userid=user, busid=bus, num_of_seats=seat)

#         bus.num_of_seats_rem -= num_of_seats_to_book
#         bus.save()

#         booking_details = {
#             'user_id': user.id,
#             'username': user.username,
#             'bus_id': bus.id,
#             'bus_name': bus.name,
#             'source': bus.source,
#             'destination': bus.destination,
#             'time': bus.time,
#             'date': bus.date,
#             'num_of_seats': num_of_seats_to_book,
#             'selected_seats': selected_seats,  
#             'price': bus.price,
#             'total_cost': num_of_seats_to_book * bus.price,
#         }
#         return render(request, 'home/bookings.html', {'booking_details': booking_details})
#     return redirect('/find')  

# def book(request): imp
#     if request.method == 'POST':
#         user = request.user
#         bus_id = request.POST.get('bus_id')
#         selected_seats = request.POST.get('num_of_seats').split(',')

#         if not selected_seats or selected_seats == ['']:
#             error_msg = "Select at least one seat"
#             bus = Bus.objects.get(id=bus_id)
#             booked_seats = bus.get_booked_seats()
#             seats_layout = {
#                 'left_column1': ['1WD', '5WD', '9WD'],
#                 'left_column2': ['2S', '6S', '10S'],
#                 'right_column1': ['3S', '7S', '11S'],
#                 'right_column2': ['4WD', '8WD', '12WD']
#             }
#             return render(request, 'home/bus_seats.html', {
#                 'bus': bus,
#                 'booked_seats': booked_seats,
#                 'seats_layout': seats_layout,
#                 'error_msg': error_msg
#             })

#         bus = Bus.objects.get(id=bus_id)
#         num_of_seats_to_book = len(selected_seats)

#         if num_of_seats_to_book > bus.num_of_seats_rem:
#             return render(request, 'home/error.html', {'message': 'Not enough available seats'})

#         for seat in selected_seats:
#             Book.objects.create(userid=user, busid=bus, num_of_seats=seat)

#         bus.num_of_seats_rem -= num_of_seats_to_book
#         bus.save()

#         booking_details = {
#             'user_id': user.id,
#             'username': user.username,
#             'bus_id': bus.id,
#             'bus_name': bus.name,
#             'source': bus.source,
#             'destination': bus.destination,
#             'time': bus.time,
#             'date': bus.date,
#             'num_of_seats': num_of_seats_to_book,
#             'selected_seats': selected_seats,
#             'price': bus.price,
#             'total_cost': num_of_seats_to_book * bus.price,
#         }
#         return render(request, 'home/bookings.html', {'booking_details': booking_details})
#     return redirect('/find')


def book(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        selected_seats = request.POST.get('num_of_seats').split(',')

        if not selected_seats or selected_seats == ['']:
            error_msg = "Select at least one seat"
            bus = Bus.objects.get(id=bus_id)
            booked_seats = bus.get_booked_seats()
            seats_layout = {
                'left_column1': ['1WD', '5WD', '9WD'],
                'left_column2': ['2S', '6S', '10S'],
                'right_column1': ['3S', '7S', '11S'],
                'right_column2': ['4WD', '8WD', '12WD']
            }
            return render(request, 'home/bus_seats.html', {
                'bus': bus,
                'booked_seats': booked_seats,
                'seats_layout': seats_layout,
                'error_msg': error_msg
            })

        bus = Bus.objects.get(id=bus_id)
        num_of_seats_to_book = len(selected_seats)

        if num_of_seats_to_book > bus.num_of_seats_rem:
            return render(request, 'home/error.html', {'message': 'Not enough available seats'})

        # Store selected seats and bus ID in session
        request.session['selected_seats'] = selected_seats
        request.session['bus_id'] = bus_id

        booking_details = {
            'user_id': request.user.id,
            'username': request.user.username,
            'bus_id': bus.id,
            'bus_name': bus.name,
            'source': bus.source,
            'destination': bus.destination,
            'time': bus.time,
            'date': bus.date,
            'num_of_seats': num_of_seats_to_book,
            'selected_seats': selected_seats,
            'price': bus.price,
            'total_cost': num_of_seats_to_book * bus.price,
        }
        return render(request, 'home/bookings.html', {'booking_details': booking_details})
    return redirect('/find')


import razorpay

def payment(request):
    if request.method == 'POST':
        bus_id = request.session.get('bus_id')
        selected_seats = request.session.get('selected_seats')

        if not bus_id or not selected_seats:
            return render(request, 'home/error.html', {'message': 'Session expired. Please start the booking process again.'})

        bus = Bus.objects.get(id=bus_id)
        num_of_seats_to_book = len(selected_seats)

        if num_of_seats_to_book > bus.num_of_seats_rem:
            return render(request, 'home/error.html', {'message': 'Not enough available seats'})

        user = request.user

        for seat in selected_seats:
            Book.objects.create(userid=user, busid=bus, num_of_seats=seat)

        bus.num_of_seats_rem -= num_of_seats_to_book
        bus.save()

        total_cost = num_of_seats_to_book * bus.price * 100  # Convert to paise for Razorpay

        client = razorpay.Client(auth=("rzp_test_pvABMx4GHcVJ0U", "xwv4lVzeJQ0PU6LiKe8PoHdl"))
        data = {
            "amount": total_cost,
            "currency": "INR",
            "receipt": "booking_receipt_id_123",
        }
        try:
            payment = client.order.create(data=data)
        except Exception as e:
            return render(request, 'home/error.html', {'message': 'Error creating Razorpay order'})

        context = {'id': payment['id'], 'amount': total_cost, 'currency': "INR"}
        return render(request, 'home/pay.html', context=context)
    return render(request, 'home/error.html', {'message': 'Invalid request method'})



#import razorpay
# def payment(request):
#     if request.method == 'POST':
#         try:
#             total_cost = int(request.POST['total_cost']) * 100
#             client = razorpay.Client(auth=("rzp_test_pvABMx4GHcVJ0U", "xwv4lVzeJQ0PU6LiKe8PoHdl"))

#             data = {
#                 "amount": total_cost,
#                 "currency": "INR",
#                 "receipt": "booking_receipt_id_123",
#             }
#             try:
#                 payment = client.order.create(data=data)
#             except Exception as e:
#                 print(e)
#                 return render(request, 'home/error.html', {'message': 'Error creating Razorpay order'})

#             context = {'id': payment['id'], 'amount': total_cost, 'currency': "INR"}
#             return render(request, 'home/pay.html', context=context)
#         except KeyError:
#             return render(request, 'home/error.html', {'message': 'Missing total cost in request'})
#     return render(request, 'home/error.html', {'message': 'Invalid request method'})

def booking_details(request):
    user = request.user
    bookings = Book.objects.filter(userid=user).order_by('-id')  

    booking_dict = {}
    
    for booking in bookings:
        bus = booking.busid
        bus_id = bus.id
        if bus_id not in booking_dict:
            booking_dict[bus_id] = {
                'busid': bus.id,
                'busname': bus.name,
                'source': bus.source,
                'destination': bus.destination,
                'date': bus.date,
                'time': bus.time,
                'seats': [],
                'total_cost': 0
            }
        booking_dict[bus_id]['seats'].append(booking.num_of_seats)       
        booking_dict[bus_id]['total_cost'] += bus.price
        
    data = {
        'bookings': booking_dict.values(),  
    }
    return render(request, 'home/booking_details.html', context=data)

 
#rzp_test_pvABMx4GHcVJ0U
#xwv4lVzeJQ0PU6LiKe8PoHdl

def cancel(request):
    return redirect('/find')
 
