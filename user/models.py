from django.db.models import *

class User(Model):
    email = EmailField(null=False, unique=True)
    mobile = DecimalField(null=False, unique=True, max_digits=10, decimal_places=0)
    first_name = CharField(max_length=25)
    last_name = CharField(max_length=25)
    password = CharField(max_length=64, null=False)
    active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email

class Home(Model):
    name = CharField(max_length=50, null=False)
    root_user = ForeignKey(User, on_delete=RESTRICT)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "home"

    def __str__(self):
        return self.root_user.email

class HomeUser(Model):
    home = ForeignKey(Home, on_delete=RESTRICT)
    user = ForeignKey(User, on_delete=RESTRICT)
    is_root = BooleanField(default=False)

    class Meta:
        db_table = "home_user"

    def __str__(self):
        return self.user.email

class ForgotPasswordToken(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    token = CharField(null=False, max_length=32, primary_key=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "forgot_password_token"

    def __str__(self):
        return self.user.email