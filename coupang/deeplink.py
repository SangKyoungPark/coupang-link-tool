"""쿠팡파트너스 딥링크 생성 모듈"""

import os
import json
import requests

from coupang.config import DOMAIN, DEEPLINK_PATH
from coupang.auth import GenerateHmac


def GenerateDeeplinks(urls: list[str]) -> list[dict]:
    """쿠팡 상품 URL들을 제휴 추적 딥링크로 변환한다.

    Args:
        urls: 쿠팡 상품 URL 리스트

    Returns:
        [{originalUrl, shortenUrl}] 형태의 딕셔너리 리스트
    """
    accessKey = os.getenv("COUPANG_ACCESS_KEY", "")
    secretKey = os.getenv("COUPANG_SECRET_KEY", "")

    if not accessKey or not secretKey:
        raise ValueError("COUPANG_ACCESS_KEY, COUPANG_SECRET_KEY가 .env에 설정되어 있지 않습니다.")

    authorization = GenerateHmac("POST", DEEPLINK_PATH, secretKey, accessKey)

    url = f"{DOMAIN}{DEEPLINK_PATH}"
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json;charset=UTF-8",
    }

    payload = {
        "coupangUrls": urls
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("rCode") != "0":
        raise RuntimeError(f"API 오류: {data.get('rMessage', '알 수 없는 오류')}")

    results = []
    for item in data.get("data", []):
        results.append({
            "originalUrl": item.get("originalUrl", ""),
            "shortenUrl": item.get("shortenUrl", ""),
        })

    return results
