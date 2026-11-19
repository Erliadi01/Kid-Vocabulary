import os
import urllib.request
from pathlib import Path

IMAGES_DIR = Path("assets/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = {
    # 30 Animals
    "lion": "1f981",
    "monkey": "1f412",
    "elephant": "1f418",
    "giraffe": "1f992",
    "tiger": "1f405",
    "zebra": "1f993",
    "hippo": "1f99b",
    "parrot": "1f99c",
    "cat": "1f408",
    "dog": "1f415",
    "rabbit": "1f407",
    "bear": "1f43b",
    "panda": "1f43c",
    "koala": "1f428",
    "kangaroo": "1f998",
    "crocodile": "1f40a",
    "turtle": "1f422",
    "snake": "1f40d",
    "frog": "1f438",
    "fish": "1f41f",
    "shark": "1f988",
    "whale": "1f433",
    "dolphin": "1f42c",
    "penguin": "1f427",
    "eagle": "1f985",
    "owl": "1f989",
    "chicken": "1f414",
    "cow": "1f404",
    "horse": "1f40e",
    "sheep": "1f411",
    
    # 18 Accurate Fruits (100% Verified Twemoji Emojis)
    "apple": "1f34e",
    "green_apple": "1f34f",
    "banana": "1f34c",
    "orange": "1f34a",
    "lemon": "1f34b",
    "grape": "1f347",
    "strawberry": "1f353",
    "blueberry": "1fad0",
    "cherry": "1f352",
    "peach": "1f351",
    "pear": "1f350",
    "mango": "1f96d",
    "watermelon": "1f349",
    "melon": "1f348",
    "pineapple": "1f34d",
    "coconut": "1f965",
    "kiwi": "1f95d",
    "avocado": "1f951",
}

# Old inaccurate fruit images to remove
REMOVED_FRUITS = [
    "papaya.png", "durian.png", "mangosteen.png", "rambutan.png",
    "dragon_fruit.png", "guava.png", "lime.png", "plum.png",
    "pomegranate.png", "lychee.png", "starfruit.png", "jackfruit.png",
    "passion_fruit.png"
]

def clean_removed_images():
    removed_count = 0
    for filename in REMOVED_FRUITS:
        p = IMAGES_DIR / filename
        if p.exists():
            try:
                p.unlink()
                removed_count += 1
                print(f"[Clean] Removed obsolete image: {filename}")
            except Exception as e:
                print(f"[Clean] Error removing {filename}: {e}")
    if removed_count:
        print(f"[Clean] Total removed obsolete fruit images: {removed_count}")

def download_all():
    clean_removed_images()
    print(f"Starting download/verification of {len(ITEMS)} icons (30 Animals + 18 Fruits) to {IMAGES_DIR}...")
    success = 0
    failed = []

    for name, code in ITEMS.items():
        file_path = IMAGES_DIR / f"{name}.png"
        if file_path.exists() and file_path.stat().st_size > 0:
            success += 1
            print(f"[OK/Cached] {name}.png ({file_path.stat().st_size} bytes)")
            continue

        url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{code}.png"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(file_path, "wb") as f:
                    f.write(data)
            success += 1
            print(f"[{success}/{len(ITEMS)}] Downloaded: {name}.png ({len(data)} bytes)")
        except Exception as e:
            failed.append((name, str(e)))
            print(f"[ERROR] Failed {name}: {e}")

    print("\n" + "=" * 50)
    print(f"Finished! Total valid images: {success}/{len(ITEMS)}.")
    if failed:
        print(f"Failed count: {len(failed)}")
    print("=" * 50)

if __name__ == "__main__":
    download_all()
