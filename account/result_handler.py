from django.http import HttpResponse
from robokassa.views import ResultURL

from account.models import Payment


def send_notification(notification_type, transaction_id):
    # реализуйте вашу логику отправки уведомлений здесь
    # например, отправка уведомления на email или SMS
    print(f"Отправка уведомления типа '{notification_type}' для транзакции с ID {transaction_id}")


def result_handler(request):
    # получаем данные из POST-запроса
    transaction_id = request.POST.get('transaction_id')
    amount = request.POST.get('amount')
    status = request.POST.get('status')

    # выполняем необходимые операции с полученными данными
    # например, записываем результаты платежа в базу данных или отправляем уведомление

    if status == 'success':
        # если статус платежа успешный, выполнить определенные действия

        # записываем результаты платежа в базу данных
        Payment.objects.create(transaction_id=transaction_id, amount=amount, status=status)

        # отправляем уведомление о успешном платеже
        send_notification('payment_success', transaction_id)
    elif status == 'failure':
        # если статус платежа неудачный, выполнить другие действия

        # записываем результаты платежа в базу данных
        Payment.objects.create(transaction_id=transaction_id, amount=amount, status=status)

        # отправляем уведомление о неудачном платеже
        send_notification('payment_failure', transaction_id)
    else:
        # если статус неизвестен или отсутствует, выполнить еще другие действия

        # записываем результаты платежа в базу данных со статусом 'unknown'
        Payment.objects.create(transaction_id=transaction_id, amount=amount, status='unknown')

        # отправляем уведомление о неизвестном статусе платежа
        send_notification('payment_unknown', transaction_id)

    # возвращаем HTTP-ответ "Результаты платежа успешно обработаны"
    return HttpResponse('Результаты платежа успешно обработаны')


class MyCustomResultURL(ResultURL):
    """Класс MyCustomResultURL, класс-наследник класса ResultURL из библиотеки Django-Payments, который используется
    для обработки результатов платежа. Метод get_template_names() определяет список шаблонов,
    которые будут использоваться для отображения результатов платежа. В данном случае, метод возвращает список,
    содержащий один шаблон result.html. Это означает, что результаты платежа будут отображаться
    с использованием шаблона result.html. Метод post()обрабатывает результаты платежа, когда поступает POST-запрос
    на данный URL. Внутри метода выполняется обработка результатов платежа и вызов функции result_handler.
    Затем результаты обрабатываются с помощью метода process_result(), который передает запрос request дальше
    для обработки. Возможно, этот метод определен в родительском классе ResultURL.
    После выполнения всех операций обработки результатов платежа, метод post() возвращает результат вызова
    self.process_result(request), что, перенаправит пользователя на другую страницу или выполнит
    другую необходимую операцию в вашем приложении."""

    def get_template_names(self):
        # указываем шаблон, который будет использоваться для отображения результатов
        return ['result.html']

    def post(self, request, *args, **kwargs):
        # получаем POST-запрос от клиента с результатами платежа
        # обрабатываем результаты платежа
        result = self.process_result(request)

        return result

    def process_result(self, request):
        # вызываем функцию result_handler для обработки результатов платежа
        result_handler(request)

        # возвращаем сообщение об успешной обработке результатов платежа
        return HttpResponse("Результаты платежа успешно обработаны")
