import re
import psycopg2
import psycopg2.extras


connection = psycopg2.connect(
    'dbname=example user=example password=example host=localhost',
    cursor_factory=psycopg2.extras.RealDictCursor)
connection.set_session(autocommit=True)


def query(fileName, params={}):
    with open(fileName) as f:
        sql_query = f.read()

    sql_query = _adapt_sql(sql_query)

    cursor = connection.cursor()
    cursor.execute(sql_query, params)

    try:
        return cursor.fetchall()
    except psycopg2.ProgrammingError:
        # no results to fetch
        return None

def _adapt_sql(sql):
    """
    in sql files, variables use ":key" syntax:
     SELECT * FROM people WHERE name = :name
    but python's sql need:
     SELECT * FROM people WHERE name = %(name)s
    So we need to replace all :x with %(x)s

    >>> _adapt_sql('SELECT * FROM t WHERE x = :abc AND n % 2 = 0')
    'SELECT * FROM t WHERE x = %(abc)s AND n %% 2 = 0'
    """
    # first need to escape any existing % chars:
    sql = sql.replace('%', r'%%')

    # now replace :x with %(x)s
    sql = re.sub(
        r':([\w]+)',
        lambda match: '%(' + match.group(1) + ')s',
        sql
    )

    return sql