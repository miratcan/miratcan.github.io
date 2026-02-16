"""
BTC Wyckoff birikim makalesi için candlestick grafikleri.
Binance'den veri çekip mplfinance ile grafik oluşturur.
"""
import requests
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates
from datetime import datetime, timezone
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_klines(symbol="BTCUSDT", interval="1d", start_str="2025-12-15", end_str="2026-02-16"):
    """Binance'den kline verisi çek."""
    start_ms = int(datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_ms = int(datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)

    url = "https://api.binance.com/api/v3/klines"
    all_klines = []
    current_start = start_ms

    while current_start < end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_ms,
            "limit": 1000,
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        all_klines.extend(data)
        current_start = data[-1][0] + 1

    df = pd.DataFrame(all_klines, columns=[
        "Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote volume", "Trades", "Taker buy base",
        "Taker buy quote", "Ignore"
    ])
    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    df.set_index("Open time", inplace=True)
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = df[col].astype(float)
    return df[["Open", "High", "Low", "Close", "Volume"]]


def make_style():
    """Koyu tema stili."""
    mc = mpf.make_marketcolors(
        up="#26a69a", down="#ef5350",
        edge="inherit",
        wick="inherit",
        volume={"up": "#26a69a", "down": "#ef5350"},
    )
    return mpf.make_mpf_style(
        marketcolors=mc,
        base_mpf_style="nightclouds",
        facecolor="#1a1a2e",
        edgecolor="#1a1a2e",
        figcolor="#1a1a2e",
        gridcolor="#2d2d44",
        gridstyle="--",
        gridaxis="both",
        y_on_right=True,
        rc={
            "font.size": 10,
            "axes.labelcolor": "#e0e0e0",
            "xtick.color": "#e0e0e0",
            "ytick.color": "#e0e0e0",
        }
    )


def draw_trendline(ax, df, date1, price1, date2, price2, extend_to_end=True):
    """İki nokta arasında trend çizgisi çiz. mplfinance integer index kullanır."""
    # mplfinance x ekseninde integer index kullanır, date2num değil
    x1 = df.index.get_loc(pd.Timestamp(date1))
    x2 = df.index.get_loc(pd.Timestamp(date2))

    if extend_to_end:
        x_end = len(df) - 1
        slope = (price2 - price1) / (x2 - x1)
        y_end = price1 + slope * (x_end - x1)
        ax.plot([x1, x_end], [price1, y_end],
                color="#ff9800", linewidth=2, linestyle="--", alpha=0.85)
    else:
        ax.plot([x1, x2], [price1, price2],
                color="#ff9800", linewidth=2, linestyle="--", alpha=0.85)


def generate_daily_chart():
    """Günlük grafik: genel Wyckoff görünümü."""
    print("1d kline verisi çekiliyor...")
    df = fetch_klines(interval="1d", start_str="2025-12-15", end_str="2026-02-17")
    print(f"  {len(df)} mum çekildi")

    style = make_style()

    fig, axes = mpf.plot(
        df, type="candle", style=style,
        volume=True,
        title="\nBTC/USDT Günlük — Wyckoff Birikim Formasyonu",
        ylabel="Fiyat (USDT)",
        ylabel_lower="Hacim",
        figsize=(14, 8),
        returnfig=True,
        tight_layout=True,
        scale_padding={"left": 0.1, "right": 0.3, "top": 0.6, "bottom": 0.6},
    )

    ax = axes[0]

    # $60k destek seviyesi
    ax.axhline(y=60000, color="#ef5350", linestyle=":", alpha=0.5, linewidth=1)

    # Faz etiketleri — transAxes kullanarak güvenilir konumlama
    ax.text(0.60, 0.62, "Faz A\nSert Düşüş", transform=ax.transAxes,
            fontsize=11, color="#ff9800", alpha=0.9, fontweight="bold",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a1a2e",
                      edgecolor="#ff9800", alpha=0.7))

    ax.text(0.88, 0.32, "Faz B/C\nBirikim", transform=ax.transAxes,
            fontsize=11, color="#26a69a", alpha=0.9, fontweight="bold",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a1a2e",
                      edgecolor="#26a69a", alpha=0.7))

    # $60k bounce — integer index koordinatlarıyla
    bounce_pos = df.index.get_loc(df.index[df.index >= "2026-02-06"][0])
    text_pos = df.index.get_loc(df.index[df.index >= "2026-01-26"][0])
    ax.annotate(
        "$60,000\nSpring?",
        xy=(bounce_pos, 60000),
        xytext=(text_pos, 62000),
        fontsize=10, color="#ef5350", alpha=0.9, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#ef5350", lw=2),
        ha="center",
    )

    output = os.path.join(SCRIPT_DIR, "btc-daily-wyckoff.png")
    fig.savefig(output, dpi=150, bbox_inches="tight",
                facecolor="#1a1a2e", edgecolor="none")
    print(f"  Kaydedildi: {output}")
    return output


def generate_4h_chart():
    """4 saatlik grafik: daralan üçgen detayı."""
    print("4h kline verisi çekiliyor...")
    df = fetch_klines(interval="4h", start_str="2026-02-04", end_str="2026-02-17")
    print(f"  {len(df)} mum çekildi")

    style = make_style()

    fig, axes = mpf.plot(
        df, type="candle", style=style,
        volume=True,
        title="\nBTC/USDT 4H — Daralan Üçgen Formasyonu",
        ylabel="Fiyat (USDT)",
        ylabel_lower="Hacim",
        figsize=(14, 8),
        returnfig=True,
        tight_layout=True,
        scale_padding={"left": 0.1, "right": 0.3, "top": 0.6, "bottom": 0.6},
    )

    ax = axes[0]

    # Daralan üçgen — veriden bilinen noktalar kullanarak çiz
    # Üst trend: ilk bounce tepesi (~$72.3k, 8 Şub) -> son tepe (~$71k, 15 Şub)
    # Alt trend: $60k dip (6 Şub) -> yükselen dipler (~$65k, 12 Şub)
    # İlk olarak gerçek veriden bu noktaları bulalım

    # Bounce sonrası bölge (6 Şubat sonrası)
    post_bounce = df[df.index >= "2026-02-06"]

    # Üst çizgi: bounce sonrası en yüksek high ve sonraki belirgin bir tepe
    # İlk yüksek tepe (6-8 Şubat arası)
    early_peak_zone = post_bounce["2026-02-06":"2026-02-09"]
    peak1_idx = early_peak_zone["High"].idxmax()
    peak1_val = early_peak_zone["High"].max()
    # İkinci tepe (13-15 Şubat arası)
    late_peak_zone = post_bounce["2026-02-13":"2026-02-16"]
    peak2_idx = late_peak_zone["High"].idxmax()
    peak2_val = late_peak_zone["High"].max()

    print(f"  Üst çizgi: {peak1_idx.strftime('%m/%d %H:%M')} ${peak1_val:.0f} -> {peak2_idx.strftime('%m/%d %H:%M')} ${peak2_val:.0f}")

    # Alt çizgi: $60k dip -> sonraki belirgin dip
    # İlk dip ($60k, 6 Şubat)
    trough1_zone = post_bounce["2026-02-06":"2026-02-07"]
    trough1_idx = trough1_zone["Low"].idxmin()
    trough1_val = trough1_zone["Low"].min()
    # İkinci dip (11-13 Şubat arası)
    trough2_zone = post_bounce["2026-02-11":"2026-02-13"]
    trough2_idx = trough2_zone["Low"].idxmin()
    trough2_val = trough2_zone["Low"].min()

    print(f"  Alt çizgi: {trough1_idx.strftime('%m/%d %H:%M')} ${trough1_val:.0f} -> {trough2_idx.strftime('%m/%d %H:%M')} ${trough2_val:.0f}")

    # Üçgen çizgilerini çiz
    draw_trendline(ax, df, peak1_idx, peak1_val, peak2_idx, peak2_val, extend_to_end=True)
    draw_trendline(ax, df, trough1_idx, trough1_val, trough2_idx, trough2_val, extend_to_end=True)

    # Hacim spike annotation — integer index kullan
    max_vol_idx = df["Volume"].idxmax()
    max_vol_pos = df.index.get_loc(max_vol_idx)
    ax.annotate(
        "Hacim patlaması\n$60k'dan dönüş",
        xy=(max_vol_pos, df["Low"].iloc[max_vol_pos]),
        xytext=(max_vol_pos + 8, df["Low"].iloc[max_vol_pos] - 2000),
        fontsize=9, color="#26a69a", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#26a69a", lw=1.5),
        ha="center"
    )

    # Trend çizgisi etiketleri
    ax.text(0.82, 0.82, "Tepeler\ndüşüyor", transform=ax.transAxes,
            fontsize=10, color="#ff9800", alpha=0.9, style="italic",
            fontweight="bold", ha="center")
    ax.text(0.82, 0.25, "Dipler\nyükseliyor", transform=ax.transAxes,
            fontsize=10, color="#ff9800", alpha=0.9, style="italic",
            fontweight="bold", ha="center")

    output = os.path.join(SCRIPT_DIR, "btc-4h-triangle.png")
    fig.savefig(output, dpi=150, bbox_inches="tight",
                facecolor="#1a1a2e", edgecolor="none")
    print(f"  Kaydedildi: {output}")
    return output


if __name__ == "__main__":
    generate_daily_chart()
    print()
    generate_4h_chart()
    print("\nTamamlandı!")
