from django.db import models


class Category(models.Model):
    """
    Model for the categories
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ('id', 'name', 'description')
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Model for the subcategories
    """
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'id')
        ordering = ['id']
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        
    def __str__(self):
        return self.name

    def __unicode__(self):
        return "{} {}".format(self.id, self.name)
