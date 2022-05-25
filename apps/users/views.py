import bcrypt
import json
import jwt
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from mrmrzara.settings import SECRET_KEY, ALGORITHM
from .validators  import validate_email, validate_password
from .models      import User


class UserSignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not validate_email(data['email']) or not validate_password(data['password']):
                return JsonResponse({'message': 'INVALID_USER'}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_EXISTS'}, status=409)
            
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = data['email'],
                password = hashed_password,
                name     = data['name'],
            )
            return JsonResponse({'result': 'CREATED'}, status=201)   
        except KeyError:
            return JsonResponse({'message': 'KEY ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=404)


class UserLogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not User.objects.get(email=data['email']):
                return JsonResponse({'message': 'INVALID_USER'}, status=400)    
            
            user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_USER'}, status=400)
            
            payload = {'user-id': user.id, 'exp':datetime.utcnow() + timedelta(days=2)}
            token  = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            result = {
                'token' : token
            }
            return JsonResponse({'result': result}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)
