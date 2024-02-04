from django.test import TestCase
from model_bakery import baker
from product.models import Comment,Product
from account.models import User,Profile
from django.urls import reverse



class CommentTest(TestCase):
    def setUp(self):
        self.comm = baker.make(Comment,product__name='TV1',is_show=True)

    def test_str_obj(self):
        if self.comm.answer:
            x = 'جواب داده شد'
        else:
            x = 'جواب داده نشد'
        self.assertEqual(str(self.comm),f'True TV1 {x}')



class CommentViewTest(TestCase):
    def setUp(self):
        self.product =baker.make(Product,name='TV1',id=1000,is_show=True,_fill_optional=True,_create_files=True)
        self.user = User.objects.create_user(phone_number='09031231212')
        self.profile = Profile.objects.last()
        self.comm_show =baker.make(Comment,product=self.product,author=self.profile,text='masoud',is_show=True)

        self.comm_dontshow = baker.make(Comment,product=self.product,author=self.user,text='masoud',is_show=False)

    def test_get_comment_in_product_detail(self):
        url = reverse('product:detail',args=[self.product.category.name,self.product.id])
        resp = self.client.get(url)
        print(self.comm_show.author)
        self.assertEqual(resp.context['comments'],self.comm_show)
