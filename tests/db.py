from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

autoflush = True
engine = create_engine(
    "mysql+mysqldb://root@localhost:3306/test_gaas",
    convert_unicode=True,
    pool_size=1,
    max_overflow=0,
    echo=False
)
maker = sessionmaker(bind=engine, autoflush=autoflush)
db = scoped_session(maker)
