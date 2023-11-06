"""Custom implementations may be used to change behavior in ways that TOML configuration alone does not permit."""
from typing import Optional, Set

import sqlalchemy
from id_translation.fetching import SqlFetcher as _SqlFetcher
from id_translation.types import IdType

from id_translation import Translator as _Translator


class CustomTranslator(_Translator):
    @classmethod
    def from_config(cls, *args, **kwargs):
        ans = super().from_config(*args, **kwargs)
        print(f"Created a new Translator using {ans.config_metadata}!")
        return ans


class CustomSqlFetcher(_SqlFetcher):
    """A custom SqlFetcher for Big Corporation Inc..

    Reads the database password from AWS and filters queries based on an 'enabled' status flag.
    """

    @classmethod
    def parse_connection_string2(cls, connection_string, password_key):
        """Finalize the connection string by reading the password from AWS."""
        import json

        from aws_secretsmanager_caching import SecretCache  # type: ignore

        actual_password = json.loads(SecretCache().get_secret_string(password_key))["password"]
        return super().parse_connection_string(connection_string, actual_password)

    @classmethod
    def select_where(
        cls,
        select: sqlalchemy.sql.Select,  # type: ignore[type-arg]
        *,
        ids: Optional[Set[IdType]],
        id_column: sqlalchemy.sql.ColumnElement,  # type: ignore[type-arg]
    ) -> sqlalchemy.sql.Select:  # type: ignore[type-arg]
        table = id_column.table

        print(dir(id_column))

        if "enabled" in table.columns:
            column = table.columns["enabled"]
            select = select.where(column == 1)
        return select
