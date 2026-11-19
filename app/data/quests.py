# Quests and Achievements Definition

ACHIEVEMENTS = [
    {
        "id": "first_word",
        "title": "Jungle Explorer",
        "desc": "Listen to your first English word",
        "emoji": "🦁",
        "condition": lambda state: state.words_learned >= 1,
    },
    {
        "id": "quiz_rookie",
        "title": "Quiz Cadet",
        "desc": "Complete your first Quiz Challenge",
        "emoji": "🎯",
        "condition": lambda state: state.quizzes_completed >= 1,
    },
    {
        "id": "star_collector",
        "title": "Star Collector",
        "desc": "Collect at least 50 Gold Stars",
        "emoji": "⭐",
        "condition": lambda state: state.stars >= 50,
    },
    {
        "id": "star_legend",
        "title": "Golden Legend",
        "desc": "Collect at least 150 Gold Stars",
        "emoji": "👑",
        "condition": lambda state: state.stars >= 150,
    },
    {
        "id": "vocabulary_champ",
        "title": "Word Master",
        "desc": "Tap and learn 10 different words",
        "emoji": "📚",
        "condition": lambda state: state.words_learned >= 10,
    },
    {
        "id": "quiz_champ",
        "title": "Quiz Master",
        "desc": "Complete 3 quiz rounds",
        "emoji": "🏆",
        "condition": lambda state: state.quizzes_completed >= 3,
    },
]
