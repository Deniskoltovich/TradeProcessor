from django.db import models


class CreationDateMixinModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class EditDateMixinModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EditCreationDateMixinModel(CreationDateMixinModel, EditDateMixinModel):
    class Meta:
        abstract = True
