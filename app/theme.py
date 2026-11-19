import flet as ft

# ==========================================
# MODERN & ELEGANT RESPONSIVE DESIGN SYSTEM
# Perfect on Laptop, iPad/Tablet, and Mobile HP
# ==========================================

# Minimalist Elegant Surfaces & Backgrounds
APP_BG = "#F8FAFC"             # Slate-50: ultra-clean contemporary canvas
CARD_BG = "#FFFFFF"            # Crisp pure white
SURFACE_LIGHT = "#F1F5F9"      # Slate-100: subtle component backgrounds

# Typography Colors (High-contrast, Refined & Elegant)
TEXT_MAIN = "#0F172A"          # Slate-900: sharp modern charcoal
TEXT_SUB = "#64748B"           # Slate-500: elegant cool slate
TEXT_LIGHT = "#94A3B8"         # Slate-400: subtle placeholder/hint
TEXT_DARK = TEXT_MAIN
TEXT_MUTED = TEXT_SUB
MUTED_TEXT = TEXT_SUB
DARK_TEXT = TEXT_MAIN

# Vibrant Modern Brand Palette (Emerald, Sky, Coral, Amber, Violet)
DUO_GREEN = "#10B981"          # Emerald-500: vibrant fresh green
DUO_GREEN_RIM = "#059669"      # Emerald-600: clean subtle bottom rim
DUO_GREEN_LIGHT = "#ECFDF5"    # Emerald-50: soft pastel tint

DUO_BLUE = "#0EA5E9"           # Sky-500: modern cheerful blue
DUO_BLUE_RIM = "#0284C7"       # Sky-600
DUO_BLUE_LIGHT = "#F0F9FF"     # Sky-50

DUO_ORANGE = "#F97316"         # Orange-500: warm active orange
DUO_ORANGE_RIM = "#EA580C"     # Orange-600
DUO_ORANGE_LIGHT = "#FFF7ED"   # Orange-50

DUO_YELLOW = "#F59E0B"         # Amber-500: gold stars / badges
DUO_YELLOW_RIM = "#D97706"     # Amber-600
DUO_YELLOW_LIGHT = "#FEFCE8"   # Amber-50

DUO_PURPLE = "#8B5CF6"         # Violet-500: modern creative violet
DUO_PURPLE_RIM = "#7C3AED"     # Violet-600
DUO_PURPLE_LIGHT = "#FAF5FF"   # Violet-50

DUO_RED = "#F43F5E"            # Rose-500: lives / errors
DUO_RED_RIM = "#E11D48"        # Rose-600
DUO_RED_LIGHT = "#FFF1F2"      # Rose-50

# Surface Borders
BORDER_SUBTLE = "#E2E8F0"      # Slate-200: 1.5px clean border
BORDER_RIM = "#CBD5E1"         # Slate-300: 3px subtle rim

# Legacy Aliases (Strict Backward Compatibility)
WHITE = CARD_BG
GREEN_PRIMARY = DUO_GREEN
GREEN_DARK = DUO_GREEN_RIM
GREEN_LIGHT = "#86EFAC"
YELLOW_WARM = DUO_YELLOW
YELLOW_BRIGHT = "#FEF08A"
AMBER_GOLD = DUO_YELLOW_RIM
ORANGE_BRIGHT = DUO_ORANGE
RED_HEART = DUO_RED
BLUE_SKY = DUO_BLUE
BORDER_RADIUS_LG = 20
BORDER_RADIUS_MD = 14
BORDER_RADIUS_SM = 10

# Modern Diffused Shadows
def soft_shadow(color="#0A000000", blur=12, spread=0, offset_y=3):
    return [
        ft.BoxShadow(
            spread_radius=spread,
            blur_radius=blur,
            color=color,
            offset=ft.Offset(0, offset_y)
        )
    ]

def vibrant_shadow(color="#10000000", blur=18, spread=0, offset_y=5):
    return [
        ft.BoxShadow(
            spread_radius=spread,
            blur_radius=blur,
            color=color,
            offset=ft.Offset(0, offset_y)
        )
    ]

# ==========================================
# DEVICE RESPONSIVE METRICS
# Dynamically adapts to Laptop, iPad, Phone
# ==========================================

def get_screen_metrics(page: ft.Page):
    """Calculates responsive metrics based on real-time screen width and height.
    Supports Laptop, Classroom Smartboard / Interactive Projector, iPad/Tablet, and Mobile HP.
    """
    w = page.width if page.width and page.width > 0 else 1024
    h = page.height if page.height and page.height > 0 else 768
    
    is_mobile = w < 640
    is_tablet = 640 <= w < 1024
    is_desktop = w >= 1024

    if is_mobile:
        max_container_w = None  # Full bleed for mobile HP
        padding_h = 12
        category_cols = 2
        card_w = int(max(140, (w - 36) / 2))
        title_sz = 19
        sub_sz = 11
        bottom_nav_w = None
    elif is_tablet:
        max_container_w = 760   # iPad / Tablet width
        padding_h = 24
        category_cols = 2
        card_w = 340
        title_sz = 22
        sub_sz = 12
        bottom_nav_w = 540
    else: # Laptop & Classroom Smartboard (Widescreen 16:9, 1080p / 1440p)
        max_container_w = 1120  # Optimized widescreen classroom canvas
        padding_h = 32
        category_cols = 4       # All 4 categories spacious in one row!
        card_w = 255
        title_sz = 26
        sub_sz = 14
        bottom_nav_w = 540

    return {
        "width": w,
        "height": h,
        "is_mobile": is_mobile,
        "is_tablet": is_tablet,
        "is_desktop": is_desktop,
        "max_container_w": max_container_w,
        "grid_columns": category_cols,
        "card_width": card_w,
        "padding_h": padding_h,
        "title_size": title_sz,
        "subtitle_size": sub_sz,
        "bottom_nav_width": bottom_nav_w,
    }

# ==========================================
# MODERN COMPONENT BUILDERS
# ==========================================

def tactile_button(
    text: str,
    subtext: str | None = None,
    icon: ft.IconData | str | None = None,
    gradient_colors: list[str] | None = None,
    bg_color: str | None = None,
    border_top: str | None = None,
    border_bottom: str | None = None,
    text_color: str = WHITE,
    height: int = 50,
    width: int | float | None = None,
    border_radius: int = 18,
    on_click = None,
    font_size: int = 14,
) -> ft.Container:
    """Creates an elegant tactile button with smooth gradient and subtle 3.5px depth."""
    
    if bg_color:
        main_bg = bg_color
    elif gradient_colors and len(gradient_colors) > 0:
        main_bg = gradient_colors[0]
    else:
        main_bg = DUO_GREEN

    if not border_bottom:
        if main_bg == DUO_GREEN:
            border_bottom = DUO_GREEN_RIM
        elif main_bg == DUO_BLUE:
            border_bottom = DUO_BLUE_RIM
        elif main_bg == DUO_ORANGE:
            border_bottom = DUO_ORANGE_RIM
        elif main_bg == DUO_YELLOW:
            border_bottom = DUO_YELLOW_RIM
        elif main_bg == DUO_RED:
            border_bottom = DUO_RED_RIM
        elif main_bg == WHITE:
            border_bottom = BORDER_RIM
        else:
            border_bottom = BORDER_RIM

    border_side_color = border_top if border_top else main_bg
    if main_bg == WHITE:
        border_side_color = BORDER_SUBTLE

    icon_ctrl = None
    if isinstance(icon, ft.IconData):
        icon_ctrl = ft.Icon(icon, color=text_color, size=font_size + 4)
    elif isinstance(icon, str):
        icon_ctrl = ft.Text(icon, size=font_size + 2)

    col_content = [
        ft.Text(
            text,
            size=font_size,
            weight=ft.FontWeight.W_800,
            color=text_color,
            text_align=ft.TextAlign.CENTER
        )
    ]
    if subtext:
        col_content.append(
            ft.Text(
                subtext,
                size=max(9, font_size - 4),
                weight=ft.FontWeight.BOLD,
                color="#FFFFFFE0" if text_color == WHITE else TEXT_SUB,
                text_align=ft.TextAlign.CENTER
            )
        )

    text_column = ft.Column(
        col_content,
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    row_items = []
    if icon_ctrl:
        row_items.append(icon_ctrl)
    row_items.append(text_column)

    btn_gradient = None
    if main_bg == DUO_GREEN:
        btn_gradient = ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=["#34D399", "#059669"])
    elif main_bg == DUO_BLUE:
        btn_gradient = ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=["#38BDF8", "#0284C7"])
    elif main_bg == DUO_ORANGE:
        btn_gradient = ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=["#FB923C", "#EA580C"])
    elif main_bg == DUO_YELLOW:
        btn_gradient = ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=["#FBBF24", "#D97706"])

    return ft.Container(
        content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=6, tight=True),
        bgcolor=main_bg if not btn_gradient else None,
        gradient=btn_gradient,
        height=height,
        width=width,
        border_radius=ft.BorderRadius.all(border_radius),
        border=ft.Border(
            top=ft.BorderSide(1.5, border_side_color),
            left=ft.BorderSide(1.5, border_side_color),
            right=ft.BorderSide(1.5, border_side_color),
            bottom=ft.BorderSide(3.5, border_bottom),
        ),
        shadow=vibrant_shadow(color="#14000000", blur=8, offset_y=4),
        padding=ft.Padding.symmetric(horizontal=14),
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
    )

def tactile_card(
    content: ft.Control,
    border_color: str = BORDER_SUBTLE,
    bottom_rim_color: str = BORDER_RIM,
    bg_color: str = WHITE,
    border_radius: int = 20,
    width: int | float | None = None,
    height: int | float | None = None,
    padding: int | ft.Padding = 12,
    on_click = None,
) -> ft.Container:
    """Creates a modern white card with refined micro-border and soft depth."""
    return ft.Container(
        content=content,
        bgcolor=bg_color,
        width=width,
        height=height,
        border_radius=ft.BorderRadius.all(border_radius),
        border=ft.Border(
            top=ft.BorderSide(1.5, border_color),
            left=ft.BorderSide(1.5, border_color),
            right=ft.BorderSide(1.5, border_color),
            bottom=ft.BorderSide(3.5, bottom_rim_color),
        ),
        shadow=soft_shadow(color="#0A000000", blur=12, offset_y=3),
        padding=padding if isinstance(padding, ft.Padding) else ft.Padding.all(padding),
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
    )

def hud_pill(
    content: ft.Control | str,
    icon: str | ft.IconData | None = None,
    bg_color: str = WHITE,
    border_color: str = BORDER_SUBTLE,
    bottom_rim: str = BORDER_RIM,
    padding_h: int = 12,
    padding_v: int = 6,
    on_click = None,
    tooltip: str | None = None,
) -> ft.Container:
    """Creates a sleek, floating status capsule pill."""
    items = []
    if icon:
        if isinstance(icon, str):
            items.append(ft.Text(icon, size=14))
        else:
            items.append(ft.Icon(icon, size=14, color=TEXT_MAIN))
    if isinstance(content, str):
        items.append(ft.Text(content, size=11, weight=ft.FontWeight.W_800, color=TEXT_MAIN))
    else:
        items.append(content)

    return ft.Container(
        content=ft.Row(items, tight=True, spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=padding_h, vertical=padding_v),
        border_radius=ft.BorderRadius.all(24),
        border=ft.Border(
            top=ft.BorderSide(1.5, border_color),
            left=ft.BorderSide(1.5, border_side_color if 'border_side_color' in locals() else border_color),
            right=ft.BorderSide(1.5, border_color),
            bottom=ft.BorderSide(2.5, bottom_rim),
        ),
        shadow=soft_shadow(color="#06000000", blur=4, offset_y=2),
        on_click=on_click,
        tooltip=tooltip,
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
    )

def wood_banner(
    title: str,
    subtitle: str | None = None,
    icon_left: str = "✨",
    icon_right: str = "✨",
    width: int | float = 540,
    font_size: int = 14,
) -> ft.Container:
    """Creates a clean, modern title banner."""
    title_row = [
        ft.Text(icon_left, size=font_size + 2),
        ft.Text(title, size=font_size, weight=ft.FontWeight.W_800, color=TEXT_MAIN, text_align=ft.TextAlign.CENTER),
        ft.Text(icon_right, size=font_size + 2),
    ]

    col_items = [ft.Row(title_row, alignment=ft.MainAxisAlignment.CENTER, spacing=6, tight=True)]
    if subtitle:
        col_items.append(
            ft.Text(subtitle, size=max(10, font_size - 4), weight=ft.FontWeight.BOLD, color=TEXT_SUB, text_align=ft.TextAlign.CENTER)
        )

    return ft.Container(
        content=ft.Column(col_items, spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=WHITE,
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        border_radius=ft.BorderRadius.all(16),
        border=ft.Border(
            top=ft.BorderSide(1.5, BORDER_SUBTLE),
            left=ft.BorderSide(1.5, BORDER_SUBTLE),
            right=ft.BorderSide(1.5, BORDER_SUBTLE),
            bottom=ft.BorderSide(3.5, BORDER_RIM),
        ),
        shadow=soft_shadow(color="#0A000000", blur=6, offset_y=2),
        width=width,
        alignment=ft.Alignment.CENTER,
    )

# ==========================================
# MODERN BOTTOM NAVIGATION BAR
# ==========================================

def modern_bottom_nav(
    active_tab: str,
    navigate,
    audio,
    page: ft.Page | None = None,
    state = None,
) -> ft.Container:
    """Creates a modern floating bottom tab navigation bar."""
    
    tabs = [
        {"id": "home", "icon": "🏠", "label": "Beranda", "route": "dashboard"},
        {"id": "learn", "icon": "📖", "label": "Belajar", "route": "learn"},
        {"id": "quiz", "icon": "🎯", "label": "Kuis", "route": "quiz"},
        {"id": "avatar", "icon": "👤", "label": "Avatar", "route": "avatar"},
    ]

    buttons = []
    for t in tabs:
        is_active = t["id"] == active_tab

        def make_tab_click(target_route):
            def on_click(e):
                audio.play_click()
                navigate(target_route)
            return on_click

        tab_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Text(t["icon"], size=18 if not is_active else 20),
                    ft.Text(
                        t["label"],
                        size=11 if not is_active else 12,
                        weight=ft.FontWeight.W_900 if is_active else ft.FontWeight.BOLD,
                        color=DUO_GREEN_RIM if is_active else TEXT_SUB,
                    ),
                ],
                spacing=6,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=DUO_GREEN_LIGHT if is_active else None,
            padding=ft.Padding.symmetric(horizontal=14 if is_active else 10, vertical=8),
            border_radius=ft.BorderRadius.all(16),
            border=ft.Border.all(1.5, "#BBF7D0") if is_active else None,
            on_click=make_tab_click(t["route"]),
            animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
        )
        buttons.append(tab_btn)

    nav_w = 540
    if page:
        m = get_screen_metrics(page)
        if m["is_mobile"]:
            nav_w = None

    return ft.Container(
        content=ft.Row(
            buttons,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=WHITE,
        height=58,
        width=nav_w,
        border_radius=ft.BorderRadius.all(24),
        border=ft.Border(
            top=ft.BorderSide(1.5, "#E2E8F0"),
            left=ft.BorderSide(1.5, "#E2E8F0"),
            right=ft.BorderSide(1.5, "#E2E8F0"),
            bottom=ft.BorderSide(3.5, "#CBD5E1"),
        ),
        shadow=vibrant_shadow(color="#10000000", blur=16, offset_y=4),
        padding=ft.Padding.symmetric(horizontal=16),
        margin=ft.Padding.only(top=10, bottom=6),
    )

# ==========================================
# MODERN RESPONSIVE APP SHELL
# Full-bleed adaptive layout for Laptop, Smartboard, iPad & HP
# ==========================================

def modern_app_shell(
    content: ft.Control,
    page: ft.Page,
    bottom_nav: ft.Control | None = None,
) -> ft.Container:
    """Wraps entire screen into a genuinely responsive, modern & elegant canvas.
    - Adapts dynamically to HP (Mobile), iPad (Tablet), and Laptop/Smartboard (Desktop).
    - Eliminates awkward gaps and frames; centers comfortably on widescreen displays.
    """
    m = get_screen_metrics(page)
    max_w = m["max_container_w"]
    padding_h = m["padding_h"]

    # Centered floating bottom navigation dock if provided
    bottom_section = ft.Container(height=0)
    if bottom_nav:
        bottom_section = ft.Row(
            [bottom_nav],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # Main content column with proper spacing (no giant dead gaps!)
    inner_column = ft.Column(
        [
            content,
            bottom_section,
        ],
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
    )

    # Responsive constrained container (centers gracefully on laptop/smartboard/iPad, full width on HP)
    responsive_box = ft.Container(
        content=inner_column,
        width=max_w,
        alignment=ft.Alignment.TOP_CENTER,
    )

    # Centered Row prevents cross-axis stretching across 1920px
    centered_wrapper = ft.Row(
        [responsive_box],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # Scrollable wrapper ensuring smooth vertical panning when needed
    scroll_body = ft.Column(
        [
            centered_wrapper
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Elegant, clean, soft backdrop across the entire screen
    return ft.Container(
        content=scroll_body,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=["#F0FDF4", "#F8FAFC", "#F1F5F9"], # Fresh subtle mint to refined slate
        ),
        padding=ft.Padding.symmetric(
            horizontal=padding_h,
            vertical=14,
        ),
        expand=True,
        alignment=ft.Alignment.TOP_CENTER,
    )

# Backward Compatibility Alias
jungle_screen_container = modern_app_shell
