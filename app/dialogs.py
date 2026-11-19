import random
import flet as ft
from app.theme import (
    DUO_GREEN, DUO_GREEN_RIM, DUO_GREEN_LIGHT,
    DUO_BLUE, DUO_BLUE_RIM, DUO_BLUE_LIGHT,
    DUO_ORANGE, DUO_ORANGE_RIM, DUO_ORANGE_LIGHT,
    DUO_YELLOW, DUO_YELLOW_RIM, DUO_YELLOW_LIGHT,
    DUO_RED, DUO_RED_RIM, DUO_RED_LIGHT,
    DUO_PURPLE, DUO_PURPLE_RIM, DUO_PURPLE_LIGHT,
    WHITE, TEXT_DARK, TEXT_MUTED,
    GREEN_PRIMARY, GREEN_LIGHT, GREEN_DARK, YELLOW_WARM, YELLOW_BRIGHT,
    AMBER_GOLD, ORANGE_BRIGHT, BLUE_SKY, RED_HEART, DARK_TEXT, MUTED_TEXT,
    BORDER_RADIUS_LG, BORDER_RADIUS_MD, soft_shadow
)
from app.data.quests import ACHIEVEMENTS
from app.database import (
    get_class_leaderboard, reset_class_scores, update_student_score,
    get_student_names, add_new_student
)

def close_dialog(page: ft.Page):
    try:
        page.pop_dialog()
    except Exception:
        pass
    page.update()

def show_parent_gate(page: ft.Page, state, audio, on_update_callback=None):
    """Parent Gate dialog with random multiplication or addition challenge."""
    audio.play_click()
    num1 = random.randint(4, 9)
    num2 = random.randint(2, 6)
    expected_answer = num1 * num2

    answer_field = ft.TextField(
        label="Hasil perkalian",
        hint_text="Ketik angka hasil...",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        autofocus=True,
        width=220,
        border_radius=ft.BorderRadius.all(14),
        border_color="#CBD5E1",
        focused_border_color=DUO_GREEN,
    )

    error_text = ft.Text("", color=DUO_RED, size=12, weight=ft.FontWeight.BOLD)

    def verify_answer(e):
        user_input = answer_field.value.strip() if answer_field.value else ""
        if user_input == str(expected_answer):
            close_dialog(page)
            audio.play_correct()
            show_parent_settings(page, state, audio, on_update_callback)
        else:
            audio.play_wrong()
            error_text.value = f"Jawaban belum tepat! Coba lagi ({num1} x {num2} = ?)"
            answer_field.value = ""
            page.update()

    dlg = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=22),
        title=ft.Row(
            [
                ft.Text("🔒", size=24),
                ft.Text("PARENTS ONLY GATE", size=18, weight=ft.FontWeight.W_900, color=TEXT_DARK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Untuk keamanan anak, silakan selesaikan soal matematika berikut:",
                        size=13,
                        color=TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Text(
                            f"{num1}  ×  {num2}  =  ?",
                            size=28,
                            weight=ft.FontWeight.W_900,
                            color="#15803D",
                        ),
                        bgcolor=DUO_GREEN_LIGHT,
                        padding=ft.Padding.symmetric(horizontal=24, vertical=10),
                        border_radius=ft.BorderRadius.all(16),
                        border=ft.Border.all(2, DUO_GREEN),
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(height=6),
                    answer_field,
                    error_text,
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            width=340,
            padding=ft.Padding.all(6),
        ),
        actions=[
            ft.TextButton(
                "BATAL",
                on_click=lambda e: (audio.play_click(), close_dialog(page)),
            ),
            ft.FilledButton(
                "MASUK PENGATURAN",
                icon=ft.Icons.LOCK_OPEN,
                bgcolor=DUO_GREEN,
                on_click=verify_answer,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.show_dialog(dlg)
    page.update()

def show_parent_settings(page: ft.Page, state, audio, on_update_callback=None):
    """Parent dashboard and settings modal."""
    speed_slider = ft.Slider(
        min=100,
        max=200,
        divisions=10,
        value=state.speech_rate,
        label="{value} WPM",
        active_color=DUO_GREEN,
    )

    def on_speed_change(e):
        state.speech_rate = int(e.control.value)
        audio.speak("Testing voice speed.", rate=state.speech_rate)

    speed_slider.on_change = on_speed_change

    def handle_reset_progress(e):
        state.reset_progress()
        audio.play_click()
        close_dialog(page)
        if on_update_callback:
            on_update_callback()
        page.update()

    dlg = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=22),
        title=ft.Row(
            [
                ft.Text("⚙️", size=24),
                ft.Text("PENGATURAN ORANG TUA", size=18, weight=ft.FontWeight.W_900, color=TEXT_DARK),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Profil Anak: {state.child_name} ({state.avatar['name']})", size=14, weight=ft.FontWeight.BOLD, color="#15803D"),
                    ft.Divider(height=8),
                    ft.Text("📊 Statistik Belajar Anak:", size=13, weight=ft.FontWeight.W_700, color=TEXT_DARK),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("⭐ Bintang", size=11, color=TEXT_MUTED),
                                        ft.Text(f"{state.stars}", size=18, weight=ft.FontWeight.W_900, color=DUO_ORANGE_RIM),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor=DUO_YELLOW_LIGHT,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                                border_radius=ft.BorderRadius.all(12),
                                border=ft.Border.all(1.5, DUO_YELLOW_RIM),
                                expand=1,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("📖 Kata", size=11, color=TEXT_MUTED),
                                        ft.Text(f"{state.words_learned}", size=18, weight=ft.FontWeight.W_900, color=DUO_BLUE_RIM),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor=DUO_BLUE_LIGHT,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                                border_radius=ft.BorderRadius.all(12),
                                border=ft.Border.all(1.5, DUO_BLUE_RIM),
                                expand=1,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("🎯 Kuis", size=11, color=TEXT_MUTED),
                                        ft.Text(f"{state.quiz_score}", size=18, weight=ft.FontWeight.W_900, color="#15803D"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor=DUO_GREEN_LIGHT,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                                border_radius=ft.BorderRadius.all(12),
                                border=ft.Border.all(1.5, DUO_GREEN_RIM),
                                expand=1,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=8),
                    ft.Text("🔊 Kecepatan Suara Suara Guru (TTS):", size=13, weight=ft.FontWeight.W_700, color=TEXT_DARK),
                    speed_slider,
                    ft.Row(
                        [
                            ft.Text("Lambat (100)", size=10, color=TEXT_MUTED),
                            ft.Text("Normal (145)", size=10, color=TEXT_MUTED),
                            ft.Text("Cepat (200)", size=10, color=TEXT_MUTED),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=8),
                    ft.FilledButton(
                        "RESET PROGRESS ANAK (MULAI DARI 0)",
                        icon=ft.Icons.REFRESH,
                        bgcolor=DUO_RED,
                        on_click=handle_reset_progress,
                    ),
                ],
                tight=True,
                spacing=6,
            ),
            max_width=360,
            padding=ft.Padding.all(8),
        ),
        actions=[
            ft.FilledButton(
                "TUTUP",
                bgcolor=DUO_GREEN,
                on_click=lambda e: (audio.play_click(), close_dialog(page)),
            ),
        ],
    )

    page.show_dialog(dlg)
    page.update()

def show_daily_quests(page: ft.Page, state, audio, on_update_callback=None):
    """Daily Quests popup dialog with interactive reward claim."""
    audio.play_click()
    
    # Calculate progress ratios
    p1 = min(1.0, state.daily_words_count / max(1, state.daily_words_target))
    p2 = min(1.0, state.daily_quiz_count / max(1, state.daily_quiz_target))
    p3 = min(1.0, state.daily_stars_count / max(1, state.daily_stars_target))
    
    all_done = state.is_all_daily_quests_completed()

    def claim_reward(e):
        bonus = state.claim_daily_bonus()
        if bonus > 0:
            audio.play_fanfare()
            audio.speak("Congratulations! You completed today's quests!")
            close_dialog(page)
            if on_update_callback:
                on_update_callback()
            page.update()

    def make_quest_row(title, cur, target, progress, emoji):
        done = cur >= target
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(f"{emoji} {title}", size=13, weight=ft.FontWeight.BOLD, color=TEXT_DARK, expand=1),
                            ft.Text(f"{cur}/{target} {'✅' if done else ''}", size=12, weight=ft.FontWeight.W_900, color="#15803D" if done else TEXT_DARK),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.ProgressBar(value=progress, color=DUO_GREEN if done else DUO_ORANGE, bgcolor="#E2E8F0", height=8),
                ],
                spacing=4,
            ),
            bgcolor=DUO_GREEN_LIGHT if done else "#F8FAFC",
            padding=ft.Padding.all(10),
            border_radius=ft.BorderRadius.all(14),
            border=ft.Border.all(1.5, DUO_GREEN if done else "#E2E8F0"),
        )

    claim_btn = None
    if all_done and not state.claimed_daily_reward:
        claim_btn = ft.FilledButton(
            "🎁 KLAIM HADIAH +25 ⭐ BINTANG!",
            bgcolor=DUO_ORANGE,
            icon=ft.Icons.CARD_GIFTCARD,
            on_click=claim_reward,
        )
    elif state.claimed_daily_reward:
        claim_btn = ft.Container(
            content=ft.Text("🎉 Hadiah Harian Sudah Diklaim!", size=13, weight=ft.FontWeight.BOLD, color="#15803D"),
            alignment=ft.Alignment.CENTER,
        )

    dlg = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=22),
        title=ft.Row(
            [
                ft.Text("📅", size=24),
                ft.Text("DAILY JUNGLE QUESTS", size=18, weight=ft.FontWeight.W_900, color=TEXT_DARK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Selesaikan misi harian untuk mendapatkan bonus bintang!",
                        size=12,
                        color=TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=4),
                    make_quest_row("Pelajari 3 Kata Bahasa Inggris", state.daily_words_count, state.daily_words_target, p1, "📖"),
                    make_quest_row("Ikuti 1 Sesi Kuis Petualangan", state.daily_quiz_count, state.daily_quiz_target, p2, "🎯"),
                    make_quest_row("Kumpulkan 20 Bintang Emas", state.daily_stars_count, state.daily_stars_target, p3, "⭐"),
                    ft.Container(height=6),
                    claim_btn if claim_btn else ft.Container(),
                ],
                tight=True,
                spacing=8,
            ),
            max_width=350,
            padding=ft.Padding.all(6),
        ),
        actions=[
            ft.FilledButton(
                "TUTUP",
                bgcolor=DUO_GREEN,
                on_click=lambda e: (audio.play_click(), close_dialog(page)),
            ),
        ],
    )

    page.show_dialog(dlg)
    page.update()

def show_student_picker(page: ft.Page, state, audio, on_selected_callback=None):
    """Classroom Student Picker dialog: quick-select which student is stepping up to the projector."""
    audio.play_click()
    students = get_class_leaderboard()
    if not students:
        students = [{"student_name": f"Siswa {i}", "avatar_emoji": "🦁"} for i in range(1, 16)]

    chips = []
    current_name = (state.child_name or "Budi").strip().lower()

    def make_select_student(st_name, st_emoji):
        def on_tap(e):
            audio.play_click()
            state.child_name = st_name
            state.avatar = {"id": st_name.lower(), "name": st_name, "emoji": st_emoji}
            audio.speak(f"Halo {st_name}!")
            close_dialog(page)
            if on_selected_callback:
                on_selected_callback()
            else:
                page.update()
        return on_tap

    for s in students:
        name = s["student_name"]
        emoji = s.get("avatar_emoji", "⭐")
        is_active = (name.lower() == current_name)

        chip = ft.Container(
            content=ft.Row(
                [
                    ft.Text(emoji, size=16),
                    ft.Text(name, size=11, weight=ft.FontWeight.W_900 if is_active else ft.FontWeight.BOLD, color=TEXT_DARK),
                    ft.Text("⭐", size=10) if is_active else ft.Container(),
                ],
                tight=True,
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=DUO_YELLOW_LIGHT if is_active else WHITE,
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            border_radius=ft.BorderRadius.all(14),
            border=ft.Border(
                top=ft.BorderSide(1.5, "#FDE047" if is_active else "#E2E8F0"),
                left=ft.BorderSide(1.5, "#FDE047" if is_active else "#E2E8F0"),
                right=ft.BorderSide(1.5, "#FDE047" if is_active else "#E2E8F0"),
                bottom=ft.BorderSide(3, DUO_YELLOW_RIM if is_active else "#CBD5E1"),
            ),
            shadow=soft_shadow(color="#10000000", blur=3) if is_active else None,
            on_click=make_select_student(name, emoji),
        )
        chips.append(chip)

    # Input for new student
    new_name_field = ft.TextField(
        hint_text="Ketik nama siswa baru...",
        width=200,
        height=40,
        text_size=12,
        border_radius=ft.BorderRadius.all(12),
        border_color="#CBD5E1",
        focused_border_color=DUO_GREEN,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )

    def on_add_new_student(e):
        name = new_name_field.value.strip() if new_name_field.value else ""
        if name:
            audio.play_click()
            add_new_student(name, avatar_emoji="⭐")
            state.child_name = name
            state.avatar = {"id": name.lower(), "name": name, "emoji": "⭐"}
            audio.speak(f"Halo {name}!")
            close_dialog(page)
            if on_selected_callback:
                on_selected_callback()
            else:
                page.update()

    add_row = ft.Row(
        [
            new_name_field,
            ft.FilledButton(
                "Tambah",
                bgcolor=DUO_GREEN,
                height=40,
                on_click=on_add_new_student,
            ),
        ],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    dlg = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=22),
        title=ft.Row(
            [
                ft.Text("🎒", size=24),
                ft.Text("PILIH SISWA MAJU KE DEPAN", size=16, weight=ft.FontWeight.W_900, color=TEXT_DARK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Sentuh nama siswa yang maju ke proyektor:", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=ft.Row(chips, wrap=True, spacing=8, run_spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                        padding=ft.Padding.all(4),
                    ),
                    ft.Divider(height=12),
                    ft.Text("Atau daftarkan siswa baru:", size=10, color=TEXT_MUTED),
                    add_row,
                ],
                tight=True,
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=420,
            max_height=420,
            padding=ft.Padding.all(6),
        ),
        actions=[
            ft.TextButton("Batal / Tutup", on_click=lambda e: (audio.play_click(), close_dialog(page))),
        ],
    )
    page.show_dialog(dlg)
    page.update()

def show_class_leaderboard(page: ft.Page, state, audio, on_update_callback=None):
    """Papan Peringkat Kelas (1-15 Siswa) optimized for Classroom Projectors & Smart TVs (Duolingo League Style)."""
    audio.play_click()

    def build_leaderboard_content():
        students = get_class_leaderboard()
        if not students:
            return ft.Text("Belum ada data skor siswa.", size=12)

        items_col = []

        # Subtitle banner for classroom turns
        turn_banner = ft.Container(
            content=ft.Row(
                [
                    ft.Text("⭐ Siswa bergantian maju ke depan proyektor untuk mengumpulkan skor & bintang! ⭐",
                            size=10, weight=ft.FontWeight.BOLD, color="#15803D", text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=DUO_GREEN_LIGHT,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=ft.BorderRadius.all(10),
            border=ft.Border.all(1, "#BBF7D0"),
        )
        items_col.append(turn_banner)
        items_col.append(ft.Container(height=4))

        # Top 3 Podium Champions Highlight
        top_configs = [
            {"rank": 1, "title": "🥇 JUARA 1", "badge_bg": DUO_YELLOW_LIGHT, "border": "#FDE047", "rim": DUO_YELLOW_RIM, "crown": "👑", "glow": "#FEFCE8"},
            {"rank": 2, "title": "🥈 JUARA 2", "badge_bg": "#F1F5F9", "border": "#E2E8F0", "rim": "#94A3B8", "crown": "🥈", "glow": "#F8FAFC"},
            {"rank": 3, "title": "🥉 JUARA 3", "badge_bg": DUO_ORANGE_LIGHT, "border": "#FED7AA", "rim": DUO_ORANGE_RIM, "crown": "🥉", "glow": "#FFF7ED"},
        ]

        top_cards = []
        for i in range(min(3, len(students))):
            st = students[i]
            cfg = top_configs[i]

            champ_card = ft.Container(
                content=ft.Row(
                    [
                        # Rank Badge with crown
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(cfg["crown"], size=16),
                                    ft.Text(f"#{cfg['rank']}", size=11, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=cfg["badge_bg"],
                            width=42,
                            height=42,
                            border_radius=ft.BorderRadius.all(12),
                            border=ft.Border(
                                top=ft.BorderSide(1.5, cfg["border"]),
                                left=ft.BorderSide(1.5, cfg["border"]),
                                right=ft.BorderSide(1.5, cfg["border"]),
                                bottom=ft.BorderSide(3, cfg["rim"]),
                            ),
                            alignment=ft.Alignment.CENTER,
                        ),
                        # Avatar & Name
                        ft.Text(st.get("avatar_emoji", "🦁"), size=24),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(st["student_name"], size=14, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                                        ft.Container(
                                            content=ft.Text(cfg["title"], size=9, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                                            bgcolor=cfg["badge_bg"],
                                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                            border_radius=ft.BorderRadius.all(6),
                                            border=ft.Border.all(1, cfg["border"]),
                                        ),
                                    ],
                                    spacing=6,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Text(f"🎯 Benar: {st.get('correct_answers', 0)} soal", size=10, color=TEXT_MUTED, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                        # Score & Stars
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text(f"💯 {st.get('score', 0)} Poin", size=12, weight=ft.FontWeight.W_900, color="#15803D"),
                                    bgcolor=DUO_GREEN_LIGHT,
                                    padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=ft.BorderRadius.all(8),
                                ),
                                ft.Text(f"⭐ {st.get('stars', 0)} Bintang", size=10, weight=ft.FontWeight.BOLD, color=DUO_ORANGE_RIM),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=cfg["glow"],
                padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                border_radius=ft.BorderRadius.all(14),
                border=ft.Border(
                    top=ft.BorderSide(1.5, cfg["border"]),
                    left=ft.BorderSide(1.5, cfg["border"]),
                    right=ft.BorderSide(1.5, cfg["border"]),
                    bottom=ft.BorderSide(3.5, cfg["rim"]),
                ),
                shadow=soft_shadow(color="#10000000", blur=4, offset_y=2),
            )
            top_cards.append(champ_card)

        items_col.extend(top_cards)

        if len(students) > 3:
            items_col.append(ft.Container(height=6))
            items_col.append(
                ft.Text("DAFTAR SISWA LAINNYA (#4 – #15):", size=10, weight=ft.FontWeight.W_900, color=TEXT_MUTED)
            )

            # Ranks #4 to #15
            for idx in range(3, len(students)):
                st = students[idx]
                rank_num = idx + 1

                row_card = ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(f"#{rank_num}", size=11, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                                bgcolor="#F8FAFC",
                                width=32,
                                height=32,
                                border_radius=ft.BorderRadius.all(8),
                                alignment=ft.Alignment.CENTER,
                                border=ft.Border.all(1, "#E2E8F0"),
                            ),
                            ft.Text(st.get("avatar_emoji", "⭐"), size=20),
                            ft.Column(
                                [
                                    ft.Text(st["student_name"], size=12, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                                    ft.Text(f"🎯 {st.get('correct_answers', 0)} benar", size=9, color=TEXT_MUTED),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"💯 {st.get('score', 0)}", size=11, weight=ft.FontWeight.W_900, color="#15803D"),
                                    ft.Text(f"⭐ {st.get('stars', 0)}", size=10, weight=ft.FontWeight.BOLD, color=DUO_ORANGE_RIM),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=WHITE,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=6),
                    border_radius=ft.BorderRadius.all(10),
                    border=ft.Border(
                        top=ft.BorderSide(1, "#E2E8F0"),
                        left=ft.BorderSide(1, "#E2E8F0"),
                        right=ft.BorderSide(1, "#E2E8F0"),
                        bottom=ft.BorderSide(2.5, "#CBD5E1"),
                    ),
                )
                items_col.append(row_card)

        return ft.Column(items_col, tight=True, spacing=6, scroll=ft.ScrollMode.AUTO)

    body_container = ft.Container(
        content=build_leaderboard_content(),
        width=520,
        height=400,
        padding=ft.Padding.all(4),
    )

    def refresh_dialog():
        body_container.content = build_leaderboard_content()
        page.update()

    def confirm_reset(e):
        audio.play_click()
        confirm_dlg = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=20),
            title=ft.Row([ft.Text("⚠️", size=22), ft.Text("Konfirmasi Reset Skor", size=15, weight=ft.FontWeight.W_900)]),
            content=ft.Text("Apakah guru yakin ingin mereset skor seluruh 15 siswa kelas menjadi 0 untuk memulai sesi baru?", size=12),
            actions=[
                ft.TextButton("Batal", on_click=lambda e: (audio.play_click(), close_dialog(page))),
                ft.FilledButton(
                    "Ya, Reset Semua",
                    bgcolor=DUO_RED,
                    on_click=lambda e: (
                        audio.play_click(),
                        reset_class_scores(),
                        close_dialog(page),
                        refresh_dialog(),
                        on_update_callback() if on_update_callback else None
                    ),
                ),
            ],
        )
        page.show_dialog(confirm_dlg)
        page.update()

    # Title & Header
    title_row = ft.Row(
        [
            ft.Row(
                [
                    ft.Text("🏆", size=22),
                    ft.Text("PAPAN PERINGKAT KELAS (1–15)", size=15, weight=ft.FontWeight.W_900, color=TEXT_DARK),
                ],
                spacing=6,
                tight=True,
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("🔄", size=11),
                        ft.Text("Reset Skor Kelas", size=10, weight=ft.FontWeight.W_900, color=DUO_RED_RIM),
                    ],
                    tight=True,
                    spacing=3,
                ),
                bgcolor=DUO_RED_LIGHT,
                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                border_radius=ft.BorderRadius.all(8),
                border=ft.Border.all(1, "#FECACA"),
                on_click=confirm_reset,
                tooltip="Reset semua skor siswa menjadi 0",
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    dlg = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=22),
        title=title_row,
        content=body_container,
        actions=[
            ft.FilledButton(
                "🎒 GANTI SISWA MAJU",
                bgcolor=DUO_ORANGE,
                on_click=lambda e: (
                    close_dialog(page),
                    show_student_picker(page, state, audio, on_selected_callback=on_update_callback)
                ),
            ),
            ft.FilledButton(
                "TUTUP",
                bgcolor=DUO_GREEN,
                on_click=lambda e: (audio.play_click(), close_dialog(page), on_update_callback() if on_update_callback else None),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    page.show_dialog(dlg)
    page.update()

# Backward compatibility alias
show_achievements = show_class_leaderboard
