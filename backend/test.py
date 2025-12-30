
# from db import engine

# engine.connect()  # Test database connection

from db import engine
from sqlalchemy import text

with engine.connect() as c:
    print("CONNECTED:", c.execute(text("select current_database()")).fetchone())

