import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, nickname, status_code",
    [
        ("chaki@example.com", "string", "Chaki", 200),
        ("brotato@example.com", "string", "Brotato", 200),
        ("pers@exmaple.com", "string", "Persy", 200)
    ]
)
async def test_auth_flow(email: str, password: str, nickname: str, status_code: int, ac: AsyncClient):
    resp_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "nickname": nickname
        }
    )
    
    assert resp_register.status_code == status_code
    assert isinstance(resp_register.json(), dict)
    
    
    resp_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert resp_login.status_code == status_code
    access_token = resp_login.cookies.get("access_token")
    assert access_token 
    
    if resp_login.json().get("id") == 2:
        resp_changed_name = await ac.put(
            "/auth",
            json={
                "nickname": nickname + "Changed"
            }
        )
        
        assert resp_changed_name.status_code == 200
        
    
    resp_getme = await ac.get(
        "/auth/me"
    )
    
    assert resp_getme.status_code == 200
    user = resp_getme.json()
    assert isinstance(user, dict)
    assert user.get('email')    
    assert "password" not in user
    assert "hashed_password" not in user
    
    if resp_getme.json().get("nickname") == "Persy":
        resp_delete = await ac.delete(
            "/auth/me"
        )
        assert resp_delete.status_code == 200

        
    else:
        resp_logout = await ac.post(
            "/auth/logout"
        )
        
        assert resp_logout.status_code == 200
        assert access_token not in resp_logout.cookies
        
    
async def test_user_actions(authenticated_user: AsyncClient):
    resp_changed = await authenticated_user.put(
        "/auth",
        json= {
            "nickname": "Changed_name"
        }
    )
    
    assert resp_changed.status_code == 200
    
    resp_user = await authenticated_user.get(
        "/auth/me"
    )    
    
    assert resp_user.status_code == 200
    assert resp_user.json().get("nickname") == "Changed_name"
    

    
    
    


    