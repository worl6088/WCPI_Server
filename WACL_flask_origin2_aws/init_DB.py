from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///camera.db', echo=True)
Base = declarative_base()
metadata = Base.metadata
engine_name = engine.name


foreign_key_turn_off = {
    'mysql': 'SET FOREIGN_KEY_CHECKS=0;',
    'postgresql': 'SET CONSTRAINTS ALL DEFERRED;',
    'sqlite': 'PRAGMA foreign_keys = OFF;',
}
foreign_key_turn_on = {
    'mysql': 'SET FOREIGN_KEY_CHECKS=1;',
    'postgresql': 'SET CONSTRAINTS ALL IMMEDIATE;',
    'sqlite': 'PRAGMA foreign_keys = ON;',
}

truncate_query = {
    'mysql': 'TRUNCATE TABLE {};',
    'postgresql': 'TRUNCATE TABLE {} RESTART IDENTITY CASCADE;',
    'sqlite': 'DELETE FROM {};',
}

def remove_last_data():
    with engine.begin() as conn:
        conn.execute(foreign_key_turn_off[engine.name])

        for table in ["cam1_result","cam2_result","cam3_result"]:
            conn.execute(truncate_query[engine.name].format(table))
        conn.execute(foreign_key_turn_on[engine.name])