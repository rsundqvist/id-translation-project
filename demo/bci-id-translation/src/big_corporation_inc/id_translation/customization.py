"""Custom implementations may be used to change behavior in ways that TOML configuration alone does not permit."""

from typing import Self

import sqlalchemy
from id_translation.fetching import SqlFetcher as _SqlFetcher
from id_translation.types import IdType, NameType, SourceType

from id_translation import Translator as _Translator  # Hide in generated docs.


class CustomTranslator(_Translator[NameType, SourceType, IdType]):
    @classmethod
    def from_config(cls, *args, **kwargs) -> Self:
        ans = super().from_config(*args, **kwargs)
        print(f"Created a new Translator using {ans.config_metadata}!")
        return ans


class CustomSqlFetcher(_SqlFetcher[IdType]):
    """A custom SqlFetcher for `Big Corporation Inc.` databases.

    Reads the database password from AWS and filters queries based on an 'enabled' status flag.
    """

    @classmethod
    def parse_connection_string(
        cls, connection_string: str | sqlalchemy.engine.URL, arn: str | None
    ) -> str | sqlalchemy.engine.URL:
        """Finalize the connection string by reading the password from AWS."""
        import json

        from aws_secretsmanager_caching import SecretCache  # type: ignore

        if arn is None:
            raise ValueError("Cannot retrieve password from AWS without an ARN.")

        actual_password = json.loads(SecretCache().get_secret_string(arn))["password"]
        return super().parse_connection_string(connection_string, actual_password)

    def select_where(
        self,
        select: sqlalchemy.sql.Select[tuple[IdType, ...]],
        *,
        ids: set[IdType] | None,  # noqa: ARG002
        id_column: sqlalchemy.sql.ColumnElement[IdType],  # noqa: ARG002
        table: sqlalchemy.Table,
    ) -> sqlalchemy.sql.Select[tuple[IdType, ...]]:
        """Restrict every query to rows flagged as enabled."""
        if "enabled" in table.columns:
            enabled = table.columns["enabled"]
            select = select.where(enabled == 1)
        return select
