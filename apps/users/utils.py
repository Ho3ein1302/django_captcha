from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user) -> dict:
    """
        The function "get_tokens()" takes in "user" and returns a "dict".
        The "dict" gives us 'access token' and 'refresh token'.
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
