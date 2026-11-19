import flet as ft
from app.theme import (
    DUO_GREEN, DUO_GREEN_RIM, DUO_GREEN_LIGHT,
    DUO_BLUE, DUO_BLUE_RIM, DUO_BLUE_LIGHT,
    DUO_ORANGE, DUO_ORANGE_RIM, DUO_ORANGE_LIGHT,
    DUO_YELLOW, DUO_YELLOW_RIM, DUO_YELLOW_LIGHT,
    WHITE, TEXT_MAIN, TEXT_SUB,
    tactile_button, tactile_card, hud_pill, modern_app_shell, modern_bottom_nav,
    soft_shadow, get_screen_metrics
)
from app.data.avatars import AVATARS, get_avatar_by_id

def build_avatar_screen(page: ft.Page, state, audio, navigate):
    """Screen 2: SELECT AVATAR SCREEN (Modern & Elegant Responsive Style)
    - Adapts to Laptop, iPad, and HP seamlessly.
    - 6 pure white tactile cards for animal avatars with modern pastel selection highlight.
    - Clean rounded nickname field and sleek start button.
    - Fixed modern bottom navigation bar.
    """

    m = get_screen_metrics(page)
    is_mob = m["is_mobile"]
    is_tab = m["is_tablet"]
    is_desk = m["is_desktop"]
    selected_id = [state.avatar_id]

    # Top Header
    back_btn = tactile_button(
        text="< KEMBALI",
        subtext=None,
        icon=None,
        bg_color=DUO_GREEN,
        border_bottom=DUO_GREEN_RIM,
        height=38,
        width=100 if not is_mob else 85,
        font_size=11,
        border_radius=14,
        on_click=lambda e: (audio.play_click(), navigate("dashboard")),
    )

    title_banner = hud_pill(
        content=ft.Row(
            [
                ft.Text("🐾", size=15),
                ft.Text("PILIH TEMAN AVATAR", size=12 if not is_mob else 11, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
            ],
            tight=True,
            spacing=4,
        ),
        bg_color=WHITE,
        padding_h=14,
        padding_v=6,
    )

    header_row = ft.Row(
        [
            back_btn,
            title_banner,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 6 Avatar Cards
    if is_mob:
        card_w = int(max(95, (page.width - 40) / 3))
        card_h = 105
    elif is_tab:
        card_w = 210
        card_h = 125
    else: # Laptop
        card_w = 260
        card_h = 130

    avatar_grid = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        run_spacing=10,
    )

    def render_avatar_cards():
        avatar_grid.controls.clear()
        for av in AVATARS:
            is_selected = av["id"] == selected_id[0]

            def make_click_handler(avatar_data):
                def on_card_click(e):
                    selected_id[0] = avatar_data["id"]
                    audio.play_click()
                    audio.speak(f"{avatar_data['name']}! {avatar_data['tagline']}")
                    render_avatar_cards()
                    page.update()
                return on_card_click

            card_inner = ft.Column(
                [
                    ft.Text(av["emoji"], size=34 if not is_mob else 28),
                    ft.Text(
                        av["name"],
                        size=12 if not is_mob else 10,
                        weight=ft.FontWeight.W_900,
                        color=TEXT_MAIN,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "DIPILIH ⭐" if is_selected else av["tagline"],
                            size=9 if not is_mob else 8,
                            weight=ft.FontWeight.W_700,
                            color=WHITE if is_selected else "#15803D",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor="#15803D" if is_selected else DUO_GREEN_LIGHT,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        border_radius=ft.BorderRadius.all(6),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=2,
            )

            card = tactile_card(
                content=card_inner,
                border_color=DUO_GREEN if is_selected else "#E2E8F0",
                bottom_rim_color=DUO_GREEN_RIM if is_selected else "#CBD5E1",
                bg_color=DUO_GREEN_LIGHT if is_selected else WHITE,
                border_radius=18,
                width=card_w,
                height=card_h,
                padding=ft.Padding.all(6),
                on_click=make_click_handler(av),
            )
            avatar_grid.controls.append(card)

    render_avatar_cards()

    # Nickname input (centered, responsive width)
    input_w = 480 if not is_mob else None
    nickname_field = ft.TextField(
        value=state.child_name,
        label="Nama Panggilan Anak",
        hint_text="Ketik nama...",
        text_align=ft.TextAlign.CENTER,
        text_size=14,
        height=48,
        width=input_w,
        border_radius=ft.BorderRadius.all(14),
        border_color="#CBD5E1",
        focused_border_color=DUO_GREEN,
        bgcolor=WHITE,
        color=TEXT_MAIN,
    )

    def on_start_adventure(e):
        name_val = nickname_field.value.strip() if nickname_field.value else "BUDI"
        state.child_name = name_val.upper()
        state.avatar_id = selected_id[0]
        chosen = get_avatar_by_id(state.avatar_id)
        state.avatar = chosen

        audio.play_correct()
        audio.speak(f"Awesome, {state.child_name}! Welcome, {chosen['species']}! Let's start learning!")
        navigate("dashboard")

    # Tactile Modern Adventure Button
    start_btn = tactile_button(
        text="SIMPAN & MULAI BELAJAR! 🚀",
        subtext=None,
        icon=None,
        bg_color=DUO_ORANGE,
        border_bottom=DUO_ORANGE_RIM,
        height=50,
        width=input_w,
        font_size=14,
        border_radius=18,
        on_click=on_start_adventure,
    )

    # Bottom Nav Bar
    bottom_bar = modern_bottom_nav(active_tab="avatar", navigate=navigate, audio=audio, page=page, state=state)

    screen_content = ft.Column(
        [
            header_row,
            ft.Container(height=4),
            avatar_grid,
            ft.Container(height=4),
            ft.Column([nickname_field, start_btn], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return modern_app_shell(screen_content, page, bottom_nav=bottom_bar)
