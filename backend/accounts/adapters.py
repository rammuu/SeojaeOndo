from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        data = request.data
        user.name = data.get('name', '')
        user.phone_number = data.get('phone_number', '')
        user.nickname = data.get('nickname', '')
        user.favorite_categories = data.get('favorite_categories', [])
        user.save()
        return user
