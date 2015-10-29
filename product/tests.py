from django.test import TestCase
from . import views, models, forms
from django.contrib.auth import get_user_model
# Create your tests here.


class GetProductTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.view = views.ProductDetail.as_view()
        self.product = models.Product.objects.create(name='Product', description='Description', price='0.21')

    def test_get_request(self):
        request = self.client.get(self.product.get_absolute_url())
        self.assertEqual(request.status_code, 200)

    def test_get_absolute_url(self):
        self.assertIsNotNone(self.product.get_absolute_url())

    def test_product_details(self):
        request = self.client.get(self.product.get_absolute_url())
        self.assertContains(request, self.product.name)
        self.assertContains(request, self.product.description)
        self.assertContains(request, self.product.likes)
        self.assertContains(request, self.product.price)

    def test_comment_body(self):
        comment = models.Comments(product=self.product, comment_txt='Comment here')
        self.assertEqual(str(comment), 'Comment here comment for ' + str(self.product))

    def test_valid_data(self):
        form = forms.CommentsForm({
            'product': self.product.pk,
            'comment_txt': 'Comment here'
        })
        self.assertTrue(form.is_valid())

        comment = form.save()
        self.assertEqual(comment.product.pk, 1)
        self.assertEqual(comment.comment_txt, 'Comment here')

    def test_blank_data(self):
        form = forms.CommentsForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'product': [u'This field is required.'],
            'comment_txt': [u'This field is required.']
        })
