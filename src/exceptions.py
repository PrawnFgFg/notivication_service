from email.policy import HTTP
from fastapi import HTTPException



class BaseException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
        

class IncorrectPasswordException(BaseException):
    detail = "Пароль неверный"


class UserNotFoundException(BaseException):
    detail = "Пользователя с такием email не существует"
    
class JWTTokenHasExpiredException(BaseException):
    detail = "Токен истёк"


class ObjectAlreadyExistException(BaseException):
    detail = "Объект уже существует"
    
class NotFullBodyRequest(BaseException):
    detail = "Неполные данные в Body"
    
class InvalidTemplateException(BaseException):
    detail = "Неверный шаблон"





class BaseHTTPException(HTTPException):
    
    status_code = 500
    detail = None
    
    def __init__(self):
        super().__init__(self.status_code, self.detail)
        
        
class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Неверный пароль"
    
    
class UserNotFoundHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"
    
    
class JWTTokenHasExpiredHTTPException(BaseHTTPException):
    status_code = 498
    detail = "Токен истёк"
    
class UserAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409 
    detail = "Пользователь с таким email уже существует"
    
class NotFullBodyRequestHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Неполные данные в Body"
    
class InvalidTemplateHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Неверный шаблон"