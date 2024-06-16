from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', max_length=250)
    city = forms.CharField(label='Город', max_length=100)
    postal_code = forms.CharField(label='Почтовый индекс', max_length=20)
    country = forms.CharField(label='Страна', max_length=100)
    card_number = forms.CharField(label='Номер карты', max_length=19)
    card_expiry = forms.CharField(label='Срок действия карты', max_length=5)
    card_cvv = forms.CharField(label='CVV', max_length=3)