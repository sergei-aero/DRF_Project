import uuid
from decimal import Decimal

# Это имитация, реальные запросы к Stripe закомментированы.
# Для реальной интеграции нужно раскомментировать код с stripe и использовать библиотеку.

def create_stripe_product(name, description=''):
    """
    Создает продукт в Stripe и возвращает его ID.
    В реальности: stripe.Product.create(...)
    """
    # Здесь был бы реальный запрос:
    # product = stripe.Product.create(name=name, description=description)
    # return product.id

    # Имитация:
    product_id = f"prod_mock_{uuid.uuid4().hex[:8]}"
    return product_id

def create_stripe_price(amount, currency='usd', product_id=None):
    """
    Создает цену в Stripe. amount - сумма в основных единицах (рубли, доллары).
    В реальности цена задается в минимальных единицах (копейки, центы).
    """
    if product_id is None:
        raise ValueError("Необходимо указать product_id")
    # Реальный код:
    # unit_amount = int(amount * 100)
    # price = stripe.Price.create(
    #     unit_amount=unit_amount,
    #     currency=currency.lower(),
    #     product=product_id,
    # )
    # return price.id

    # Имитация:
    price_id = f"price_mock_{uuid.uuid4().hex[:8]}"
    return price_id

def create_checkout_session(price_id, success_url, cancel_url):
    """
    Создает сессию оплаты в Stripe и возвращает (session_id, payment_url).
    В реальности: stripe.checkout.Session.create(...)
    """
    # Реальный код:
    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
    #     line_items=[{'price': price_id, 'quantity': 1}],
    #     mode='payment',
    #     success_url=success_url,
    #     cancel_url=cancel_url,
    # )
    # return session.id, session.url

    # Имитация:
    session_id = f"cs_mock_{uuid.uuid4().hex[:8]}"
    payment_url = f"https://checkout.stripe.com/mock/{session_id}"
    return session_id, payment_url

def retrieve_checkout_session(session_id):
    """
    Получает данные сессии по ID (для проверки статуса).
    В реальности: stripe.checkout.Session.retrieve(session_id)
    """
    # Реальный код:
    # session = stripe.checkout.Session.retrieve(session_id)
    # return session.payment_status

    # Имитация: всегда возвращаем 'paid' (можно сделать случайно)
    # Для демонстрации можно вернуть 'paid', чтобы показать успешный сценарий.
    return 'paid'