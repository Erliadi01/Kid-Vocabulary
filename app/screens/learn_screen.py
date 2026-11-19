import os
import threading
import time
from pathlib import Path
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
from app.data.vocabulary import get_category_by_id
from app.database import get_vocabularies_by_category

def build_learn_screen(page: ft.Page, state, audio, navigate, category_id: str | None = None):
    """Screen 4: TAP-AND-LEARN SCREEN (Modern & Elegant Responsive Style)
    - Powered by local SQLite database (vocab_data.db)
    - 30 Animals & 18 Fruits rendered with crisp Twemoji PNG icons
    - 12 Colors rendered with vibrant circular swatches
    - 100 Numbers with segmented minimalist filter pills ("1-20", "21-40", ...)
    - Responsive GridView: 2 cols on HP, 3-4 on iPad, 4-5 on Laptop
    - Fixed modern bottom navigation bar
    """

    m = get_screen_metrics(page)
    is_mob = m["is_mobile"]
    is_desk = m["is_desktop"]

    cat_id = category_id or state.selected_category or "animals"
    category = get_category_by_id(cat_id)

    # Range state for numbers (default 1 to 20)
    current_range = {"min": 1, "max": 20 if cat_id == "numbers" else 100}

    # ==========================
    # 1. TOP HEADER & HUD BAR
    # ==========================
    back_btn = tactile_button(
        text="< MENU",
        subtext=None,
        icon=None,
        bg_color=DUO_GREEN,
        border_bottom=DUO_GREEN_RIM,
        height=40,
        width=110 if is_desk else (90 if not is_mob else 80),
        font_size=12 if is_desk else 11,
        border_radius=14,
        on_click=lambda e: (audio.play_click(), navigate("dashboard")),
    )

    cat_pill = hud_pill(
        content=ft.Row(
            [
                ft.Text(category["emoji"], size=20 if is_desk else 16),
                ft.Text(category["name"], size=14 if is_desk else (12 if not is_mob else 11), weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                ft.Text(f"({category['indonesian'].upper()})", size=11 if is_desk else 10, weight=ft.FontWeight.BOLD, color=TEXT_SUB),
            ],
            tight=True,
            spacing=6,
        ),
        bg_color=WHITE,
        padding_h=16 if is_desk else 12,
        padding_v=8 if is_desk else 6,
    )

    quiz_btn = tactile_button(
        text="🎯 KUIS KELAS" if is_desk else "🎯 KUIS",
        subtext=None,
        icon=None,
        bg_color=DUO_ORANGE,
        border_bottom=DUO_ORANGE_RIM,
        height=40,
        width=130 if is_desk else (90 if not is_mob else 80),
        font_size=12 if is_desk else 11,
        border_radius=14,
        on_click=lambda e: (audio.play_click(), audio.speak(f"Let's test your {category['name']} skills!"), navigate("quiz", category=cat_id)),
    )

    header_row = ft.Row(
        [
            back_btn,
            cat_pill,
            quiz_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Active word instruction banner
    banner_text = ft.Text(
        "Ketuk kartu kosakata atau ikon speaker 🔊 untuk mendengar pelafalan suara!",
        size=13 if is_desk else 11,
        weight=ft.FontWeight.W_800,
        color="#15803D",
        text_align=ft.TextAlign.CENTER,
    )

    banner_card = ft.Container(
        content=banner_text,
        bgcolor=WHITE,
        padding=ft.Padding.symmetric(horizontal=18, vertical=8),
        border_radius=ft.BorderRadius.all(16),
        border=ft.Border(
            top=ft.BorderSide(1.5, "#E2E8F0"),
            left=ft.BorderSide(1.5, "#E2E8F0"),
            right=ft.BorderSide(1.5, "#E2E8F0"),
            bottom=ft.BorderSide(2.5, "#CBD5E1"),
        ),
        alignment=ft.Alignment.CENTER,
        shadow=soft_shadow(color="#08000000", blur=4, offset_y=2),
    )

    # ==========================
    # 2. RESPONSIVE GRIDVIEW FOR VOCAB CARDS
    # ==========================
    cards_grid = ft.GridView(
        max_extent=240 if is_desk else (210 if not is_mob else 180),
        child_aspect_ratio=1.3 if is_desk else 1.15,
        spacing=12,
        run_spacing=12,
        height=540 if is_desk else (480 if not is_mob else 400),
    )

    def create_card_widget(item: dict) -> ft.Container:
        display_english = item["english"]
        speak_text = display_english
        if " - " in speak_text:
            speak_text = speak_text.split(" - ")[-1].strip()

        # Visual representation
        img_path = item.get("image_path")
        hex_col = item.get("hex_color")

        if img_path and (Path("assets") / img_path).exists():
            visual = ft.Image(
                src=img_path,
                width=52 if is_desk else 46,
                height=52 if is_desk else 46,
                fit=ft.BoxFit.CONTAIN,
            )
        elif hex_col:
            visual = ft.Container(
                width=46 if is_desk else 40,
                height=46 if is_desk else 40,
                bgcolor=hex_col,
                border_radius=ft.BorderRadius.all(23 if is_desk else 20),
                border=ft.Border.all(3, WHITE),
                shadow=soft_shadow(color="#20000000", blur=4, offset_y=2),
            )
        elif cat_id == "numbers":
            visual = ft.Container(
                content=ft.Text(
                    str(item["order_num"]),
                    size=24 if is_desk else 22,
                    weight=ft.FontWeight.W_900,
                    color=DUO_BLUE_RIM
                ),
                bgcolor=DUO_BLUE_LIGHT,
                padding=ft.Padding.symmetric(horizontal=14, vertical=2),
                border_radius=ft.BorderRadius.all(10),
                border=ft.Border.all(1.5, "#BAE6FD"),
            )
        else:
            visual = ft.Text(item.get("emoji", "🌟"), size=40 if is_desk else 34)

        # Minimalist modern LISTEN button
        listen_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Text("🔊", size=12 if is_desk else 11),
                    ft.Text("LISTEN", size=11 if is_desk else 10, weight=ft.FontWeight.W_900, color="#92400E"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
                tight=True,
            ),
            bgcolor=DUO_YELLOW_LIGHT,
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
            border_radius=ft.BorderRadius.all(12),
            border=ft.Border(
                top=ft.BorderSide(1, "#FDE047"),
                left=ft.BorderSide(1, "#FDE047"),
                right=ft.BorderSide(1, "#FDE047"),
                bottom=ft.BorderSide(2.5, DUO_YELLOW_RIM),
            ),
        )

        card_content = ft.Column(
            [
                visual,
                ft.Text(
                    display_english,
                    size=15 if is_desk else (13 if not is_mob else 12),
                    weight=ft.FontWeight.W_900,
                    color=TEXT_MAIN,
                    text_align=ft.TextAlign.CENTER,
                    no_wrap=False,
                ),
                ft.Text(
                    f"({item['indonesian']})",
                    size=12 if is_desk else (10 if not is_mob else 9),
                    weight=ft.FontWeight.W_600,
                    color=TEXT_SUB,
                    text_align=ft.TextAlign.CENTER,
                ),
                listen_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
        )

        if hex_col:
            border_bottom = hex_col
        elif cat_id == "animals":
            border_bottom = DUO_GREEN_RIM
        elif cat_id == "fruits":
            border_bottom = DUO_ORANGE_RIM
        elif cat_id == "numbers":
            border_bottom = DUO_BLUE_RIM
        else:
            border_bottom = "#CBD5E1"

        card_box = tactile_card(
            content=card_content,
            border_color="#E2E8F0",
            bottom_rim_color=border_bottom,
            bg_color=WHITE,
            border_radius=20,
            height=150 if is_desk else 140,
            padding=ft.Padding.all(8),
        )

        def make_learn_handler(target_card, target_item, word_to_speak):
            def on_card_tap(e):
                target_card.scale = 1.04
                banner_text.value = f"🔊 '{target_item['english']}' ({target_item['indonesian']})"
                page.update()

                audio.speak(word_to_speak)
                state.record_word_learned()

                def restore():
                    time.sleep(0.25)
                    target_card.scale = 1.0
                    page.update()
                threading.Thread(target=restore, daemon=True).start()

            return on_card_tap

        card_box.on_click = make_learn_handler(card_box, item, speak_text)
        return card_box

    def load_grid_items(range_min: int | None = None, range_max: int | None = None):
        cards_grid.controls.clear()
        if cat_id == "numbers":
            items = get_vocabularies_by_category(cat_id, range_min=range_min or 1, range_max=range_max or 20)
        else:
            items = get_vocabularies_by_category(cat_id)

        for it in items:
            cards_grid.controls.append(create_card_widget(it))

    # Initial load
    load_grid_items(current_range["min"], current_range["max"])

    # ==========================
    # 3. RANGE FILTER BAR (FOR NUMBERS 1-100)
    # ==========================
    range_filters_container = None
    if cat_id == "numbers":
        ranges = [
            ("1-20", 1, 20),
            ("21-40", 21, 40),
            ("41-60", 41, 60),
            ("61-80", 61, 80),
            ("81-100", 81, 100),
        ]
        range_buttons = []

        def make_range_click(r_label, r_min, r_max):
            def on_range_click(e):
                audio.play_click()
                current_range["min"] = r_min
                current_range["max"] = r_max
                load_grid_items(r_min, r_max)

                for b in range_buttons:
                    is_active = (b.data == r_label)
                    b.bgcolor = DUO_BLUE if is_active else WHITE
                    b.border = ft.Border(
                        top=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                        left=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                        right=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                        bottom=ft.BorderSide(3, DUO_BLUE_RIM if is_active else "#CBD5E1"),
                    )
                    b.content.color = WHITE if is_active else TEXT_MAIN

                banner_text.value = f"Angka {r_label}! Ketuk untuk mendengar suara 🔊"
                page.update()
            return on_range_click

        for r_label, r_min, r_max in ranges:
            is_active = (r_min == current_range["min"])
            btn = ft.Container(
                content=ft.Text(r_label, size=11, weight=ft.FontWeight.W_800, color=WHITE if is_active else TEXT_MAIN),
                bgcolor=DUO_BLUE if is_active else WHITE,
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border_radius=ft.BorderRadius.all(12),
                border=ft.Border(
                    top=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                    left=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                    right=ft.BorderSide(1.5, DUO_BLUE if is_active else "#E2E8F0"),
                    bottom=ft.BorderSide(3, DUO_BLUE_RIM if is_active else "#CBD5E1"),
                ),
                on_click=make_range_click(r_label, r_min, r_max),
                data=r_label,
            )
            range_buttons.append(btn)

        range_filters_container = ft.Row(
            range_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

    # Bottom Nav Bar
    bottom_bar = modern_bottom_nav(active_tab="learn", navigate=navigate, audio=audio, page=page, state=state)

    # Assemble screen
    content_list = [
        header_row,
        banner_card,
    ]
    if range_filters_container:
        content_list.append(range_filters_container)
    content_list.append(cards_grid)

    screen_content = ft.Column(
        content_list,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    return modern_app_shell(screen_content, page, bottom_nav=bottom_bar)
