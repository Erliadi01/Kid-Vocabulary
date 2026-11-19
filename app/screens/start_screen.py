import flet as ft
from app.theme import (
    DUO_GREEN, DUO_GREEN_RIM, DUO_GREEN_LIGHT,
    DUO_BLUE, DUO_BLUE_RIM, DUO_BLUE_LIGHT,
    DUO_ORANGE, DUO_ORANGE_RIM, DUO_ORANGE_LIGHT,
    DUO_YELLOW, DUO_YELLOW_RIM, DUO_YELLOW_LIGHT,
    WHITE, TEXT_MAIN, TEXT_SUB,
    tactile_button, tactile_card, hud_pill, modern_app_shell,
    soft_shadow, vibrant_shadow, get_screen_metrics
)
from app.dialogs import show_parent_gate, show_student_picker, show_class_leaderboard

def build_start_screen(page: ft.Page, state, audio, navigate):
    """Screen 1: LOGIN / START SCREEN (Modern & Elegant Responsive Style)
    - Adapts to Laptop, iPad, and HP seamlessly.
    - Clean top status bar, hero mascot card, and prominent action buttons.
    """

    m = get_screen_metrics(page)
    is_mob = m["is_mobile"]
    is_desk = m["is_desktop"]

    # ==========================
    # 1. TOP STATUS BAR
    # ==========================
    player_name = (state.child_name or "BUDI").upper()
    avatar_emoji = state.avatar.get("emoji", "🦁")

    # Left: Active Student Picker Pill
    student_pill = hud_pill(
        content=ft.Row(
            [
                ft.Text(avatar_emoji, size=16),
                ft.Text(player_name, size=11 if is_mob else 13, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                ft.Container(
                    content=ft.Text("▾", size=10, weight=ft.FontWeight.W_900, color=DUO_BLUE_RIM),
                    bgcolor="#EFF6FF",
                    padding=ft.Padding.symmetric(horizontal=5, vertical=1),
                    border_radius=ft.BorderRadius.all(6),
                ),
            ],
            tight=True,
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bg_color=WHITE,
        padding_h=12,
        padding_v=6,
        on_click=lambda e: (audio.play_click(), show_student_picker(page, state, audio, on_selected_callback=lambda: navigate("start"))),
        tooltip="Pilih siswa yang maju ke proyektor / smartboard",
    )

    # Stars counter pill
    stars_pill = hud_pill(
        content=f"⭐ {state.stars} Bintang" if not is_mob else f"⭐ {state.stars}",
        bg_color="#FFFBEB",
        border_color="#FDE68A",
        bottom_rim="#F59E0B",
        padding_h=12,
        padding_v=6,
    )

    # Right: Leaderboard & Parent Gate
    leaderboard_btn = tactile_button(
        text="🏆 PERINGKAT KELAS" if not is_mob else "🏆 KELAS",
        subtext=None,
        icon=None,
        bg_color=DUO_ORANGE,
        border_bottom=DUO_ORANGE_RIM,
        height=38,
        width=150 if not is_mob else 85,
        font_size=11,
        border_radius=14,
        on_click=lambda e: (audio.play_click(), show_class_leaderboard(page, state, audio, on_update_callback=lambda: navigate("start"))),
    )

    parent_btn = hud_pill(
        content="🔒 GURU / ORTU" if is_desk else "🔒",
        bg_color=WHITE,
        padding_h=10,
        padding_v=6,
        on_click=lambda e: (audio.play_click(), show_parent_gate(page, state, audio, on_update_callback=lambda: page.update())),
        tooltip="Menu Khusus Orang Tua / Guru",
    )

    left_header_items = []
    if is_desk:
        brand_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Text("🦁", size=18),
                    ft.Text("KATAKITA KIDS", size=12, weight=ft.FontWeight.W_900, color="#15803D"),
                ],
                spacing=5,
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=DUO_GREEN_LIGHT,
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            border_radius=ft.BorderRadius.all(14),
            border=ft.Border.all(1.5, "#BBF7D0"),
        )
        left_header_items.append(brand_badge)
    left_header_items.extend([student_pill, stars_pill])

    header_row = ft.Row(
        [
            ft.Row(left_header_items, spacing=8, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([leaderboard_btn, parent_btn], spacing=8, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ==========================
    # 2. HERO CARD (ELEGANT & SPACIOUS)
    # ==========================
    badge_dim = 110 if is_desk else (90 if not is_mob else 80)
    emoji_sz = 60 if is_desk else (52 if not is_mob else 46)

    mascot_badge = ft.Container(
        content=ft.Stack(
            [
                ft.Container(
                    width=badge_dim,
                    height=badge_dim,
                    border_radius=ft.BorderRadius.all(badge_dim // 2),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=["#FEF08A", "#FDE047", "#F59E0B"],
                    ),
                    border=ft.Border.all(4, WHITE),
                    shadow=vibrant_shadow(color="#30F59E0B", blur=20, offset_y=8),
                ),
                ft.Container(
                    content=ft.Text(avatar_emoji, size=emoji_sz),
                    width=badge_dim,
                    height=badge_dim,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            width=badge_dim,
            height=badge_dim,
            alignment=ft.Alignment.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
    )

    speech_bubble = ft.Container(
        content=ft.Row(
            [
                ft.Text("✨", size=14),
                ft.Text(f"Halo, {player_name}! Siap berpetualang belajar di proyektor kelas hari ini?", size=13 if is_desk else (12 if not is_mob else 11), weight=ft.FontWeight.W_800, color=TEXT_MAIN),
            ],
            tight=True,
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=DUO_GREEN_LIGHT,
        padding=ft.Padding.symmetric(horizontal=18, vertical=8),
        border_radius=ft.BorderRadius.all(14),
        border=ft.Border.all(1, "#BBF7D0"),
    )

    title_block = ft.Column(
        [
            ft.Text(
                "LET'S LEARN ENGLISH!",
                size=30 if is_desk else (24 if not is_mob else 20),
                weight=ft.FontWeight.W_900,
                color=TEXT_MAIN,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Aplikasi Edukasi Kosakata Bahasa Inggris Anak yang Menyenangkan & Interaktif",
                size=13 if is_desk else (12 if not is_mob else 11),
                weight=ft.FontWeight.W_600,
                color=TEXT_SUB,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 4 Feature Pills
    badge_animals = ft.Container(
        content=ft.Row([ft.Text("🐾", size=14), ft.Text("30 Hewan", size=12 if is_desk else 11, weight=ft.FontWeight.W_800, color="#15803D")], spacing=5, tight=True),
        bgcolor="#DCFCE7",
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=ft.BorderRadius.all(12),
        border=ft.Border.all(1, "#86EFAC"),
    )
    badge_fruits = ft.Container(
        content=ft.Row([ft.Text("🍎", size=14), ft.Text("18 Buah", size=12 if is_desk else 11, weight=ft.FontWeight.W_800, color="#EA580C")], spacing=5, tight=True),
        bgcolor="#FFF7ED",
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=ft.BorderRadius.all(12),
        border=ft.Border.all(1, "#FDBA74"),
    )
    badge_numbers = ft.Container(
        content=ft.Row([ft.Text("🔢", size=14), ft.Text("100 Angka", size=12 if is_desk else 11, weight=ft.FontWeight.W_800, color="#0284C7")], spacing=5, tight=True),
        bgcolor="#F0F9FF",
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=ft.BorderRadius.all(12),
        border=ft.Border.all(1, "#7DD3FC"),
    )
    badge_colors = ft.Container(
        content=ft.Row([ft.Text("🎨", size=14), ft.Text("12 Warna", size=12 if is_desk else 11, weight=ft.FontWeight.W_800, color="#9333EA")], spacing=5, tight=True),
        bgcolor="#FAF5FF",
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=ft.BorderRadius.all(12),
        border=ft.Border.all(1, "#D8B4FE"),
    )

    badges_row = ft.Row(
        [badge_animals, badge_fruits, badge_numbers, badge_colors],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        wrap=True,
    )

    hero_inner = ft.Column(
        [
            mascot_badge,
            speech_bubble,
            title_block,
            badges_row,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=14 if is_desk else 12,
    )

    hero_card = tactile_card(
        content=hero_inner,
        border_color="#E2E8F0",
        bottom_rim_color="#CBD5E1",
        bg_color=WHITE,
        border_radius=26,
        padding=ft.Padding.symmetric(horizontal=24, vertical=28 if is_desk else 22),
    )

    # ==========================
    # 3. ACTION BUTTONS (RESPONSIVE)
    # ==========================
    def on_quick_play(e):
        audio.play_click()
        audio.speak(f"Hello {state.child_name}! Let's start learning!")
        navigate("dashboard")

    def on_select_avatar(e):
        audio.play_click()
        audio.speak("Choose your favorite avatar!")
        navigate("avatar")

    # Primary Modern Green Action Button
    quick_play_btn = tactile_button(
        text="▶ MULAI BELAJAR",
        subtext="START LEARNING 🚀",
        bg_color=DUO_GREEN,
        border_bottom=DUO_GREEN_RIM,
        height=62 if is_desk else 54,
        width=350 if is_desk else (300 if not is_mob else None),
        font_size=16 if is_desk else 15,
        border_radius=20 if is_desk else 18,
        on_click=on_quick_play,
    )

    # Secondary Sleek Blue Action Button
    select_avatar_btn = tactile_button(
        text="🐾 PILIH AVATAR",
        subtext="CHOOSE AVATAR",
        bg_color=DUO_BLUE,
        border_bottom=DUO_BLUE_RIM,
        height=62 if is_desk else (54 if not is_mob else 46),
        width=350 if is_desk else (300 if not is_mob else None),
        font_size=15 if is_desk else 13,
        border_radius=20 if is_desk else 18,
        on_click=on_select_avatar,
    )

    if is_mob:
        action_layout = ft.Column(
            [quick_play_btn, select_avatar_btn],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        # Tablet & Laptop: side-by-side buttons
        action_layout = ft.Row(
            [quick_play_btn, select_avatar_btn],
            spacing=16,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    footnote = ft.Text(
        "🏫 Dirancang Khusus untuk Layar Sentuh Smartboard Kelas, Laptop, Tablet, & HP",
        size=11 if is_desk else 10,
        weight=ft.FontWeight.W_600,
        color=TEXT_SUB,
        text_align=ft.TextAlign.CENTER,
    )

    # Master Column
    screen_content = ft.Column(
        [
            header_row,
            ft.Container(height=4),
            hero_card,
            ft.Container(height=4),
            action_layout,
            footnote,
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return modern_app_shell(screen_content, page)
