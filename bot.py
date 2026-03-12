import json
import os
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("TOKEN", "HIER_DEIN_BOTFATHER_TOKEN")
ADMIN_ID = 6051699852
DATA_FILE = "users.json"
LOGO_FILE = "logo.png"

THEORY_TEXT = (
    "📘 Theorie: Einführung in Python\n\n"
    "Python ist eine Programmiersprache. Sie ist einfach und sehr gut für Anfänger geeignet.\n\n"
    "Mit Python kann man Programme schreiben, Daten verarbeiten und viele Aufgaben automatisieren.\n\n"
    "Eine Variable speichert einen Wert.\n\n"
    "Beispiel:\n"
    "x = 10\n\n"
    "Hier ist:\n"
    "• x → die Variable\n"
    "• 10 → der Wert\n\n"
    "Ein weiteres Beispiel:\n"
    "name = \"Ali\"\n\n"
    "Die Funktion print() gibt Informationen auf dem Bildschirm aus.\n\n"
    "Beispiel:\n"
    "print(\"Hallo\")\n\n"
    "Wichtige Regeln:\n"
    "• Texte stehen in Anführungszeichen\n"
    "• Zahlen schreibt man direkt\n"
    "• Das Gleichheitszeichen = benutzt man für eine Zuweisung\n\n"
    "Wenn Sie fertig sind, senden Sie bitte /weiter."
)

VOCAB_TEXT = (
    "📚 Wortschatz: Python-Grundlagen\n\n"
    "die Programmiersprache — dasturlash tili — язык программирования\n"
    "das Programm — dastur — программа\n"
    "der Code — kod — код\n"
    "programmieren — dasturlash — программировать\n"
    "die Variable — o‘zgaruvchi — переменная\n"
    "der Wert — qiymat — значение\n"
    "die Zahl — son — число\n"
    "der Text — matn — текст\n"
    "die Zeichenkette — satr / string — строка\n"
    "die Funktion — funksiya — функция\n"
    "die print-Funktion — print funksiyasi — функция print\n"
    "ausgeben — chiqarish — выводить\n"
    "anzeigen — ko‘rsatish — отображать\n"
    "das Gleichheitszeichen — teng belgisi — знак равенства\n"
    "die Klammer — qavs — скобка\n"
    "die Anführungszeichen — qo‘shtirnoq — кавычки\n"
    "der Befehl — buyruq — команда\n"
    "das Ergebnis — natija — результат\n"
    "der Fehler — xato — ошибка\n"
    "die Datei — fayl — файл\n\n"
    "Wenn Sie fertig sind, senden Sie bitte /weiter."
)

MISSIONS = [
    {
        "id": 1,
        "task": (
            "Mission 1 💻\n\n"
            "Erstellen Sie eine Variable `x` mit dem Wert `10`.\n\n"
            "Bitte senden Sie Ihre Antwort als normale Nachricht."
        ),
        "answers": ["x=10"],
    },
    {
        "id": 2,
        "task": (
            "Mission 2 💻\n\n"
            "Erstellen Sie eine Variable `name` mit dem Wert `\"Ali\"`.\n\n"
            "Bitte senden Sie Ihre Antwort als normale Nachricht."
        ),
        "answers": ["name=ali"],
    },
    {
        "id": 3,
        "task": (
            "Mission 3 💻\n\n"
            "Schreiben Sie einen Befehl mit `print()`, der `\"Hallo\"` ausgibt.\n\n"
            "Bitte senden Sie Ihre Antwort als normale Nachricht."
        ),
        "answers": ["print(hallo)"],
    },
]

QUIZZES = [
    {
        "question": "Was ist Python?",
        "options": {"a": "ein Betriebssystem", "b": "eine Programmiersprache", "c": "ein Browser"},
        "correct": "b",
        "explanation": "Richtig ist: Python ist eine Programmiersprache.",
    },
    {
        "question": "Was ist eine Variable?",
        "options": {"a": "ein gespeicherter Name für einen Wert", "b": "ein Bild", "c": "ein Fehler"},
        "correct": "a",
        "explanation": "Richtig ist: Eine Variable speichert einen Wert.",
    },
    {
        "question": "Welches Zeichen benutzt man für eine Zuweisung?",
        "options": {"a": "+", "b": "=", "c": ":"},
        "correct": "b",
        "explanation": "Richtig ist: =",
    },
    {
        "question": "Was ist ein Text?",
        "options": {"a": "15", "b": "\"Ali\"", "c": "10"},
        "correct": "b",
        "explanation": "Richtig ist: \"Ali\" ist ein Text.",
    },
    {
        "question": "Was macht print()?",
        "options": {"a": "Es löscht Daten", "b": "Es erstellt Variablen", "c": "Es gibt Informationen aus"},
        "correct": "c",
        "explanation": "Richtig ist: print() gibt Informationen aus.",
    },
    {
        "question": "Welche Schreibweise ist richtig?",
        "options": {"a": "name = Ali", "b": "name = \"Ali\"", "c": "name : \"Ali\""},
        "correct": "b",
        "explanation": "Richtig ist: name = \"Ali\"",
    },
    {
        "question": "Was ist die Ausgabe?\n\nx = 5\nprint(x)",
        "options": {"a": "x", "b": "5", "c": "Fehler"},
        "correct": "b",
        "explanation": "Richtig ist: 5",
    },
    {
        "question": "Was ist eine Zahl?",
        "options": {"a": "\"10\"", "b": "10", "c": "\"Hallo\""},
        "correct": "b",
        "explanation": "Richtig ist: 10 ist eine Zahl.",
    },
    {
        "question": "Welche Zeile ist Python-Code?",
        "options": {"a": "print(\"Hallo\")", "b": "<h1>Hallo</h1>", "c": "SELECT * FROM users"},
        "correct": "a",
        "explanation": "Richtig ist: print(\"Hallo\")",
    },
    {
        "question": "Wofür braucht man Variablen?",
        "options": {"a": "zum Zeichnen", "b": "zum Speichern von Werten", "c": "zum Drucken von Bildern"},
        "correct": "b",
        "explanation": "Richtig ist: Variablen speichert man für Werte.",
    },
]


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_user(update: Update, data: dict):
    user_id = str(update.effective_user.id)
    if user_id not in data:
        data[user_id] = {
            "name": update.effective_user.first_name or "Student/in",
            "points": 0,
            "step": "start",   # theory, vocab, mission_1 ... quiz_10, done
            "quiz_index": None,
        }
    return user_id, data[user_id]


def normalize_text(text: str) -> str:
    return (
        text.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace('"', "")
        .replace("'", "")
        .replace("`", "")
        .lower()
    )


def get_level(points: int) -> str:
    if points >= 130:
        return "Experte/Expertin"
    if points >= 90:
        return "Fortgeschritten"
    if points >= 50:
        return "Lerner/Lernerin"
    return "Anfänger/Anfängerin"


async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Bot starten"),
        BotCommand("weiter", "Zum nächsten Schritt gehen"),
        BotCommand("hilfe", "Hilfe öffnen"),
        BotCommand("punkte", "Punkte anzeigen"),
        BotCommand("niveau", "Niveau anzeigen"),
    ]
    await app.bot.set_my_commands(commands)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    user["step"] = "theory"
    user["quiz_index"] = None
    save_data(data)

    caption = (
        f"Willkommen, {user['name']}! 👋\n\n"
        "Lektion 1: Einführung in Python\n"
        "Thema: Variablen und print()\n\n"
        "Lernweg:\n"
        "1. Theorie\n"
        "2. Wortschatz\n"
        "3. 3 Missionen\n"
        "4. 10 Quizfragen\n"
        "5. Abschluss\n\n"
        "Befehle:\n"
        "/weiter – nächster Schritt\n"
        "/hilfe – Hilfe\n"
        "/punkte – Ihre Punkte\n"
        "/niveau – Ihr Niveau\n\n"
        "Bitte lesen Sie jetzt zuerst die Theorie."
    )

    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "rb") as photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=caption
            )
    else:
        await update.message.reply_text(caption)

    await update.message.reply_text(THEORY_TEXT)


async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Hilfebereich 🛠\n\n"
        "So arbeiten Sie mit dem Bot:\n"
        "1. /start\n"
        "2. Theorie lesen\n"
        "3. /weiter\n"
        "4. Wortschatz lesen\n"
        "5. /weiter\n"
        "6. Missionen lösen\n"
        "7. /weiter\n"
        "8. Quiz lösen\n\n"
        "Befehle:\n"
        "/start\n"
        "/weiter\n"
        "/hilfe\n"
        "/punkte\n"
        "/niveau\n\n"
        "Quiz-Antworten:\n"
        "/a\n"
        "/b\n"
        "/c"
    )
    await update.message.reply_text(text)


async def weiter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    step = user.get("step", "start")

    if step == "theory":
        user["step"] = "vocab"
        save_data(data)
        await update.message.reply_text(VOCAB_TEXT)
        return

    if step == "vocab":
        user["step"] = "mission_1"
        save_data(data)
        await update.message.reply_text(MISSIONS[0]["task"])
        return

    if step == "mission_1_done":
        user["step"] = "mission_2"
        save_data(data)
        await update.message.reply_text(MISSIONS[1]["task"])
        return

    if step == "mission_2_done":
        user["step"] = "mission_3"
        save_data(data)
        await update.message.reply_text(MISSIONS[2]["task"])
        return

    if step == "mission_3_done":
        user["step"] = "quiz_1"
        user["quiz_index"] = 0
        save_data(data)
        await send_quiz(update, context, 0)
        return

    if step.startswith("quiz_"):
        quiz_index = user.get("quiz_index")
        if quiz_index is None:
            await update.message.reply_text("Bitte senden Sie zuerst /start.")
            return

        if quiz_index < len(QUIZZES) - 1:
            quiz_index += 1
            user["quiz_index"] = quiz_index
            user["step"] = f"quiz_{quiz_index + 1}"
            save_data(data)
            await send_quiz(update, context, quiz_index)
            return
        else:
            user["step"] = "done"
            save_data(data)
            await send_final_result(update, context, user)
            return

    if step == "done":
        await update.message.reply_text(
            "Sie haben diese Lektion bereits abgeschlossen. 🎉\n"
            "Senden Sie /start, wenn Sie noch einmal beginnen möchten."
        )
        return

    await update.message.reply_text("Bitte senden Sie zuerst /start.")


async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, index: int):
    q = QUIZZES[index]
    text = (
        f"Quiz {index + 1} 🧠\n\n"
        f"{q['question']}\n\n"
        f"a) {q['options']['a']}\n"
        f"b) {q['options']['b']}\n"
        f"c) {q['options']['c']}\n\n"
        "Bitte antworten Sie mit:\n"
        "/a\n"
        "/b\n"
        "/c"
    )
    await update.message.reply_text(text)


async def answer_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_quiz_answer(update, context, "a")


async def answer_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_quiz_answer(update, context, "b")


async def answer_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_quiz_answer(update, context, "c")


async def check_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str):
    data = load_data()
    user_id, user = get_user(update, data)

    step = user.get("step", "")
    if not step.startswith("quiz_"):
        await update.message.reply_text(
            "Im Moment ist kein Quiz aktiv.\nBitte senden Sie /weiter."
        )
        return

    quiz_index = user.get("quiz_index")
    if quiz_index is None:
        await update.message.reply_text("Bitte senden Sie /weiter.")
        return

    q = QUIZZES[quiz_index]

    if answer == q["correct"]:
        user["points"] += 10
        save_data(data)

        await update.message.reply_text(
            f"Richtig! ✅\n{q['explanation']}\nSie haben +10 Punkte bekommen.\n\n"
            "Senden Sie /weiter für den nächsten Schritt."
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Frage: {q['question']}\n"
                f"Antwort: /{answer}\n"
                f"Ergebnis: RICHTIG ✅\n"
                f"Vergebene Punkte: +10\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )
    else:
        save_data(data)

        await update.message.reply_text(
            f"Falsch ❌\n{q['explanation']}\nVergebene Punkte: 0\n\n"
            "Senden Sie /weiter für den nächsten Schritt."
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Frage: {q['question']}\n"
                f"Antwort: /{answer}\n"
                f"Ergebnis: FALSCH ❌\n"
                f"Vergebene Punkte: 0\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )


async def punkte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    await update.message.reply_text(
        f"{user['name']}, Ihre Gesamtpunktzahl ist: {user['points']} 🏆"
    )


async def niveau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    await update.message.reply_text(
        f"{user['name']}, Ihr aktuelles Niveau ist: {get_level(user['points'])}"
    )


async def send_final_result(update: Update, context: ContextTypes.DEFAULT_TYPE, user: dict):
    text = (
        "🎉 Abschluss der Lektion\n\n"
        "Sie haben die erste Python-Lektion erfolgreich abgeschlossen.\n\n"
        f"Gesamtpunktzahl: {user['points']} 🏆\n"
        f"Niveau: {get_level(user['points'])}\n\n"
        "Senden Sie /start, wenn Sie noch einmal beginnen möchten."
    )
    await update.message.reply_text(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    data = load_data()
    user_id, user = get_user(update, data)
    step = user.get("step", "")

    message_text = update.message.text
    normalized = normalize_text(message_text)

    if step == "mission_1":
        if normalized in MISSIONS[0]["answers"]:
            user["points"] += 15
            user["step"] = "mission_1_done"
            save_data(data)

            await update.message.reply_text(
                "Richtig! ✅\n"
                "Mission 1 wurde erfolgreich gelöst.\n"
                "Sie haben +15 Punkte bekommen.\n\n"
                "Senden Sie /weiter."
            )

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📩 Missions-Antwort\n\n"
                    f"Student/in: {user['name']}\n"
                    f"ID: {user_id}\n\n"
                    f"Mission: 1\n"
                    f"Antwort: {message_text}\n"
                    f"Ergebnis: RICHTIG ✅\n"
                    f"Vergebene Punkte: +15\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal."
            )
        return

    if step == "mission_2":
        if normalized in MISSIONS[1]["answers"]:
            user["points"] += 15
            user["step"] = "mission_2_done"
            save_data(data)

            await update.message.reply_text(
                "Richtig! ✅\n"
                "Mission 2 wurde erfolgreich gelöst.\n"
                "Sie haben +15 Punkte bekommen.\n\n"
                "Senden Sie /weiter."
            )

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📩 Missions-Antwort\n\n"
                    f"Student/in: {user['name']}\n"
                    f"ID: {user_id}\n\n"
                    f"Mission: 2\n"
                    f"Antwort: {message_text}\n"
                    f"Ergebnis: RICHTIG ✅\n"
                    f"Vergebene Punkte: +15\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal."
            )
        return

    if step == "mission_3":
        if normalized in MISSIONS[2]["answers"]:
            user["points"] += 15
            user["step"] = "mission_3_done"
            save_data(data)

            await update.message.reply_text(
                "Richtig! ✅\n"
                "Mission 3 wurde erfolgreich gelöst.\n"
                "Sie haben +15 Punkte bekommen.\n\n"
                "Senden Sie /weiter."
            )

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📩 Missions-Antwort\n\n"
                    f"Student/in: {user['name']}\n"
                    f"ID: {user_id}\n\n"
                    f"Mission: 3\n"
                    f"Antwort: {message_text}\n"
                    f"Ergebnis: RICHTIG ✅\n"
                    f"Vergebene Punkte: +15\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal."
            )
        return


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weiter", weiter))
    app.add_handler(CommandHandler("hilfe", hilfe))
    app.add_handler(CommandHandler("punkte", punkte))
    app.add_handler(CommandHandler("niveau", niveau))

    app.add_handler(CommandHandler("a", answer_a))
    app.add_handler(CommandHandler("b", answer_b))
    app.add_handler(CommandHandler("c", answer_c))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.post_init = set_bot_commands

    print("Bot ist gestartet...")
    app.run_polling()


if __name__ == "__main__":
    main()