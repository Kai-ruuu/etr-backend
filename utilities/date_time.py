from backend.utilities.environment import envi

from datetime import datetime, timedelta, timezone

reset_token_lifespan = envi('TOKEN_RESET_EXPIRATION_SECONDS') or 1800
short_lifespan = envi('TOKEN_SHORT_ACCESS_EXPIRATION_SECONDS') or 3600
long_lifespan = envi('TOKEN_LONG_ACCESS_EXPIRATION_SECONDS') or 2_592_000

def get_session_cookie_lifespan_seconds(remembered: bool) -> int:
   return long_lifespan if remembered else short_lifespan

def utc_now() -> datetime:
   return datetime.now(timezone.utc)

def auth_reset_utc_now_expires_at() -> datetime:
   return utc_now() + timedelta(seconds=reset_token_lifespan)

def auth_login_utc_now_expires_at(remembered: bool) -> datetime:
   return utc_now() + timedelta(seconds=get_session_cookie_lifespan_seconds(remembered))