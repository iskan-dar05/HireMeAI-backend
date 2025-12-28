from app.core.database import engine
from sqlalchemy import text

# open connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✅ Database connected:", result.scalar())
