from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from rest_framework.authtoken.models import Token
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        print("[ACCOUNT_ADAPTER ENTRY] get_login_redirect_url called!")
        logger.info(f"[AccountAdapter] LOGIN_REDIRECT_URL from settings: {settings.LOGIN_REDIRECT_URL}")
        logger.info(f"[AccountAdapter] Request user: {request.user}, Is authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            logger.warning("[AccountAdapter] User is NOT authenticated. Redirecting without token.")
            return settings.LOGIN_REDIRECT_URL

        try:
            token, created = Token.objects.get_or_create(user=request.user)
            logger.info(f"[AccountAdapter] Token {'created' if created else 'retrieved'} for user {request.user}: {token.key}")
        except Exception as e:
            logger.error(f"[AccountAdapter] Error getting or creating token for user {request.user}: {e}")
            return settings.LOGIN_REDIRECT_URL

        parsed_url = urlparse(settings.LOGIN_REDIRECT_URL)
        query_params = parse_qs(parsed_url.query)
        query_params['token'] = [token.key]

        new_query = urlencode(query_params, doseq=True)
        
        redirect_url_with_token = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
        logger.info(f"[AccountAdapter] Final redirect URL with token: {redirect_url_with_token}")
        return redirect_url_with_token

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print(f"[SOCIALACCOUNT_ADAPTER PRE_SOCIAL_LOGIN] Incoming user (from social provider): {sociallogin.user}")
        print(f"[SOCIALACCOUNT_ADAPTER PRE_SOCIAL_LOGIN] Email from social provider: {sociallogin.account.extra_data.get('email')}")
        print(f"[SOCIALACCOUNT_ADAPTER PRE_SOCIAL_LOGIN] Is existing user identified by allauth? {sociallogin.is_existing}")
        if sociallogin.is_existing:
            print(f"[SOCIALACCOUNT_ADAPTER PRE_SOCIAL_LOGIN] Existing user PK: {sociallogin.user.pk}")
        # sociallogin.connect(request, sociallogin.user) might be relevant if auto-connect isn't happening.
        pass

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a new social user.
        This method is called when a user signs up via social login.
        """
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data

        # Populate user fields from extra_data
        # Note: Field names in extra_data can vary by provider.
        # Example for Naver: 'name', 'nickname', 'mobile' (for phone_number)
        # Example for Google: 'name', 'given_name', 'family_name', 'email' (email is usually handled by allauth)

        # Consolidate name
        # Naver might provide 'name', Google might provide 'name' or 'given_name' + 'family_name'
        if not user.name: # Only set if not already set by allauth or a previous step
            user.name = extra_data.get('name', '')
            if not user.name and extra_data.get('given_name'):
                 user.name = f"{extra_data.get('given_name', '')} {extra_data.get('family_name', '')}".strip()
        
        # Populate nickname
        if not user.nickname:  # Only set if not already set
            # Try to get nickname from Naver's 'nickname' field
            nickname = extra_data.get('nickname')
            
            if not nickname:
                # For Google, try 'given_name' or derive from email if 'given_name' is not available
                # Or if it's Naver and 'nickname' was empty
                if sociallogin.account.provider == 'google':
                    nickname = extra_data.get('given_name')
                    if not nickname:
                        # Fallback for Google: use email prefix if username is email-based
                        if '@' in user.username:
                           nickname = user.username.split('@')[0]
                        else:
                           nickname = user.username # Or just username if not email
            
            # If nickname is still None or an empty string after trying, set user.nickname to None.
            # This relies on the User model allowing null=True for nickname.
            
            # Before assigning, check if the derived nickname (if not None/empty) already exists for another user.
            # We only do this if we are about to set a non-empty nickname.
            if nickname:
                User = sociallogin.user.__class__ # Get the User model
                if User.objects.filter(nickname=nickname).exclude(pk=user.pk).exists():
                    # Nickname exists for another user. Force profile completion by setting to None.
                    logger.warning(f"Derived nickname '{nickname}' already exists. Setting to None for user {user.username}.")
                    user.nickname = None
                else:
                    user.nickname = nickname
            else:
                # If nickname is still None or empty after trying, set user.nickname to None.
                user.nickname = None

            # If your User model's nickname field cannot be blank/null and must be unique,
            # you'd need more sophisticated logic here to generate a unique nickname
            # e.g., by appending a random suffix if user.nickname is empty or already taken.
            # For now, we rely on CompleteProfile.vue if nickname is empty.

        # Populate phone_number
        # Naver might provide 'mobile'
        if not user.phone_number: # Assuming 'phone_number' is a field on your User model
            user.phone_number = extra_data.get('mobile', '') # Naver uses 'mobile'
            if not user.phone_number:
                 user.phone_number = extra_data.get('phone_number', '') # A more generic key

        # 'favorite_categories' is a custom field and unlikely to be in extra_data.
        # It should be populated via another process (e.g., a profile completion step).
        # user.favorite_categories = [] # Or some default if necessary

        user.save()
        return user

    # We are moving get_login_redirect_url to CustomAccountAdapter
    # as allauth uses the account adapter's method for the final login redirect.
    # The CustomSocialAccountAdapter's get_login_redirect_url might be used in other contexts
    # (e.g. connecting social accounts when already logged in), but for the initial
    # social login -> redirect, the account adapter is key.
    pass
