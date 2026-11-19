# Animal Avatar Definitions for Jungle Adventure

AVATARS = [
    {
        "id": "lion",
        "name": "Leo the Lion",
        "species": "Lion",
        "emoji": "🦁",
        "tagline": "Brave Safari King!",
        "color": "#FFF3E0",
        "border_color": "#FF9800",
        "badge_color": "#FFA726",
    },
    {
        "id": "giraffe",
        "name": "Gigi the Giraffe",
        "species": "Giraffe",
        "emoji": "🦒",
        "tagline": "Curious Sky Scout!",
        "color": "#FFFDE7",
        "border_color": "#FDD835",
        "badge_color": "#FFEE58",
    },
    {
        "id": "monkey",
        "name": "Momo the Monkey",
        "species": "Monkey",
        "emoji": "🐒",
        "tagline": "Fun Acrobat Buddy!",
        "color": "#EFEBE9",
        "border_color": "#8D6E63",
        "badge_color": "#A1887F",
    },
    {
        "id": "elephant",
        "name": "Ellie the Elephant",
        "species": "Elephant",
        "emoji": "🐘",
        "tagline": "Wise & Gentle Giant!",
        "color": "#ECEFF1",
        "border_color": "#78909C",
        "badge_color": "#90A4AE",
    },
    {
        "id": "tiger",
        "name": "Toby the Tiger",
        "species": "Tiger",
        "emoji": "🐯",
        "tagline": "Speedy Jungle Runner!",
        "color": "#FBE9E7",
        "border_color": "#FF7043",
        "badge_color": "#FF8A65",
    },
    {
        "id": "panda",
        "name": "Pip the Panda",
        "species": "Panda",
        "emoji": "🐼",
        "tagline": "Cuddly Bamboo Scout!",
        "color": "#F5F5F5",
        "border_color": "#424242",
        "badge_color": "#616161",
    },
]

def get_avatar_by_id(avatar_id: str) -> dict:
    for a in AVATARS:
        if a["id"] == avatar_id:
            return a
    return AVATARS[0]
