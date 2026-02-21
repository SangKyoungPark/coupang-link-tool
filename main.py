"""쿠팡파트너스 링크 자동 생성 도구 — 텅장실험실

Usage:
    python main.py "청소기"              # 키워드 검색 → 상품 목록 출력
    python main.py "청소기" --youtube    # 유튜브 설명란 텍스트 생성
    python main.py "청소기" --copy       # 결과를 클립보드에 복사
    python main.py --urls "https://..." "https://..."  # URL 직접 딥링크 변환
"""

import argparse
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from coupang.search import SearchProducts
from coupang.deeplink import GenerateDeeplinks
from formatter.youtube import FormatYoutubeDescription

console = Console()


def DisplayProducts(products: list[dict]) -> None:
    """상품 목록을 테이블로 출력한다."""
    table = Table(title="🔍 쿠팡 검색 결과", show_lines=True)
    table.add_column("#", style="bold cyan", width=3)
    table.add_column("상품명", style="white", max_width=50)
    table.add_column("가격", style="green", justify="right")
    table.add_column("로켓", style="yellow", justify="center")
    table.add_column("딥링크", style="blue", max_width=40)

    for i, p in enumerate(products, 1):
        price = f"{int(p.get('productPrice', 0)):,}원"
        rocket = "🚀" if p.get("isRocket") else "-"
        deeplink = p.get("deeplink", "-")
        if len(deeplink) > 37:
            deeplink = deeplink[:37] + "..."

        table.add_row(str(i), p["productName"], price, rocket, deeplink)

    console.print(table)


def HandleSearch(keyword: str, limit: int, youtube: bool, copy: bool) -> None:
    """키워드 검색 → 딥링크 생성 → 출력"""
    console.print(f"\n[bold cyan]'{keyword}'[/] 검색 중...\n")

    # 1) 상품 검색
    try:
        products = SearchProducts(keyword, limit)
    except Exception as e:
        console.print(f"[bold red]검색 실패:[/] {e}")
        sys.exit(1)

    if not products:
        console.print("[yellow]검색 결과가 없습니다.[/]")
        return

    console.print(f"[green]{len(products)}개 상품 발견[/]")

    # 2) 딥링크 생성
    productUrls = [p["productUrl"] for p in products if p.get("productUrl")]
    if productUrls:
        try:
            console.print("딥링크 생성 중...")
            deeplinks = GenerateDeeplinks(productUrls)
            deeplinkMap = {d["originalUrl"]: d["shortenUrl"] for d in deeplinks}
            for p in products:
                p["deeplink"] = deeplinkMap.get(p["productUrl"], p["productUrl"])
        except Exception as e:
            console.print(f"[yellow]딥링크 생성 실패 (원본 URL 사용):[/] {e}")
            for p in products:
                p["deeplink"] = p["productUrl"]

    # 3) 출력
    DisplayProducts(products)

    # 4) 유튜브 설명란 생성
    if youtube or copy:
        description = FormatYoutubeDescription(
            products,
            copyToClipboard=copy,
            saveToFile=youtube,
        )
        console.print()
        console.print(Panel(description, title="📺 유튜브 설명란", border_style="bright_blue"))

        if copy:
            console.print("\n[bold green]✓ 클립보드에 복사되었습니다![/]")
        if youtube:
            console.print("[bold green]✓ output/ 폴더에 저장되었습니다![/]")


def HandleDeeplinks(urls: list[str], copy: bool) -> None:
    """URL 직접 딥링크 변환"""
    console.print(f"\n[bold cyan]{len(urls)}개 URL[/] 딥링크 변환 중...\n")

    try:
        deeplinks = GenerateDeeplinks(urls)
    except Exception as e:
        console.print(f"[bold red]딥링크 생성 실패:[/] {e}")
        sys.exit(1)

    table = Table(title="🔗 딥링크 변환 결과", show_lines=True)
    table.add_column("#", style="bold cyan", width=3)
    table.add_column("원본 URL", style="white", max_width=50)
    table.add_column("딥링크", style="green", max_width=50)

    result_lines = []
    for i, d in enumerate(deeplinks, 1):
        table.add_row(str(i), d["originalUrl"], d["shortenUrl"])
        result_lines.append(d["shortenUrl"])

    console.print(table)

    if copy:
        import pyperclip
        pyperclip.copy("\n".join(result_lines))
        console.print("\n[bold green]✓ 딥링크가 클립보드에 복사되었습니다![/]")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="쿠팡파트너스 링크 자동 생성 도구 — 텅장실험실",
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="검색할 상품 키워드",
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        help="딥링크로 변환할 쿠팡 URL 리스트",
    )
    parser.add_argument(
        "--youtube",
        action="store_true",
        help="유튜브 설명란 형식으로 출력 및 파일 저장",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="결과를 클립보드에 복사",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="검색 결과 수 (최대 10, 기본값: 10)",
    )

    args = parser.parse_args()

    # 배너 출력
    banner = Text("🧪 텅장실험실 — 쿠팡파트너스 링크 생성기", style="bold bright_magenta")
    console.print(Panel(banner, border_style="bright_magenta"))

    if args.urls:
        HandleDeeplinks(args.urls, args.copy)
    elif args.keyword:
        HandleSearch(args.keyword, args.limit, args.youtube, args.copy)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
