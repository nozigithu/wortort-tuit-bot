import json
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

TOKEN = os.getenv("TOKEN")
DATA_FILE = "users.json"

# -------------------------
# Ma'lumotlar
# -------------------------

THEORY = "📘 Theorie: Die Familie\n\nDie Familie ist sehr wichtig."
VOCAB = "📚 Wortschatz\nVater, Mutter, Bruder, Schwester"
GRAMMAR = "📘 Grammatik\nmein Vater, meine Mutter"

QUIZ = [
    {
        "q": "Das ist ___ Vater.",
        "a": "mein",
        "b": "meine",
        "c": "meinen",
        "correct": "a"
    },
    {
        "q": "Das ist ___ Mutter.",
        "a": "mein",
        "b": "meine",
        "c": "meinen",
        "correct": "b"
    }
]

# -------------------------
# DATA
# -------------------------

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def save(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

# -------------------------
# MENU
# -------------------------

def menu():
    return ReplyKeyboardMarkup(
        [
            ["▶️ Weiter"],
            ["🏆 Ranking","📊 Punkte"],
            ["🔄 Start"]
        ],
        resize_keyboard=True
    )

# -------------------------
# START
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = load()
    uid = str(update.effective_user.id)

    data[uid] = {
        "name": update.effective_user.first_name,
        "points":0,
        "step":"theory",
        "quiz":0
    }

    save(data)

    await update.message.reply_text(
        "Willkommen! 👋\n\nThema: Die Familie",
        reply_markup=menu()
    )

    await update.message.reply_text(THEORY)

# -------------------------
# WEITER
# -------------------------

async def weiter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = load()
    uid = str(update.effective_user.id)

    if uid not in data:
        return

    step = data[uid]["step"]

    if step == "theory":
        data[uid]["step"] = "vocab"
        save(data)
        await update.message.reply_text(VOCAB)
        return

    if step == "vocab":
        data[uid]["step"] = "grammar"
        save(data)
        await update.message.reply_text(GRAMMAR)
        return

    if step == "grammar":
        data[uid]["step"] = "mission"
        save(data)
        await update.message.reply_text(
            "Mission: Wie viele Geschwister?",
        )
        return

    if step == "mission_done":
        data[uid]["step"] = "quiz"
        data[uid]["quiz"] = 0
        save(data)
        await send_quiz(update, context, 0)
        return

    if step == "quiz":
        i = data[uid]["quiz"] + 1

        if i >= len(QUIZ):
            await update.message.reply_text(
                "🎉 Lektion beendet!",
                reply_markup=menu()
            )
            return

        data[uid]["quiz"] = i
        save(data)

        await send_quiz(update, context, i)
        return

# -------------------------
# QUIZ
# -------------------------

async def send_quiz(update, context, i):

    q = QUIZ[i]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("A",callback_data="a"),
            InlineKeyboardButton("B",callback_data="b"),
            InlineKeyboardButton("C",callback_data="c")
        ]
    ])

    await update.message.reply_text(
        f"🧠 {q['q']}\n\nA) {q['a']}\nB) {q['b']}\nC) {q['c']}",
        reply_markup=keyboard
    )

# -------------------------
# QUIZ ANSWER
# -------------------------

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = load()
    uid = str(query.from_user.id)

    if uid not in data:
        return

    i = data[uid]["quiz"]
    q = QUIZ[i]

    if query.data == q["correct"]:
        data[uid]["points"] += 10
        await query.message.reply_text("Richtig! ✅")
    else:
        await query.message.reply_text("Falsch ❌")

    save(data)

    await query.message.reply_text("▶️ Weiter drücken")

# -------------------------
# MESSAGE
# -------------------------

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "▶️ Weiter":
        await weiter(update, context)
        return

    if text == "🔄 Start":
        await start(update, context)
        return

    data = load()
    uid = str(update.effective_user.id)

    if uid not in data:
        return

    if data[uid]["step"] == "mission":

        if "zwei" in text or "2" in text:

            data[uid]["points"] += 20
            data[uid]["step"] = "mission_done"
            save(data)

            await update.message.reply_text(
                "Richtig! Mission geschafft. ✅"
            )

        else:

            await update.message.reply_text(
                "Noch einmal versuchen."
            )

# -------------------------
# MAIN
# -------------------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT,message))
    app.add_handler(CallbackQueryHandler(quiz_answer))

    print("Bot läuft...")

    app.run_polling()

if __name__ == "__main__":
    main()