import sys
import flet as ft
from app.state import AppState
from app.database import init_db
from app.audio_manager import AudioManager
from app.screens.start_screen import build_start_screen
from app.screens.avatar_screen import build_avatar_screen
from app.screens.dashboard_screen import build_dashboard_screen
from app.screens.learn_screen import build_learn_screen
from app.screens.quiz_screen import build_quiz_screen

def main(page: ft.Page):
    # Initialize SQLite database & seed 172 items if empty
    init_db()

    # Modern elegant background and zero padding
    page.bgcolor = "#F8FAFC"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.title = "Let's Learn English! 🌴🦁"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Ensure overlay is clean and empty (no Unknown control errors)
    try:
        page.overlay.clear()
    except Exception:
        pass

    # Desktop window size (if running as desktop window)
    try:
        if page.window:
            page.window.width = 1024
            page.window.height = 640
            page.window.min_width = 360
            page.window.min_height = 500
            page.window.resizable = True
            page.window.center()
    except Exception:
        pass

    # App State & Audio Engine (bound to page for mobile web audio)
    state = AppState()
    audio = AudioManager(state, page)

    # Navigation state tracking for responsive real-time resize
    current_nav = {"route": "start", "kwargs": {}}

    def navigate(route_name: str, is_resize: bool = False, **kwargs):
        if not is_resize:
            current_nav["route"] = route_name
            current_nav["kwargs"] = kwargs

        # Re-bind page to audio manager
        audio.set_page(page)

        page.controls.clear()

        if route_name == "start":
            view = build_start_screen(page, state, audio, navigate)
        elif route_name == "avatar":
            view = build_avatar_screen(page, state, audio, navigate)
        elif route_name == "dashboard":
            view = build_dashboard_screen(page, state, audio, navigate)
        elif route_name == "learn":
            cat = kwargs.get("category", state.selected_category)
            view = build_learn_screen(page, state, audio, navigate, category_id=cat)
        elif route_name == "quiz":
            cat = kwargs.get("category", None)
            view = build_quiz_screen(page, state, audio, navigate, category_id=cat)
        else:
            view = build_start_screen(page, state, audio, navigate)

        page.controls.append(view)
        page.update()

    # Real-time responsive resize handler
    def handle_resize(e):
        try:
            navigate(current_nav["route"], is_resize=True, **current_nav["kwargs"])
        except Exception:
            pass

    page.on_resize = handle_resize
    try:
        setattr(page, "on_resized", handle_resize)
    except Exception:
        pass

    # Initial Screen: Start Screen
    navigate("start")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
