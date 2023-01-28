from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

metadata = MetaData()

users_table = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("email", String, unique=True),
            Column("password", String),
        )

cameras_table = Table(
            "cameras",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("stream_mode", Integer, nullable=False),
            Column("name", String, unique=True, nullable=False),
            Column("ip", String, nullable=True, default=None),
            Column("port", String, nullable=True, default=None),
            Column("typeof", String, nullable=True, default=None),
            Column("protocol", String, nullable=True, default=None),
            Column("local_path", String, nullable=True, default=None),
            Column("floor_id", Integer, ForeignKey("floors.id"))
        )

floors_table = Table(
            "floors",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, unique=True, nullable=False),
        )