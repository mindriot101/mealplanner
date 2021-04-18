import uuid

from sqlalchemy.types import TypeDecorator, BINARY  # type: ignore
from sqlalchemy.dialects.postgresql import UUID as psqlUUID  # type: ignore


class UUID(TypeDecorator):
    impl = BINARY

    def load_dialect_impl(self, dialect):  # type: ignore
        if dialect.name == "postgresql":
            return dialect.type_descriptor(psqlUUID())
        else:
            return dialect.type_descriptor(BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                if isinstance(value, bytes):
                    value = uuid.UUID(bytes=value)
                elif isinstance(value, int):
                    value = uuid.UUID(int=value)
                elif isinstance(value, str):
                    value = uuid.UUID(value)

        if dialect.name == "postgresql":
            return str(value)
        else:
            return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "postgresql":
            return uuid.UUID(value)
        else:
            return uuid.UUID(bytes=value)
