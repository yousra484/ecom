from django.shortcuts import render,redirect
from .models import  *
from django.contrib.auth import authenticate, login ,logout


# Create your views here.
#CRED 
def createUser(data):
   user= User.objects.create_user(username=data['username'],password=data['password'],email=data['email'])
   #user.set_password user =User.objects.create 
   return user 

def Home(request):
    msg='you are not logged in '
    islogged=False
    clients=Client.objects.all()
    print(request.user)
    if request.user.is_authenticated:
        islogged= True
        msg='welcome , ' +request.user.username
    context={
        'clients':clients,
        'msg': msg,
        'islogged':islogged
          }
    return render(request,'home.html',context)

def createClient(request):
   
    if request.method=='POST':
        name=request.POST['username']
        email=request.POST['email']
        phone=request.POST['number']
        password=request.POST['password']
        user_id= createUser({'username': name ,'password':password ,'email':email})
        Client.objects.create(user=user_id,phone_number=phone)
        return redirect(Home)
    
def createSeller (request):
   
    if request.method=='POST':
        name=request.POST['username']
        email=request.POST['email']
        phone=request.POST['number']
        password=request.POST['password']
        user_id= createUser({'username': name ,'password':password ,'email':email})
        Seller.objects.create(user=user_id,phone_number=phone)
        return redirect(Home)
    
def productView (request):
    if request.method=='GET':
       seller=Seller.objects.get(user=request.user)
       products=Product.objects.filter(owner=seller)
       context={'products': products}
       return render(request, 'product.html',context)
    
    if request.method=='POST':
        title=request.POST['title']
        price=request.POST['price']
        description=request.POST['desc']

        Product.objects.create ( 
            title=title,
            price=price,
            description=description,
            owner=seller
        )

        return redirect(productView)

def cartView (request):
    orders=Order.objects.filter(client=Client.objects.get(user=request.user).id)
    context={
        'orders':orders
    }
    return render (request , 'cart.html' ,context)

def catalogView (request):
    products=Product.objects.all()
    context ={
        'products':products
      }
    return render(request ,'catalog.html' ,context)

    
def orderView (request, productid, status ):
    
    client=Client.objects.get(user=request.user)
    product=Product.objects.get(id=productid)
    order=Order.objects.create(client=client ,product=product , status=status)
    print(order)
    return redirect(cartView)

def confirmOrder(request ,status ,orderid):
    order=Order.objects.get(id=orderid)
    order.status=status
    order.save()
    return redirect(cartView)
  

def deleteClient (request ,id ):
    Client.objects.get(id=id).delete()
    return redirect (Home)


def updatePage (request , id ):
    if request.method=='GET':
        client= Client.objects.get(id=id)
        context={
            'client':client
        }
        return render(request,'update.html',context)

    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['number']
        email=request.POST['email']
        client= Client.objects.get(id=id)
        client.name=name 
        client.email=email
        client.phone_number=phone 
        client.save()
        return redirect (Home)
    
def loginView (request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
           login(request,user)
           return redirect (Home)
            
    return render(request,'login.html')
    

def logoutView(request):
    logout(request)
    return redirect(Home)




           

            



   







