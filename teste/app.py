from chalice import Chalice
from configparser import ConfigParser
import psycopg2
import os

app = Chalice(app_name='teste2')
DB_CONFIG_FILE = os.path.dirname(__file__) + '/database.ini'


def config(filename=DB_CONFIG_FILE, section='postgresql'):
    # create a parser
    parser = ConfigParser()

    # read the configuration
    parser.read(filename)

    # get the section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0] not found in the {1} file', format(section, filename))
    return db


@app.route('/c')
def connect_to_rds():
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the postgresql database
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL Database Version:")
        cur.execute('SELECT version()')

        # fetch the data
        db_version = cur.fetchone()
        print(db_version)

        # close the connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')


@app.route('/')
def index():
    return {'hello': 'world'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
