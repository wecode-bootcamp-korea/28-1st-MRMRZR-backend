import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.models           import User
from my_settings            import SECRET_KEY, ALGORITHM

def LogInDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if not request.headers.get('Authorization'):
                return JsonResponse({'message' : 'NO_TOKEN'}, status = 403)
            
            access_token  = request.headers.get('Authorization', None)
            decoded_token = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            request.user  = User.objects.get(id = decoded_token['user_id'])
            
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 403)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 403)
        
        return func(self, request, *args, **kwargs)
    return wrapper