from django.shortcuts import render
from .forms import CurrencyConversionForm
import requests
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django.shortcuts import render

def currency_convert_form(request):
    return render(request, 'converter/conversion_form.html')

def currency_converter_form_view(request):
    result = None
    error = None

    if request.method == "POST":
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            from_currency = form.cleaned_data["from_currency"].upper()
            to_currency = form.cleaned_data["to_currency"].upper()
            amount = form.cleaned_data["amount"]

            try:
                url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
                res = requests.get(url, timeout=5)
                res.raise_for_status()
                data = res.json()
                converted = Decimal(str(data["rates"][to_currency]))
                rate = (converted / amount).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
                result = {
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount,
                    "converted": converted,
                    "rate": rate
                }
            except Exception as e:
                error = f"Conversion error: {str(e)}"
    else:
        form = CurrencyConversionForm()

    return render(request, "converter/conversion_form.html", {
        "form": form,
        "result": result,
        "error": error
    })
