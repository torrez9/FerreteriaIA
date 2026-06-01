from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:@localhost/bd_fhls"
)