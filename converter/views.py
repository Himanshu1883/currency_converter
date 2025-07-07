from django.shortcuts import render
from .forms import CurrencyConversionForm
import requests
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ConversionLog
from .serializers import ConversionLogSerializer

# --- UI View ---
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

# --- API View ---
class CurrencyConvertAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        from_currency = data.get('from_currency', '').upper()
        to_currency = data.get('to_currency', '').upper()
        amount = data.get('amount')

        if not from_currency or not to_currency or amount is None:
            return Response({"error": "All fields are required."}, status=400)

        try:
            amount = Decimal(str(amount)).quantize(Decimal('0.0000001'))
        except (InvalidOperation, ValueError):
            return Response({"error": "Invalid amount."}, status=400)

        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"

        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            data = res.json()
            converted = Decimal(str(data["rates"][to_currency]))
            rate = (converted / amount).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
        except Exception as e:
            return Response({"error": "Conversion error", "details": str(e)}, status=400)

        log = ConversionLog.objects.create(
            user=request.user,
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted,
            rate=rate
        )

        serializer = ConversionLogSerializer(log)
        return Response(serializer.data, status=201)
