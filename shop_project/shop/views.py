from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

# Create your views here.
def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods}
    return render(request,'shop/index.html', params)


def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query , item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

        if len(prod) != 0:
            allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods}
    if len(allprods) == 0 or len(query)<4:
        params = {'msg': "please enter proper search query"}

    return render(request,'shop/search.html',params)







def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":

        name= request.POST.get('name','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        desc= request.POST.get('desc','')
        print(name ,email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank= True
    return render(request,'shop/contact.html', {'thank':thank})





def products(request, id):
    # id used for fetching product
    product = Product.objects.filter(id=id)

    return render(request,'shop/productview.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsjson','')
        name= request.POST.get('name','')
        amount= request.POST.get('amount','')
        email= request.POST.get('email','')
        adress= request.POST.get('address1','') + " " + request.POST.get('address2','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zip_code= request.POST.get('zip_code','')
        mobile = request.POST.get('mobile')
        print(name ,email)
        order = Orders(name=name, email=email, city=city, adress=adress,amount=amount, state=state, zip_code=zip_code, mobile=mobile, items_json=items_json)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been palced")
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html', {'thank':thank, 'id':id})
    #     here type code for paytm to transfer amount to our own account once user payed the bill.
        # this will be customer email id
        # this will be the order id of shopcart database which is autofield
        #  so this MID is merchant id whih is iven by paytm when we open merchant account at present it is paytm demo id
        # param_dict = {
        #     'MID':'WorldP64425807474247',
        #     'ORDER_ID': str(order.order_id),
        #     'TXN_AMOUNT':str(amount),
        #     'CUST_ID':email,
        #     'INDUSTRY_TYPE_ID':'Retail',
        #     'WEBSITE':'WEBSAGING',
        #     'CHANNEL_ID':'WEB',
	    #     'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request,'shop/checkout.html')

# @csrf_exempt
# def handlerequest(request):
# #     paytm will send post request for payment
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('your order was successful')
#         else:
#             print('order was unsuccessful due to' + response_dict['RESPMSG'])
#     return render(request,'shop/paymentstatus.html', {'response':response_dict})





def tracker(request):
    if request.method == "POST":
        orderId= request.POST.get('orderId','')
        email= request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success', "updates": updates, 'itemsJson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else :
                return HttpResponse('{"status":"noitem"} ')
        except Exception as e:
            return HttpResponse("{'status':'error'}")
        #     pass
        #
        # return render(request, 'shop/tracker.html')
    return render(request,'shop/tracker.html')

