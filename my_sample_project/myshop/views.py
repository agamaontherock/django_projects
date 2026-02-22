from django.shortcuts import render

from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .forms import CartAddProductForm, OrderCreateForm
from .models import Category, Product, OrderItem
from .cart import Cart

from .tasks import order_created
import stripe
from django.conf import settings
from django.urls import reverse
from .models import Order
from decimal import Decimal

import hmac
import hashlib



# from django.views.generic import TemplateView
# from django.shortcuts import render
# from django.http import HttpResponse

# class PayView(TemplateView):
#     template_name = 'liqpay.html'

#     def get(self, request, *args, **kwargs):
#         liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
#         params = {
#             'action': 'pay',
#             'amount': '100',
#             'currency': 'USD',
#             'description': 'Payment for clothes',
#             'order_id': 'order_id_1',
#             'version': '3',
#             'sandbox': 1, # sandbox mode, set to 1 to enable it
#             'server_url' : request.build_absolute_uri(reverse('shop:payment_completed'))
#             # 'server_url': 'https://test.com/billing/pay-callback/', # url to callback view
#         }
#         signature = liqpay.cnb_signature(params)
#         data = liqpay.cnb_data(params)
#         return render(request, self.template_name, {'signature': signature, 'data': data})

# @method_decorator(csrf_exempt, name='dispatch')
# class PayCallbackView(View):
#     def post(self, request, *args, **kwargs):
#         liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
#         data = request.POST.get('data')
#         signature = request.POST.get('signature')
#         sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
#         if sign == signature:
#             print('callback is valid')
#         response = liqpay.decode_data_from_str(data)
#         print('callback data', response)
#         return HttpResponse()

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'myshop/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'myshop/detail.html',
        {'product': product,
         'cart_product_form': cart_product_form},
    )

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'myshop/cart_detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('shop:payment_process')
            # return render(
            #     request, 'myshop/order_created.html', {'order': order}
            # )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'myshop/order_create.html',
        {'cart': cart, 'form': form},
    )

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
from liqpay import LiqPay
def payment_liqpay_form():
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    html = liqpay.cnb_form({
        'action': 'pay',
        'amount': '404',
        'currency': 'UAH',
        'description': 'description text',
        'order_id': 'order_id_1',
        'version': '3',
        'rro_info': {
            "items": [
                {
                    "amount": 2,
                    "price": 202,
                    "cost": 404,
                    "id": 123456
                }
            ],
            "delivery_emails": ["email1@email.com", "email2@email.com"]
        },
        'result_url': 'http://127.0.0.1:8000/payment_successful'
    })
    return html

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

#  merchantAccount, merchantDomainName, orderReference, orderDate, amount, currency, productName [0],
# productName [1] ..., productName [n], productCount [0], productCount [1], ..., productCount [n], productPrice [0], productPrice [1], ..., productPrice [n] розділених ";" (крапка з комою) в кодуванні UTF-8
    # string = "test_merchant;www.market.ua;DH783023;1415379863;1547.36;UAH;Процесор Intel Core i5-4670 3.4GHz;Пам'ять Kingston DDR3-1600 4096MB PC3-12800;1;1;1000;547.36";
    # key = "dhkq3vUi94{Z!5frxs(02ML";
    # wfp_hmac =hmac.new(key.encode(), string.encode(), hashlib.md5).hexdigest()
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('shop:payment_completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('shop:payment_canceled')
        )
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
            {
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        ctx = locals()
        ctx['liqpay_form'] = payment_liqpay_form()
        return render(request, 'myshop/payment/process.html', ctx)
    
def payment_completed(request):
    return render(request, 'myshop/payment/completed.html')

def payment_canceled(request):
    return render(request, 'myshop/payment/canceled.html')

from rest_framework.response import Response
from rest_framework.decorators import api_view
@api_view(['GET'])
def hello(request): 
    return Response({'message': 'Hello from Django!'})
