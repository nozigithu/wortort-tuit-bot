import json
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# =========================================================
# TOKEN
# Railway ishlatsangiz TOKEN variable orqali oladi.
# Qo'lda yozmoqchi bo'lsangiz ikkinchi qiymat o'rniga tokenni yozing.
# =========================================================
TOKEN = os.getenv("TOKEN", "8753301957:AAFpx6qa7DoNItH80kxboa8rnVByCnithe0")

DATA_FILE = "users.json"
LOGO_FILE = "logo.png"

# =========================================================
# LEKTIONSINHALTE
# =========================================================

THEORY_TEXT = (
    "📘 *Lektion 1: Die erste Bekanntschaft*\n\n"
    "In dieser Lektion lernen Sie:\n"
    "• sich vorstellen\n"
    "• nach Namen, Herkunft und Wohnort fragen\n"
    "• über Studium oder Arbeit sprechen\n"
    "• wichtige Verben im Präsens verwenden\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

VOCAB_TEXT = (
    "📚 *Wortschatz: Die erste Bekanntschaft*\n\n"
    "die Bekanntschaft — tanishuv — знакомство\n"
    "sich vorstellen — o‘zini tanishtirmoq — представляться\n"
    "kennenlernen — tanishmoq — знакомиться\n"
    "der Name — ism — имя\n"
    "der Vorname — ism — имя\n"
    "der Nachname — familiya — фамилия\n"
    "der Student — talaba — студент\n"
    "die Studentin — talaba qiz — студентка\n"
    "der Lehrer — o‘qituvchi — учитель\n"
    "die Lehrerin — o‘qituvchi ayol — учительница\n"
    "der Ingenieur — muhandis — инженер\n"
    "die Universität — universitet — университет\n"
    "die Schule — maktab — школа\n"
    "die Sprache — til — язык\n"
    "Deutsch — nemis tili — немецкий язык\n"
    "Englisch — ingliz tili — английский язык\n"
    "Usbekisch — o‘zbek tili — узбекский язык\n"
    "Russisch — rus tili — русский язык\n"
    "sprechen — gapirmoq — говорить\n"
    "lernen — o‘rganmoq — учить\n"
    "studieren — o‘qimoq — учиться\n"
    "arbeiten — ishlamoq — работать\n"
    "wohnen — yashamoq — жить\n"
    "kommen — kelmoq — приходить\n"
    "heißen — atalmoq / ismga ega bo‘lmoq — зваться\n"
    "fragen — so‘ramoq — спрашивать\n"
    "antworten — javob bermoq — отвечать\n"
    "sagen — aytmoq — говорить\n"
    "treffen — uchrashmoq — встречать\n"
    "nett — yoqimli — приятный\n"
    "freundlich — mehribon — дружелюбный\n"
    "interessant — qiziqarli — интересный\n"
    "wer — kim — кто\n"
    "wie — qanday — как\n"
    "wo — qayerda — где\n"
    "woher — qayerdan — откуда\n"
    "was — nima — что\n"
    "wie heißen Sie? — ismingiz nima? — как вас зовут?\n"
    "wie heißt du? — isming nima? — как тебя зовут?\n"
    "ich heiße … — mening ismim … — меня зовут …\n"
    "ich komme aus … — men …danman — я из …\n"
    "ich wohne in … — men …da yashayman — я живу в …\n"
    "ich studiere … — men …ni o‘qiyman — я изучаю …\n"
    "ich arbeite als … — men … bo‘lib ishlayman — я работаю …\n"
    "freut mich — tanishganimdan xursandman — приятно познакомиться\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

GRAMMAR_TEXT = (
    "📘 *Grammatik: Verbkonjugation im Präsens*\n\n"
    "Das Präsens benutzt man für:\n"
    "• Handlungen in der Gegenwart\n"
    "• Gewohnheiten\n"
    "• allgemeine Aussagen\n\n"
    "*Personalpronomen:*\n"
    "ich, du, er/sie/es, wir, ihr, sie/Sie\n\n"
    "*Beispiel: heißen*\n"
    "ich heiße\n"
    "du heißt\n"
    "er/sie heißt\n"
    "wir heißen\n"
    "ihr heißt\n"
    "sie/Sie heißen\n\n"
    "*Beispiel: kommen*\n"
    "ich komme\n"
    "du kommst\n"
    "er/sie kommt\n"
    "wir kommen\n"
    "ihr kommt\n"
    "sie/Sie kommen\n\n"
    "*Beispiel: studieren*\n"
    "ich studiere\n"
    "du studierst\n"
    "er/sie studiert\n"
    "wir studieren\n"
    "ihr studiert\n"
    "sie/Sie studieren\n\n"
    "*Beispiele:*\n"
    "Ich heiße Ali.\n"
    "Ich komme aus Usbekistan.\n"
    "Ich studiere Informatik.\n"
    "Ich spreche Deutsch und Englisch.\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

TEXT_TEXT = (
    "📖 *Lesetext: Erste Bekanntschaft an der Universität*\n\n"
    "Ali ist ein neuer Student an der Universität.\n\n"
    "Am ersten Tag trifft er eine Studentin.\n\n"
    "Ali sagt:\n"
    "„Hallo! Ich heiße Ali. Ich komme aus Taschkent und ich studiere Informatik.“\n\n"
    "Die Studentin antwortet:\n"
    "„Hallo! Ich heiße Maria. Ich komme aus Deutschland und ich studiere Wirtschaft.“\n\n"
    "Ali fragt:\n"
    "„Wo wohnst du jetzt?“\n\n"
    "Maria sagt:\n"
    "„Ich wohne jetzt in Taschkent.“\n\n"
    "Ali fragt weiter:\n"
    "„Welche Sprachen sprichst du?“\n\n"
    "Maria antwortet:\n"
    "„Ich spreche Deutsch, Englisch und ein bisschen Usbekisch.“\n\n"
    "Ali sagt:\n"
    "„Freut mich, dich kennenzulernen!“\n\n"
    "Maria sagt:\n"
    "„Freut mich auch!“\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

DIALOG_TEXT = (
    "🗣 *Dialoge*\n\n"
    "*Informell:*\n"
    "A: Hallo! Wie heißt du?\n"
    "B: Ich heiße Ali. Und du?\n\n"
    "A: Ich heiße Maria.\n"
    "B: Woher kommst du?\n\n"
    "A: Ich komme aus Deutschland.\n"
    "B: Ich komme aus Usbekistan.\n\n"
    "A: Wo wohnst du?\n"
    "B: Ich wohne in Taschkent.\n\n"
    "A: Was studierst du?\n"
    "B: Ich studiere Informatik.\n\n"
    "A: Freut mich!\n"
    "B: Mich auch!\n\n"
    "*Formell:*\n"
    "A: Guten Tag! Wie heißen Sie?\n"
    "B: Ich heiße Herr Müller.\n\n"
    "A: Woher kommen Sie?\n"
    "B: Ich komme aus Deutschland.\n\n"
    "A: Was arbeiten Sie?\n"
    "B: Ich arbeite als Ingenieur.\n\n"
    "A: Freut mich, Sie kennenzulernen.\n"
    "B: Mich auch.\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

MISSIONS = [
    {
        "id": 1,
        "task": (
            "✍️ *Mission 1*\n\n"
            "Lesen Sie den Text und beantworten Sie die Fragen:\n\n"
            "1. Wie heißt der Student?\n"
            "2. Woher kommt Maria?\n"
            "3. Was studiert Ali?\n\n"
            "Bitte schreiben Sie eine kurze Antwort."
        ),
        "keywords": ["ali", "deutschland", "informatik"],
        "points": 20,
    },
    {
        "id": 2,
        "task": (
            "✍️ *Mission 2*\n\n"
            "Stellen Sie sich in *drei bis fünf Sätzen* vor.\n\n"
            "Schreiben Sie über:\n"
            "• Ihren Namen\n"
            "• Ihre Herkunft\n"
            "• Ihren Wohnort\n"
            "• Ihr Studium oder Ihre Arbeit\n\n"
            "Beispiel:\n"
            "Ich heiße Ali.\n"
            "Ich komme aus Usbekistan.\n"
            "Ich wohne in Taschkent.\n"
            "Ich studiere Informatik."
        ),
        "special": "self_introduction",
        "points": 25,
    },
]

QUIZZES = [
    {
        "question": "Wie sagt man „ism“ auf Deutsch?",
        "options": {"a": "Name", "b": "Stadt", "c": "Land"},
        "correct": "a",
        "explanation": "Richtig ist: *Name*.",
    },
    {
        "question": "Wie sagt man „qayerdan“ auf Deutsch?",
        "options": {"a": "wo", "b": "woher", "c": "wer"},
        "correct": "b",
        "explanation": "Richtig ist: *woher*.",
    },
    {
        "question": "Ich ___ Ali.",
        "options": {"a": "heißt", "b": "heiße", "c": "heißen"},
        "correct": "b",
        "explanation": "Richtig ist: *Ich heiße Ali.*",
    },
    {
        "question": "Woher kommst du?",
        "options": {
            "a": "Ich komme aus Usbekistan.",
            "b": "Ich heiße Ali.",
            "c": "Ich studiere Informatik."
        },
        "correct": "a",
        "explanation": "Richtig ist: *Ich komme aus Usbekistan.*",
    },
    {
        "question": "Wie heißt „talaba“?",
        "options": {"a": "Student", "b": "Lehrer", "c": "Ingenieur"},
        "correct": "a",
        "explanation": "Richtig ist: *Student*.",
    },
    {
        "question": "Ich ___ Informatik.",
        "options": {"a": "studiere", "b": "studiert", "c": "studieren"},
        "correct": "a",
        "explanation": "Richtig ist: *Ich studiere Informatik.*",
    },
    {
        "question": "Wie fragt man informell nach dem Namen?",
        "options": {
            "a": "Wie heißen Sie?",
            "b": "Wie heißt du?",
            "c": "Wo wohnen Sie?"
        },
        "correct": "b",
        "explanation": "Richtig ist: *Wie heißt du?*",
    },
    {
        "question": "Wie sagt man „tanishganimdan xursandman“?",
        "options": {"a": "Danke", "b": "Freut mich", "c": "Entschuldigung"},
        "correct": "b",
        "explanation": "Richtig ist: *Freut mich*.",
    },
    {
        "question": "Wo ___ du?",
        "options": {"a": "wohnen", "b": "wohnst", "c": "wohnt"},
        "correct": "b",
        "explanation": "Richtig ist: *Wo wohnst du?*",
    },
    {
        "question": "Ich ___ aus Deutschland.",
        "options": {"a": "komme", "b": "kommt", "c": "kommst"},
        "correct": "a",
        "explanation": "Richtig ist: *Ich komme aus Deutschland.*",
    },
]

# =========================================================
# HILFSFUNKTIONEN
# =========================================================

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(update: Update, data: dict):
    user_id = str(update.effective_user.id)
    first_name = update.effective_user.first_name if update.effective_user else "Student/in"

    if user_id not in data:
        data[user_id] = {
            "name": first_name or "Student/in",
            "points": 0,
            "step": "start",
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
        .replace("„", "")
        .replace("“", "")
        .lower()
    )

def get_level(points: int) -> str:
    if points >= 120:
        return "Sehr gut"
    if points >= 80:
        return "Fortgeschritten"
    if points >= 40:
        return "Lerner/in"
    return "Anfänger/in"

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["▶️ Weiter", "🏆 Ranking"],
            ["📊 Punkte", "📈 Niveau"],
            ["❓ Hilfe", "🔄 Start"],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )

def continue_inline():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ Weiter", callback_data="continue")]]
    )

def quiz_inline_keyboard(index: int):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("A", callback_data=f"quiz:{index}:a"),
            InlineKeyboardButton("B", callback_data=f"quiz:{index}:b"),
            InlineKeyboardButton("C", callback_data=f"quiz:{index}:c"),
        ]]
    )

# =========================================================
# BOT COMMANDS
# =========================================================

async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Lektion starten"),
        BotCommand("weiter", "Zum nächsten Schritt gehen"),
        BotCommand("hilfe", "Hilfe öffnen"),
        BotCommand("punkte", "Punkte anzeigen"),
        BotCommand("niveau", "Niveau anzeigen"),
        BotCommand("ranking", "Bestenliste anzeigen"),
    ]
    await app.bot.set_my_commands(commands)

# =========================================================
# START / MENÜ
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    user["step"] = "theory"
    user["quiz_index"] = None
    save_data(data)

    caption = (
        f"Willkommen, {user['name']}! 👋\n\n"
        "*Lektion 1:* Die erste Bekanntschaft\n"
        "*Niveau:* A1–A2\n\n"
        "*Lernweg:*\n"
        "1. Theorie\n"
        "2. Wortschatz\n"
        "3. Grammatik\n"
        "4. Lesetext\n"
        "5. Dialoge\n"
        "6. 2 Missionen\n"
        "7. 10 Quizfragen\n"
        "8. Abschluss + Ranking\n\n"
        "Bitte beginnen Sie mit der Theorie."
    )

    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "rb") as photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard(),
            )
    else:
        await update.message.reply_text(
            caption,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )

    await update.message.reply_text(
        THEORY_TEXT,
        parse_mode="Markdown",
        reply_markup=continue_inline(),
    )

async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "*Hilfebereich* 🛠\n\n"
        "So arbeiten Sie mit dem Bot:\n"
        "1. Starten Sie die Lektion\n"
        "2. Lesen Sie Theorie, Wortschatz, Grammatik, Text und Dialoge\n"
        "3. Lösen Sie die Missionen\n"
        "4. Beantworten Sie die Quizfragen mit Buttons\n"
        "5. Sehen Sie am Ende Ihr Niveau und das Ranking\n\n"
        "*Menü:*\n"
        "• ▶️ Weiter\n"
        "• 📊 Punkte\n"
        "• 📈 Niveau\n"
        "• 🏆 Ranking\n"
        "• 🔄 Start"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

async def punkte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    await update.message.reply_text(
        f"{user['name']}, Ihre Gesamtpunktzahl ist: *{user['points']}* 🏆",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

async def niveau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    await update.message.reply_text(
        f"{user['name']}, Ihr aktuelles Niveau ist: *{get_level(user['points'])}*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    if not data:
        await update.message.reply_text(
            "Es gibt noch keine Daten.",
            reply_markup=main_menu_keyboard(),
        )
        return

    sorted_users = sorted(
        data.items(),
        key=lambda item: item[1].get("points", 0),
        reverse=True,
    )

    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 *Bestenliste*\n\n"

    for i, (_, user) in enumerate(sorted_users[:10], start=1):
        prefix = medals[i - 1] if i <= 3 else f"{i}."
        text += f"{prefix} {user.get('name', 'Student/in')} — {user.get('points', 0)} Punkte\n"

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

# =========================================================
# QUIZ SENDEN
# =========================================================

async def send_quiz(message_func, index: int):
    q = QUIZZES[index]
    text = (
        f"🧠 *Quiz {index + 1}*\n\n"
        f"{q['question']}\n\n"
        f"A) {q['options']['a']}\n"
        f"B) {q['options']['b']}\n"
        f"C) {q['options']['c']}\n\n"
        "Bitte wählen Sie eine Antwort:"
    )
    await message_func(
        text,
        parse_mode="Markdown",
        reply_markup=quiz_inline_keyboard(index),
    )

# =========================================================
# WEITER-LOGIK
# =========================================================

async def weiter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_next_step(update, context)

async def go_next_step(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    if hasattr(update_or_query, "effective_user"):
        update = update_or_query
        message_func = update.message.reply_text
        data = load_data()
        _, user = get_user(update, data)
    else:
        query = update_or_query
        user_id = str(query.from_user.id)
        data = load_data()
        if user_id not in data:
            data[user_id] = {
                "name": query.from_user.first_name or "Student/in",
                "points": 0,
                "step": "start",
                "quiz_index": None,
            }
        user = data[user_id]
        message_func = query.message.reply_text

    step = user.get("step", "start")

    if step == "theory":
        user["step"] = "vocab"
        save_data(data)
        await message_func(VOCAB_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "vocab":
        user["step"] = "grammar"
        save_data(data)
        await message_func(GRAMMAR_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "grammar":
        user["step"] = "text"
        save_data(data)
        await message_func(TEXT_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "text":
        user["step"] = "dialog"
        save_data(data)
        await message_func(DIALOG_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "dialog":
        user["step"] = "mission_1"
        save_data(data)
        await message_func(MISSIONS[0]["task"], parse_mode="Markdown", reply_markup=main_menu_keyboard())
        return

    if step == "mission_1_done":
        user["step"] = "mission_2"
        save_data(data)
        await message_func(MISSIONS[1]["task"], parse_mode="Markdown", reply_markup=main_menu_keyboard())
        return

    if step == "mission_2_done":
        user["step"] = "quiz_1"
        user["quiz_index"] = 0
        save_data(data)
        await send_quiz(message_func, 0)
        return

    if step.startswith("quiz_"):
        idx = user.get("quiz_index")
        if idx is None:
            await message_func("Bitte starten Sie zuerst mit *🔄 Start*.", parse_mode="Markdown")
            return

        if idx < len(QUIZZES) - 1:
            idx += 1
            user["quiz_index"] = idx
            user["step"] = f"quiz_{idx + 1}"
            save_data(data)
            await send_quiz(message_func, idx)
            return
        else:
            user["step"] = "done"
            save_data(data)
            await send_final_result(message_func, user)
            return

    if step == "done":
        await message_func(
            "Sie haben diese Lektion bereits abgeschlossen. 🎉\n"
            "Drücken Sie *🔄 Start*, wenn Sie noch einmal beginnen möchten.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return

    await message_func(
        "Bitte starten Sie zuerst mit *🔄 Start*.",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

# =========================================================
# CALLBACKS
# =========================================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data == "continue":
        await query.edit_message_reply_markup(reply_markup=None)
        await go_next_step(query, context)
        return

    if callback_data.startswith("quiz:"):
        await query.edit_message_reply_markup(reply_markup=None)
        await check_quiz_answer(query, context, callback_data)
        return

async def check_quiz_answer(query, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    data = load_data()
    user_id = str(query.from_user.id)

    if user_id not in data:
        await query.message.reply_text(
            "Bitte starten Sie zuerst mit *🔄 Start*.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return

    user = data[user_id]
    parts = callback_data.split(":")
    idx = int(parts[1])
    answer = parts[2]

    if user.get("step") != f"quiz_{idx + 1}":
        await query.message.reply_text("Diese Frage ist nicht mehr aktiv.")
        return

    q = QUIZZES[idx]

    if answer == q["correct"]:
        user["points"] += 10
        result_text = (
            f"Richtig! ✅\n{q['explanation']}\n"
            "Bitte klicken Sie auf *▶️ Weiter*."
        )
        points_text = "+10"
        result_label = "RICHTIG ✅"
    else:
        result_text = (
            f"Falsch ❌\n{q['explanation']}\n"
            "Bitte klicken Sie auf *▶️ Weiter*."
        )
        points_text = "0"
        result_label = "FALSCH ❌"

    save_data(data)

    await query.message.reply_text(
        result_text,
        parse_mode="Markdown",
        reply_markup=continue_inline(),
    )

# =========================================================
# MISSIONEN + MENÜBUTTONS
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text == "▶️ Weiter":
        await go_next_step(update, context)
        return
    if text == "🏆 Ranking":
        await ranking(update, context)
        return
    if text == "📊 Punkte":
        await punkte(update, context)
        return
    if text == "📈 Niveau":
        await niveau(update, context)
        return
    if text == "❓ Hilfe":
        await hilfe(update, context)
        return
    if text == "🔄 Start":
        await start(update, context)
        return

    data = load_data()
    user_id, user = get_user(update, data)
    step = user.get("step", "")
    message_text = update.message.text
    normalized = normalize_text(message_text)

    if step == "mission_1":
        found = 0
        for keyword in MISSIONS[0]["keywords"]:
            if keyword in normalized:
                found += 1

        if found >= 3:
            user["points"] += MISSIONS[0]["points"]
            user["step"] = "mission_1_done"
            save_data(data)

            await update.message.reply_text(
                f"Richtig! ✅\nMission 1 wurde erfolgreich gelöst.\n"
                f"Sie haben *+{MISSIONS[0]['points']} Punkte* bekommen.",
                parse_mode="Markdown",
                reply_markup=continue_inline(),
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\n"
                "Bitte nennen Sie: *Ali*, *Deutschland* und *Informatik*.",
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard(),
            )
        return

    if step == "mission_2":
        text_lower = message_text.lower()
        sentence_count = message_text.count(".") + message_text.count("!") + message_text.count("?")
        intro_words = [
            "heiße", "komme", "wohne", "studiere", "arbeite", "spreche"
        ]
        found = any(word in text_lower for word in intro_words)

        if sentence_count >= 3 and found:
            user["points"] += MISSIONS[1]["points"]
            user["step"] = "mission_2_done"
            save_data(data)

            await update.message.reply_text(
                f"Richtig! ✅\nMission 2 wurde erfolgreich gelöst.\n"
                f"Sie haben *+{MISSIONS[1]['points']} Punkte* bekommen.",
                parse_mode="Markdown",
                reply_markup=continue_inline(),
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\n"
                "Bitte schreiben Sie *drei bis fünf Sätze* über sich.",
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard(),
            )
        return

# =========================================================
# ABSCHLUSS
# =========================================================

async def send_final_result(message_func, user: dict):
    text = (
        "🎉 *Abschluss der Lektion*\n\n"
        "Sie haben die Lektion *„Die erste Bekanntschaft“* erfolgreich abgeschlossen.\n\n"
        f"*Gesamtpunktzahl:* {user['points']} 🏆\n"
        f"*Niveau:* {get_level(user['points'])}\n\n"
        "Nutzen Sie *🏆 Ranking*, um die Bestenliste zu sehen.\n"
        "Nutzen Sie *🔄 Start*, wenn Sie die Lektion noch einmal bearbeiten möchten."
    )
    await message_func(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

# =========================================================
# MAIN
# =========================================================

def main():
    if not TOKEN or TOKEN == "HIER_BOTFATHER_TOKEN_EINFUEGEN":
        raise ValueError("Bitte tragen Sie zuerst Ihren echten Bot-Token ein oder setzen Sie die Railway-Variable TOKEN.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weiter", weiter))
    app.add_handler(CommandHandler("hilfe", hilfe))
    app.add_handler(CommandHandler("punkte", punkte))
    app.add_handler(CommandHandler("niveau", niveau))
    app.add_handler(CommandHandler("ranking", ranking))

    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.post_init = set_bot_commands

    print("Bot ist gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()