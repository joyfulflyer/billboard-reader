import unittest
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from reader.models.chart import Chart


class TestSQLAlchemy(unittest.TestCase):
    def test_dupes(self):
        engine = create_engine('sqlite:///:memory:')

        metadata = MetaData()
        charts = Table('charts', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('type', String),
                       Column('date_string', String, unique=True))

        metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        print(Session)
        print(Session())
        session = Session()

        chart_date = "chart.date"

        c1 = Chart(type="hot-100", date_string=chart_date)
        c2 = Chart(type="hot-100", date_string=chart_date)
        session.add(c1)
        saved_object = session.query(Chart).filter_by(type="hot-100", date_string=chart_date)[0]
        session.add(c2)
        saved_object2 = session.query(Chart).filter_by(type="hot-100", date_string=chart_date)[0]

        self.assertEqual(saved_object2.id, saved_object.id)
        session.close()


    def sandbox(self):
        engine = create_engine('sqlite:///:memory:')

        metadata = MetaData()
        charts = Table('charts', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('type', String),
                       Column('date_string', String, unique=True))

        metadata.create_all(engine)




        Session = sessionmaker(bind=engine)
        print(Session)
        print(Session())
        session = Session()

        chart_date = "chart.date"

        c1 = Chart(type="hot-100", date_string=chart_date)
        c2 = Chart(type="hot-100", date_string=chart_date)
        session.add(c1)
        session.commit()
        print(c1)
        session.close()



if __name__ == '__main__':
    unittest.main()
