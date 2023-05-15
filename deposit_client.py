from datetime import datetime

from sqlalchemy import text


def invest_money(data, db):

    # check if the user_id exists in the deposit_clients table
    query = text("SELECT * FROM deposit_clients WHERE client_id = %s" % data['user_id'])
    response = db.session.execute(query)
    result = response.fetchone()

    # check if any results were returned
    if result is not None:
        # update the balance_wait field for the given user_id
        query = text("UPDATE deposit_clients SET balance_wait = balance_wait + %s WHERE client_id = %s" %
                     (data['amount'], data['user_id']))

        db.session.execute(query)
        db.session.commit()
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = text("INSERT INTO transactions (account_id, amount, type, created_at) VALUES (%s, %s, '%s', '%s')" %
                     (data['user_id'], data['amount'], 'deposit', transaction_time))
        db.session.execute(query)
        db.session.commit()

        # return a success message
        return {'status': 'success', 'action': 'invest'}
    else:
        # return a failure message if no results were found
        return {'status': 'fail', 'action': 'invest', 'error_message': 'account is not exist'}



