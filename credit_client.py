from sqlalchemy import text
from datetime import datetime, timedelta


def get_user_credits(user_id, db):
    # Check if the user exists
    query = text('SELECT * FROM accounts WHERE id = %s' % user_id)
    response = db.session.execute(query)
    result = response.fetchone()

    if not result:
        # If the user does not exist, return an error message
        return {'status': 'fail', 'action': 'get_credits', 'error_message': 'user not found'}

    # Check if the user is a deposit client
    query = text('SELECT * FROM deposit_clients WHERE client_id = %s' % user_id)
    response = db.session.execute(query)
    result = response.fetchone()

    if result:
        # If the user is a deposit client, return an error message
        return {'status': 'fail', 'action': 'get_credits', 'error_message': 'User is a deposit client'}
    else:
        # If the user is not a deposit client, retrieve their credits
        query = text('''
                SELECT credit.*
                FROM credit_clients
                JOIN credit ON credit_clients.client_id = credit.account_id
                WHERE credit_clients.client_id = %s
                ''' % user_id)
        response = db.session.execute(query)
        result = response.fetchall()

        # Convert the result to a list of dictionaries
        credits_list = []
        for row in result:
            credit = {
                'id': row[0],
                'account_id': row[1],
                'total_amount': row[2],
                'interest': row[3],
                'final_price': row[4]
            }
            credits_list.append(credit)

        # Return the result as JSON
        return {'status': 'success', 'credits': credits_list, 'action': 'get_credits'}


def get_credit_repayment_schedule(credit_id, user_id, db):
    # query the repayment_schedule table for the given credit_id and user_id
    query = text("""
        SELECT due_date, credit_amount_due, interest_amount_due
        FROM repayment_schedule
        WHERE credit_id = %s AND credit_client_id = %s
    """ % (credit_id, user_id))
    response = db.session.execute(query)
    result = response.fetchall()

    # check if any results were returned
    if result:
        # create a list of dictionaries to represent the repayment schedule
        repayment_schedule = []
        for row in result:
            repayment_schedule.append({
                'due_date': row[0],
                'credit_amount_due': row[1],
                'interest_amount_due': row[2]
            })

        # return a success message with the repayment schedule
        return {'status': 'success', 'credit_id': credit_id, 'repayment_schedule': repayment_schedule,
                'action': 'get_repayment_schedule'}
    else:
        # return a failure message if no results were found
        return {'status': 'fail', 'action': 'get_repayment_schedule', 'error_message': 'credit not found'}


def take_credit_for_user(data, db):
    user_id = data['user_id']
    credit_amount = data['credit_amount']

    # check if user is a credit client
    credit_client = db.session.execute(text('SELECT * FROM credit_clients WHERE client_id = %s' % user_id)).fetchone()
    if not credit_client:
        return {'status': 'fail', 'action': 'take_credit', 'error_message': 'user is not a credit client'}

    # check if user is has a credit
    has_credit = db.session.execute(
        text('SELECT id FROM credit WHERE account_id = %s' % user_id)).fetchone()
    if has_credit is not None:
        print(has_credit)
        return {'status': 'fail', 'action': 'take_credit', 'error_message': 'user already has active credit'}

    # check if total waiting balance of all deposit clients is more or equal to asked credit amount
    deposit_clients = db.session.execute(text('SELECT client_id, name, address, phone_number, email, score, '
                                              'interest_rate, balance_working, '
                                              'balance_wait FROM deposit_clients')).fetchall()
    total_waiting_balance = sum([client[8] for client in deposit_clients])
    if total_waiting_balance < credit_amount:
        return {'status': 'fail', 'action': 'take_credit', 'error_message': 'credit allocation is not possible'}

    # start transaction
    db.session.execute(text('START TRANSACTION'))

    # collect money from each deposit client waiting balance and create credit record
    remaining_amount = credit_amount
    for client in deposit_clients:
        if remaining_amount == 0:
            break
        allocation_amount = min(remaining_amount, client[8])
        remaining_amount -= allocation_amount
        db.session.execute(
            text('UPDATE deposit_clients SET balance_wait = balance_wait - %s WHERE client_id = %s' % (
                allocation_amount, client[0])))
        db.session.execute(
            text('UPDATE deposit_clients SET balance_working = balance_working + %s WHERE client_id = %s' % (
                allocation_amount, client[0])))

    interest = credit_amount * 0.2
    final_price = credit_amount + interest
    # update the credit_client's balance
    db.session.execute(
        text('UPDATE credit_clients SET balance = balance - %s WHERE client_id = %s' % (
            final_price, user_id)))

    db.session.execute(
        text('INSERT INTO credit (account_id, total_amount, interest, final_price) VALUES (%s, %s, %s, %s)' % (
            user_id, credit_amount, interest, final_price)))

    # get the id of the newly inserted credit record
    credit_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

    # save information in the credit_allocations table
    remaining_amount = credit_amount
    for client in deposit_clients:
        if remaining_amount == 0:
            break
        allocation_amount = min(remaining_amount, client[8])
        remaining_amount -= allocation_amount
        db.session.execute(
            text('INSERT INTO credit_allocations (credit_id, deposit_client_id, credit_client_id, amount_allocated) '
                 'VALUES (%s, %s, %s, %s)' % (credit_id, client[0], user_id,
                                              allocation_amount)))

    # create repayment schedule for 6 months from today's date
    due_date = datetime.now() + timedelta(days=30)
    credit_amount_due = final_price / 6
    interest_amount_due = interest / 6
    for i in range(6):
        db.session.execute(
            text(
                'INSERT INTO repayment_schedule (credit_id, credit_client_id, due_date, credit_amount_due, interest_amount_due) '
                'VALUES (%s, %s, "%s", %s, %s)' % (credit_id, user_id,
                                                   due_date.strftime('%Y-%m-%d'), credit_amount_due,
                                                   interest_amount_due)))
        due_date += timedelta(days=30)

    # commit transaction
    db.session.execute(text('COMMIT'))

    return {'status': 'success', 'action': 'take_credit'}


# function to pay credit for user
def pay_credit_for_user(data, db):
    user_id = data['user_id']
    credit_id = data['credit_id']
    amount_paid = data['amount_paid']

    # check if credit exists
    credit = db.session.execute(text('SELECT id, total_amount FROM credit WHERE id = %s' % credit_id)).fetchone()
    if not credit:
        return {'status': 'fail', 'action': 'pay_credit', 'error_message': 'credit not found'}

    # check if user is a credit client
    credit_client = db.session.execute(text('SELECT client_id, balance FROM credit_clients WHERE client_id = %s' % user_id)).fetchone()
    if not credit_client:
        return {'status': 'fail', 'action': 'pay_credit', 'error_message': 'user is not a credit client'}

    # check if credit is already closed
    if credit_client[1] >= 0:
        return {'status': 'fail', 'action': 'pay_credit', 'error_message': 'credit already closed'}

    # add record to transactions table
    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.execute(text("INSERT INTO transactions (account_id, amount, type, created_at) VALUES (%s, %s, '%s', '%s')" % (user_id, amount_paid, 'credit', transaction_time)))

    # increase credit user balance
    db.session.execute(text('UPDATE credit_clients SET balance = balance + %s WHERE client_id = %s' % (amount_paid, user_id)))

    # update deposit user balances according to credit allocation
    total_credit_amount = credit[1]
    credit_allocations = db.session.execute(text('SELECT deposit_client_id, amount_allocated FROM credit_allocations WHERE credit_id = %s' % credit_id)).fetchall()
    for allocation in credit_allocations:
        deposit_client_id = allocation[0]
        amount_allocated = allocation[1]
        deposit_amount = amount_paid * float(amount_allocated / total_credit_amount)
        db.session.execute(text('UPDATE deposit_clients SET balance_working = balance_working - %s, balance_wait = balance_wait + %s WHERE client_id = %s' % (deposit_amount, deposit_amount, deposit_client_id)))

    db.session.commit()

    return {'status': 'success', 'action': 'pay_credit'}

