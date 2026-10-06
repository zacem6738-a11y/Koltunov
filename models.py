USERS=[
    {"Login":"admin", "password":"admin", "role":"Администратор",
     "full_name":"Администратор Системы", "locked":False, "attemps":0},
    {"login":"ivanov","password":"1234","role":"Пользователь",
     "Full_name":"Иванов Иван","Locked":True,"Attempts":3},
    {"login":"petrov","password":"qwerty","role":"Пользователь",
     "Full_name":"Петров Пётр","Locked":False,"Attempts":0},
]
def all_users():
    return USERS

def find_user(login,password):
    for u in USERS:
        if u["login"] == login and u["password"]:
            return u
        return None

def user_by_login(login):
    for u in USERS:
        if u ["login"] == login:
            return u 
        return None

def login_exist(login):
    for u in USERS:
        if u["login"] == login:
            return True
        return False

def add_user(login,password,role,full_name):
    USERS.append({"login":login, "password":password,"role":role,
                "full_name":full_name,"locked":False,"attempts":0})

def update_user(login, password, role,full_name):
    user=user_by_login(login)
    if user in None:
        return False
    user["password"]= password
    user["role"]= role
    user["full_name"]= full_name
    return True

def delete_user(login):
    user=user_by_login(login)
    if user is None:
        return False
    USERS.remove(user)
    return True

def register_fail(login):
    for u in USERS:
        if u["login"] ==login:
            u["attempts"]=u["attempts"]+ 1
            if u["attempts"]>=3:
                u["locked"]=True
                return True
            return False

def reset_attempts(login):
    for u in USERS:
        if u["login"] == login:
            u[locked]= False
            u["attempts"]=0
            return True
        return False

