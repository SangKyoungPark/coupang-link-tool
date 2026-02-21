"""유튜브 설명란 포맷터"""

import os
from datetime import datetime

import pyperclip


def FormatYoutubeDescription(
    products: list[dict],
    channelName: str = "텅장실험실",
    copyToClipboard: bool = False,
    saveToFile: bool = True,
) -> str:
    """상품 목록을 유튜브 영상 설명란 형식으로 포맷팅한다.

    Args:
        products: 상품 정보 딕셔너리 리스트 (deeplink 포함)
        channelName: 채널 이름
        copyToClipboard: 클립보드에 복사할지 여부
        saveToFile: output/ 폴더에 파일로 저장할지 여부

    Returns:
        포맷팅된 유튜브 설명란 텍스트
    """
    lines = []
    lines.append(f"▼ 오늘 실험한 제품들 ▼")
    lines.append("")

    for i, product in enumerate(products, 1):
        name = product.get("productName", "상품명 없음")
        price = product.get("productPrice", 0)
        isRocket = product.get("isRocket", False)
        deeplink = product.get("deeplink", product.get("productUrl", ""))

        priceStr = f"{int(price):,}원" if price else "가격 정보 없음"
        rocketStr = " (로켓배송)" if isRocket else ""

        lines.append(f"{i}. {name} — {priceStr}{rocketStr}")
        lines.append(f"   👉 {deeplink}")
        lines.append("")

    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"📺 {channelName}")
    lines.append("")
    lines.append("※ 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

    result = "\n".join(lines)

    if copyToClipboard:
        try:
            pyperclip.copy(result)
        except pyperclip.PyperclipException:
            pass  # 클립보드 접근 불가 환경에서는 무시

    if saveToFile:
        outputDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(outputDir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filePath = os.path.join(outputDir, f"youtube_desc_{timestamp}.txt")
        with open(filePath, "w", encoding="utf-8", errors="replace") as f:
            f.write(result)

    return result
