from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import connect_db
from UsersManagment import *
from credit_client import *
from deposit_client import *
from flask_cors import CORS

host, db_user, db_password, database = connect_db.db_connection('db_cred.ini')
db_url = f'mysql://{db_user}:{db_password}@{host}/{database}'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)
CORS(app)


@app.route('/')
# function return json with port number and ip address of the server
def main():
    time = datetime.now().strftime("%H:%M:%S")
    return {'status': 'success', 'time': time, 'action': 'main'}


# route to log in, takes json file with username and password and returns json with status
# if status is success, then user is logged in
@app.route('/login', methods=['POST'])
def login():
    # request json format is {'username': 'username', 'password': 'password'}
    data = request.get_json()
    # return json format is {'status': 'fail', 'action': 'login', 'error_message': 'wrong username or password'}
    # or {'status': 'success', 'action': 'login', 'user_id': 'user_id',
    # 'username': 'username', 'user_type': 'user_type'}
    return login_user(data, db)


# route to register, takes json file with username and password and returns json with status
# if status is success, then user is registered
@app.route('/register', methods=['POST'])
def register():
    # json format is {'username': 'username', 'password': 'password', 'name': 'name', 'address': 'address',
    # 'phone_number': 'phone_number', 'email': 'email', 'user_type': 'user_type'}
    data = request.get_json()
    # return json format is {'status': 'fail', 'action': 'register', 'error_message': 'username already exists'}
    # or {'status': 'success', 'action': 'register'}
    return register_user(data, db)


# route to get information about the user, takes user_id and returns json with all personal information
@app.route('/user/get_info', methods=['GET'])
def user_info():
    # rout from should be like this: http://localhost:3000/user/get_info?user_id=user_id
    user_id = request.args.get('user_id')
    # return {'status': 'success', 'name': 'name', 'address': 'address', 'phone_number': 'phone_number',
    # 'email': 'email', 'user_type': 'user_type', 'user_id': 'user_id', 'username': 'username', 'action':
    # 'get_user_data'}
    # or {'status': 'fail', 'action': 'get_user_data', 'error_message': 'user not found'}
    return get_user_data(user_id, db)


# route to update user information
@app.route('/user/update_info', methods=['PUT'])
def update_info():
    # data json format is {'user_id': user_id, 'name': name, 'address': address, 'phone_number': phone_number,
    # 'email': email,  'user_type': user_type, 'username': username}
    data = request.get_json()
    # return {'status': 'success', 'action': 'update_user_data'}
    # or {'status': 'fail', 'action': 'update_user_data', 'error_message': 'user not found'}
    return update_user_data(data, db)


# route to get all credits for particular user
@app.route('/user/get_credits', methods=['GET'])
def get_credits():
    # rout from should be like this: http://localhost:3000/user/get_credits?user_id=user_id
    user_id = request.args.get('user_id')
    # return {'status': 'success', 'credits': {list of credits}, 'action': 'get_credits'}
    # or {'status': 'fail', 'action': 'get_credits', 'error_message': 'user not found'}
    # or {'status': 'fail', 'action': 'get_credits', 'error_message': 'User is a deposit client'}
    return get_user_credits(user_id, db)


# route to get repayment schedule for particular credit of particular user
@app.route('/user/get_repayment_schedule', methods=['GET'])
def get_repayment_schedule():
    # rout from should be like this:
    # http://localhost:3000/user/get_repayment_schedule?user_id=user_id&credit_id=credit_id
    user_id = request.args.get('user_id')
    credit_id = request.args.get('credit_id')
    # return {'status': 'success', 'credit_id': credit_id,'repayment_schedule': {list of repayment_schedule}, 'action':
    # 'get_repayment_schedule'}
    # or {'status': 'fail', 'action': 'get_repayment_schedule', 'error_message': 'credit not found'}
    return get_credit_repayment_schedule(credit_id, user_id, db)


# route for deposit clients to invest money
@app.route('/user/invest', methods=['POST'])
def invest():
    # data json format is {'user_id': user_id, 'amount': amount}
    data = request.get_json()
    # return {'status': 'success', 'action': 'invest'}
    # or {'status': 'fail', 'action': 'invest', 'error_message': 'account is not exist'}
    return invest_money(data, db)


# route for credit client to take a credit
@app.route('/user/take_credit', methods=['POST'])
def take_credit():
    # data json format is {'user_id': user_id, 'credit_amount': credit_amount}
    data = request.get_json()
    # return {'status': 'success', 'action': 'take_credit'}
    # or {'status': 'fail', 'action': 'take_credit', 'error_message': 'user is not a credit client'}
    # or {'status': 'fail', 'action': 'take_credit', 'error_message': 'credit allocation is not possible'}
    return take_credit_for_user(data, db)


# route for credit client to pay a credit
@app.route('/user/pay_credit', methods=['POST'])
def pay_credit():
    # data json format is {'user_id': user_id, 'credit_id': credit_id}
    data = request.get_json()
    # return {'status': 'success', 'action': 'pay_credit'}
    # or {'status': 'fail', 'action': 'pay_credit', 'error_message': 'credit not found'}
    # or {'status': 'fail', 'action': 'pay_credit', 'error_message': 'credit is not active'}
    return pay_credit_for_user(data, db)


if __name__ == '__main__':
    # run the server on port 5000 and host it on the local machine.
    app.run(host='0.0.0.0', port=3000)


# pip freeze and save requirements.txt
# pip freeze > requirements.txt