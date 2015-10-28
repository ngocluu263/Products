from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Like(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return '{}'.format(self.user)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    modified_at = models.DateTimeField('modified_at', auto_now=True)
    likes = models.ManyToManyField(Like, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def like(self, user):
        try:
            like = Like.objects.get(user=user)
            self.likes.add(like)
        except Like.DoesNotExist:
            self.likes.create(user=user)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


class Comments(models.Model):
    product = models.ForeignKey(Product)
    comment_txt = models.TextField()
    pub_date = models.DateTimeField('created_at', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return '{} comment for {}'.format(self.comment_txt, self.product)
