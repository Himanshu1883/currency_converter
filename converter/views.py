import requests
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ConversionLog
from .serializers import ConversionLogSerializer

class CurrencyConvertAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        from_currency = data.get('from_currency', '').upper()
        to_currency = data.get('to_currency', '').upper()
        amount = data.get('amount')

        if not from_currency or not to_currency or amount is None:
            return Response({"error": "All fields (from_currency, to_currency, amount) are required."}, status=400)

        try:
            amount = Decimal(str(amount)).quantize(Decimal('0.0000001'))  # Up to 7 decimal places
        except (InvalidOperation, ValueError):
            return Response({"error": "Amount must be a valid decimal number."}, status=400)

        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"

        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": "Failed to fetch live exchange rate.", "details": str(e)}, status=502)

        result = res.json()
        print("API response:", result)

        try:
            converted_amount = Decimal(str(result['rates'][to_currency]))
            rate = (converted_amount / amount).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
        except (KeyError, ZeroDivisionError, InvalidOperation) as e:
            return Response({"error": "Invalid currency code or conversion failed."}, status=400)

        log = ConversionLog.objects.create(
            user=request.user,
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted_amount,
            rate=rate
        )

        serializer = ConversionLogSerializer(log)
        return Response(serializer.data, status=201)


