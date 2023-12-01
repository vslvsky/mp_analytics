import environs
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

env = environs.Env()
env.read_env()

host = env("HOST")
password = env("PASSWORD")
database = env("DB_NAME")
port = env("PORT")

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}:{port}/{database}")

session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.metadata.schema = 'ozon'
Base.query = session.query_property()
