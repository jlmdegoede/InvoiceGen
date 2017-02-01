from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    contents = models.TextField()
    created = models.DateField()
    author = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    image = models.FileField(upload_to='static/images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_blogpost', kwargs={'blog_id': self.id, 'slug': slugify(self.title)})
