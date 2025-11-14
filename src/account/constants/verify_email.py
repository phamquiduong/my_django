from common.constants.base import ChoicesEnum

VERIFY_EMAIL_REDIS_KEY = 'verify-email:{user_id}'


class VerifyEmailType(str, ChoicesEnum):
    OTP = 'otp'
    TOKEN = 'token'
