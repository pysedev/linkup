from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    description = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'tags'
