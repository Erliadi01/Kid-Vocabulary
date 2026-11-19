import flet as ft
from app.theme import (
    DUO_GREEN, DUO_GREEN_RIM, DUO_GREEN_LIGHT,
    DUO_BLUE, DUO_BLUE_RIM, DUO_BLUE_LIGHT,
    DUO_ORANGE, DUO_ORANGE_RIM, DUO_ORANGE_LIGHT,
    DUO_YELLOW, DUO_YELLOW_RIM, DUO_YELLOW_LIGHT,
    DUO_PURPLE, DUO_PURPLE_RIM, DUO_PURPLE_LIGHT,
    WHITE, TEXT_MAIN, TEXT_SUB,
    tactile_button, tactile_card, hud_pill, modern_app_shell, modern_bottom_nav,
    soft_shadow, get_screen_metrics
)
from app.database import get_category_counts
from app.data.vocabulary import CATEGORIES
from app.dialogs import show_parent_gate, show_daily_quests, show_student_picker, show_class_leaderboard

def build_dashboard_screen(page: ft.Page, state, audio, navigate):
    """Screen 3: MAIN MENU / LEARNING DASHBOARD (Modern & Elegant Responsive Style)
    - Perfectly adapts to Laptop, iPad, and HP.
    - Floating top bar, greeting card, 4 rich category cards, and quick actions.
    - Fixed modern bottom navigation bar.
    """

    m = get_screen_metrics(page)
    is_mob = m["is_mobile"]
    is_tab = m["is_tablet"]
    is_desk = m["is_desktop"]

    # ==========================
    # 1. TOP FLOATING HUD ROW
    # ==========================
    avatar_info = state.avatar
    student_name = state.child_name or "Budi"

    # Student switcher pill
    student_pill = hud_pill(
        content=ft.Row(
            [
                ft.Text(avatar_info.get("emoji", "🦁"), size=16),
                ft.Text(student_name, size=11 if is_mob else 13, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
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
        on_click=lambda e: (audio.play_click(), show_student_picker(page, state, audio, on_selected_callback=lambda: navigate("dashboard"))),
        tooltip="Pilih siswa yang maju ke proyektor / smartboard",
    )

    # Stars pill
    stars_pill = hud_pill(
        content=f"⭐ {state.stars} Bintang" if not is_mob else f"⭐ {state.stars}",
        bg_color="#FFFBEB",
        border_color="#FDE68A",
        bottom_rim="#F59E0B",
        padding_h=12,
        padding_v=6,
    )

    # Sound toggle pill
    sound_icon_text = ft.Text("SUARA" if state.sound_enabled else "MUTE", size=10, weight=ft.FontWeight.W_800, color=TEXT_MAIN)
    sound_icon = ft.Icon(ft.Icons.VOLUME_UP if state.sound_enabled else ft.Icons.VOLUME_OFF, size=14, color=TEXT_MAIN)

    def toggle_sound(e):
        is_on = state.toggle_sound()
        audio.play_click()
        sound_icon_text.value = "SUARA" if is_on else "MUTE"
        sound_icon.name = ft.Icons.VOLUME_UP if is_on else ft.Icons.VOLUME_OFF
        if is_on:
            audio.speak("Sound on!")
        page.update()

    sound_pill = hud_pill(
        content=ft.Row([sound_icon, sound_icon_text], tight=True, spacing=4),
        bg_color=WHITE,
        padding_h=10,
        padding_v=6,
        on_click=toggle_sound,
        tooltip="Nyalakan/Matikan Suara",
    )

    parent_pill = hud_pill(
        content="🔒 GURU / ORTU" if is_desk else "🔒",
        bg_color=WHITE,
        padding_h=10,
        padding_v=6,
        on_click=lambda e: (audio.play_click(), show_parent_gate(page, state, audio, on_update_callback=lambda: page.update())),
        tooltip="Menu Khusus Orang Tua / Guru",
    )

    # In desktop/smartboard, include app logo brand badge & quick leaderboard button in top header
    left_header_items = []
    if is_desk:
        brand_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Text("🦁", size=18),
                    ft.Text("LET'S LEARN ENGLISH", size=12, weight=ft.FontWeight.W_900, color="#15803D"),
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

    right_header_items = []
    if is_desk:
        quick_board_btn = tactile_button(
            text="🏆 PERINGKAT KELAS",
            subtext=None,
            icon=None,
            bg_color=DUO_ORANGE,
            border_bottom=DUO_ORANGE_RIM,
            height=36,
            width=150,
            font_size=11,
            border_radius=12,
            on_click=lambda e: (audio.play_click(), show_class_leaderboard(page, state, audio, on_update_callback=lambda: navigate("dashboard"))),
        )
        right_header_items.append(quick_board_btn)
    right_header_items.extend([sound_pill, parent_pill])

    header_row = ft.Row(
        [
            ft.Row(left_header_items, spacing=8, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row(right_header_items, spacing=8, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ==========================
    # 2. GREETING BANNER
    # ==========================
    greeting_card = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(avatar_info.get("emoji", "🦁"), size=34 if is_desk else (28 if is_tab else 24)),
                            bgcolor=DUO_GREEN_LIGHT,
                            width=52 if is_desk else (44 if is_tab else 38),
                            height=52 if is_desk else (44 if is_tab else 38),
                            border_radius=ft.BorderRadius.all(14),
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(1.5, "#BBF7D0"),
                            shadow=soft_shadow(color="#10000000", blur=6, offset_y=2),
                        ),
                        ft.Column(
                            [
                                ft.Text(f"Halo, {student_name}! 👋", size=17 if is_desk else (15 if is_tab else 13), weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                                ft.Text("Pilih kategori belajar seru di bawah ini atau tantang dirimu di Kuis Kelas!", size=12 if is_desk else (11 if is_tab else 10), color=TEXT_SUB),
                            ],
                            spacing=2,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text("📅", size=14),
                                    ft.Text("Misi Harian", size=11, weight=ft.FontWeight.W_800, color="#15803D"),
                                ],
                                tight=True,
                                spacing=4,
                            ),
                            bgcolor="#DCFCE7",
                            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            border_radius=ft.BorderRadius.all(12),
                            border=ft.Border.all(1, "#86EFAC"),
                            on_click=lambda e: show_daily_quests(page, state, audio, on_update_callback=lambda: page.update()),
                            tooltip="Misi Harian",
                        ),
                    ],
                    spacing=6,
                    tight=True,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=WHITE,
        padding=ft.Padding.symmetric(horizontal=18, vertical=14 if is_desk else 12),
        border_radius=ft.BorderRadius.all(20),
        border=ft.Border(
            top=ft.BorderSide(1.5, "#E2E8F0"),
            left=ft.BorderSide(1.5, "#E2E8F0"),
            right=ft.BorderSide(1.5, "#E2E8F0"),
            bottom=ft.BorderSide(3.5, "#CBD5E1"),
        ),
        shadow=soft_shadow(color="#08000000", blur=8, offset_y=2),
    )

    # ==========================
    # 3. CATEGORY CARDS (RESPONSIVE GRID)
    # ==========================
    counts = get_category_counts()

    cat_palettes = {
        "animals": {"bg": "#F0FDF4", "border": "#DCFCE7", "rim": "#86EFAC", "text": "#15803D", "badge_bg": "#DCFCE7"},
        "fruits": {"bg": "#FFF7ED", "border": "#FFEDD5", "rim": "#FDBA74", "text": "#EA580C", "badge_bg": "#FFEDD5"},
        "colors": {"bg": "#FAF5FF", "border": "#F3E8FF", "rim": "#D8B4FE", "text": "#9333EA", "badge_bg": "#F3E8FF"},
        "numbers": {"bg": "#F0F9FF", "border": "#E0F2FE", "rim": "#7DD3FC", "text": "#0284C7", "badge_bg": "#E0F2FE"},
    }

    # Card dimensions adapt to screen
    if is_mob:
        card_w = int(max(140, (page.width - 36) / 2))
        card_h = 110
    elif is_tab:
        card_w = 340
        card_h = 125
    else: # Desktop & Classroom Smartboard
        card_w = 255
        card_h = 170

    category_cards = []

    for cat in CATEGORIES:
        cid = cat["id"]
        c_name = cat["name"]
        c_indo = cat["indonesian"]
        c_emoji = cat["emoji"]
        c_count = counts.get(cid, cat.get("item_count", 0))
        palette = cat_palettes.get(cid, cat_palettes["animals"])

        count_label = f"{c_count} Item"
        if cid == "animals":
            count_label = f"{c_count} Hewan"
        elif cid == "fruits":
            count_label = f"{c_count} Buah"
        elif cid == "colors":
            count_label = f"{c_count} Warna"
        elif cid == "numbers":
            count_label = f"{c_count} Angka"

        def make_cat_click(target_id, target_name):
            def on_card_click(e):
                audio.play_click()
                audio.speak(f"Let's explore {target_name}!")
                state.selected_category = target_id
                navigate("learn", category=target_id)
            return on_card_click

        if is_desk:
            # Widescreen 4-column rich card layout for laptop & smartboard
            card_content = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(c_emoji, size=32),
                                bgcolor=palette["badge_bg"],
                                width=52,
                                height=52,
                                border_radius=ft.BorderRadius.all(16),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text(count_label, size=10, weight=ft.FontWeight.W_800, color=palette["text"]),
                                bgcolor=palette["badge_bg"],
                                padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                border_radius=ft.BorderRadius.all(10),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(c_name, size=17, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                            ft.Text(f"({c_indo})", size=12, weight=ft.FontWeight.W_600, color=TEXT_SUB),
                        ],
                        spacing=2,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("Mulai Belajar", size=10, weight=ft.FontWeight.W_800, color=palette["text"]),
                                ft.Text("➔", size=11, weight=ft.FontWeight.W_900, color=palette["text"]),
                            ],
                            tight=True,
                            spacing=4,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor=palette["bg"],
                        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                        border_radius=ft.BorderRadius.all(10),
                        border=ft.Border.all(1, palette["border"]),
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        else:
            # Horizontal layout for mobile & tablet
            card_content = ft.Row(
                [
                    ft.Container(
                        content=ft.Text(c_emoji, size=28 if not is_mob else 24),
                        bgcolor=palette["badge_bg"],
                        width=46 if not is_mob else 40,
                        height=46 if not is_mob else 40,
                        border_radius=ft.BorderRadius.all(12),
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(c_name, size=13 if not is_mob else 11, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                            ft.Text(c_indo, size=10 if not is_mob else 9, weight=ft.FontWeight.W_600, color=TEXT_SUB),
                            ft.Container(
                                content=ft.Text(count_label, size=9 if not is_mob else 8, weight=ft.FontWeight.W_700, color=palette["text"]),
                                bgcolor=palette["badge_bg"],
                                padding=ft.Padding.symmetric(horizontal=6, vertical=1),
                                border_radius=ft.BorderRadius.all(6),
                            ),
                        ],
                        spacing=1,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                    ft.Text("➔", size=14, color=palette["text"], weight=ft.FontWeight.W_900),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        card = ft.Container(
            content=card_content,
            bgcolor=WHITE,
            width=card_w,
            height=card_h,
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            border_radius=ft.BorderRadius.all(20),
            border=ft.Border(
                top=ft.BorderSide(1.5, "#E2E8F0"),
                left=ft.BorderSide(1.5, "#E2E8F0"),
                right=ft.BorderSide(1.5, "#E2E8F0"),
                bottom=ft.BorderSide(3.5, palette["rim"]),
            ),
            shadow=soft_shadow(color="#0A000000", blur=8, offset_y=3),
            on_click=make_cat_click(cid, c_name),
            animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
        )
        category_cards.append(card)

    categories_grid = ft.Row(
        category_cards,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
        run_spacing=12,
    )

    # ==========================
    # 4. ACTION BUTTONS (SMARTBOARD & LAPTOP ERGONOMICS)
    # ==========================
    def on_quiz_click(e):
        audio.play_click()
        audio.speak("Quiz time! Let's test your knowledge!")
        navigate("quiz")

    # Main Quiz Action Button (Radiant Orange 3D)
    quiz_action_btn = tactile_button(
        text="🎯 MAIN KUIS SEKARANG",
        subtext="Uji Kemampuan & Kumpulkan Bintang! ⭐",
        bg_color=DUO_ORANGE,
        border_bottom=DUO_ORANGE_RIM,
        height=60 if is_desk else 52,
        width=525 if is_desk else (500 if is_tab else None),
        font_size=15 if is_desk else 14,
        border_radius=20 if is_desk else 18,
        on_click=on_quiz_click,
    )

    # Sub Action Button: Class Leaderboard (Sky Blue 3D)
    leaderboard_btn = tactile_button(
        text="🏆 Papan Peringkat Kelas (1-15 Siswa)",
        subtext="Lihat Skor & Bintang Seluruh Teman Sekelas 🥇" if is_desk else None,
        icon=None,
        bg_color=DUO_BLUE,
        border_bottom=DUO_BLUE_RIM,
        height=60 if is_desk else 44,
        width=525 if is_desk else (500 if is_tab else None),
        font_size=14 if is_desk else 12,
        border_radius=20 if is_desk else 16,
        on_click=lambda e: (audio.play_click(), show_class_leaderboard(page, state, audio, on_update_callback=lambda: navigate("dashboard"))),
    )

    if is_desk:
        # On Desktop & Smartboard: side-by-side action deck!
        actions_layout = ft.Row(
            [quiz_action_btn, leaderboard_btn],
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    else:
        # On Tablet & Mobile: stacked column
        actions_layout = ft.Column(
            [quiz_action_btn, leaderboard_btn],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # Bottom Nav Bar
    bottom_bar = modern_bottom_nav(active_tab="home", navigate=navigate, audio=audio, page=page, state=state)

    # Master Layout (No forced giant gaps!)
    screen_content = ft.Column(
        [
            header_row,
            ft.Container(height=4),
            greeting_card,
            ft.Container(height=4),
            categories_grid,
            ft.Container(height=6),
            actions_layout,
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return modern_app_shell(screen_content, page, bottom_nav=bottom_bar)
