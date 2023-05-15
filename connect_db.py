# function that return a tuple of database connection parameters from ini file
import configparser


def db_connection(db_cred_file):
    config = configparser.ConfigParser()
    # read the database credential file and assign the return value to variables
    config.read(db_cred_file)
    db_cred = config['DB_CRED']
    host = db_cred['host']
    user = db_cred['user']
    password = db_cred['password']
    database = db_cred['database']
    return host, user, password, database


# a function that return a url for the database connection
def db_url():
    # call db_connection function and assign the return value to variables
    host, user, password, database = db_connection('db_cred.ini')
    return 'mysql://%s:%s@%s/%s' % (user, password, host, database)
