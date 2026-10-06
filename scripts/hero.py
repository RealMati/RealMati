"""Render hero.svg with today's Ethiopian date (Africa/Addis_Ababa). Stdlib only."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

MONTHS = [
    ("መስከረም", "Meskerem"), ("ጥቅምት", "Tikimt"), ("ኅዳር", "Hidar"),
    ("ታኅሣሥ", "Tahsas"), ("ጥር", "Tir"), ("የካቲት", "Yekatit"),
    ("መጋቢት", "Megabit"), ("ሚያዝያ", "Miyazya"), ("ግንቦት", "Ginbot"),
    ("ሰኔ", "Sene"), ("ሐምሌ", "Hamle"), ("ነሐሴ", "Nehase"),
    ("ጳጉሜን", "Pagume"),
]
ETHIOPIC_ERA_JDN = 1723856  # era offset for the 1461-day (4-year) cycle inverse


def gregorian_to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2, m2 = y + 4800 - a, m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def to_ethiopian(y: int, m: int, d: int) -> tuple[int, int, int]:
    days = gregorian_to_jdn(y, m, d) - ETHIOPIC_ERA_JDN
    cycle, r = divmod(days, 1461)  # 4-year cycle: 3*365 + 366
    n = r % 365 + 365 * (r // 1460)
    year = 4 * cycle + r // 365 - r // 1460
    return year, n // 30 + 1, n % 30 + 1


SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260" viewBox="0 0 900 260" role="img" aria-label="Mati Milkessa Ensermu. Today in Addis Ababa: {en_date}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b0f14"/>
      <stop offset="1" stop-color="#101923"/>
    </linearGradient>
    <linearGradient id="flag" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#078930"/>
      <stop offset="0.5" stop-color="#fcdd09"/>
      <stop offset="1" stop-color="#da121a"/>
    </linearGradient>
  </defs>
  <rect width="900" height="260" rx="14" fill="url(#bg)"/>
  <rect x="0" y="244" width="900" height="6" fill="url(#flag)"/>
  <text x="48" y="150" font-size="110" font-weight="700" fill="#f4f1ea"
        font-family="'Noto Sans Ethiopic','Abyssinica SIL',Nyala,Kefa,'Menlo',sans-serif">ማቲ</text>
  <text x="48" y="190" font-size="22" fill="#9fb3c8"
        font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">Mati Milkessa Ensermu</text>
  <text x="48" y="218" font-size="14" fill="#5f7388"
        font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">real-time systems / Elixir / TypeScript / Flutter</text>
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" text-anchor="end">
    <text x="852" y="92" font-size="13" fill="#5f7388">today in Addis Ababa</text>
    <text x="852" y="132" font-size="30" fill="#fcdd09"
          font-family="'Noto Sans Ethiopic','Abyssinica SIL',Nyala,Kefa,sans-serif">{gz_month} {day}</text>
    <text x="852" y="162" font-size="18" fill="#f4f1ea">{en_date}</text>
    <text x="852" y="188" font-size="13" fill="#5f7388">{greg}</text>
  </g>
</svg>
"""


def main() -> None:
    now = datetime.now(ZoneInfo("Africa/Addis_Ababa"))
    ey, em, ed = to_ethiopian(now.year, now.month, now.day)
    gz, en = MONTHS[em - 1]
    out = SVG.format(
        gz_month=gz, day=ed, en_date=f"{en} {ed}, {ey} EC",
        greg=now.strftime("%d %b %Y").lstrip("0"),
    )
    Path(__file__).resolve().parent.parent.joinpath("hero.svg").write_text(out, encoding="utf-8")
    print(f"{gz} {ed}, {ey} EC ({en}) <- {now:%Y-%m-%d}")


if __name__ == "__main__":
    main()
