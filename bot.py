import json
import os
import random
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "8753301957:AAFpx6qa7DoNItH80kxboa8rnVByCnithe0"
ADMIN_ID = 6051699852
DATA_FILE = "users.json"
LOGO_FILE = "logo.png"

QUIZZES = [
    {
        "question": "Was ist der richtige bestimmte Artikel für „Buch“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "c",
        "explanation": "Richtig ist: das Buch."
    },
    {
        "question": "Was ist der richtige bestimmte Artikel für „Tisch“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "a",
        "explanation": "Richtig ist: der Tisch."
    },
    {
        "question": "Was ist der richtige bestimmte Artikel für „Lampe“?",
        "options": {"a": "der", "b": "die", "c": "das"},
        "correct": "b",
        "explanation": "Richtig ist: die Lampe."
    },
    {
        "question": "Wie lautet der Plural von „das Buch“?",
        "options": {"a": "die Buchs", "b": "die Bücher", "c": "die Buche"},
        "correct": "b",
        "explanation": "Der Plural ist: die Bücher."
    },
    {
        "question": "Wie lautet der Plural von „der Student“?",
        "options": {"a": "die Studenten", "b": "die Studenteninnen", "c": "die Studente"},
        "correct": "a",
        "explanation": "Der Plural ist: die Studenten."
    },
    {
        "question": "Welche Form ist richtig: Ich ___ aus Usbekistan.",
        "options": {"a": "kommt", "b": "komme", "c": "kommen"},
        "correct": "b",
        "explanation": "Richtig ist: Ich komme aus Usbekistan."
    },
    {
        "question": "Welche Form ist richtig: Er ___ Informatik.",
        "options": {"a": "studierst", "b": "studiere", "c": "studiert"},
        "correct": "c",
        "explanation": "Richtig ist: Er studiert Informatik."
    },
    {
        "question": "Welche Form ist richtig: Wir ___ Deutsch.",
        "options": {"a": "lernen", "b": "lernt", "c": "lerne"},
        "correct": "a",
        "explanation": "Richtig ist: Wir lernen Deutsch."
    },
    {
        "question": "Welches Wort passt? Ich lerne Deutsch ___ Python.",
        "options": {"a": "und", "b": "oder", "c": "aber"},
        "correct": "a",
        "explanation": "Richtig ist: Ich lerne Deutsch und Python."
    },
    {
        "question": "Welches Personalpronomen passt zu „Ali“?",
        "options": {"a": "sie", "b": "es", "c": "er"},
        "correct": "c",
        "explanation": "Für Ali passt: er."
    },
    {
        "question": "Welches Personalpronomen passt zu „Madina“?",
        "options": {"a": "sie", "b": "er", "c": "es"},
        "correct": "a",
        "explanation": "Für Madina passt: sie."
    },
    {
        "question": "Was ist richtig?",
        "options": {
            "a": "Ich bin Studentin.",
            "b": "Ich ist Studentin.",
            "c": "Ich sind Studentin."
        },
        "correct": "a",
        "explanation": "Richtig ist: Ich bin Studentin."
    },
    {
        "question": "Was ist richtig?",
        "options": {
            "a": "Das Auto ist neu.",
            "b": "Die Auto ist neu.",
            "c": "Der Auto ist neu."
        },
        "correct": "a",
        "explanation": "Richtig ist: Das Auto ist neu."
    },
    {
        "question": "Welches Wort ist ein Verb?",
        "options": {"a": "lernen", "b": "Buch", "c": "Universität"},
        "correct": "a",
        "explanation": "„lernen“ ist ein Verb."
    },
    {
        "question": "Welche Übersetzung ist richtig: „Schleife“?",
        "options": {"a": "Variable", "b": "Loop", "c": "Funktion"},
        "correct": "b",
        "explanation": "„Schleife“ bedeutet: Loop."
    },
]

MISSIONS = [
    {
        "id": 1,
        "task": "Erstellen Sie eine Variable 'strom' und geben Sie ihr den Wert 50.",
        "answers": ["strom=50"]
    },
    {
        "id": 2,
        "task": "Erstellen Sie eine Variable 'zahl' und geben Sie ihr den Wert 100.",
        "answers": ["zahl=100"]
    },
    {
        "id": 3,
        "task": "Erstellen Sie eine Variable 'name' und geben Sie ihr den Text 'Python'.",
        "answers": ['name="python"', "name='python'"]
    },
    {
        "id": 4,
        "task": "Schreiben Sie einen Python-Befehl, der 'Hallo' ausgibt.",
        "answers": ['print("hallo")', "print('hallo')"]
    },
    {
        "id": 5,
        "task": "Erstellen Sie eine Liste mit dem Namen 'zahlen' und den Werten 1, 2, 3.",
        "answers": ["zahlen=[1,2,3]"]
    },
    {
        "id": 6,
        "task": "Erstellen Sie eine Variable 'aktiv' mit dem Wert True.",
        "answers": ["aktiv=true"]
    },
    {
        "id": 7,
        "task": "Schreiben Sie eine Bedingung: Wenn x größer als 5 ist, soll 'groß' ausgegeben werden.",
        "answers": [
            'ifx>5:print("groß")',
            "ifx>5:print('groß')"
        ]
    },
    {
        "id": 8,
        "task": "Schreiben Sie eine Schleife, die 3-mal 'Hallo' ausgibt.",
        "answers": [
            'foriinrange(3):print("hallo")',
            "foriinrange(3):print('hallo')"
        ]
    },
    {
        "id": 9,
        "task": "Erstellen Sie eine Funktion mit dem Namen 'gruss', die 'Hallo' ausgibt.",
        "answers": [
            'defgruss():print("hallo")',
            "defgruss():print('hallo')"
        ]
    },
    {
        "id": 10,
        "task": "Erstellen Sie ein Dictionary 'student' mit name='Ali' und alter=20.",
        "answers": [
            "student={'name':'ali','alter':20}",
            'student={"name":"ali","alter":20}',
            'student={"alter":20,"name":"ali"}',
            "student={'alter':20,'name':'ali'}"
        ]
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
            "name": update.effective_user.first_name,
            "points": 0,
            "quiz_answer": None,
            "quiz_question": None,
            "current_mission": None,
        }
    return user_id, data[user_id]


def normalize_text(text: str) -> str:
    return text.strip().replace(" ", "").replace("\n", "").lower()


def get_level(points: int) -> str:
    if points >= 150:
        return "Python-Meister"
    if points >= 100:
        return "Fortgeschritten"
    if points >= 50:
        return "Junior-Lerner"
    return "Anfänger"

async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Bot starten"),
        BotCommand("hilfe", "Hilfe öffnen"),
        BotCommand("aufgabe", "Eine Python-Aufgabe erhalten"),
        BotCommand("quiz", "Ein Deutsch-Quiz erhalten"),
        BotCommand("punkte", "Gesamtpunktzahl anzeigen"),
        BotCommand("niveau", "Aktuelles Niveau anzeigen"),
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)
    save_data(data)

    caption = (
        f"Willkommen beim WortOrt–TUIT Lernbot, {user['name']}! 🇩🇪\n\n"
        "Deutsch + Python lernen\n"
        "Digitale Plattform für den Fernunterricht\n\n"
        "Befehle:\n"
        "/aufgabe – Python-Aufgabe\n"
        "/quiz – Deutsch-Quiz\n"
        "/punkte – Ihre Punkte\n"
        "/niveau – Ihr Niveau\n"
        "/hilfe – Hilfe"
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


async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Hilfebereich 🛠\n\n"
        "Verfügbare Befehle:\n"
        "/start – Bot starten\n"
        "/aufgabe – eine Python-Aufgabe erhalten\n"
        "/quiz – ein Deutsch-Quiz erhalten\n"
        "/punkte – Ihre Gesamtpunktzahl sehen\n"
        "/niveau – Ihr aktuelles Niveau sehen\n"
        "/hilfe – Hilfefenster öffnen\n\n"
        "Quiz-Antworten:\n"
        "/a\n"
        "/b\n"
        "/c\n\n"
        "Die Antwort auf eine Aufgabe soll als normale Nachricht gesendet werden."
    )
    await update.message.reply_text(text)


async def aufgabe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)

    mission_obj = random.choice(MISSIONS)
    user["current_mission"] = mission_obj["id"]
    save_data(data)

    text = (
        f"Python-Aufgabe {mission_obj['id']} 💻\n\n"
        f"{mission_obj['task']}\n\n"
        "Bitte senden Sie Ihre Antwort als normale Nachricht."
    )
    await update.message.reply_text(text)


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id, user = get_user(update, data)

    quiz_obj = random.choice(QUIZZES)
    user["quiz_answer"] = quiz_obj["correct"]
    user["quiz_question"] = quiz_obj["question"]
    save_data(data)

    text = (
        "Deutsch-Quiz 🇩🇪\n\n"
        f"{quiz_obj['question']}\n\n"
        f"a) {quiz_obj['options']['a']}\n"
        f"b) {quiz_obj['options']['b']}\n"
        f"c) {quiz_obj['options']['c']}\n\n"
        "Bitte senden Sie Ihre Antwort:\n"
        "/a\n"
        "/b\n"
        "/c"
    )
    await update.message.reply_text(text)


async def answer_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_answer(update, context, "a")


async def answer_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_answer(update, context, "b")


async def answer_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_answer(update, context, "c")


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str):
    data = load_data()
    user_id, user = get_user(update, data)

    correct_answer = user.get("quiz_answer")
    quiz_question = user.get("quiz_question")

    if correct_answer is None:
        await update.message.reply_text("Bitte senden Sie zuerst /quiz.")
        return

    quiz_obj = None
    for q in QUIZZES:
        if q["question"] == quiz_question:
            quiz_obj = q
            break

    if answer == correct_answer:
        user["points"] += 10

        await update.message.reply_text(
            f"Richtig! ✅\n{quiz_obj['explanation']}\nSie haben +10 Punkte bekommen."
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Frage: {quiz_question}\n"
                f"Antwort: /{answer}\n"
                f"Ergebnis: RICHTIG ✅\n"
                f"Vergebene Punkte: +10\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )
    else:
        await update.message.reply_text(
            f"Falsch ❌\n{quiz_obj['explanation']}\nVergebene Punkte: 0"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Frage: {quiz_question}\n"
                f"Antwort: /{answer}\n"
                f"Ergebnis: FALSCH ❌\n"
                f"Vergebene Punkte: 0\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )

    user["quiz_answer"] = None
    user["quiz_question"] = None
    save_data(data)


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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    data = load_data()
    user_id, user = get_user(update, data)

    current_mission_id = user.get("current_mission")
    message_text = update.message.text

    if current_mission_id is None:
        return

    mission_obj = None
    for m in MISSIONS:
        if m["id"] == current_mission_id:
            mission_obj = m
            break

    if mission_obj is None:
        return

    normalized = normalize_text(message_text)

    if normalized in mission_obj["answers"]:
        user["points"] += 15
        user["current_mission"] = None
        save_data(data)

        await update.message.reply_text(
            "Richtig! ✅\n"
            "Die Aufgabe wurde erfolgreich gelöst.\n"
            "Sie haben +15 Punkte bekommen."
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📩 Neue Antwort zur Aufgabe\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Aufgabe: {mission_obj['id']}\n"
                f"Text der Aufgabe: {mission_obj['task']}\n"
                f"Antwort: {message_text}\n"
                f"Ergebnis: RICHTIG ✅\n"
                f"Vergebene Punkte: +15\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )
    else:
        save_data(data)

        await update.message.reply_text(
            "Noch nicht richtig ❌\n"
            "Bitte versuchen Sie es noch einmal."
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📩 Neue Antwort zur Aufgabe\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n\n"
                f"Aufgabe: {mission_obj['id']}\n"
                f"Text der Aufgabe: {mission_obj['task']}\n"
                f"Antwort: {message_text}\n"
                f"Ergebnis: FALSCH ❌\n"
                f"Vergebene Punkte: 0\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hilfe", hilfe))
    app.add_handler(CommandHandler("aufgabe", aufgabe))
    app.add_handler(CommandHandler("quiz", quiz))
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