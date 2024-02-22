from django.test import TestCase
from model_bakery import baker
from product.models import Comment,Product
from account.models import User,Profile
from django.urls import reverse
from django.contrib.messages import get_messages
import logging

logger = logging.getLogger(__name__)

class CommentTest(TestCase):
    def setUp(self):
        self.comm_by_answer = baker.make(Comment,product__name='TV1',answer='Hi',is_show=True)
        self.comm_with_out_answer = baker.make(Comment,product__name='TV2',answer='',is_show=True)

    def test_str_obj(self):
        contain_answer = 'جواب داده شد'

        doesnt_contain_answer = 'جواب داده نشد'
        self.assertEqual(str(self.comm_by_answer),f'True TV1 {contain_answer}')

        self.assertEqual(str(self.comm_with_out_answer),f'True TV2 {doesnt_contain_answer}')



class CommentViewTest(TestCase):
    def setUp(self):
        self.product =baker.make(Product,name='TV1',id=1000,is_show=True,_fill_optional=True,_create_files=True)
        self.user = User.objects.create_user(phone_number='09031231212')
        self.profile = Profile.objects.last()
        self.comm_show =baker.make(Comment,product=self.product,author=self.profile,text='masoud',is_show=True)

        self.comm_dontshow = baker.make(Comment,product=self.product,author=self.profile,text='masoud',is_show=False)

    def test_get_comment_in_product_detail(self):
        url = reverse('product:detail',args=[self.product.category.name,self.product.id])
        resp = self.client.get(url)

        self.assertIn(self.comm_show,resp.context['comments'])

        self.assertNotIn(self.comm_dontshow,resp.context['comments'])

        self.assertEqual(resp.context['comments'].count(),1)

    def test_post_comment_in_product_detail_in_signout_mode(self):
        url = reverse('product:detail',args=[self.product.category.name,self.product.id])
        resp = self.client.post(url,data={'text':'from masoud'})

        error_msg = 'لطفا ابتدا وارد حساب کاربری خود شوید'
        # self.assertEqual()
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages),1)

        self.assertEqual(str(messages[0]),str(error_msg))

    def test_post_comment_in_product_detail_in_signin_mode(self):
        self.client.force_login(self.user)
        url = reverse('product:detail',args=[self.product.category.name,self.product.id])
        resp = self.client.post(url,data={'text':'from masoud'})

        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages),1)

        sucess_msg  = 'پیام شما با موفقیت دریافت شد'

        self.assertEqual(str(messages[0]),str(sucess_msg))

    def test_post_many_comment(self):
        self.client.force_login(self.user)
        for _ in range(4):
            self.comm_show =baker.make(Comment,product=self.product,author=self.profile,text='masoud')

        url = reverse('product:detail',args=[self.product.category.name,self.product.id])
        resp = self.client.post(url,data={'text':'from masoud'})
        messages = list(get_messages(resp.wsgi_request))

        error_msg = 'شما نمیتوانید بیشتر از سه کامنت برای یک محصول ثبت کنید'
        self.assertEqual(str(messages[0]),str(error_msg))

