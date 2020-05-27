from django.db import models

class Account(models.Model):
    name       = models.CharField(verbose_name = '이름'       , max_length = 20)
    user_id    = models.CharField(verbose_name = '유저아이디' , max_length = 20)
    password   = models.CharField(verbose_name = '비밀번호'   , max_length = 60)
    email      = models.EmailField(verbose_name = "이메일"    , max_length = 254)
    post       = models.CharField(verbose_name="주소"         , max_length=250 , null=True)
    phone      = models.CharField(verbose_name = "폰번호"     , max_length = 100)
    is_active  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    kakao_id   = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "accounts"

class ShippingAddress(models.Model):
    account    = models.ForeignKey("Account"     , on_delete = models.CASCADE , null=True)
    address    = models.CharField(max_length=500 , null=True)
    is_default = models.BooleanField(False       , null=True)

    class Meta:
        db_table = "shipping_addresses"
