
'''

def make_cam1_table():
   engine = create_engine('sqlite:///camera.db', echo=True)
   command = "DROP TABLE IF EXISTS cam1_table;"
   connection = engine.raw_connection()
   meta = MetaData()
   cam1_table = Table(
      'camera1', meta,
      Column('id', Integer, primary_key = True),
      Column('start_time', String),
      Column('end_time', String),
      Column('profile_image', String)
   )
   command = "DROP TABLE IF EXISTS cam1_table;"
   connection = engine.raw_connection()
   cursor = connection.cursor()
   cursor.execute(command)
   connection.commit()
   meta.create_all(engine)
   cursor.close()

def make_cam2_table():
   engine = create_engine('sqlite:///camera.db', echo=True)
   meta = MetaData()
   cam2_table = Table(
      'camera2', meta,
      Column('id', Integer, primary_key=True),
      Column('start_time', String),
      Column('end_time', String),
      Column('profile_image', String)
   )
   connection = engine.raw_connection()
   cursor = connection.cursor()
   command = "DROP TABLE IF EXISTS cam2_table"
   cursor.execute(command)
   connection.commit()
   meta.create_all(engine)
   cursor.close()

def drop_table(table_name):
   engine = create_engine(URL('sqlite:///camera.db'))
   base = declarative_base()
   metadata = MetaData(engine, reflect=True)
   table = metadata.tables.get(table_name)
   if table is not None:
       logging.info(f'Deleting {table_name} table')
       base.metadata.drop_all(engine, [table], checkfirst=True)

def initialize_db():
   drop_table('cam1_table')

initialize_db()
'''