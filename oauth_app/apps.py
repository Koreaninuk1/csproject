from django.apps import AppConfig
from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig

class OauthAppConfig(AppConfig):
    name = 'oauth_app'
    default_auto_field = 'django.db.models.AutoField'

class ModifiedAccountConfig(AccountConfig):
    default_auto_field = 'django.db.models.AutoField'

class ModifiedSocialAccountConfig(SocialAccountConfig):
    default_auto_field = 'django.db.models.AutoField'
