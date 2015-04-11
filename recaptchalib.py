#!/usr/bin/python
import sys
import requests
import json

'''
A Python implementation of Google's PHP example code for calling
the reCAPTCHA API.
'''


class ReCaptchaResponse:
    def __init__(self):
        self.success = None
        self.error_codes = None


class ReCaptcha:
    def __init__(self, secret, remote_ip, **kwargs):
        self.__SIGNUP_URL = kwargs.get('signup_url',
                                       "https://www.google.com/recaptcha/admin")
        self.__SITE_VERIFY_URL = kwargs.get('site_verify_url',
                                            "https://www.google.com/recaptcha/api/siteverify?")
        self.__secret = secret
        self.__remote_ip = remote_ip
        self.__version = kwargs.get('version',
                                    "python_1.0")

    def recaptcha(self, secret):
        if secret is None or secret == "":
            sys.exit(1)
        self.__secret = secret

    def __submit_get(self, path, params):
        response = requests.post(path, params)
        return response

    def verify_response(self, remote_ip, response):
        if response is None or len(response) == 0:
            recaptcha_response = ReCaptchaResponse()
            recaptcha_response.success = False
            recaptcha_response.error_codes = 'missing-input'
            return recaptcha_response

        get_response = self.__submit_get(self.__SITE_VERIFY_URL,
                                         {'secret': self.__secret,
                                          'remote_ip': self.__remote_ip,
                                          'v': self.__version})
        answers = json.dump(get_response, True)
        recaptcha_response = ReCaptchaResponse()

        if answers['success'].strip() is True:
            recaptcha_response.success = True
        else:
            recaptcha_response.success = False
            recaptcha_response.error_codes = answers['error-codes']

        return recaptcha_response
