from django.shortcuts import render , redirect
from bus.models import Bus ,Book
# Create your views here.

def add_bus(request):
   if request.method=='POST':
      name=request.POST.get('name')
      source=request.POST.get('source')
      destination=request.POST.get('destination')
      num_of_seats=request.POST.get('num_of_seats')
      num_of_seats_rem=request.POST.get('num_of_seats_rem')
      price=request.POST.get('price')
      date=request.POST.get('date')
      time=request.POST.get('time')
      added_bus=Bus.objects.create(name=name,source=source,destination=destination,num_of_seats=num_of_seats,num_of_seats_rem=num_of_seats_rem,price=price,date=date,time=time)
      added_bus.save()

      return redirect("/admins/bus/view/")
   return render(request,'admin/bus/add_bus.html')

def view_buses(request):
   data = {}
   buses = Bus.objects.all()  
   data['buses'] = buses
   return render(request,'admin/bus/view_bus.html',context=data)

def see_bookings(request):
    # Fetch all booking details
    bookings = Book.objects.all().select_related('busid', 'userid')
    
    booking_list = []
    for booking in bookings:
        booking_list.append({
            'user_id': booking.userid.id,
            'user_name': booking.userid.username,
            'seat_names': booking.num_of_seats,
            'bus_id': booking.busid.id,
            'bus_name': booking.busid.name,
            'source': booking.busid.source,
            'destination': booking.busid.destination,
            'date': booking.busid.date,
            'time': booking.busid.time,
        })   
    data = {
        'bookings': booking_list
    }
    return render(request, 'admin/bus/see_bookings.html', context=data)



def update_bus(request, busid):
    data = {}
    if request.method == 'POST':
        bus_name = request.POST['name']
        bus_source = request.POST['source']
        bus_destination = request.POST['destination']
        bus_num_of_seats = request.POST['num_of_seats']
        bus_num_of_seats_rem = request.POST['num_of_seats_rem']
        bus_price = request.POST['price']
        bus_date = request.POST['date']
        bus_time = request.POST['time']
        
        bus = Bus.objects.filter(pk=busid)
        bus.update(name=bus_name, source=bus_source, destination=bus_destination,
                   num_of_seats=bus_num_of_seats, num_of_seats_rem=bus_num_of_seats_rem,
                   price=bus_price, date=bus_date, time=bus_time)
        
        return redirect('/admins/bus/view')

    fetched_bus = Bus.objects.get(id=busid)
    data['bus'] = fetched_bus
    return render(request, 'admin/bus/update_bus.html', context=data)


def delete_bus(request,busid):
   bus=Bus.objects.get(id=busid)
   bus.delete()
   return redirect("/admins/bus/view/")

