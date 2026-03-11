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

TOKEN = os.getenv("TOKEN", "8753301957:AAFpx6qa7DoNItH80kxboa8rnVByCnithe0")

ADMIN_ID = 6051699852
DATA_FILE = "users.json"
LOGO_FILE = "logo.png"

THEORY_TEXT = (
    "📘 Theorie: Geschlecht und Artikel im Deutschen\n\n"
    "Im Deutschen gibt es drei grammatische Geschlechter:\n"
    "• Maskulinum → der\n"
    "• Femininum → die\n"
    "• Neutrum → das\n\n"
    "Beispiele:\n"
    "• der Mann\n"
    "• die Frau\n"
    "• das Kind\n\n"
    "Bestimmte Artikel:\n"
    "• der Tisch\n"
    "• die Lampe\n"
    "• das Buch\n\n"
    "Unbestimmte Artikel:\n"
    "• ein Mann\n"
    "• eine Frau\n"
    "• ein Kind\n\n"
    "Im Plural steht immer der Artikel „die“:\n"
    "• der Tisch → die Tische\n"
    "• die Lampe → die Lampen\n"
    "• das Buch → die Bücher\n\n"
    "Merksatz:\n"
    "Lernen Sie jedes Nomen immer mit Artikel.\n\n"
    "Wenn Sie fertig sind, senden Sie bitte /weiter."
)

MISSIONS = [
    {
        "id": 1,
        "task": (
            "Mission 1 ✍️\n\n"
            "Ergänzen Sie die richtigen bestimmten Artikel.\n\n"
            "Wörter:\n"
            "• Buch\n"
            "• Tisch\n"
            "• Lampe\n\n"
            "Bitte senden Sie Ihre Antwort als normale Nachricht."
        ),
        "answers": [
            "dasbuch,dertisch,dielampe",
            "dasbuch;dertisch;dielampe",
            "dasbuchdertischdielampe",
        ],
    },
    {
        "id": 2,
        "task": (
            "Mission 2 ✍️\n\n"
            "Schreiben Sie die Nomen mit richtigem Artikel.\n\n"
            "Wörter:\n"
            "• Mann\n"
            "• Frau\n"
            "• Kind\n\n"
            "Bitte senden Sie Ihre Antwort als normale Nachricht."
        ),
        "answers": [
            "dermann,diefrau,daskind",
            "dermann;diefrau;daskind",
            "dermanndiefraudaskind",
        ],
    },
]

QUIZZES = [
    {
        "question": "Was ist der richtige Artikel für „Buch“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "c",
        "explanation": "Richtig ist: das Buch.",
    },
    {
        "question": "Was ist der richtige Artikel für „Tisch“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "a",
        "explanation": "Richtig ist: der Tisch.",
    },
    {
        "question": "Was ist der richtige Artikel für „Lampe“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "b",
        "explanation": "Richtig ist: die Lampe.",
    },
    {
        "question": "Welcher Artikel ist feminin?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "b",
        "explanation": "Feminin ist: die.",
    },
    {
        "question": "Welcher Artikel ist neutrum?",
        "options": {"a": "das", "b": "der", "c": "die"},
        "correct": "a",
        "explanation": "Neutrum ist: das.",
    },
    {
        "question": "Welcher Artikel ist maskulin?",
        "options": {"a": "die", "b": "das", "c": "der"},
        "correct": "c",
        "explanation": "Maskulin ist: der.",
    },
    {
        "question": "Was ist richtig?",
        "options": {"a": "das Frau", "b": "die Frau", "c": "der Frau"},
        "correct": "b",
        "explanation": "Richtig ist: die Frau.",
    },
    {
        "question": "Was ist richtig?",
        "options": {"a": "das Kind", "b": "die Kind", "c": "der Kind"},
        "correct": "a",
        "explanation": "Richtig ist: das Kind.",
    },
    {
        "question": "Welcher Artikel steht im Plural?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "b",
        "explanation": "Im Plural steht immer: die.",
    },
    {
        "question": "Was ist richtig?",
        "options": {"a": "der Buch", "b": "die Buch", "c": "das Buch"},
        "correct": "c",
        "explanation": "Richtig ist: das Buch.",
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
            "step": "start",      # start, theorie, mission_1, mission_2, quiz_1 ... quiz_10, done
            "quiz_index": None,
        }
    return user_id, data[user_id]


def normalize_text(text: str) -> str:
    return (
        text.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace("„", "")
        .replace("“", "")
        .replace('"', "")
        .replace("'", "")
        .lower()
    )


def get_level(points: int) -> str:
    if points >= 120:
        return "Experte/Expertin"
    if points >= 80:
        return "Fortgeschritten"
    if points >= 40:
        return "Lerner/Lernerin"
    return "Anfänger/Anfängerin"


async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Bot starten"),
        BotCommand("weiter", "Zum nächsten Schritt gehen"),
        BotCommand("punkte", "Punkte anzeigen"),
        BotCommand("niveau", "Niveau anzeigen"),
        BotCommand("hilfe", "Hilfe öffnen"),
    ]
    await app.bot.set_my_commands(commands)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    user["step"] = "theorie"
    user["quiz_index"] = None
    save_data(data)

    caption = (
        f"Willkommen, {user['name']}! 👋\n\n"
        "Thema: Geschlecht und Artikel im Deutschen\n\n"
        "Lernweg:\n"
        "1. Theorie lesen\n"
        "2. Mission 1 lösen\n"
        "3. Mission 2 lösen\n"
        "4. 10 Quizfragen beantworten\n"
        "5. Ergebnis sehen\n\n"
        "Befehle:\n"
        "/weiter – nächster Schritt\n"
        "/punkte – Ihre Punkte\n"
        "/niveau – Ihr Niveau\n"
        "/hilfe – Hilfe\n\n"
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
        "Dieser Bot arbeitet Schritt für Schritt.\n\n"
        "So gehen Sie vor:\n"
        "• /start\n"
        "• Theorie lesen\n"
        "• /weiter\n"
        "• Mission lösen\n"
        "• /weiter\n"
        "• nächste Mission lösen\n"
        "• /weiter\n"
        "• Quiz lösen\n\n"
        "Wichtige Befehle:\n"
        "/start – Bot starten\n"
        "/weiter – nächster Schritt\n"
        "/punkte – Punkte sehen\n"
        "/niveau – Niveau sehen\n"
        "/hilfe – Hilfe\n\n"
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

    if step == "theorie":
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
        user["step"] = "quiz_1"
        user["quiz_index"] = 0
        save_data(data)
        await send_quiz(update, context, 0)
        return

    if step.startswith("quiz_"):
        quiz_index = user.get("quiz_index")
        if quiz_index is None:
            await update.message.reply_text("Bitte starten Sie zuerst mit /start.")
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
            "Sie haben diese Lerneinheit bereits abgeschlossen. 🎉\n"
            "Senden Sie /start, wenn Sie noch einmal beginnen möchten."
        )
        return

    await update.message.reply_text(
        "Bitte starten Sie zuerst mit /start."
    )


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
            "Senden Sie /weiter für die nächste Aufgabe."
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
            "Senden Sie /weiter für die nächste Aufgabe."
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
        "🎉 Abschluss der Lerneinheit\n\n"
        "Sie haben das Thema „Geschlecht und Artikel im Deutschen“ abgeschlossen.\n\n"
        f"Gesamtpunktzahl: {user['points']} 🏆\n"
        f"Niveau: {get_level(user['points'])}\n\n"
        "Senden Sie /start, wenn Sie die Einheit noch einmal bearbeiten möchten."
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
        mission_obj = MISSIONS[0]
        if normalized in mission_obj["answers"]:
            user["points"] += 15
            user["step"] = "mission_1_done"
            save_data(data)

            await update.message.reply_text(
                "Richtig! ✅\n"
                "Mission 1 wurde erfolgreich gelöst.\n"
                "Sie haben +15 Punkte bekommen.\n\n"
                "Senden Sie /weiter für Mission 2."
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
                "Noch nicht richtig ❌\n"
                "Bitte versuchen Sie es noch einmal."
            )
        return

    if step == "mission_2":
        mission_obj = MISSIONS[1]
        if normalized in mission_obj["answers"]:
            user["points"] += 15
            user["step"] = "mission_2_done"
            save_data(data)

            await update.message.reply_text(
                "Richtig! ✅\n"
                "Mission 2 wurde erfolgreich gelöst.\n"
                "Sie haben +15 Punkte bekommen.\n\n"
                "Senden Sie /weiter für Quiz 1."
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
                "Noch nicht richtig ❌\n"
                "Bitte versuchen Sie es noch einmal."
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