from django.apps import AppConfig
from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig

class OauthAppConfig(AppConfig):
    name = 'oauth_app'
    default_auto_field = 'django.db.models.AutoField'
    label = 'oauthappconfig'

class ModifiedAccountConfig(AccountConfig):
    default_auto_field = 'django.db.models.AutoField'
    label = 'modifiedaccountconfig'

class ModifiedSocialAccountConfig(SocialAccountConfig):
    default_auto_field = 'django.db.models.AutoField'
    label = 'modifiedsocialaccountconfig'
