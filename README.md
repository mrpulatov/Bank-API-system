
# Bank API system

This project is a financial system that manages accounts, credit clients, deposit clients, transactions, credit, repayment schedules, credit allocations. This project allocates credit between many deposit clients money, which reduses risk of NPL. This project could be useful for financial institutions or companies that need to manage credit & deposit system.


## Authors

- [@mrpulatov](https://www.github.com/mrpulatov)


## Installation

Export sql schema to you database
```bash
mysql -u username -p database_name < database.sql
```


In db_cred.ini file change parameters to connect you database
```bash
[DB_CRED]
host = host
user = flask_user
password = password
database = db_prject
```


Installation of this project on windows by using venv which is located at the same directory as this file

```bash
python -m venv venv
venv\Scripts\activate
python app.py
```
    
## API Reference

#### Main page

- **URL**: `http://localhost:3000/`
- **Method**: `GET`
- **Return JSON format**: `{'status': 'success', 'action': 'main', 'time': time}`

#### Login

- **URL**: `http://localhost:3000/login`
- **Method**: `POST`
- **JSON format**: `{'username': 'username', 'password': 'password'}`
- **Return JSON format**: `{'status': 'fail', 'action': 'login', 'error_message': 'wrong username or password'}` or `{'status': 'success', 'action': 'login', 'user_id': 'user_id', 'username': 'username', 'user_type': 'user_type'}`

#### Register

- **URL**: `http://localhost:3000/register`
- **Method**: `POST`
- **JSON format**: `{'username': 'username', 'password': 'password', 'name': 'name', 'address': 'address', 'phone_number': 'phone_number', 'email': 'email', 'user_type': 'user_type'}`
- **Return JSON format**: `{'status': 'fail', 'action': 'register', 'error_message': 'username already exists'}` or `{'status': 'success', 'action': 'register'}`

#### Get user information

- **URL**: `http://localhost:3000/user/get_info?user_id=user_id`
- **Method**: `GET`
- **Query string**: `user_id`
- **If user_type is credit return JSON format is**: `{'status': 'success', 'name': name, 'address': address,  'phone_numberphone_number, 'email': email,  'user_typeuser_type, 'user_id': user_id,  'actionaction: 'get_user_data',  'balancebalance: balance}`
- **If user_type is deposit return JSON format is**: `{'status': success, 'name': name,  'addressaddress: address, 'phone_numberphone_number: phone_number, 'email': email,  'user_typeuser_type: user_type, 'user_id': user_id,  'actionaction: 'get_user_data',  'balance_working': balance_working, 'balance_wait': balance_wait}`
- **Or** `{'status':'fail','action':'get_user_data','error_message':'user not found'}`

#### Update user information

- **URL**: `http://localhost:3000/user/update_info`
- **Method**: `PUT`
- **JSON format**: `{'user_id': user_id, 'name': name, 'address': address, 'phone_number': phone_number, 'email': email, 'user_type': user_type, 'username': username}`
- **Return JSON format**: `{'status': 'success', 'action': 'update_user_data'}` or `{'status': 'fail', 'action': 'update_user_data', 'error_message': 'user not found'}`

#### Get all credits for particular user

- **URL**: `http://localhost:3000/user/get_credits?user_id=user_id`
- **Method**: `GET`
- **Query string**: `user_id`
- **Return JSON format**: `{'status': 'success', 'credits': {list of credits}, 'action': 'get_credits'}` or `{'status': 'fail', 'action': 'get_credits', 'error_message': 'user not found'}` or `{'status': 'fail', 'action': 'get_credits', 'error_message': 'User is a deposit client'}`

#### Get repayment schedule for particular credit of particular user

- **URL**: `http://localhost:3000/user/get_repayment_schedule?user_id=user_id&credit_id=credit_id`
- **Method**: `GET`
- **Query string**: `user_id`, `credit_id`
- **Return JSON format**: `{'status': 'success', 'credit_idcredit_id: credit_id,'repayment_schedule': {list of repayment_schedule}, 'actionaction: 'get_repayment_schedule'}` or `{'status':'fail','action':'get_repayment_schedule','error_message':'credit not found'}`

#### Route for deposit clients to invest money

- **URL**: `http://localhost:3000/user/invest`
- **Method**: `POST`
- **JSON format**: `{'user_id': user_id, 'amount': amount}`
- **Return JSON format**: `{'status': 'success', 'action': 'invest'}` or `{'status': 'fail', 'action': 'invest', 'error_message': 'account is not exist'}`

#### Route for credit client to take a credit

- **URL**: `http://localhost:3000/user/take_credit`
- **Method**: `POST`
- **JSON format**: `{'user_id': user_id, 'credit_amount': credit_amount}`
- **Return JSON format**: `{'status': 'success', 'action': 'take_credit'}` or `{'status': 'fail', 'action': 'take_credit', 'error_message': 'user is not a credit client'}` or `{'status': 'fail', 'action': 'take_credit', 'error_message': 'credit allocation is not possible'}`

#### Route for credit client to pay a credit

- **URL**: `http://localhost:3000/user/pay_credit`
- **Method**: `POST`
- **JSON format**: `{'user_id': user_id, 'credit_id': credit_id, 'amount_paid': amount}`
- **Return JSON format**: `{'status':'success','action':'pay_credit'}` or
`{'status':'fail','action':'pay_credit','error_message':'credit not found'}` or
`{'status':'fail','action':'pay_credit','error_message':'user is not a credit client'}` or
`{'status':'fail','action':'pay_credit','error_message':'credit already closed'}`





## Documentation

Currently under development, project is not big enough to have documentation.


## Feedback

If you have any feedback, please reach out to us at https://t.me/IamUbaydulloh


