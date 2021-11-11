from django.db import models

from django.utils.translation import gettext_lazy as _


class Core(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=40)
    reuse_count = models.PositiveSmallIntegerField(_("reuse count"), default=0)
    payload = models.PositiveSmallIntegerField(_("payload"), default=0)

    class Meta:
        verbose_name = _("Core")
        verbose_name_plural = _("Cores")

    def __str__(self) -> str:
        return f"({self.id}, {self.reuse_count}, {self.payload})"
