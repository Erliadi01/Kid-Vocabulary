from app.data.avatars import get_avatar_by_id

class AppState:
    def __init__(self):
        # Child Profile
        self.child_name: str = "BUDI"
        self.avatar_id: str = "lion"
        self._custom_avatar: dict | None = None
        self.stars: int = 120

        # Audio settings
        self.sound_enabled: bool = True
        self.speech_rate: int = 145  # Child-friendly pacing

        # Learning Metrics
        self.words_learned: int = 4
        self.quizzes_completed: int = 1

        # Daily Quests
        self.daily_words_count: int = 2
        self.daily_words_target: int = 3

        self.daily_quiz_count: int = 0
        self.daily_quiz_target: int = 1

        self.daily_stars_count: int = 10
        self.daily_stars_target: int = 20
        self.claimed_daily_reward: bool = False

        # Current navigation selection
        self.selected_category: str = "animals"

    @property
    def avatar(self) -> dict:
        if self._custom_avatar:
            return self._custom_avatar
        return get_avatar_by_id(self.avatar_id)

    @avatar.setter
    def avatar(self, val):
        """Allows assigning either an avatar dict or an avatar ID string without crashing."""
        if isinstance(val, dict):
            self._custom_avatar = val
            if "id" in val and val["id"]:
                self.avatar_id = val["id"]
        elif isinstance(val, str):
            self.avatar_id = val
            self._custom_avatar = None
        elif val is None:
            self._custom_avatar = None

    def add_stars(self, count: int):
        self.stars += count
        self.daily_stars_count = min(self.daily_stars_target, self.daily_stars_count + count)

    def record_word_learned(self):
        self.words_learned += 1
        if self.daily_words_count < self.daily_words_target:
            self.daily_words_count += 1

    def record_quiz_completed(self, score: int):
        self.quizzes_completed += 1
        if self.daily_quiz_count < self.daily_quiz_target:
            self.daily_quiz_count += 1

    def claim_daily_bonus(self) -> int:
        if not self.claimed_daily_reward and self.is_all_daily_quests_completed():
            bonus = 25
            self.add_stars(bonus)
            self.claimed_daily_reward = True
            return bonus
        return 0

    def is_all_daily_quests_completed(self) -> bool:
        return (
            self.daily_words_count >= self.daily_words_target
            and self.daily_quiz_count >= self.daily_quiz_target
            and self.daily_stars_count >= self.daily_stars_target
        )

    def toggle_sound(self) -> bool:
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def reset_progress(self):
        self.stars = 0
        self.words_learned = 0
        self.quizzes_completed = 0
        self.daily_words_count = 0
        self.daily_quiz_count = 0
        self.daily_stars_count = 0
        self.claimed_daily_reward = False
