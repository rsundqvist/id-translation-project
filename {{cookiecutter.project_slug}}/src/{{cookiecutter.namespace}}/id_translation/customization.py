"""Custom implementations may be used to change behavior in ways that TOML configuration alone does not permit."""
from typing import Any

import sqlalchemy
from id_translation import Translator as _Translator
from id_translation.fetching import SqlFetcher as _SqlFetcher


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
    def parse_connection_string(cls, connection_string, password_key):
        """Finalize the connection string by reading the password from AWS."""
        import json

        from aws_secretsmanager_caching import SecretCache  # type: ignore

        actual_password = json.loads(SecretCache().get_secret_string(password_key))["password"]
        return super().parse_connection_string(connection_string, actual_password)

    def finalize_statement(
        self,
        select: sqlalchemy.sql.Select[Any],
        id_column: sqlalchemy.Column,  # type: ignore[type-arg]
        table: sqlalchemy.Table,
    ) -> sqlalchemy.sql.Select[Any]:
        if "enabled" in table.columns:
            column = table.columns["enabled"]
            select = select.where(column == 1)
        return select
