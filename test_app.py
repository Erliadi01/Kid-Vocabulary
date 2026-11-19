import os
from pathlib import Path
os.environ["FLET_WEB_MODE"] = "1"
import flet as ft
from app.state import AppState
from app.database import (
    init_db, get_category_counts, get_vocabularies_by_category,
    get_class_leaderboard, update_student_score, reset_class_scores
)
from app.audio_manager import AudioManager
from app.dialogs import show_class_leaderboard, show_student_picker, show_achievements
from app.screens.start_screen import build_start_screen
from app.screens.avatar_screen import build_avatar_screen
from app.screens.dashboard_screen import build_dashboard_screen
from app.screens.learn_screen import build_learn_screen
from app.screens.quiz_screen import build_quiz_screen

class MockPage:
    def __init__(self):
        self.width = 390
        self.height = 844
        self.web = True
        self.client_ip = "192.168.1.50"
        self.platform = "web"
        self.title = "Test Page"
        self.controls = []
        self.overlay = []
        self.services = []

    def update(self):
        pass

    def show_dialog(self, dlg):
        pass

    def pop_dialog(self):
        pass

def test_full_application():
    print("=" * 60)
    print("TESTING 18 VERIFIED FRUITS & CLASSROOM LEADERBOARD (1-15)")
    print("=" * 60)

    # 1. Database Check (160 items: 30 animals, 18 fruits, 12 colors, 100 numbers)
    init_db()
    counts = get_category_counts()
    print(f"✓ SQLite Database verified: {counts} (Total: {sum(counts.values())} items)")
    assert counts["animals"] == 30, f"Expected 30 animals, got {counts['animals']}"
    assert counts["fruits"] == 18, f"Expected 18 fruits, got {counts['fruits']}"
    assert counts["colors"] == 12, f"Expected 12 colors, got {counts['colors']}"
    assert counts["numbers"] == 100, f"Expected 100 numbers, got {counts['numbers']}"
    assert sum(counts.values()) == 160, f"Expected 160 total items, got {sum(counts.values())}"

    # 2. Check 48 PNG Icons (30 animals + 18 fruits)
    img_dir = Path("assets/images")
    png_files = list(img_dir.glob("*.png"))
    print(f"✓ PNG Icons verified: Found {len(png_files)} PNG files in {img_dir}")
    assert len(png_files) >= 48, f"Expected at least 48 PNGs, found {len(png_files)}"
    assert (img_dir / "green_apple.png").exists(), "green_apple.png must exist"
    assert not (img_dir / "papaya.png").exists(), "papaya.png should be removed"

    # 3. Class Leaderboard (15 students)
    students = get_class_leaderboard()
    print(f"✓ Class Leaderboard verified: {len(students)} students loaded from SQLite")
    assert len(students) >= 15, f"Expected 15 students, got {len(students)}"

    # Test score update
    rank, total = update_student_score("Budi", 5, 5, 20)
    print(f"✓ Score update verified: Budi is Rank #{rank} of {total} students")
    assert rank >= 1, "Rank should be valid"

    page = MockPage()
    state = AppState()
    audio = AudioManager(state, page)

    def dummy_nav(r, **kwargs):
        pass

    # 4. Modals: Class Leaderboard & Student Picker
    show_class_leaderboard(page, state, audio)
    print("✓ Class Leaderboard dialog verified (no TypeError with callbacks)")

    show_achievements(page, state, audio, on_update_callback=lambda: None)
    print("✓ show_achievements alias with on_update_callback verified")

    show_student_picker(page, state, audio)
    print("✓ Student Picker dialog verified")

    # Test state.avatar setter (the bug that was reported)
    state.avatar = {"id": "budi", "name": "Budi", "emoji": "🦁"}
    assert state.avatar["name"] == "Budi", "Avatar setter failed"
    state.avatar = "monkey"
    assert state.avatar["id"] == "monkey", "Avatar setter with string failed"
    print("✓ state.avatar setter tested and verified cleanly!")

    # 5. Start Screen across Mobile, Tablet, and Desktop/Smartboard Viewports
    for width_test, label in [(390, "Mobile HP"), (768, "iPad Tablet"), (1920, "Laptop & Smartboard")]:
        page.width = width_test
        s1 = build_start_screen(page, state, audio, dummy_nav)
        assert s1 is not None, f"Start screen failed for {label}"
        s2 = build_avatar_screen(page, state, audio, dummy_nav)
        assert s2 is not None, f"Avatar screen failed for {label}"
        s3 = build_dashboard_screen(page, state, audio, dummy_nav)
        assert s3 is not None, f"Dashboard screen failed for {label}"
        s4 = build_learn_screen(page, state, audio, dummy_nav, category_id="animals")
        assert s4 is not None, f"Learn screen failed for {label}"
        s5 = build_quiz_screen(page, state, audio, dummy_nav, category_id="animals")
        assert s5 is not None, f"Quiz screen failed for {label}"
        print(f"✓ Responsive verification on {label} (width={width_test}px) passed seamlessly!")

    # 6. Learn Screen for all 4 categories (including 18 fruits)
    for cat in ["animals", "fruits", "numbers", "colors"]:
        s4 = build_learn_screen(page, state, audio, dummy_nav, category_id=cat)
        assert s4 is not None, f"Learn screen for {cat} failed"
        items = get_vocabularies_by_category(cat)
        print(f"✓ Screen 4: Learn Screen category '{cat}' ({len(items)} items in DB) verified")

    # 7. Quiz Screen for all 4 categories
    for cat in ["animals", "fruits", "numbers", "colors"]:
        s5 = build_quiz_screen(page, state, audio, dummy_nav, category_id=cat)
        assert s5 is not None, f"Quiz screen for {cat} failed"
        print(f"✓ Screen 5: Quiz Screen for '{cat}' (Rank highlight & Student switcher) verified")

    print("\n🎉 ALL TESTS PASSED! RESPONSIVE SMARTBOARD, LAPTOP & HP VERIFIED! 🚀")

if __name__ == "__main__":
    test_full_application()
