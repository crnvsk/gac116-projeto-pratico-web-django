from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Attempt to get the token from the 'Authorization' header (default behavior)
        header = self.get_header(request)
        if header is None:
            # If no header, check for the token in the cookie
            raw_token = request.COOKIES.get('access_token')
            if not raw_token:
                return None  # No token found
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed as exc:
            raise AuthenticationFailed("Invalid token or expired.")

        return self.get_user(validated_token), validated_token