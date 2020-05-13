import json

import pytest
from django.test import TestCase, Client

from .models import Account
from .views import (SignUpView,
                    SignInView,
                    ProfileView)


class TestSignUp(TestCase):
    def setUp(self):
        Account.objects.create(
            name     = 'name-setup',
            user_id  = 'user-setup',
            password = 'pass-setup',
            email    = 'email-setup',
            phone    = 'phone-setup'
        )
    
    def tearDown(self):
        Account.objects.all().delete()

    def test_post_return_200(self):
        '''
        회원 가입 성공 테스트
        '''
        client = Client()
        payload = {
            'name'     : 'name-test',
            'user_id'  : 'user-test',
            'password' : 'pass-test',
            'email'    : 'email-test',
            'phone'    : 'phone-test'
        }

        response = client.post('/account/sign-up', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 200)

    def test_post_existing_user_id_return_400(self):
        '''
        회원 가입 시 이메일 중복 테스트
        '''
        client  = Client()
        payload = {
            'name': 'name-test',
            'user_id': 'user-setup'
        }

        response = client.post('/account/sign-up', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 400)

    def test_post_invalid_key(self):
        '''
        회원 가입 시 키 유효성 테스트
        '''
        client = Client()
        payload = {
            'name': 'name-test',
            'user_id': 'user-test'
        }
        
        response = client.post('/account/sign-up', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KEY'})


class TestSignIn(TestCase):
    def setUp(self):
        Account.objects.create(
            name     = 'name-setup',
            user_id  = 'user-setup',
            password = 'pass-setup',
            email    = 'email-setup',
            phone    = 'phone-setup'
        )
    
    def tearDown(self):
        Account.objects.all().delete()

    def test_post_return_200(self):
        '''
        로그인 성공 테스트
        '''
        client = Client()
        payload = {
            'name'     : 'name-setup',
            'user_id'  : 'user-setup',
            'password' : 'pass-setup',
            'email'    : 'email-setup',
            'phone'    : 'phone-setup'
        }

        response = client.post('/account/sign-in', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 200)

    def test_post_wrong_password_return_401(self):
        '''
        로그인 시 비밀번호 틀렸을 때 테스트
        '''
        client = Client()
        payload = {
            'user_id': 'user-setup',
            'password': 'pass-wrong',
        }

        response = client.post('/account/sign-in', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 401)


    def test_post_invalid_key(self):
        '''
        로그인 시 키 유효성 테스트
        '''
        client  = Client()
        payload = {
        }

        response = client.post('/account/sign-in', data=json.dumps(payload), content_type = "application/json")

        self.assertEqual(response.status_code, 400)

