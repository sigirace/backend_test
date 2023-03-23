from django.db import models


class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # DB에서 바라보지 말라는 의미 -> abstract
    class Meta:
        abstract = True
