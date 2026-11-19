import os
import sqlite3
from pathlib import Path

DB_FILE = Path("vocab_data.db")

ANIMALS_DATA = [
    ("Lion", "Singa", "🦁", "images/lion.png"),
    ("Monkey", "Monyet", "🐒", "images/monkey.png"),
    ("Elephant", "Gajah", "🐘", "images/elephant.png"),
    ("Giraffe", "Jerapah", "🦒", "images/giraffe.png"),
    ("Tiger", "Harimau", "🐅", "images/tiger.png"),
    ("Zebra", "Zebra", "🦓", "images/zebra.png"),
    ("Hippo", "Kuda Nil", "🦛", "images/hippo.png"),
    ("Parrot", "Burung Beo", "🦜", "images/parrot.png"),
    ("Cat", "Kucing", "🐱", "images/cat.png"),
    ("Dog", "Anjing", "🐶", "images/dog.png"),
    ("Rabbit", "Kelinci", "🐰", "images/rabbit.png"),
    ("Bear", "Beruang", "🐻", "images/bear.png"),
    ("Panda", "Panda", "🐼", "images/panda.png"),
    ("Koala", "Koala", "🐨", "images/koala.png"),
    ("Kangaroo", "Kanguru", "🦘", "images/kangaroo.png"),
    ("Crocodile", "Buaya", "🐊", "images/crocodile.png"),
    ("Turtle", "Kura-kura", "🐢", "images/turtle.png"),
    ("Snake", "Ular", "🐍", "images/snake.png"),
    ("Frog", "Katak", "🐸", "images/frog.png"),
    ("Fish", "Ikan", "🐟", "images/fish.png"),
    ("Shark", "Hiu", "🦈", "images/shark.png"),
    ("Whale", "Paus", "🐋", "images/whale.png"),
    ("Dolphin", "Lumba-lumba", "🐬", "images/dolphin.png"),
    ("Penguin", "Penguin", "🐧", "images/penguin.png"),
    ("Eagle", "Elang", "🦅", "images/eagle.png"),
    ("Owl", "Burung Hantu", "🦉", "images/owl.png"),
    ("Chicken", "Ayam", "🐔", "images/chicken.png"),
    ("Cow", "Sapi", "🐮", "images/cow.png"),
    ("Horse", "Kuda", "🐴", "images/horse.png"),
    ("Sheep", "Domba", "🐑", "images/sheep.png"),
]

# 18 Accurate Fruits with 100% verified Twemoji emojis
FRUITS_DATA = [
    ("Apple", "Apel", "🍎", "images/apple.png"),
    ("Green Apple", "Apel Hijau", "🍏", "images/green_apple.png"),
    ("Banana", "Pisang", "🍌", "images/banana.png"),
    ("Orange", "Jeruk", "🍊", "images/orange.png"),
    ("Lemon", "Lemon", "🍋", "images/lemon.png"),
    ("Grape", "Anggur", "🍇", "images/grape.png"),
    ("Strawberry", "Stroberi", "🍓", "images/strawberry.png"),
    ("Blueberry", "Bluberi", "🫐", "images/blueberry.png"),
    ("Cherry", "Ceri", "🍒", "images/cherry.png"),
    ("Peach", "Persik", "🍑", "images/peach.png"),
    ("Pear", "Pir", "🍐", "images/pear.png"),
    ("Mango", "Mangga", "🥭", "images/mango.png"),
    ("Watermelon", "Semangka", "🍉", "images/watermelon.png"),
    ("Melon", "Melon", "🍈", "images/melon.png"),
    ("Pineapple", "Nanas", "🍍", "images/pineapple.png"),
    ("Coconut", "Kelapa", "🥥", "images/coconut.png"),
    ("Kiwi", "Kiwi", "🥝", "images/kiwi.png"),
    ("Avocado", "Alpukat", "🥑", "images/avocado.png"),
]

COLORS_DATA = [
    ("Red", "Merah", "🔴", "#E53935"),
    ("Blue", "Biru", "🔵", "#1E88E5"),
    ("Yellow", "Kuning", "🟡", "#FDD835"),
    ("Green", "Hijau", "🟢", "#43A047"),
    ("Orange", "Oranye", "🟠", "#FB8C00"),
    ("Purple", "Ungu", "🟣", "#8E24AA"),
    ("Pink", "Merah Muda", "🌸", "#EC407A"),
    ("Black", "Hitam", "⚫", "#212121"),
    ("White", "Putih", "⚪", "#F5F5F5"),
    ("Brown", "Cokelat", "🟤", "#6D4C41"),
    ("Grey", "Abu-abu", "🔘", "#757575"),
    ("Gold", "Emas", "⭐", "#FFB300"),
]

DEFAULT_CLASS_STUDENTS = [
    ("Budi", "🦁", 100, 20, 5, 5),
    ("Siti", "🐰", 95, 19, 5, 5),
    ("Andi", "🐯", 90, 18, 4, 5),
    ("Rina", "🐼", 85, 17, 4, 5),
    ("Dimas", "🐵", 80, 16, 4, 5),
    ("Putri", "🐱", 75, 15, 3, 5),
    ("Rizky", "🐶", 70, 14, 3, 5),
    ("Nabila", "🦊", 65, 13, 3, 5),
    ("Fajar", "🐻", 60, 12, 3, 5),
    ("Aisyah", "🐨", 55, 11, 2, 5),
    ("Gilang", "🐸", 50, 10, 2, 5),
    ("Zahra", "🦄", 45, 9, 2, 5),
    ("Iqbal", "🐘", 40, 8, 2, 5),
    ("Maya", "🦒", 35, 7, 1, 5),
    ("Aldi", "🦛", 30, 6, 1, 5),
]

def _number_to_words(n: int) -> tuple[str, str]:
    ones_en = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
               "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
               "Seventeen", "Eighteen", "Nineteen"]
    tens_en = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    ones_id = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan"]

    if n == 100:
        return "One Hundred", "Seratus"
    if n < 20:
        eng = ones_en[n]
        if n == 10:
            ind = "Sepuluh"
        elif n == 11:
            ind = "Sebelas"
        elif n < 10:
            ind = ones_id[n]
        else:
            ind = ones_id[n - 10] + " Belas"
        return eng, ind

    t = n // 10
    o = n % 10
    if o == 0:
        eng = tens_en[t]
        ind = ones_id[t] + " Puluh"
    else:
        eng = f"{tens_en[t]}-{ones_en[o]}"
        ind = f"{ones_id[t]} Puluh {ones_id[o]}"
    return eng, ind

def get_connection(db_path: str | Path = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str | Path = DB_FILE) -> None:
    """Initializes vocab_data.db: seeds 160 verified vocabularies & 15 class students."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Vocabularies Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabularies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            english TEXT NOT NULL,
            indonesian TEXT NOT NULL,
            emoji TEXT,
            image_path TEXT,
            hex_color TEXT,
            order_num INTEGER
        )
    """)

    # 2. Classroom Leaderboard Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE,
            avatar_emoji TEXT,
            score INTEGER DEFAULT 0,
            stars INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Check fruits count (must be exactly 18 verified fruits)
    cursor.execute("SELECT COUNT(*) FROM vocabularies WHERE category = 'fruits'")
    fruit_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vocabularies")
    total_vocab = cursor.fetchone()[0]

    # Re-seed if empty or outdated fruit count
    if total_vocab == 0 or fruit_count != 18:
        print("[Database] Seeding/Updating 160 vocabularies (with 18 accurate fruits)...")
        cursor.execute("DELETE FROM vocabularies")
        records = []

        # 30 Animals
        for idx, (eng, ind, emo, img) in enumerate(ANIMALS_DATA, start=1):
            records.append(("animals", eng, ind, emo, img, None, idx))

        # 18 Fruits
        for idx, (eng, ind, emo, img) in enumerate(FRUITS_DATA, start=1):
            records.append(("fruits", eng, ind, emo, img, None, idx))

        # 12 Colors
        for idx, (eng, ind, emo, hex_val) in enumerate(COLORS_DATA, start=1):
            records.append(("colors", eng, ind, emo, None, hex_val, idx))

        # 100 Numbers (1 to 100)
        number_emojis = {
            1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣",
            6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"
        }
        for n in range(1, 101):
            eng, ind = _number_to_words(n)
            emo = number_emojis.get(n, "🔢")
            records.append(("numbers", f"{n} - {eng}", ind, emo, None, None, n))

        cursor.executemany("""
            INSERT INTO vocabularies (category, english, indonesian, emoji, image_path, hex_color, order_num)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, records)
        conn.commit()
        print(f"[Database] Successfully seeded {len(records)} vocabularies into vocab_data.db!")

    # Check class leaderboard seed
    cursor.execute("SELECT COUNT(*) FROM class_leaderboard")
    lb_count = cursor.fetchone()[0]
    if lb_count == 0:
        print("[Database] Seeding 15 class students into class_leaderboard...")
        cursor.executemany("""
            INSERT OR IGNORE INTO class_leaderboard (student_name, avatar_emoji, score, stars, correct_answers, total_questions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, DEFAULT_CLASS_STUDENTS)
        conn.commit()
        print("[Database] Successfully seeded 15 class students!")

    conn.close()

def get_category_counts(db_path: str | Path = DB_FILE) -> dict[str, int]:
    """Returns dynamic item counts per category from SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as cnt FROM vocabularies GROUP BY category")
    rows = cursor.fetchall()
    conn.close()
    counts = {r["category"]: r["cnt"] for r in rows}
    return {
        "animals": counts.get("animals", 30),
        "fruits": counts.get("fruits", 18),
        "colors": counts.get("colors", 12),
        "numbers": counts.get("numbers", 100),
    }

def get_vocabularies_by_category(category: str, range_min: int | None = None, range_max: int | None = None, db_path: str | Path = DB_FILE) -> list[dict]:
    """Fetches vocabularies by category, optionally filtered by order_num range."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    if range_min is not None and range_max is not None:
        cursor.execute(
            "SELECT * FROM vocabularies WHERE category = ? AND order_num >= ? AND order_num <= ? ORDER BY order_num ASC",
            (category, range_min, range_max)
        )
    else:
        cursor.execute(
            "SELECT * FROM vocabularies WHERE category = ? ORDER BY order_num ASC",
            (category,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_quiz_question(category: str | None = None, db_path: str | Path = DB_FILE) -> dict | None:
    """Gets 1 target question and 3 distractors randomly from SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    if category and category != "all":
        cursor.execute(
            "SELECT * FROM vocabularies WHERE category = ? ORDER BY RANDOM() LIMIT 4",
            (category,)
        )
    else:
        cursor.execute(
            "SELECT * FROM vocabularies ORDER BY RANDOM() LIMIT 4"
        )
    rows = cursor.fetchall()
    conn.close()
    if not rows or len(rows) < 4:
        return None

    items = [dict(r) for r in rows]
    target = items[0]
    import random
    options = list(items)
    random.shuffle(options)

    return {
        "target": target,
        "options": options,
        "correct_id": target["id"]
    }

# ==========================================
# CLASSROOM LEADERBOARD FUNCTIONS (PROJEKTOR)
# ==========================================

def get_class_leaderboard(db_path: str | Path = DB_FILE) -> list[dict]:
    """Returns all students sorted by score DESC, stars DESC, correct_answers DESC."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM class_leaderboard 
        ORDER BY score DESC, stars DESC, correct_answers DESC, played_at ASC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def update_student_score(student_name: str, correct_count: int, total_count: int, stars_earned: int, avatar_emoji: str = "⭐", db_path: str | Path = DB_FILE) -> tuple[int, int]:
    """Updates student score in class_leaderboard and returns (rank, total_students)."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    quiz_points = correct_count * 20
    clean_name = student_name.strip() if student_name else "Siswa"

    cursor.execute("SELECT * FROM class_leaderboard WHERE LOWER(student_name) = LOWER(?)", (clean_name,))
    existing = cursor.fetchone()

    if existing:
        new_score = existing["score"] + quiz_points
        new_stars = existing["stars"] + stars_earned
        new_correct = existing["correct_answers"] + correct_count
        new_total = existing["total_questions"] + total_count
        cursor.execute("""
            UPDATE class_leaderboard 
            SET score = ?, stars = ?, correct_answers = ?, total_questions = ?, 
                avatar_emoji = COALESCE(?, avatar_emoji), played_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_score, new_stars, new_correct, new_total, avatar_emoji, existing["id"]))
    else:
        cursor.execute("""
            INSERT INTO class_leaderboard (student_name, avatar_emoji, score, stars, correct_answers, total_questions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (clean_name, avatar_emoji, quiz_points, stars_earned, correct_count, total_count))

    conn.commit()

    # Determine rank
    cursor.execute("""
        SELECT student_name FROM class_leaderboard 
        ORDER BY score DESC, stars DESC, correct_answers DESC, played_at ASC
    """)
    all_students = [r["student_name"].lower() for r in cursor.fetchall()]
    conn.close()

    total = len(all_students)
    try:
        rank = all_students.index(clean_name.lower()) + 1
    except ValueError:
        rank = total

    return rank, total

def reset_class_scores(db_path: str | Path = DB_FILE) -> None:
    """Resets all students' scores to 0 for a fresh classroom session."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE class_leaderboard 
        SET score = 0, stars = 0, correct_answers = 0, total_questions = 0, played_at = CURRENT_TIMESTAMP
    """)
    conn.commit()
    conn.close()

def get_student_names(db_path: str | Path = DB_FILE) -> list[str]:
    """Returns list of student names."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT student_name FROM class_leaderboard ORDER BY id ASC")
    names = [r["student_name"] for r in cursor.fetchall()]
    conn.close()
    return names

def add_new_student(name: str, avatar_emoji: str = "⭐", db_path: str | Path = DB_FILE) -> None:
    """Adds a new student to the class leaderboard if not exists."""
    clean_name = name.strip()
    if not clean_name:
        return
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO class_leaderboard (student_name, avatar_emoji, score, stars, correct_answers, total_questions)
        VALUES (?, ?, 0, 0, 0, 0)
    """, (clean_name, avatar_emoji))
    conn.commit()
    conn.close()
