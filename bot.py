import json
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# =========================
# BOT TOKEN HIER EINFÜGEN
# =========================
TOKEN = "8753301957:AAFpx6qa7DoNItH80kxboa8rnVByCnithe0"

DATA_FILE = "users.json"

THEORY_TEXT = (
    "📘 Theorie: Die Familie\n\n"
    "Die Familie ist sehr wichtig.\n"
    "Wir sprechen über Vater, Mutter, Bruder, Schwester und Eltern.\n\n"
    "Bitte klicken Sie auf ▶️ Weiter."
)

VOCAB_TEXT = (
    "📚 Wortschatz\n\n"
    "der Vater — ota — отец\n"
    "die Mutter — ona — мать\n"
    "der Bruder — aka/uka — брат\n"
    "die Schwester — opa/singil — сестра\n"
    "die Eltern — ota-ona — родители\n"
    "die Familie — oila — семья\n\n"
    "Bitte klicken Sie auf ▶️ Weiter."
)

GRAMMAR_TEXT = (
    "📘 Grammatik: Possessivartikel\n\n"
    "mein Vater\n"
    "meine Mutter\n"
    "mein Bruder\n"
    "meine Schwester\n\n"
    "Bitte klicken Sie auf ▶️ Weiter."
)

QUIZZES = [
    {
        "question": "Das ist ___ Vater.",
        "a": "mein",
        "b": "meine",
        "c": "meinen",
        "correct": "a",
        "explanation": "Richtig ist: mein Vater.",
    },
    {
        "question": "Wie sagt man „ona“ auf Deutsch?",
        "a": "Bruder",
        "b": "Mutter",
        "c": "Schwester",
        "correct": "b",
        "explanation": "Richtig ist: Mutter.",
    },
]


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user(update: Update, data: dict):
    user_id = str(update.effective_user.id)
    if user_id not in data:
        data[user_id] = {
            "name": update.effective_user.first_name or "Student/in",
            "points": 0,
            "step": "start",
            "quiz_index": 0,
        }
    return user_id, data[user_id]


def get_level(points: int) -> str:
    if points >= 40:
        return "Sehr gut"
    if points >= 20:
        return "Lerner/in"
    return "Anfänger/in"


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["▶️ Weiter"],
            ["📊 Punkte", "📈 Niveau"],
            ["🏆 Ranking", "🔄 Start"],
        ],
        resize_keyboard=True,
    )


def quiz_keyboard():
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("A", callback_data="a"),
            InlineKeyboardButton("B", callback_data="b"),
            InlineKeyboardButton("C", callback_data="c"),
        ]]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    user["step"] = "theory"
    user["quiz_index"] = 0
    save_data(data)

    await update.message.reply_text(
        f"Willkommen, {user['name']}! 👋\n\n"
        "Thema: Die Familie\n"
        "Niveau: A2–B1\n\n"
        "Lernweg:\n"
        "1. Theorie\n"
        "2. Wortschatz\n"
        "3. Grammatik\n"
        "4. Mission\n"
        "5. Quiz\n\n"
        "Bitte beginnen Sie jetzt.",
        reply_markup=main_menu(),
    )

    await update.message.reply_text(THEORY_TEXT, reply_markup=main_menu())


async def weiter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    step = user["step"]

    if step == "theory":
        user["step"] = "vocab"
        save_data(data)
        await update.message.reply_text(VOCAB_TEXT, reply_markup=main_menu())
        return

    if step == "vocab":
        user["step"] = "grammar"
        save_data(data)
        await update.message.reply_text(GRAMMAR_TEXT, reply_markup=main_menu())
        return

    if step == "grammar":
        user["step"] = "mission"
        save_data(data)
        await update.message.reply_text(
            "✍️ Mission 1\n\n"
            "Wie viele Geschwister hat die Person?\n\n"
            "Bitte schreiben Sie:\n"
            "zwei",
            reply_markup=main_menu(),
        )
        return

    if step == "mission_done":
        user["step"] = "quiz"
        user["quiz_index"] = 0
        save_data(data)
        await send_quiz(update.message.reply_text, user["quiz_index"])
        return

    if step == "quiz_done":
        next_index = user["quiz_index"] + 1
        if next_index < len(QUIZZES):
            user["quiz_index"] = next_index
            user["step"] = "quiz"
            save_data(data)
            await send_quiz(update.message.reply_text, next_index)
            return
        else:
            user["step"] = "done"
            save_data(data)
            await update.message.reply_text(
                f"🎉 Lektion beendet!\n\n"
                f"Punkte: {user['points']}\n"
                f"Niveau: {get_level(user['points'])}",
                reply_markup=main_menu(),
            )
            return

    if step == "done":
        await update.message.reply_text(
            "Sie haben die Lektion schon abgeschlossen.\n"
            "Drücken Sie 🔄 Start, um neu zu beginnen.",
            reply_markup=main_menu(),
        )
        return

    await update.message.reply_text(
        "Bitte bearbeiten Sie zuerst den aktuellen Schritt.",
        reply_markup=main_menu(),
    )


async def send_quiz(reply_func, index: int):
    q = QUIZZES[index]
    text = (
        f"🧠 Quiz {index + 1}\n\n"
        f"{q['question']}\n\n"
        f"A) {q['a']}\n"
        f"B) {q['b']}\n"
        f"C) {q['c']}"
    )
    await reply_func(text, reply_markup=quiz_keyboard())


async def handle_quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = load_data()
    user_id = str(query.from_user.id)

    if user_id not in data:
        await query.message.reply_text("Bitte zuerst 🔄 Start drücken.")
        return

    user = data[user_id]

    if user["step"] != "quiz":
        await query.message.reply_text("Im Moment ist kein Quiz aktiv.")
        return

    index = user["quiz_index"]
    q = QUIZZES[index]
    answer = query.data

    if answer == q["correct"]:
        user["points"] += 10
        text = f"Richtig! ✅\n{q['explanation']}"
    else:
        text = f"Falsch ❌\n{q['explanation']}"

    user["step"] = "quiz_done"
    save_data(data)

    await query.message.reply_text(
        text + "\n\nBitte drücken Sie ▶️ Weiter.",
        reply_markup=main_menu(),
    )


async def punkte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    await update.message.reply_text(
        f"Ihre Punkte: {user['points']} 🏆",
        reply_markup=main_menu(),
    )


async def niveau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    await update.message.reply_text(
        f"Ihr Niveau: {get_level(user['points'])}",
        reply_markup=main_menu(),
    )


async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    if not data:
        await update.message.reply_text(
            "Noch keine Daten vorhanden.",
            reply_markup=main_menu(),
        )
        return

    sorted_users = sorted(
        data.values(),
        key=lambda x: x.get("points", 0),
        reverse=True,
    )

    text = "🏆 Bestenliste\n\n"
    for i, user in enumerate(sorted_users[:10], start=1):
        text += f"{i}. {user['name']} — {user['points']} Punkte\n"

    await update.message.reply_text(text, reply_markup=main_menu())


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text == "🔄 Start":
        await start(update, context)
        return

    if text == "▶️ Weiter":
        await weiter(update, context)
        return

    if text == "📊 Punkte":
        await punkte(update, context)
        return

    if text == "📈 Niveau":
        await niveau(update, context)
        return

    if text == "🏆 Ranking":
        await ranking(update, context)
        return

    data = load_data()
    _, user = get_user(update, data)

    if user["step"] == "mission":
        if text.lower() in ["zwei", "2"]:
            user["points"] += 20
            user["step"] = "mission_done"
            save_data(data)
            await update.message.reply_text(
                "Richtig! ✅\nMission geschafft.\n\nBitte drücken Sie ▶️ Weiter.",
                reply_markup=main_menu(),
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal.",
                reply_markup=main_menu(),
            )
        return


def main():
    if not TOKEN or TOKEN == "BU_YERGA_BOTFATHER_TOKENINI_QOYING":
        raise ValueError("Bitte tragen Sie zuerst Ihren echten Bot-Token in TOKEN ein.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weiter", weiter))
    app.add_handler(CommandHandler("punkte", punkte))
    app.add_handler(CommandHandler("niveau", niveau))
    app.add_handler(CommandHandler("ranking", ranking))

    app.add_handler(CallbackQueryHandler(handle_quiz_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot läuft...")
    app.run_polling()


if __name__ == "__main__":
    main()