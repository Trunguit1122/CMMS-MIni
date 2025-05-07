# import thư viện
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Khởi tạo engine
engine = create_engine(DATABASE_URL)

# Tạo session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class để tạo models
Base = declarative_base()

# Dependency để lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Cuối file database.py
if __name__ == "__main__":
    try:
        db = SessionLocal()
        print("✅ Kết nối Postgres thành công!")
    except Exception as e:
        print("❌ Lỗi kết nối:", e)
