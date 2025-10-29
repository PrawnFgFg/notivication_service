from fastapi import APIRouter, Request, Response


from src.api.dependencies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.schemas.auth import UserCreateRequest, UserLoginIn, UserPutUpdate
from src.exceptions import IncorrectPasswordException, IncorrectPasswordHTTPException, \
    UserNotFoundException, UserNotFoundHTTPException, ObjectAlreadyExistException, \
        UserAlreadyExistHTTPException

router = APIRouter(prefix="/auth", tags=["Пользователи"])


@router.post("/register", summary="Регистрация")
async def register_user(
    data_add: UserCreateRequest,
    db: DBDep,
):
    try:
        await AuthService(db).create_user(data_add)
        return {"status": "Регистрация выполнена"}
    except ObjectAlreadyExistException:
        raise UserAlreadyExistHTTPException



@router.post("/login", summary="Войти в аккаунт")
async def login_in(
    db: DBDep,
    schema_login: UserLoginIn,
    response: Response,
):
    try:
        await AuthService(db).login_in(schema_login, response=response)
        return {"status": "Ok"}
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException


@router.get('/me', summary="Получить информацию о себе")
async def get_me(
    db: DBDep,
    user_id: UserIdDep
):
    return await AuthService(db).get_me(user_id=user_id)
    


@router.post("/logout", summary="Выйти из аккаунта")
async def logout(
    db: DBDep,
    response: Response
):
    return await AuthService(db).logout(response=response)


@router.put("", summary="Поменять ник")
async def change_nickname(
    db: DBDep,
    user_id: UserIdDep,
    schema_updt: UserPutUpdate,
):
    await AuthService(db).change_name(user_id=user_id, schema_updt=schema_updt)
    return {"message": f"Теперь ваше имя: {schema_updt.nickname}"}


@router.delete("/me", summary="Удалить аккаунт")
async def delete_my_account(
    db: DBDep,
    request: Request,
    response: Response,
):
    await AuthService(db).delete_me(request=request, response=response)
    return {"status": "Аккаунт удалён"}



    


