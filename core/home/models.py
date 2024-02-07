from django.db import models



class SiteSettings(models.Model):
    top_banner = models.ImageField()
    site_logo = models.ImageField()
    left_sidebar_banner_1 = models.ImageField()
    left_sidebar_banner_2 = models.ImageField()
    footer_seo_text = models.TextField()
    is_active = models.BooleanField(default=True)


class Slider(models.Model):
    image = models.ImageField()


class NewsLatter(models.Model):
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.email


class Navbar(models.Model):
    name = models.CharField(max_length=250)
    link = models.CharField(max_length=250, null=True)


    def __str__(self):
        return self.name


class Footer(models.Model):
    name = models.CharField(max_length=250)


    def __str__(self):
        return self.name


class SubFooter(models.Model):
    parent = models.ForeignKey(Footer,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=250)
    link = models.CharField(max_length=250,default="#")


    def __str__(self):
        return self.name
