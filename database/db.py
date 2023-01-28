import databases
import sqlalchemy

from . import models
import cfg


class Database:
    def __init__(self):
        self.db = databases.Database(cfg.connection_string)
        self.metadata = models.metadata
        self.users = models.users_table
        self.floors = models.floors_table
        self.cameras = models.cameras_table
        self.engine = sqlalchemy.create_engine(
            cfg.connection_string, pool_size=3, max_overflow=0
        )
        self.metadata.create_all(self.engine)

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()
