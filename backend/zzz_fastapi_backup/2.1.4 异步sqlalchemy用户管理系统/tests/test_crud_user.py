from passlib.hash import argon2

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return argon2.hash(password)

def test_get_password_hash():
    # 创建一个 User 实例
    password = 'full122name'
    
    hashpasswd = get_password_hash(password)
    

    print(password)
    print(hashpasswd)

    is_valid = argon2.verify(password, "$argon2id$v=19$m=65536,t=3,p=4$fu8d4/x/D+Hcm9N6r7WWcg$bo4lTPdVUvWunCW5l5HBCbwjxwam7mkvzdo3VW4yXTc")


    print(is_valid)



def main():
    test_get_password_hash()

if __name__ == '__main__':
    main()



