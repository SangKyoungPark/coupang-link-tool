"""쿠팡파트너스 HMAC-SHA256 인증 모듈"""

import hmac
import hashlib
import time
from datetime import datetime, timezone


def GenerateHmac(method: str, url: str, secretKey: str, accessKey: str) -> str:
    """HMAC-SHA256 서명을 생성하여 Authorization 헤더 값을 반환한다.

    Args:
        method: HTTP 메서드 (GET, POST 등)
        url: 요청 경로 (쿼리스트링 포함)
        secretKey: 쿠팡파트너스 Secret Key
        accessKey: 쿠팡파트너스 Access Key

    Returns:
        CEA 포맷의 Authorization 헤더 값
    """
    datetime_now = datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")

    message = datetime_now + method.upper() + url

    signature = hmac.new(
        secretKey.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return f"CEA algorithm=HmacSHA256, access-key={accessKey}, signed-date={datetime_now}, signature={signature}"
