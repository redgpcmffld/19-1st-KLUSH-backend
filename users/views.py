import json
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from .utils        import validate_account_name, validate_phone_number, validate_email, validate_password
from my_settings   import ALGORITHM, SECRET_KEY
from users.models  import User
from orders.models import Order, OrderStatus

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            name         = data['name']
            phone_number = data['phone_number']
            email        = data['email']
            nickname     = data.get('nickname', None)
            account_name = data['account_name']
            password     = data['password']

            if not validate_phone_number(phone_number):
                return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
            
            if not validate_email(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)

            if not validate_account_name(account_name):
                return JsonResponse({'MESSAGE':'INVALID_ACCOUNT_NAME'}, status=400)

            if not validate_password(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(
                    Q(phone_number = phone_number) |
                    Q(email = email) |
                    Q(account_name = account_name)
                    ).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

            password        = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')

            user = User.objects.create(
                    name         = name,
                    phone_number = phone_number,
                    email        = email,
                    nickname     = nickname,
                    account_name = account_name,
                    password     = hashed_password,
                    )

            Order.objects.create(
                    user         = user, 
                    order_status = OrderStatus.objects.get(status=0)
                    )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
