from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
import datetime


class Like(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey('Product')

    def __str__(self):
        return '{} likes {}'.format(self.user, self.product)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    modified_at = models.DateTimeField('modified_at', auto_now=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def like(self, user):
        try:
            Like.objects.get(user=user, product__name=self.name)
        except Like.DoesNotExist:
            product = Product.objects.get(name=self.name)
            Like.objects.create(user=user, product=product)
            self.likes += 1

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def get_comments(self):
        now = datetime.datetime.now()
        last = now - datetime.timedelta(hours=24)
        return Comments.objects.filter(product__name=self.name, pub_date__range=(last, now)).order_by('-pub_date')

    def sort_likes(self):
        return self.objects.order_by('-likes')


class Comments(models.Model):
    product = models.ForeignKey(Product)
    comment_txt = models.TextField()
    pub_date = models.DateTimeField('created_at', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return '{} comment for {}'.format(self.comment_txt, self.product)
