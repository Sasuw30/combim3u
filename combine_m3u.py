import requests

OUTPUT_FILE = "combined_playlist.m3u"

M3U_SOURCES = [
    "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/buddylive_v1.m3u",
    "https://ppv.atone77721.workers.dev/SportsWebcast.m3u8",



]

MAIN_EPG = "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/en/videoall.xml"


def fetch_m3u(url):
    """Fetch M3U content with timeout and basic error handling."""
    try:
        res = requests.get(url, timeout=25)
        if res.status_code == 200 and "#EXTM3U" in res.text:
            print(f"✅ Loaded {url}")
            return res.text
        else:
            print(f"⚠️ Invalid playlist: {url}")
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
    return ""


def main():
    combined = [f'#EXTM3U url-tvg="{MAIN_EPG}"']

    for src in M3U_SOURCES:
        print(f"📡 Fetching → {src}")
        text = fetch_m3u(src)
        if not text:
            continue

        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line and line != "#EXTM3U":
                combined.append(line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(combined))

    print(f"🎉 Combined playlist saved to: {OUTPUT_FILE}")
    print(f"📺 Total lines: {len(combined)}")


if __name__ == "__main__":
    main()
