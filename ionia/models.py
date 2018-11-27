from django.db import models
from django.utils import timezone
from fity3 import generator, to_timestamp


def get_id():
    """Generates snowflake id

    See-Also:
        https://stackoverflow.com/q/16925129/1649917
    """
    return next(generator(0))


class CommonInfo(models.Model):
    """Attributes common to all/most models in the project.

    This adds:
        Snowflake id
        created_at, derived from snowflake id

    See-Also:
        https://github.com/cablehead/python-fity3
        https://github.com/spookyUnknownUser/python-fity3/blob/master/README.rst#django
        https://stackoverflow.com/q/16925129/1649917
    """

    id = models.BigIntegerField(primary_key=True, default=get_id, editable=False)

    def created_at(self):
        timestamp = to_timestamp(self.id)
        return timezone.datetime.fromtimestamp(timestamp)

    class Meta:
        """Order by most recently created"""

        abstract = True
        ordering = ["-id"]
