import requests

OUTPUT_FILE = "combined_playlist.m3u"

M3U_SOURCES = [
    "https://raw.githubusercontent.com/ryansnetcafe/ott-playlist/refs/heads/main/ryansnetcafe.m3u",
    "https://ppv.atone77721.workers.dev/SportsWebcast.m3u8",
]

MAIN_EPG = "https://raw.githubusercontent.com/BuddyChewChew/buddylive/refs/heads/main/en/videoall.xml"


def fetch_m3u(url):
    """Fetch M3U content with timeout and basic error handling."""
    try:
        res = requests.get(url, timeout=25)
        res.raise_for_status()
        if "#EXTM3U" in res.text:
            print(f"✅ Loaded: {url}")
            return res.text
        else:
            print(f"⚠️  Skipped (not a valid M3U playlist): {url}")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
    return ""


def parse_channels(text):
    """
    Parse M3U text into a list of (extinf_line, stream_url) tuples.
    Skips malformed entries (missing URL after #EXTINF).
    """
    channels = []
    lines = [l.strip() for l in text.splitlines() if l.strip() and l.strip() != "#EXTM3U"]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            # Next non-comment line should be the stream URL
            j = i + 1
            while j < len(lines) and lines[j].startswith("#"):
                j += 1
            if j < len(lines) and not lines[j].startswith("#"):
                channels.append((line, lines[j]))
                i = j + 1
                continue
        i += 1

    return channels


def main():
    all_channels = []
    seen_urls = set()
    total_dupes = 0

    for src in M3U_SOURCES:
        print(f"\n📡 Fetching → {src}")
        text = fetch_m3u(src)
        if not text:
            continue

        channels = parse_channels(text)
        print(f"   Found {len(channels)} channel entries")

        for extinf, url in channels:
            if url in seen_urls:
                total_dupes += 1
                continue
            seen_urls.add(url)
            all_channels.append((extinf, url))

    # Build output
    output_lines = [f'#EXTM3U url-tvg="{MAIN_EPG}"']
    for extinf, url in all_channels:
        output_lines.append(extinf)
        output_lines.append(url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"\n🎉 Saved to: {OUTPUT_FILE}")
    print(f"📺 Unique channels: {len(all_channels)}")
    print(f"🗑️  Duplicates removed: {total_dupes}")


if __name__ == "__main__":
    main()
