import stripe
from django.conf import settings
from stripe.api_resources.product import Product


def get_session(instance):
    """Возаращаем сессию для оплаты курса или урока по API"""

    # __/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\__измени на .енв
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # __/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\__

    # payment_id = instance.kwargs["pk"]

    product_name = str(instance.user) + str(instance.date_of_payment)
    product = stripe.Product.create(name=f'{product_name}')

    YOUR_DOMAIN = "http://127.0.0.1:8000"
    # payment_name = instance.user + instance.date_of_payment

    price = stripe.Price.create(
        unit_amount=instance.payment_amount,
        currency='rub',
        product=f'{product.id}'
    )

    session = stripe.checkout.Session.create(
        # succes_url='https://example.com/success',
        # payment_method_types=['card'],
        line_items=[
            {
                # 'price_data': {
                #     # 'currency': 'rub',
                #     # 'unit_amount': payment.payment_amount,
                #     'product_data': {
                #         # можно подумать конечно
                #         'name': payment_name
                #     },

                'price': f"{price.id}",
                'quantity': 1,
            },
        ],
        # metadata={
        #     "product_id": payment.id
        # },
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
        # надеюсь сработает
        customer_email=f"{instance.user.email}",
    )
    # # хмммммммммм
    # return JsonResponse({
    #     'id': checkout_session.id
    # })

    return session


def retrieve_session(session):
    """ Возвращаем obj сессии по АПИ, id передаем в аргумент функц"""
    #__/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\__измени на .енв
    stripe.api_key = settings.STRIPE_SECRET_KEY
    #__/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\____/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\__

    return stripe.checkout.Session.retrieve(session,)
