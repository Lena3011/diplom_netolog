import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData, Sequence
from sqlalchemy.orm import sessionmaker
from config import DSN

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'

    id = sq.Column(sq.Integer, Sequence('some_id_seq'), primary_key=True)
    profile_id = sq.Column(sq.Integer)
    worksheet_id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'{self.id}: {self.profile_id}, {self.worksheet_id}'


def insert_data_viewed(user_id, worksheet_id):
    to_bd = Viewed(profile_id=user_id, worksheet_id=worksheet_id)
    session.add(to_bd)
    session.commit()


def select_of_unviewed(profile_id):
    session.commit()
    from_bd = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    return from_bd

if __name__ == '__main__':
    # Base.metadata.drop_all(engine)  # удаляет все существующие таблицы из нашей БД
    # Base.metadata.create_all(engine)
    # insert_data_viewed(11111, 222258)
    from_bd = session.query(Viewed).filter(Viewed.profile_id == 11111).all()
    print(from_bd)
    if 222258 in from_bd:
        print(222258)
    else:
        print('-')
    # session.commit()
    # from_bd = session.query(Viewed).all()
    # print(from_bd)
