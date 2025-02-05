from auth.authorization import auth
from fastapi_pagination import Page
from redis import Redis
from .schemas import (
    UserVo,
    Register,
    CreateRole,
    UserInfo,
    UserList,
    UpdateUserInfo,
    Permissions,
    RegisterList,
    PermissionsList,
)
from sql_app.redisServe import get_redis
from utils.scopes import set_scopes, Scopes
from fastapi import APIRouter, Form, Security, Header, Depends
from .services import (
    user_check,
    create_user,
    edit_password,
    create_role,
    delete_role,
    user_list,
    user_info,
    delete_user,
    update_user_info,
    create_permissions,
    roles_join_permissions,
    role_list,
    permissions_list,
    delete_permissions,
    redis_test_demo,
)


user = APIRouter(tags=["admin-user"], prefix="/admin")


@user.post("/login", summary="用户登录", response_model=UserVo)
async def admin_user_login(
    username: str = Form(min_length=6, max_length=12),
    password: str = Form(min_length=6, max_length=12),
):
    return await user_check(username, password)


@user.post(
    "/user",
    summary="用户注册",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def admin_user_register(register: Register):
    return await create_user(register)



@user.get(
    "/user",
    summary="查询用户列表",
    response_model=Page[UserList],
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def get_user_list(
    username: str = None,
    start_time: str = None,
    end_time: str = None,
    is_frozen: bool = None,
    is_admin: bool = None,
):
    return await user_list(username, start_time, end_time, is_frozen, is_admin)


@user.get(
    "/user/{id}",
    summary="查询用户详细信息",
    response_model=UserInfo,
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def get_user_info(id: int):
    return await user_info(id)


@user.delete(
    "/user/{id}",
    summary="删除用户",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def delete_users(id: int):
    return await delete_user(id)


@user.put(
    "/user/{id}",
    summary="修改用户信息",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def update_users_info(id: int, user_info: UpdateUserInfo):
    return await update_user_info(id, user_info)


@user.post("/password", summary="修改密码")
async def admin_user_edit_password(
    Authorization: str = Header(),
    password: str = Form(min_length=6, max_length=12),
    new_password: str = Form(min_length=6, max_length=12),
):
    return await edit_password(Authorization, password, new_password)

@user.post(
    "/role",
    summary="创建角色",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def create_roles(createRole: CreateRole):
    return await create_role(createRole)


@user.delete(
    "/role/{id}",
    summary="删除角色",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def delete_roles(id: int):
    return await delete_role(id)


@user.get(
    "/role",
    summary="获取角色列表",
    response_model=Page[RegisterList],
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def roles_list(name: str = None):
    return await role_list(name)



@user.post(
    "/permissions",
    summary="创建权限",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def create_permission(permissions: Permissions):
    return await create_permissions(permissions)


@user.get(
    "/permissions",
    summary="获取权限列表",
    response_model=Page[PermissionsList],
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def get_permissions_list(description: str = None, code: int = None):
    return await permissions_list(description, code)


@user.delete(
    "/permissions/{id}",
    summary="删除权限",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def del_permissions(id: int):
    return await delete_permissions(id)


@user.post(
    "/role_{role_id}/permissions_{permissions_id}",
    summary="角色分配权限",
    dependencies=[
        Security(auth, scopes=set_scopes(Scopes(roles=["admin"], permissions=["1"])))
    ],
)
async def role_join_permissions(role_id: int, permissions_id: int):
    return await roles_join_permissions(role_id, permissions_id)





@user.get("/test_redis", summary="测试rides连接池")
async def redis_demo(redis: Redis = Depends(get_redis)):
    return await redis_test_demo(redis)
