import re
from django.db.models import Q

from rest_framework.serializers import(
     ModelSerializer,
     EmailField, 
     CharField,
     ValidationError,
     SerializerMethodField,
     Serializer,
     )

from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings


from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

#reset password

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserDetailSerializer(ModelSerializer):
    name = SerializerMethodField()

    def get_name(self,instance):
        return instance.first_name +" "+ instance.last_name

    class Meta:
        model = User
        fields = ['username','name']



class UserCreateSerializer(ModelSerializer):
    token           = CharField(allow_blank=True, read_only=True)
    firstname       = CharField()
    lastname        = CharField() 
    email           = EmailField()
    phonenumber     = CharField()
    city            = CharField(allow_blank=True)
    class Meta:
        model = User
        fields = ['firstname', 'lastname','email', 'password', 'phonenumber','token']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_email(self, email):
        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]
        domain = email.split("@")[1]
        if domain not in allowedDomains:
            raise ValidationError('Invalid email address')
        user_qs = User.objects.filter(email__iexact=email)
        if user_qs.exists():
            raise ValidationError('User with this Email already exists')
        return email

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password

    def create(self, validatedData):
        email = validatedData['email']
        password = validatedData['password']
        firstname = validatedData['firstname']
        lastname = validatedData['lastname']
        phonenumber = validatedData['phonenumber']
        # idcard = validatedData['idcard']
        # usertype = validatedData['usertype']
        username = firstname+phonenumber
        userObj = User(email=email,username=username,first_name=firstname,
            last_name=lastname
            )

        userObj.set_password(password)
        userObj.save()
        # UserOtherInfo.objects.create(user=userObj, phone = phonenumber,
        #     idcard=idcard,isphvarified=True, usertype=usertype)


        # subject = 'Activate Your Meenfee Account'
        # message = render_to_string('account_activation_email.html', {
        #     'user': userObj,
        #     'domain':'localhost:8000',
        #     'uid': urlsafe_base64_encode(force_bytes(userObj.pk)).decode(),
        #     'token': account_activation_token.make_token(userObj),
        # })
        # userObj.email_user(subject, message)

        payload = jwt_payload_handler(userObj)
        token = jwt_encode_handler(payload)
        
        validatedData['token'] = token
        return validatedData


class UserLoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    def validate(self, data):
        userObj = None
        username = data['username']
        password = data['password']
         
        userA =User.objects.filter(username__iexact=username)
        userB =User.objects.filter(email__iexact=username)
        user = userA | userB
        user = user.exclude(email__isnull=True).exclude(email__iexact='').distinct()
        if user.exists() and user.count() == 1:           
            userObj = user.first()
        else:
            raise ValidationError("Email/username is not exist")
        if userObj:
            if not userObj.is_active:
                raise ValidationError("Please confirm your email")
            passPasses = userObj.check_password(password)
            if passPasses:
                payload = jwt_payload_handler(userObj)
                token = jwt_encode_handler(payload)
                data['username'] = userObj.username
                data['token'] = token
                return data
        raise ValidationError('Incorrect Password')
    class Meta:
        model = User
        fields = ['token', 'username','password']

        extra_kwargs = {'password': {'write_only': True}}

class ChangePasswordSerializer(Serializer):
    oldPassword = CharField(required=True)
    newPassword = CharField(required=True)

    def validate_oldPassword(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password
    def validate_newPassword(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password



class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()
    class Meta:
        model = User
        fields = [
           
            'email',
            
            
        ]

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('This e-mail address is not linked with any account'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)

