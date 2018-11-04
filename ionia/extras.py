from django.contrib.postgres.fields import citext
from django.db import models


class EmailNullField(citext.EmailField):
    """Subclass of the CItext EmailField that allows empty strings to be stored as NULL.

    From https://stackoverflow.com/a/1934764/1649917 - mightyhal
    """
    description = "EmailField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection, context):
        """Gets value right out of the db and changes it if its ``None``."""
        if value is None:
            return ""
        else:
            return value

    def to_python(self, value):
        """Gets value right out of the db or an instance, and changes it if its ``None``."""
        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        if value is None:
            # If db has NULL, convert it to ''.
            return ""

        # Otherwise, just return the value.
        return value

    def get_prep_value(self, value):
        """Catches value right before sending to db."""
        if value == "":
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value
