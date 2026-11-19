import random
import threading
import time
from pathlib import Path
import flet as ft
from app.theme import (
    DUO_GREEN, DUO_GREEN_RIM, DUO_GREEN_LIGHT,
    DUO_BLUE, DUO_BLUE_RIM, DUO_BLUE_LIGHT,
    DUO_ORANGE, DUO_ORANGE_RIM, DUO_ORANGE_LIGHT,
    DUO_YELLOW, DUO_YELLOW_RIM, DUO_YELLOW_LIGHT,
    DUO_RED, DUO_RED_RIM, DUO_RED_LIGHT,
    DUO_PURPLE, DUO_PURPLE_RIM, DUO_PURPLE_LIGHT,
    WHITE, TEXT_MAIN, TEXT_SUB,
    tactile_button, tactile_card, hud_pill, modern_app_shell, modern_bottom_nav,
    soft_shadow, get_screen_metrics
)
from app.data.vocabulary import get_category_by_id
from app.database import get_connection, update_student_score
from app.dialogs import show_student_picker, show_class_leaderboard

OPTION_THEMES = [
    {"border": DUO_BLUE, "rim": DUO_BLUE_RIM, "badge_bg": DUO_BLUE_LIGHT},
    {"border": DUO_GREEN, "rim": DUO_GREEN_RIM, "badge_bg": DUO_GREEN_LIGHT},
    {"border": DUO_ORANGE, "rim": DUO_ORANGE_RIM, "badge_bg": DUO_ORANGE_LIGHT},
    {"border": DUO_PURPLE, "rim": DUO_PURPLE_RIM, "badge_bg": DUO_PURPLE_LIGHT},
]

def generate_quiz_questions(category_id: str | None = None, num_questions: int = 5):
    """Generates quiz questions with 1 correct target and 3 distractors from SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    if category_id and category_id != "all":
        cursor.execute("SELECT * FROM vocabularies WHERE category = ? ORDER BY RANDOM() LIMIT ?", (category_id, num_questions * 4))
    else:
        cursor.execute("SELECT * FROM vocabularies ORDER BY RANDOM() LIMIT ?", (num_questions * 4,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if len(rows) < 4:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vocabularies ORDER BY RANDOM() LIMIT 20")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

    questions = []
    used_ids = set()

    for item in rows:
        if len(questions) >= num_questions:
            break
        if item["id"] in used_ids:
            continue
        used_ids.add(item["id"])
        target = item
        distractor_pool = [x for x in rows if x["id"] != target["id"]]
        if len(distractor_pool) < 3:
            continue
        distractors = random.sample(distractor_pool, 3)
        choices = [target] + distractors
        random.shuffle(choices)
        questions.append({
            "target": target,
            "choices": choices,
        })

    return questions

def build_quiz_screen(page: ft.Page, state, audio, navigate, category_id: str | None = None):
    """Screen 5: QUIZ TIME & REWARD SCREEN (Modern & Elegant Responsive Style)
    - Adapts to Laptop, iPad, and HP seamlessly.
    - Floating top bar, progress bar, hero question card, and 4 tactile choice cards.
    - Bottom action buttons and fixed modern bottom navigation bar.
    """

    m = get_screen_metrics(page)
    is_mob = m["is_mobile"]
    is_tab = m["is_tablet"]
    is_desk = m["is_desktop"]

    cat_id = category_id or state.selected_category or "animals"
    category = get_category_by_id(cat_id)

    session_data = {
        "current_index": 0,
        "score_correct": 0,
        "stars_earned": 0,
        "lives": 3,
        "selected_choice": None,
        "checked": False,
        "questions": generate_quiz_questions(cat_id, 5),
        "is_finished": False,
    }

    content_slot = ft.Container()

    def render_current_view():
        if session_data["is_finished"]:
            render_score_view()
        else:
            render_question_view()
        page.update()

    def render_question_view():
        idx = session_data["current_index"]
        total_q = len(session_data["questions"])
        q = session_data["questions"][idx]
        target = q["target"]

        session_data["selected_choice"] = None
        session_data["checked"] = False

        # ==========================
        # 1. HEADER ROW & STATUS BADGE
        # ==========================
        back_btn = tactile_button(
            text="< MENU",
            subtext=None,
            icon=None,
            bg_color=DUO_GREEN,
            border_bottom=DUO_GREEN_RIM,
            height=40,
            width=110 if is_desk else (95 if not is_mob else 85),
            font_size=12 if is_desk else 11,
            border_radius=14,
            on_click=lambda e: (audio.play_click(), navigate("dashboard")),
        )

        cat_badge = hud_pill(
            content=ft.Row(
                [
                    ft.Text(category["emoji"], size=18 if is_desk else 15),
                    ft.Text(category["name"], size=13 if is_desk else (12 if not is_mob else 11), weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                ],
                tight=True,
                spacing=5,
            ),
            bg_color=WHITE,
            padding_h=14 if is_desk else 12,
            padding_v=8 if is_desk else 6,
        )

        lives_str = "❤️" * max(1, session_data["lives"])
        status_badge = hud_pill(
            content=ft.Row(
                [
                    ft.Text(lives_str, size=14 if is_desk else 12),
                    ft.Text(f"| ⭐ {state.stars}", size=12 if is_desk else 11, weight=ft.FontWeight.W_900, color=DUO_ORANGE_RIM),
                ],
                tight=True,
                spacing=5,
            ),
            bg_color=WHITE,
            border_color="#FDE047",
            bottom_rim=DUO_YELLOW_RIM,
            padding_h=12 if is_desk else 10,
            padding_v=8 if is_desk else 6,
        )

        header_bar = ft.Row(
            [
                back_btn,
                cat_badge,
                status_badge,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Progress bar: 'Pertanyaan X dari Y' with active student indicator
        progress_val = (idx + 1) / total_q
        student_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("👤 Siswa:", size=11, color=TEXT_SUB),
                    ft.Text(f"{state.avatar.get('emoji', '🦁')} {state.child_name}", size=12, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                    ft.Container(
                        content=ft.Text("Ganti ▾", size=9, weight=ft.FontWeight.W_900, color=DUO_BLUE_RIM),
                        bgcolor="#EFF6FF",
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        border_radius=ft.BorderRadius.all(8),
                        border=ft.Border.all(1, "#BAE6FD"),
                        on_click=lambda e: (audio.play_click(), show_student_picker(page, state, audio, on_selected_callback=lambda: render_current_view())),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
                tight=True,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=ft.BorderRadius.all(10),
            bgcolor=WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
        )

        progress_block = ft.Column(
            [
                student_bar,
                ft.Row(
                    [
                        ft.Text(f"Pertanyaan {idx + 1} dari {total_q}", size=12 if not is_mob else 11, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                        ft.Text(f"+{session_data['stars_earned']} Bintang ⭐", size=12 if not is_mob else 11, weight=ft.FontWeight.W_800, color=DUO_ORANGE_RIM),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(
                    value=progress_val,
                    height=6,
                    color=DUO_GREEN,
                    bgcolor="#E2E8F0",
                ),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ==========================
        # 2. QUESTION CARD (HERO)
        # ==========================
        def play_clue_audio(e):
            audio.play_click()
            speak_word = target["english"]
            if " - " in speak_word:
                speak_word = speak_word.split(" - ")[-1].strip()
            audio.speak(speak_word)

        listen_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Text("🔊", size=12),
                    ft.Text("DENGARKAN SUARA / LISTEN!", size=10, weight=ft.FontWeight.W_900, color="#92400E"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
                tight=True,
            ),
            bgcolor=DUO_YELLOW_LIGHT,
            padding=ft.Padding.symmetric(horizontal=12, vertical=5),
            border_radius=ft.BorderRadius.all(12),
            border=ft.Border(
                top=ft.BorderSide(1, "#FDE047"),
                left=ft.BorderSide(1, "#FDE047"),
                right=ft.BorderSide(1, "#FDE047"),
                bottom=ft.BorderSide(2.5, DUO_YELLOW_RIM),
            ),
            on_click=play_clue_audio,
        )

        img_path = target.get("image_path")
        hex_col = target.get("hex_color")

        if img_path and (Path("assets") / img_path).exists():
            target_visual = ft.Image(
                src=img_path,
                width=52 if not is_mob else 46,
                height=52 if not is_mob else 46,
                fit=ft.BoxFit.CONTAIN,
            )
        elif hex_col:
            target_visual = ft.Container(
                width=46 if not is_mob else 40,
                height=46 if not is_mob else 40,
                bgcolor=hex_col,
                border_radius=ft.BorderRadius.all(23),
                border=ft.Border.all(3, WHITE),
                shadow=soft_shadow(color="#20000000", blur=4, offset_y=2),
            )
        elif target.get("category") == "numbers":
            target_visual = ft.Container(
                content=ft.Text(
                    str(target["order_num"]),
                    size=26 if not is_mob else 22,
                    weight=ft.FontWeight.W_900,
                    color=DUO_BLUE_RIM
                ),
                bgcolor=DUO_BLUE_LIGHT,
                padding=ft.Padding.symmetric(horizontal=14, vertical=3),
                border_radius=ft.BorderRadius.all(10),
                border=ft.Border.all(1.5, "#BAE6FD"),
            )
        else:
            target_visual = ft.Text(target.get("emoji", "🌟"), size=44 if not is_mob else 38)

        question_card_inner = ft.Column(
            [
                ft.Text(
                    f"Gambar manakah yang merupakan {target['english']}?",
                    size=15 if not is_mob else 13,
                    weight=ft.FontWeight.W_900,
                    color=TEXT_MAIN,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Artinya: \"{target['indonesian']}\"",
                    size=12 if not is_mob else 10,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_SUB,
                    text_align=ft.TextAlign.CENTER,
                ),
                target_visual,
                listen_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        )

        question_card = tactile_card(
            content=question_card_inner,
            border_color="#E2E8F0",
            bottom_rim_color="#CBD5E1",
            bg_color=WHITE,
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        )

        # ==========================
        # 3. 2x2 ANSWER OPTIONS GRID
        # ==========================
        if is_mob:
            card_w = int(max(140, (page.width - 36) / 2))
            btn_h = 58
        elif is_tab:
            card_w = 340
            btn_h = 64
        else: # Laptop & Classroom Smartboard
            card_w = 525
            btn_h = 72

        option_cards = []
        letters = ["A", "B", "C", "D"]

        feedback_text = ft.Text(
            "Pilih jawaban yang benar lalu tekan CEK JAWABAN! 👇",
            size=13 if is_desk else 11,
            weight=ft.FontWeight.W_800,
            color="#15803D",
            text_align=ft.TextAlign.CENTER,
        )

        feedback_banner = ft.Container(
            content=feedback_text,
            bgcolor=WHITE,
            padding=ft.Padding.symmetric(horizontal=16, vertical=8 if is_desk else 6),
            border_radius=ft.BorderRadius.all(14),
            border=ft.Border(
                top=ft.BorderSide(1.5, "#E2E8F0"),
                left=ft.BorderSide(1.5, "#E2E8F0"),
                right=ft.BorderSide(1.5, "#E2E8F0"),
                bottom=ft.BorderSide(2.5, "#CBD5E1"),
            ),
            alignment=ft.Alignment.CENTER,
        )

        choice_boxes = {}

        for i, choice in enumerate(q["choices"]):
            theme = OPTION_THEMES[i % len(OPTION_THEMES)]
            letter = letters[i]

            c_img = choice.get("image_path")
            c_hex = choice.get("hex_color")
            if c_img and (Path("assets") / c_img).exists():
                choice_visual = ft.Image(src=c_img, width=36 if is_desk else 28, height=36 if is_desk else 28, fit=ft.BoxFit.CONTAIN)
            elif c_hex:
                choice_visual = ft.Container(
                    width=28 if is_desk else 22,
                    height=28 if is_desk else 22,
                    bgcolor=c_hex,
                    border_radius=ft.BorderRadius.all(14 if is_desk else 11),
                    border=ft.Border.all(2, WHITE),
                )
            elif choice.get("category") == "numbers":
                choice_visual = ft.Container(
                    content=ft.Text(str(choice["order_num"]), size=16 if is_desk else 13, weight=ft.FontWeight.W_900, color=DUO_BLUE_RIM),
                    bgcolor=DUO_BLUE_LIGHT,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=ft.BorderRadius.all(8),
                )
            else:
                choice_visual = ft.Text(choice.get("emoji", "🌟"), size=28 if is_desk else 22)

            badge_dim = 32 if is_desk else 26
            choice_content = ft.Row(
                [
                    ft.Container(
                        content=ft.Text(letter, size=13 if is_desk else 11, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                        bgcolor=theme["badge_bg"],
                        width=badge_dim,
                        height=badge_dim,
                        border_radius=ft.BorderRadius.all(badge_dim // 2),
                        alignment=ft.Alignment.CENTER,
                        border=ft.Border.all(1.5, theme["border"]),
                    ),
                    choice_visual,
                    ft.Text(
                        choice["english"],
                        size=15 if is_desk else (12 if not is_mob else 11),
                        weight=ft.FontWeight.W_900,
                        color=TEXT_MAIN,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8 if is_desk else 6,
                tight=True,
            )

            box = tactile_card(
                content=choice_content,
                border_color="#E2E8F0",
                bottom_rim_color="#CBD5E1",
                bg_color=WHITE,
                border_radius=18 if is_desk else 16,
                width=card_w,
                height=btn_h,
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            )

            choice_boxes[choice["english"]] = (box, theme, choice)

            def make_select_handler(chosen_item):
                def on_click(e):
                    if session_data["checked"]:
                        return
                    audio.play_click()
                    session_data["selected_choice"] = chosen_item

                    for eng, (b, t, c) in choice_boxes.items():
                        if eng == chosen_item["english"]:
                            b.border = ft.Border(
                                top=ft.BorderSide(1.5, DUO_BLUE),
                                left=ft.BorderSide(1.5, DUO_BLUE),
                                right=ft.BorderSide(1.5, DUO_BLUE),
                                bottom=ft.BorderSide(3.5, DUO_BLUE_RIM),
                            )
                            b.bgcolor = DUO_BLUE_LIGHT
                        else:
                            b.border = ft.Border(
                                top=ft.BorderSide(1.5, "#E2E8F0"),
                                left=ft.BorderSide(1.5, "#E2E8F0"),
                                right=ft.BorderSide(1.5, "#E2E8F0"),
                                bottom=ft.BorderSide(3.5, "#CBD5E1"),
                            )
                            b.bgcolor = WHITE
                    page.update()
                return on_click

            box.on_click = make_select_handler(choice)
            option_cards.append(box)

        options_grid = ft.Row(
            option_cards,
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            run_spacing=10,
        )

        # ==========================
        # 4. BOTTOM ACTION BUTTONS
        # ==========================
        def on_check_answer(e):
            if session_data["checked"]:
                return
            chosen = session_data["selected_choice"]
            if not chosen:
                feedback_text.value = "⚠️ Sentuh salah satu pilihan jawaban dulu ya! 😊"
                page.update()
                return

            session_data["checked"] = True
            is_correct = chosen["english"] == target["english"]

            if is_correct:
                session_data["score_correct"] += 1
                session_data["stars_earned"] += 4
                audio.play_correct()
                clean_target = chosen['english']
                if ' - ' in clean_target:
                    clean_target = clean_target.split(' - ')[-1].strip()
                audio.speak(f"Correct! {clean_target}!")
                state.record_quiz_completed(True)

                box, t, c = choice_boxes[chosen["english"]]
                box.bgcolor = DUO_GREEN_LIGHT
                box.border = ft.Border(
                    top=ft.BorderSide(1.5, DUO_GREEN),
                    left=ft.BorderSide(1.5, DUO_GREEN),
                    right=ft.BorderSide(1.5, DUO_GREEN),
                    bottom=ft.BorderSide(3.5, DUO_GREEN_RIM),
                )

                feedback_banner.bgcolor = DUO_GREEN_LIGHT
                feedback_banner.border = ft.Border(
                    top=ft.BorderSide(1.5, DUO_GREEN),
                    left=ft.BorderSide(1.5, DUO_GREEN),
                    right=ft.BorderSide(1.5, DUO_GREEN),
                    bottom=ft.BorderSide(2.5, DUO_GREEN_RIM),
                )
                feedback_text.value = f"🎉 BENAR SEKALI! '{chosen['english']}'! (+4 Bintang ⭐)"
                page.update()
            else:
                session_data["lives"] = max(0, session_data["lives"] - 1)
                audio.play_wrong()
                audio.speak("Oops! Try again!")

                box, t, c = choice_boxes[chosen["english"]]
                box.bgcolor = DUO_RED_LIGHT
                box.border = ft.Border(
                    top=ft.BorderSide(1.5, DUO_RED),
                    left=ft.BorderSide(1.5, DUO_RED),
                    right=ft.BorderSide(1.5, DUO_RED),
                    bottom=ft.BorderSide(3.5, DUO_RED_RIM),
                )

                feedback_banner.bgcolor = DUO_RED_LIGHT
                feedback_banner.border = ft.Border(
                    top=ft.BorderSide(1.5, DUO_RED),
                    left=ft.BorderSide(1.5, DUO_RED),
                    right=ft.BorderSide(1.5, DUO_RED),
                    bottom=ft.BorderSide(2.5, DUO_RED_RIM),
                )
                feedback_text.value = f"❌ Kurang tepat! Jawaban benar adalah: {target['english']} 😊"
                page.update()

        def on_next_question(e):
            audio.play_click()
            if not session_data["checked"] and session_data["selected_choice"]:
                on_check_answer(None)

            if session_data["current_index"] + 1 < len(session_data["questions"]):
                session_data["current_index"] += 1
                render_current_view()
            else:
                session_data["is_finished"] = True
                render_current_view()

        btn_action_w = 525 if is_desk else (card_w if not is_desk else 410)

        check_btn = tactile_button(
            text="CEK JAWABAN",
            subtext=None,
            icon=None,
            bg_color=DUO_GREEN,
            border_bottom=DUO_GREEN_RIM,
            height=58 if is_desk else 48,
            width=btn_action_w,
            font_size=15 if is_desk else 12,
            border_radius=18 if is_desk else 16,
            on_click=on_check_answer,
        )

        next_btn = tactile_button(
            text="LANJUT / NEXT ▶",
            subtext=None,
            icon=None,
            bg_color=DUO_ORANGE,
            border_bottom=DUO_ORANGE_RIM,
            height=58 if is_desk else 48,
            width=btn_action_w,
            font_size=15 if is_desk else 12,
            border_radius=18 if is_desk else 16,
            on_click=on_next_question,
        )

        bottom_buttons_row = ft.Row(
            [
                check_btn,
                next_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        content_slot.content = ft.Column(
            [
                header_bar,
                ft.Container(height=2),
                progress_block,
                question_card,
                feedback_banner,
                options_grid,
                ft.Container(height=2),
                bottom_buttons_row,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ==========================
    # 5. REWARD / SCORE CELEBRATION
    # ==========================
    def render_score_view():
        audio.play_correct()
        audio.speak("Quiz completed! Fantastic effort!")

        stars_got = session_data["stars_earned"]
        correct_count = session_data["score_correct"]
        total_q = len(session_data["questions"])

        rank, total_students = update_student_score(
            student_name=state.child_name,
            correct_count=correct_count,
            total_count=total_q,
            stars_earned=stars_got,
            avatar_emoji=state.avatar.get("emoji", "🦁")
        )

        if correct_count >= 5:
            stars_rating_text = "⭐⭐⭐"
            compliment = "Luar Biasa! Nilai Sempurna! Kamu Sang Juara! 👑"
        elif correct_count >= 3:
            stars_rating_text = "⭐⭐"
            compliment = "Hebat Sekali! Kamu Petualang Pintar yang Hebat! 🌟"
        else:
            stars_rating_text = "⭐"
            compliment = "Bagus Sekali! Terus Berlatih & Pantang Menyerah! 💪"

        def restart_quiz(e=None):
            audio.play_click()
            session_data["current_index"] = 0
            session_data["score_correct"] = 0
            session_data["stars_earned"] = 0
            session_data["lives"] = 3
            session_data["questions"] = generate_quiz_questions(cat_id, 5)
            session_data["is_finished"] = False
            render_current_view()

        rank_badge_bg = DUO_YELLOW_LIGHT if rank <= 3 else "#F0FDF4"
        rank_border = DUO_YELLOW_RIM if rank <= 3 else DUO_GREEN_RIM
        rank_medal = "👑 🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else "🏆"))

        rank_container = ft.Container(
            content=ft.Row(
                [
                    ft.Text(rank_medal, size=24),
                    ft.Column(
                        [
                            ft.Text(f"Hebat {state.child_name}!", size=13, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                            ft.Text(f"Kamu berada di Peringkat #{rank} dari {total_students} Siswa Kelas!", size=11, weight=ft.FontWeight.BOLD, color="#15803D"),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=rank_badge_bg,
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            border_radius=ft.BorderRadius.all(14),
            border=ft.Border(
                top=ft.BorderSide(1.5, rank_border),
                left=ft.BorderSide(1.5, rank_border),
                right=ft.BorderSide(1.5, rank_border),
                bottom=ft.BorderSide(3, rank_border),
            ),
        )

        btn_w = 220 if not is_mob else int(max(140, (page.width - 36) / 2))

        leaderboard_btn = tactile_button(
            text="🏆 PERINGKAT KELAS",
            subtext=None,
            icon=None,
            bg_color=DUO_ORANGE,
            border_bottom=DUO_ORANGE_RIM,
            height=46,
            width=btn_w,
            font_size=11,
            border_radius=16,
            on_click=lambda e: (audio.play_click(), show_class_leaderboard(page, state, audio, on_update_callback=lambda: render_current_view())),
        )

        next_student_btn = tactile_button(
            text="🎮 SISWA BERIKUTNYA",
            subtext=None,
            icon=None,
            bg_color=DUO_BLUE,
            border_bottom=DUO_BLUE_RIM,
            height=46,
            width=btn_w,
            font_size=11,
            border_radius=16,
            on_click=lambda e: (audio.play_click(), show_student_picker(page, state, audio, on_selected_callback=restart_quiz)),
        )

        play_again_btn = tactile_button(
            text="MAIN LAGI 🔄",
            subtext=None,
            icon=None,
            bg_color=WHITE,
            border_bottom="#CBD5E1",
            text_color=TEXT_MAIN,
            height=42,
            width=btn_w,
            font_size=11,
            border_radius=16,
            on_click=restart_quiz,
        )

        home_btn = tactile_button(
            text="MENU UTAMA 🏠",
            subtext=None,
            icon=None,
            bg_color=DUO_GREEN,
            border_bottom=DUO_GREEN_RIM,
            height=42,
            width=btn_w,
            font_size=11,
            border_radius=16,
            on_click=lambda e: (audio.play_click(), navigate("dashboard")),
        )

        celebration_inner = ft.Column(
            [
                ft.Text("🏆 PETUALANGAN SELESAI! 🏆", size=17, weight=ft.FontWeight.W_900, color=TEXT_MAIN, text_align=ft.TextAlign.CENTER),
                ft.Text(stars_rating_text, size=28),
                rank_container,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"+{stars_got} BINTANG EMAS! ⭐", size=14, weight=ft.FontWeight.W_900, color=DUO_ORANGE_RIM),
                            ft.Text(f"Jawaban Benar: {correct_count} dari {total_q} Soal ({state.stars} Total Bintang)", size=11, weight=ft.FontWeight.BOLD, color=TEXT_SUB),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    bgcolor=DUO_YELLOW_LIGHT,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                    border_radius=ft.BorderRadius.all(12),
                    border=ft.Border.all(1.5, DUO_YELLOW_RIM),
                ),
                ft.Text(compliment, size=11, weight=ft.FontWeight.BOLD, color=TEXT_MAIN, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )

        celebration_card = tactile_card(
            content=celebration_inner,
            border_color="#E2E8F0",
            bottom_rim_color=DUO_GREEN_RIM,
            bg_color=WHITE,
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=14, vertical=14),
        )

        buttons_row_1 = ft.Row([leaderboard_btn, next_student_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        buttons_row_2 = ft.Row([play_again_btn, home_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

        content_slot.content = ft.Column(
            [
                celebration_card,
                ft.Container(height=4),
                buttons_row_1,
                buttons_row_2,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    render_current_view()

    # Bottom Nav Bar
    bottom_bar = modern_bottom_nav(active_tab="quiz", navigate=navigate, audio=audio, page=page, state=state)

    return modern_app_shell(content_slot, page, bottom_nav=bottom_bar)
