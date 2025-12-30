import psycopg2

def pg_probe(host):
    try:
        conn = psycopg2.connect(
            host=host,
            port=5432,
            user="postgres",
            password="postgres",
            dbname="postgres",
            connect_timeout=3
        )
        conn.close()
        return "OK"
    except Exception as e:
        return repr(e)

print("localhost:", pg_probe("localhost"))
print("container_name:", pg_probe("expense"))
