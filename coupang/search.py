"""쿠팡파트너스 상품 검색 모듈"""

import os
import requests
from urllib.parse import urlencode

from coupang.config import DOMAIN, SEARCH_PATH, DEFAULT_LIMIT
from coupang.auth import GenerateHmac


def SearchProducts(keyword: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
    """키워드로 쿠팡 상품을 검색한다.

    Args:
        keyword: 검색 키워드
        limit: 반환할 상품 수 (최대 10)

    Returns:
        상품 정보 딕셔너리 리스트
        [{productId, productName, productPrice, productImage, productUrl, isRocket, isFreeShipping}]
    """
    accessKey = os.getenv("COUPANG_ACCESS_KEY", "")
    secretKey = os.getenv("COUPANG_SECRET_KEY", "")

    if not accessKey or not secretKey:
        raise ValueError("COUPANG_ACCESS_KEY, COUPANG_SECRET_KEY가 .env에 설정되어 있지 않습니다.")

    params = {
        "keyword": keyword,
        "limit": min(limit, 10),
    }
    queryString = urlencode(params)
    requestUrl = f"{SEARCH_PATH}?{queryString}"

    authorization = GenerateHmac("GET", requestUrl, secretKey, accessKey)

    url = f"{DOMAIN}{requestUrl}"
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json;charset=UTF-8",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("rCode") != "0":
        raise RuntimeError(f"API 오류: {data.get('rMessage', '알 수 없는 오류')}")

    products = []
    for item in data.get("data", {}).get("productData", []):
        products.append({
            "productId": item.get("productId", ""),
            "productName": item.get("productName", ""),
            "productPrice": item.get("productPrice", 0),
            "productImage": item.get("productImage", ""),
            "productUrl": item.get("productUrl", ""),
            "isRocket": item.get("isRocket", False),
            "isFreeShipping": item.get("isFreeShipping", False),
        })

    return products
