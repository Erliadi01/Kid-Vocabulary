import os
import re
from pathlib import Path
from gtts import gTTS
from app.data.vocabulary import VOCABULARY

def generate_all_audio():
    out_dir = Path("assets/audio")
    out_dir.mkdir(parents=True, exist_ok=True)

    words_to_generate = {}
    for cat in VOCABULARY.values():
        for item in cat:
            filename = re.sub(r"[^a-z0-9_]", "", item["id"].lower().replace(" ", "_")) + ".mp3"
            words_to_generate[filename] = item["pronunciation"]

    extra = {
        "correct.mp3": "Correct! Well done!",
        "try_again.mp3": "Try again, you can do it!",
        "great_job.mp3": "Great job!",
        "awesome.mp3": "Awesome!",
        "sound_on.mp3": "Sound on!",
        "lets_learn_english.mp3": "Let's learn English!",
        "welcome.mp3": "Welcome to Jungle Adventure!",
        "quiz_completed.mp3": "Quiz completed! Fantastic effort!",
        "leo_the_lion.mp3": "Leo the Lion",
        "maya_the_monkey.mp3": "Maya the Monkey",
        "eli_the_elephant.mp3": "Eli the Elephant",
        "gigi_the_giraffe.mp3": "Gigi the Giraffe",
        "toby_the_tiger.mp3": "Toby the Tiger",
        "pipo_the_parrot.mp3": "Pipo the Parrot"
    }
    words_to_generate.update(extra)

    print(f"Total audio files to check/generate: {len(words_to_generate)}")
    for fn, text in words_to_generate.items():
        dest = out_dir / fn
        if not dest.exists():
            try:
                tts = gTTS(text=text, lang="en", slow=False)
                tts.save(str(dest))
                print(f"Generated: {fn} -> '{text}'")
            except Exception as e:
                print(f"Failed {fn}: {e}")
        else:
            print(f"Exists: {fn}")

    print("All audio files ready in assets/audio/!")

if __name__ == "__main__":
    generate_all_audio()
