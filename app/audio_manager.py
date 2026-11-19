import os
import re
import json
import base64
import random
import time
import threading
import queue
from pathlib import Path
import flet as ft

AUDIO_DIR = Path("assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def safe_filename(text: str) -> str:
    """Converts a phrase into a clean filename like 'lion.mp3'."""
    clean = re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip().lower()).strip("_")
    if not clean:
        clean = "speech"
    return f"{clean}.mp3"

def ensure_mp3_exists(text: str) -> str:
    """Ensures an .mp3 file exists for the given text using gTTS if missing."""
    filename = safe_filename(text)
    file_path = AUDIO_DIR / filename
    if not file_path.exists():
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(str(file_path))
            print(f"[AudioManager/gTTS] Generated audio file: assets/audio/{filename} for '{text}'")
        except Exception as e:
            print(f"[AudioManager/gTTS] Notice: Could not generate mp3 online ({e}), will use browser speech.")
    return filename

class AudioManager:
    """Next-Generation Multi-Platform Audio Engine:
    - Web / HP mode: 100% audio directly through user device browser speaker:
      * HTML5 Audio element: new Audio('/audio/{filename}').play()
      * Fallback: Web Speech API (window.speechSynthesis)
      * High-fidelity Web Audio API for interactive SFX (clicks, chimes, buzzers)
      * Server laptop stays 100% silent in web mode.
    - Native Desktop mode: Safe Windows SAPI in background thread.
    - Clean terminal logs for real-time monitoring.
    """

    def __init__(self, state, page: ft.Page | None = None):
        self.state = state
        self.page = page

        if self.page:
            self._bind_page(self.page)

        # Clear overlay completely to prevent 'Unknown control' red boxes
        if self.page and hasattr(self.page, "overlay"):
            try:
                self.page.overlay.clear()
            except Exception:
                pass

        # Desktop TTS worker queue (only active in native desktop window mode)
        self.desktop_queue = queue.Queue()
        self.running = True
        self.desktop_thread = None

        if not self.is_web_mode():
            self.desktop_thread = threading.Thread(target=self._desktop_worker, daemon=True)
            self.desktop_thread.start()

    def _bind_page(self, page: ft.Page):
        """Binds page and ensures page.run_javascript is attached."""
        self.page = page
        
        # Attach user-friendly run_javascript helper to page
        def _exec_js(code: str):
            self._execute_client_js(code)
            
        self.page.run_javascript = _exec_js
        if hasattr(self.page, "overlay"):
            try:
                self.page.overlay.clear()
            except Exception:
                pass

    def set_page(self, page: ft.Page):
        """Update active page reference."""
        self._bind_page(page)

    def is_web_mode(self) -> bool:
        """Checks if current session is running in web mode (HP, tablet, or web browser)."""
        if os.environ.get("FLET_WEB_MODE") == "1" or os.environ.get("FLET_FORCE_WEB_SERVER") == "1":
            return True
        if self.page:
            if getattr(self.page, "web", False):
                return True
            if getattr(self.page, "client_ip", None):
                return True
            p_str = str(getattr(self.page, "platform", "")).lower()
            if "web" in p_str:
                return True
        return False

    def _execute_client_js(self, code: str):
        """Sends JavaScript to client browser to execute."""
        if not self.page:
            return
        clean_code = code.strip()
        try:
            b64_str = base64.b64encode(clean_code.encode("utf-8")).decode("ascii")
            token = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"
            self.page.title = f"JS:{b64_str}##{token}"
            self.page.update()
        except Exception as e:
            print(f"[AudioManager] JS dispatch error: {e}")

    def speak(self, text: str, rate: int | None = None):
        """Speak English text through client device speaker (HP) or desktop speaker."""
        if not self.state.sound_enabled or not text:
            return

        print(f"[AudioManager] Speaking: '{text}'")

        # 1. MODE WEB (HP / TABLET / BROWSER):
        # Jalankan audio langsung di speaker browser HP via HTML5 Audio + Web Speech API fallback.
        # Server laptop tetap 100% hening!
        if self.is_web_mode() and self.page:
            # Pastikan file audio mp3 sudah siap di assets/audio/
            filename = ensure_mp3_exists(text)
            safe_text_json = json.dumps(str(text))

            # Jalankan JavaScript Audio HTML5 dengan fallback Web Speech API
            audio_js = f"""
            try {{
                const audio = new Audio('/audio/{filename}');
                const playPromise = audio.play();
                if (playPromise !== undefined) {{
                    playPromise.catch(err => {{
                        console.warn('Audio play error, using Web Speech API fallback:', err);
                        window.speechSynthesis.cancel();
                        const u = new SpeechSynthesisUtterance({safe_text_json});
                        u.lang = 'en-US';
                        u.rate = 0.9;
                        window.speechSynthesis.speak(u);
                    }});
                }}
            }} catch(e) {{
                try {{
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance({safe_text_json});
                    u.lang = 'en-US';
                    u.rate = 0.9;
                    window.speechSynthesis.speak(u);
                }} catch(e2) {{
                    console.error('TTS error:', e2);
                }}
            }}
            """
            try:
                # Trigger via bridge and page.run_javascript
                token = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"
                self.page.title = f"SND:file:{filename}:{text}##{token}"
                self.page.update()
                print(f"[AudioManager] Dispatched '{text}' -> /audio/{filename} to HP speaker")
            except Exception as e:
                print(f"[AudioManager] Web dispatch error: {e}")
            return  # Stop di sini! Jangan bunyikan laptop server

        # 2. MODE DESKTOP LOKAL (main.py di Windows):
        try:
            if not self.desktop_thread:
                self.desktop_thread = threading.Thread(target=self._desktop_worker, daemon=True)
                self.desktop_thread.start()

            while not self.desktop_queue.empty():
                try:
                    self.desktop_queue.get_nowait()
                    self.desktop_queue.task_done()
                except Exception:
                    pass
            self.desktop_queue.put((str(text), rate))
        except Exception:
            pass

    # ==========================
    # SOUND EFFECTS (SFX)
    # ==========================

    def play_click(self):
        """Short soft tactile sound effect when pressing buttons."""
        if not self.state.sound_enabled:
            return

        if self.is_web_mode() and self.page:
            try:
                token = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"
                self.page.title = f"SND:sfx:click##{token}"
                self.page.update()
                print("[AudioManager] Played SFX: click on HP")
            except Exception:
                pass
            return

        # Desktop fallback beep
        try:
            import winsound
            threading.Thread(target=lambda: winsound.Beep(700, 30), daemon=True).start()
        except Exception:
            pass

    def play_correct(self):
        """Happy ascending chime when answering correctly."""
        if not self.state.sound_enabled:
            return

        if self.is_web_mode() and self.page:
            try:
                token = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"
                self.page.title = f"SND:sfx:correct##{token}"
                self.page.update()
                print("[AudioManager] Played SFX: correct on HP")
            except Exception:
                pass
            return

        # Desktop fallback chime
        def _desk_chime():
            try:
                import winsound
                winsound.Beep(523, 70)
                winsound.Beep(659, 70)
                winsound.Beep(784, 120)
            except Exception:
                pass
        threading.Thread(target=_desk_chime, daemon=True).start()

    def play_wrong(self):
        """Gentle encouraging sound when wrong answer is picked."""
        if not self.state.sound_enabled:
            return

        if self.is_web_mode() and self.page:
            try:
                token = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"
                self.page.title = f"SND:sfx:wrong##{token}"
                self.page.update()
                print("[AudioManager] Played SFX: wrong on HP")
            except Exception:
                pass
            return

        # Desktop fallback buzzer
        def _desk_buzz():
            try:
                import winsound
                winsound.Beep(260, 100)
                winsound.Beep(180, 150)
            except Exception:
                pass
        threading.Thread(target=_desk_buzz, daemon=True).start()

    # ==========================
    # DESKTOP SAPI WORKER
    # ==========================

    def _desktop_worker(self):
        """Persistent background worker for desktop mode."""
        sapi_voice = None
        com_initialized = False
        try:
            import pythoncom
            pythoncom.CoInitialize()
            com_initialized = True
            import win32com.client
            sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_voice.Rate = -1
            sapi_voice.Volume = 100
        except Exception as e:
            print(f"[AudioManager] Desktop SAPI notice: {e}")

        while self.running:
            try:
                item = self.desktop_queue.get(timeout=0.5)
                if item is None:
                    break
                text, rate = item
                if sapi_voice:
                    try:
                        if rate is not None:
                            sapi_voice.Rate = rate
                        sapi_voice.Speak(str(text))
                    except Exception as e:
                        print(f"[AudioManager] Desktop speech error: {e}")
                self.desktop_queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                pass

        if com_initialized:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def stop(self):
        """Shutdown worker cleanly."""
        self.running = False
        if self.desktop_thread and self.desktop_thread.is_alive():
            try:
                self.desktop_queue.put(None)
            except Exception:
                pass
