from datetime import datetime
from sqlalchemy import text


# function to check username existence, takes username and return final status
def check_username(data, db):
    username = data['username']
    sql = text("SELECT * FROM accounts WHERE username = '%s' " % username)
    response = db.session.execute(sql)
    user = response.fetchone()
    if user is None:
        return "success"
    else:
        return "fail"


# function to register new user, takes all values and return final status
def register_user(data, db):
    username = data['username']
    is_username_exist = check_username(data, db)
    if is_username_exist == "success":
        password = data['password']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = data['name']
        address = data['address']
        phone_number = data['phone_number']
        email = data['email']
        user_type = data['user_type']
        if user_type == 'credit':
            sql = """
                    START TRANSACTION;
                    INSERT INTO accounts (type, created_at, username, password) VALUES ('%s', '%s', '%s', '%s');
                    SET @id = LAST_INSERT_ID();
                    INSERT INTO credit_clients (client_id, name, address, phone_number, email, balance) VALUES (@id, '%s', '%s', '%s', '%s', 0);
                    COMMIT;
                  """
        else:
            sql = """
                    START TRANSACTION;
                    INSERT INTO accounts (type, created_at, username, password) VALUES ('%s', '%s', '%s', '%s');
                    SET @id = LAST_INSERT_ID();
                    INSERT INTO deposit_clients (client_id, name, address, phone_number, email, score, interest_rate, balance_working, balance_wait) 
                    VALUES (@id, '%s', '%s', '%s', '%s', 0, 1, 0, 0);
                    COMMIT;
                  """
        query = text(sql % (user_type, created_at, username, password, name, address, phone_number, email))
        db.session.execute(query)
        db.session.commit()
        return {'status': 'success', 'action': 'register'}
    else:
        return {'status': 'fail', 'action': 'register', 'error_message': 'username already exists'}


# function to log in user, takes all values and return final status
def login_user(data, db):
    username = data['username']
    password = data['password']
    sql = text("SELECT id, username, type FROM accounts WHERE username = '%s' AND password = '%s' " %
               (username, password))
    result = db.session.execute(sql)
    user = result.fetchone()
    # fetch format is (user_id, username, user_type)
    if user is None:
        return {'status': 'fail', 'action': 'login', 'error_message': 'wrong username or password'}
    else:
        return {'status': 'success', 'user_type': user[2], 'user_id': user[0], 'username': user[1], 'action': 'login'}


# function to get user data, takes user id and return user data
def get_user_data(account_id, db):
    sql = text("SELECT type FROM accounts WHERE id = '%s'" % account_id)
    result = db.session.execute(sql)
    user_type = result.fetchone()
    if user_type is None:
        return {'status': 'fail', 'action': 'get_user_data', 'error_message': 'user not found'}
    else:
        if user_type[0] == 'credit':
            sql = text(
                "SELECT name, address, phone_number, email, balance FROM credit_clients WHERE client_id = '%s' " % account_id)
            result = db.session.execute(sql)
            user = result.fetchone()
            return {'status': 'success', 'name': user[0], 'address': user[1], 'phone_number': user[2], 'email': user[3],
                    'user_type': user_type[0], 'user_id': account_id, 'action': 'get_user_data', 'balance': user[4]}
        else:
            sql = text(
                "SELECT name, address, phone_number, email, balance_working, balance_wait FROM deposit_clients WHERE client_id = '%s' " % account_id)
            result = db.session.execute(sql)
            user = result.fetchone()
            return {'status': 'success', 'name': user[0], 'address': user[1], 'phone_number': user[2], 'email': user[3],
                    'user_type': user_type[0], 'user_id': account_id, 'action': 'get_user_data',
                    'balance_working': user[4], 'balance_wait': user[5]}


# function to update user data, takes user id and return final status
def update_user_data(data, db):
    # data json format is {'name': name, 'address': address, 'phone_number': phone_number,
    # 'email': email, 'username': username, 'password': 'password'}
    username = data['username']
    password = data['password']
    sql = text("SELECT type, id FROM accounts WHERE username = '%s' AND password = '%s' " % (username, password))
    result = db.session.execute(sql)
    user = result.fetchone()
    if user is None:
        return {'status': 'fail', 'action': 'update_user_data', 'error_message': 'username or password is wrong'}
    else:
        user_id = user[1]
        name = data['name']
        address = data['address']
        phone_number = data['phone_number']
        email = data['email']
        username = data['username']
        user_type = user[0]
        if user_type == 'credit':
            sql = """
                        START TRANSACTION;
                        UPDATE credit_clients SET name = '%s', address = '%s', phone_number = '%s', email = '%s' 
                        WHERE client_id = '%s';
                        UPDATE accounts SET username = '%s' WHERE id = '%s';
                        COMMIT;
                      """
        else:
            sql = """
                        START TRANSACTION;
                        UPDATE deposit_clients SET name = '%s', address = '%s', phone_number = '%s', email = '%s' 
                        WHERE client_id = '%s';
                        UPDATE accounts SET username = '%s' WHERE id = '%s';
                        COMMIT;
                      """
        query = text(sql % (name, address, phone_number, email, user_id, username, user_id))
        db.session.execute(query)
        db.session.commit()
        return {'status': 'success', 'action': 'update_user_data'}
