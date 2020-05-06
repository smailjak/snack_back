from django.db import models

class Account(models.Model):
    name = models.CharField(verbose_name = '이름', max_length = 20)
    user_id = models.CharField(verbose_name = '이름', max_length = 20)
    password = models.CharField(verbose_name = '비밀번호', max_length = 60)
    email = models.EmailField(max_length = 254)
    phone = models.CharField(verbose_name="이메일", max_length = 100) # 우선 charfield로 했는데 인증할 수 있게 phoefield?로 바꿔야함
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "accounts"