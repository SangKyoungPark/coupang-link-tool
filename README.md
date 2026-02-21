# 🧪 텅장실험실 — 쿠팡파트너스 링크 자동 생성 도구

유튜브 채널 **텅장실험실**의 쿠팡파트너스 제휴 링크를 자동으로 생성하는 CLI 도구입니다.

매 영상마다 수동으로 쿠팡에서 상품을 검색하고 링크를 생성하는 과정을 자동화하여, 콘텐츠 제작에 집중할 수 있도록 합니다.

## 주요 기능

- **키워드 검색** — 쿠팡파트너스 API로 상품 검색 (상품명, 가격, 로켓배송 여부)
- **딥링크 자동 생성** — 쿠팡 상품 URL → 제휴 추적 딥링크 변환
- **유튜브 설명란 생성** — 검색된 상품들을 유튜브 영상 설명란 형식으로 자동 포맷팅
- **클립보드 복사** — 생성된 텍스트를 바로 붙여넣기 가능

## 설치

```bash
pip install -r requirements.txt
```

## API 키 설정

1. [쿠팡파트너스](https://partners.coupang.com/) 가입
2. API 키 발급 (Access Key / Secret Key)
3. `.env.example`을 복사하여 `.env` 생성 후 키 입력

```bash
cp .env.example .env
```

```
COUPANG_ACCESS_KEY=your-access-key
COUPANG_SECRET_KEY=your-secret-key
```

## 사용법

```bash
# 키워드로 상품 검색
python main.py "청소기"

# 유튜브 설명란 텍스트 생성 + 파일 저장
python main.py "청소기" --youtube

# 결과를 클립보드에 복사
python main.py "청소기" --copy

# 유튜브 설명란 + 클립보드 복사 동시에
python main.py "청소기" --youtube --copy

# 쿠팡 URL 직접 딥링크 변환
python main.py --urls "https://www.coupang.com/vp/products/..." "https://www.coupang.com/vp/products/..."

# 검색 결과 수 제한 (최대 10)
python main.py "청소기" --limit 5
```

## 유튜브 설명란 출력 예시

```
▼ 오늘 실험한 제품들 ▼

1. 다이슨 청소기 V15 — 599,000원 (로켓배송)
   👉 https://link.coupang.com/xxxxx
2. 샤오미 무선청소기 — 89,000원
   👉 https://link.coupang.com/xxxxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📺 텅장실험실

※ 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
```

## 프로젝트 구조

```
coupang-link-tool/
├── .env                    # API 키 (gitignore)
├── .env.example            # API 키 템플릿
├── requirements.txt        # 의존성
├── main.py                 # CLI 진입점
├── coupang/
│   ├── auth.py             # HMAC-SHA256 인증
│   ├── search.py           # 상품 검색 API
│   ├── deeplink.py         # 딥링크 생성 API
│   └── config.py           # API 설정
├── formatter/
│   └── youtube.py          # 유튜브 설명란 포맷터
└── output/                 # 생성된 텍스트 저장
```

## API 제약사항

- 호출 제한: 1시간에 최대 10회
- 상품 수: 요청당 최대 10개
- 인증: HMAC-SHA256 (CEA 헤더)

## 기술 스택

- Python 3.10+
- requests — HTTP 호출
- hmac / hashlib — HMAC-SHA256 인증
- rich — CLI 터미널 출력
- python-dotenv — API 키 관리
- pyperclip — 클립보드 복사
