import requests

from beaver_app.blueprints.order.models import Order
from beaver_app.blueprints.user.models import User


def notify_about_order(user: User, order: Order) -> None:
    if user.tg_id is not None:
        text = prepare_text(order)
        send_message(str(user.tg_id), text)
    return


def prepare_text(order: Order) -> str:
    return f'Ваш заказ № {order.id} на сумму {order.total} рублей принят. И будет доставлен по адресу {order.address}'


def send_message(chat_id: str, text: str) -> None:
    requests.post(
        'https://bot.green-beaver.ru/send_message',
        json={
            'chat_id': chat_id,
            'text': text,
        },
    )
    return
