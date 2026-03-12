import json
import os
from telegram import (
    Update,
    BotCommand,
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

TOKEN = os.getenv("TOKEN", "HIER_DEIN_BOTFATHER_TOKEN")
ADMIN_ID = 6051699852
DATA_FILE = "users.json"
LOGO_FILE = "logo.png"

# -----------------------------------
# LEKTIONSINHALTE
# -----------------------------------
THEORY_TEXT = (
    "📘 *Theorie: Die Familie*\n\n"
    "Die Familie ist ein wichtiges Thema im Alltag. "
    "Man spricht oft über Eltern, Geschwister, Großeltern und Kinder.\n\n"
    "In dieser Lektion lernen Sie:\n"
    "• Wortschatz zum Thema Familie\n"
    "• einen Lesetext\n"
    "• Grammatik: Possessivartikel\n"
    "• Missionen\n"
    "• Quizfragen\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

VOCAB_TEXT = (
    "📚 *Wortschatz: Die Familie*\n\n"
    "die Familie — oila — семья\n"
    "der Vater — ota — отец\n"
    "die Mutter — ona — мать\n"
    "die Eltern — ota-ona — родители\n"
    "der Sohn — o‘g‘il — сын\n"
    "die Tochter — qiz — дочь\n"
    "der Bruder — aka/uka — брат\n"
    "die Schwester — opa/singil — сестра\n"
    "die Geschwister — aka-uka / opa-singillar — братья и сёстры\n"
    "der Großvater — bobo — дедушка\n"
    "die Großmutter — buvi — бабушка\n"
    "die Großeltern — bobo va buvi — дедушка и бабушка\n"
    "der Enkel — nabira — внук\n"
    "die Enkelin — nabira qiz — внучка\n"
    "der Onkel — amaki / tog‘a — дядя\n"
    "die Tante — xola / amma — тётя\n"
    "der Cousin — amakivachcha — двоюродный брат\n"
    "die Cousine — amakivachcha qiz — двоюродная сестра\n"
    "der Ehemann — er — муж\n"
    "die Ehefrau — xotin — жена\n"
    "das Kind — bola — ребёнок\n"
    "die Kinder — bolalar — дети\n"
    "ledig — bo‘ydoq — холостой\n"
    "verheiratet — turmush qurgan — женат / замужем\n"
    "geschieden — ajrashgan — разведён / разведена\n"
    "die Hochzeit — to‘y — свадьба\n"
    "heiraten — turmush qurmoq — жениться / выходить замуж\n"
    "wohnen — yashamoq — жить\n"
    "arbeiten — ishlamoq — работать\n"
    "studieren — o‘qimoq — учиться в университете\n"
    "zur Schule gehen — maktabga bormoq — ходить в школу\n"
    "freundlich — mehribon — дружелюбный\n"
    "der Zusammenhalt — jipslik — сплочённость\n"
    "wichtig — muhim — важный\n"
    "mein / meine — mening — мой / моя / мои\n"
    "sein / seine — uning — его\n"
    "ihr / ihre — uning — её\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

READING_TEXT = (
    "📖 *Lesetext: Meine Familie*\n\n"
    "Meine Familie ist nicht sehr groß, aber sehr freundlich.\n"
    "Ich habe einen Vater, eine Mutter und zwei Geschwister.\n\n"
    "Mein Vater heißt Karim. Er ist Ingenieur und arbeitet in einer Firma.\n"
    "Meine Mutter heißt Dilnoza. Sie ist Lehrerin und arbeitet an einer Schule.\n\n"
    "Ich habe einen Bruder und eine Schwester.\n"
    "Mein Bruder studiert Informatik an der Universität.\n"
    "Meine Schwester geht noch zur Schule.\n\n"
    "Meine Großeltern wohnen in einem Dorf.\n"
    "Wir besuchen sie oft am Wochenende.\n\n"
    "In meiner Familie ist Zusammenhalt sehr wichtig.\n"
    "Wir essen oft zusammen und sprechen über unseren Tag.\n"
    "Ich liebe meine Familie sehr.\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

GRAMMAR_TEXT = (
    "📘 *Grammatik: Possessivartikel*\n\n"
    "Possessivartikel zeigen Besitz oder Zugehörigkeit.\n\n"
    "Beispiele:\n"
    "• mein Vater\n"
    "• meine Mutter\n"
    "• mein Bruder\n"
    "• meine Schwester\n"
    "• meine Eltern\n\n"
    "*Tabelle:*\n"
    "ich → mein / meine\n"
    "du → dein / deine\n"
    "er → sein / seine\n"
    "sie → ihr / ihre\n"
    "wir → unser / unsere\n\n"
    "*Merksatz:*\n"
    "• maskulin / neutrum → oft *mein*\n"
    "• feminin / Plural → oft *meine*\n\n"
    "Beispiele:\n"
    "Das ist mein Vater.\n"
    "Das ist meine Mutter.\n"
    "Das sind meine Eltern.\n\n"
    "Bitte klicken Sie danach auf *▶️ Weiter*."
)

MISSIONS = [
    {
        "id": 1,
        "task": (
            "✍️ *Mission 1*\n\n"
            "Lesen Sie den Text und beantworten Sie die Frage:\n\n"
            "*Wie viele Geschwister hat die Person?*\n\n"
            "Bitte senden Sie Ihre Antwort als normales Wort oder als Zahl."
        ),
        "answers": ["zwei", "2"],
        "points": 15,
    },
    {
        "id": 2,
        "task": (
            "✍️ *Mission 2*\n\n"
            "Schreiben Sie *zwei Sätze* über Ihre Familie.\n\n"
            "Beispiel:\n"
            "Das ist mein Vater.\n"
            "Das ist meine Mutter."
        ),
        "special": "free_text_family",
        "points": 20,
    },
    {
        "id": 3,
        "task": (
            "✍️ *Mission 3*\n\n"
            "Ergänzen Sie den richtigen Possessivartikel:\n\n"
            "*Das ist ___ Bruder.*\n\n"
            "Bitte senden Sie nur *ein Wort*."
        ),
        "answers": ["mein"],
        "points": 15,
    },
]

GRAMMAR_QUIZZES = [
    {
        "question": "Das ist ___ Vater.",
        "options": {"a": "mein", "b": "meine", "c": "meinen"},
        "correct": "a",
        "explanation": "Richtig ist: *mein Vater*.",
    },
    {
        "question": "Das ist ___ Mutter.",
        "options": {"a": "mein", "b": "meine", "c": "meiner"},
        "correct": "b",
        "explanation": "Richtig ist: *meine Mutter*.",
    },
    {
        "question": "Das sind ___ Eltern.",
        "options": {"a": "mein", "b": "meine", "c": "meiner"},
        "correct": "b",
        "explanation": "Richtig ist: *meine Eltern*.",
    },
    {
        "question": "Das ist ___ Bruder.",
        "options": {"a": "mein", "b": "meine", "c": "meinen"},
        "correct": "a",
        "explanation": "Richtig ist: *mein Bruder*.",
    },
    {
        "question": "Das ist ___ Schwester.",
        "options": {"a": "mein", "b": "meine", "c": "meinen"},
        "correct": "b",
        "explanation": "Richtig ist: *meine Schwester*.",
    },
    {
        "question": "„sein Vater“ bedeutet …",
        "options": {"a": "uning otasi", "b": "mening otam", "c": "sizning otangiz"},
        "correct": "a",
        "explanation": "Richtig ist: *uning otasi*.",
    },
    {
        "question": "„ihre Mutter“ bedeutet …",
        "options": {"a": "uning onasi", "b": "mening onam", "c": "bizning onamiz"},
        "correct": "a",
        "explanation": "Richtig ist: *uning onasi*.",
    },
    {
        "question": "Possessivartikel zeigen …",
        "options": {"a": "Zeit", "b": "Besitz", "c": "Ort"},
        "correct": "b",
        "explanation": "Richtig ist: *Besitz*.",
    },
    {
        "question": "Das ist ___ Familie.",
        "options": {"a": "mein", "b": "meine", "c": "meiner"},
        "correct": "b",
        "explanation": "Richtig ist: *meine Familie*.",
    },
    {
        "question": "Das ist ___ Kind.",
        "options": {"a": "mein", "b": "meine", "c": "meiner"},
        "correct": "a",
        "explanation": "Richtig ist: *mein Kind*.",
    },
]

FAMILY_QUIZZES = [
    {
        "question": "Wie sagt man „ota“ auf Deutsch?",
        "options": {"a": "Vater", "b": "Bruder", "c": "Sohn"},
        "correct": "a",
        "explanation": "Richtig ist: *der Vater*.",
    },
    {
        "question": "Wie sagt man „ona“ auf Deutsch?",
        "options": {"a": "Schwester", "b": "Mutter", "c": "Tante"},
        "correct": "b",
        "explanation": "Richtig ist: *die Mutter*.",
    },
    {
        "question": "Bruder bedeutet …",
        "options": {"a": "aka/uka", "b": "bobo", "c": "amaki"},
        "correct": "a",
        "explanation": "Richtig ist: *aka/uka*.",
    },
    {
        "question": "Schwester bedeutet …",
        "options": {"a": "opa/singil", "b": "qiz", "c": "xola"},
        "correct": "a",
        "explanation": "Richtig ist: *opa/singil*.",
    },
    {
        "question": "Eltern bedeutet …",
        "options": {"a": "ota-ona", "b": "bolalar", "c": "amakivachchalar"},
        "correct": "a",
        "explanation": "Richtig ist: *ota-ona*.",
    },
    {
        "question": "Großvater bedeutet …",
        "options": {"a": "bobo", "b": "amaki", "c": "tog‘a"},
        "correct": "a",
        "explanation": "Richtig ist: *bobo*.",
    },
    {
        "question": "Großmutter bedeutet …",
        "options": {"a": "buvi", "b": "xola", "c": "opa"},
        "correct": "a",
        "explanation": "Richtig ist: *buvi*.",
    },
    {
        "question": "Cousin bedeutet …",
        "options": {"a": "amakivachcha", "b": "o‘g‘il", "c": "ota"},
        "correct": "a",
        "explanation": "Richtig ist: *amakivachcha*.",
    },
    {
        "question": "Enkel bedeutet …",
        "options": {"a": "nabira", "b": "aka", "c": "ota"},
        "correct": "a",
        "explanation": "Richtig ist: *nabira*.",
    },
    {
        "question": "Hochzeit bedeutet …",
        "options": {"a": "to‘y", "b": "tug‘ilgan kun", "c": "bayram"},
        "correct": "a",
        "explanation": "Richtig ist: *to‘y*.",
    },
]

# -----------------------------------
# HILFSFUNKTIONEN
# -----------------------------------
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
    first_name = update.effective_user.first_name if update.effective_user else "Student/in"

    if user_id not in data:
        data[user_id] = {
            "name": first_name or "Student/in",
            "points": 0,
            "step": "start",
            "grammar_quiz_index": None,
            "family_quiz_index": None,
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
    if points >= 220:
        return "Top-Lerner/in"
    if points >= 170:
        return "Sehr gut"
    if points >= 120:
        return "Fortgeschritten"
    if points >= 70:
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

def quiz_inline_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("A", callback_data="quiz:a"),
                InlineKeyboardButton("B", callback_data="quiz:b"),
                InlineKeyboardButton("C", callback_data="quiz:c"),
            ]
        ]
    )

# -----------------------------------
# BOT COMMANDS
# -----------------------------------
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

# -----------------------------------
# START / MENÜ
# -----------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    _, user = get_user(update, data)
    user["step"] = "theory"
    user["grammar_quiz_index"] = None
    user["family_quiz_index"] = None
    save_data(data)

    caption = (
        f"Willkommen, {user['name']}! 👋\n\n"
        "*Thema:* Die Familie\n"
        "*Niveau:* A2–B1\n\n"
        "*Lernweg:*\n"
        "1. Theorie\n"
        "2. Wortschatz\n"
        "3. Lesetext\n"
        "4. Grammatik\n"
        "5. 3 Missionen\n"
        "6. 10 Grammatik-Quizfragen\n"
        "7. 10 Quizfragen zum Thema Familie\n"
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
        "2. Lesen Sie Theorie, Wortschatz, Text und Grammatik\n"
        "3. Lösen Sie die Missionen\n"
        "4. Beantworten Sie die Quizfragen über Buttons\n\n"
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
        reverse=True
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

# -----------------------------------
# QUIZ SENDEN
# -----------------------------------
async def send_grammar_quiz(message_func, index: int):
    q = GRAMMAR_QUIZZES[index]
    text = (
        f"🧠 *Grammatik-Quiz {index + 1}*\n\n"
        f"{q['question']}\n\n"
        f"A) {q['options']['a']}\n"
        f"B) {q['options']['b']}\n"
        f"C) {q['options']['c']}\n\n"
        "Bitte wählen Sie eine Antwort:"
    )
    await message_func(text, parse_mode="Markdown", reply_markup=quiz_inline_keyboard())

async def send_family_quiz(message_func, index: int):
    q = FAMILY_QUIZZES[index]
    text = (
        f"👨‍👩‍👧‍👦 *Familie-Quiz {index + 1}*\n\n"
        f"{q['question']}\n\n"
        f"A) {q['options']['a']}\n"
        f"B) {q['options']['b']}\n"
        f"C) {q['options']['c']}\n\n"
        "Bitte wählen Sie eine Antwort:"
    )
    await message_func(text, parse_mode="Markdown", reply_markup=quiz_inline_keyboard())

# -----------------------------------
# WEITER-LOGIK
# -----------------------------------
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
                "grammar_quiz_index": None,
                "family_quiz_index": None,
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
        user["step"] = "reading"
        save_data(data)
        await message_func(READING_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "reading":
        user["step"] = "grammar"
        save_data(data)
        await message_func(GRAMMAR_TEXT, parse_mode="Markdown", reply_markup=continue_inline())
        return

    if step == "grammar":
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
        user["step"] = "mission_3"
        save_data(data)
        await message_func(MISSIONS[2]["task"], parse_mode="Markdown", reply_markup=main_menu_keyboard())
        return

    if step == "mission_3_done":
        user["step"] = "grammar_quiz_1"
        user["grammar_quiz_index"] = 0
        save_data(data)
        await send_grammar_quiz(message_func, 0)
        return

    if step.startswith("grammar_quiz_"):
        idx = user.get("grammar_quiz_index")
        if idx is None:
            await message_func("Bitte starten Sie zuerst mit *Start*.", parse_mode="Markdown")
            return
        if idx < len(GRAMMAR_QUIZZES) - 1:
            idx += 1
            user["grammar_quiz_index"] = idx
            user["step"] = f"grammar_quiz_{idx + 1}"
            save_data(data)
            await send_grammar_quiz(message_func, idx)
            return
        else:
            user["step"] = "family_quiz_1"
            user["family_quiz_index"] = 0
            save_data(data)
            await send_family_quiz(message_func, 0)
            return

    if step.startswith("family_quiz_"):
        idx = user.get("family_quiz_index")
        if idx is None:
            await message_func("Bitte starten Sie zuerst mit *Start*.", parse_mode="Markdown")
            return
        if idx < len(FAMILY_QUIZZES) - 1:
            idx += 1
            user["family_quiz_index"] = idx
            user["step"] = f"family_quiz_{idx + 1}"
            save_data(data)
            await send_family_quiz(message_func, idx)
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

# -----------------------------------
# CALLBACK BUTTONS
# -----------------------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data == "continue":
        await go_next_step(query, context)
        return

    if callback_data.startswith("quiz:"):
        answer = callback_data.split(":")[1]
        await check_quiz_answer(query, context, answer)
        return

async def check_quiz_answer(query, context: ContextTypes.DEFAULT_TYPE, answer: str):
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
    step = user.get("step", "")

    if step.startswith("grammar_quiz_"):
        idx = user.get("grammar_quiz_index")
        if idx is None:
            await query.message.reply_text("Bitte nutzen Sie *▶️ Weiter*.", parse_mode="Markdown")
            return
        q = GRAMMAR_QUIZZES[idx]
        quiz_type = "Grammatik"

    elif step.startswith("family_quiz_"):
        idx = user.get("family_quiz_index")
        if idx is None:
            await query.message.reply_text("Bitte nutzen Sie *▶️ Weiter*.", parse_mode="Markdown")
            return
        q = FAMILY_QUIZZES[idx]
        quiz_type = "Familie"

    else:
        await query.message.reply_text(
            "Im Moment ist kein Quiz aktiv.\nBitte nutzen Sie *▶️ Weiter*.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return

    if answer == q["correct"]:
        user["points"] += 10
        save_data(data)

        await query.message.reply_text(
            f"Richtig! ✅\n{q['explanation']}\nSie haben *+10 Punkte* bekommen.\n\n"
            "Bitte klicken Sie auf *▶️ Weiter*.",
            parse_mode="Markdown",
            reply_markup=continue_inline(),
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n"
                f"Bereich: {quiz_type}\n\n"
                f"Frage: {q['question']}\n"
                f"Antwort: {answer}\n"
                f"Ergebnis: RICHTIG ✅\n"
                f"Vergebene Punkte: +10\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )
    else:
        save_data(data)

        await query.message.reply_text(
            f"Falsch ❌\n{q['explanation']}\nVergebene Punkte: 0\n\n"
            "Bitte klicken Sie auf *▶️ Weiter*.",
            parse_mode="Markdown",
            reply_markup=continue_inline(),
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🧠 Quiz-Antwort\n\n"
                f"Student/in: {user['name']}\n"
                f"ID: {user_id}\n"
                f"Bereich: {quiz_type}\n\n"
                f"Frage: {q['question']}\n"
                f"Antwort: {answer}\n"
                f"Ergebnis: FALSCH ❌\n"
                f"Vergebene Punkte: 0\n"
                f"Gesamtpunktzahl: {user['points']} 🏆"
            )
        )

# -----------------------------------
# MISSIONEN
# -----------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    # Menü-Tasten
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
        if normalized in MISSIONS[0]["answers"]:
            user["points"] += MISSIONS[0]["points"]
            user["step"] = "mission_1_done"
            save_data(data)

            await update.message.reply_text(
                f"Richtig! ✅\nMission 1 wurde erfolgreich gelöst.\n"
                f"Sie haben *+{MISSIONS[0]['points']} Punkte* bekommen.",
                parse_mode="Markdown",
                reply_markup=continue_inline(),
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
                    f"Vergebene Punkte: +{MISSIONS[0]['points']}\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal.",
                reply_markup=main_menu_keyboard(),
            )
        return

    if step == "mission_2":
        text_lower = message_text.lower()
        sentence_count = message_text.count(".") + message_text.count("!") + message_text.count("?")
        family_words = [
            "vater", "mutter", "bruder", "schwester", "familie",
            "eltern", "großvater", "großmutter", "kind", "kinder",
            "onkel", "tante", "cousin", "cousine"
        ]
        found = any(word in text_lower for word in family_words)

        if sentence_count >= 2 and found:
            user["points"] += MISSIONS[1]["points"]
            user["step"] = "mission_2_done"
            save_data(data)

            await update.message.reply_text(
                f"Richtig! ✅\nMission 2 wurde erfolgreich gelöst.\n"
                f"Sie haben *+{MISSIONS[1]['points']} Punkte* bekommen.",
                parse_mode="Markdown",
                reply_markup=continue_inline(),
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
                    f"Vergebene Punkte: +{MISSIONS[1]['points']}\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte schreiben Sie zwei Sätze über Ihre Familie.",
                reply_markup=main_menu_keyboard(),
            )
        return

    if step == "mission_3":
        if normalized in MISSIONS[2]["answers"]:
            user["points"] += MISSIONS[2]["points"]
            user["step"] = "mission_3_done"
            save_data(data)

            await update.message.reply_text(
                f"Richtig! ✅\nMission 3 wurde erfolgreich gelöst.\n"
                f"Sie haben *+{MISSIONS[2]['points']} Punkte* bekommen.",
                parse_mode="Markdown",
                reply_markup=continue_inline(),
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
                    f"Vergebene Punkte: +{MISSIONS[2]['points']}\n"
                    f"Gesamtpunktzahl: {user['points']} 🏆"
                )
            )
        else:
            await update.message.reply_text(
                "Noch nicht richtig ❌\nBitte versuchen Sie es noch einmal.",
                reply_markup=main_menu_keyboard(),
            )
        return

# -----------------------------------
# ABSCHLUSS
# -----------------------------------
async def send_final_result(message_func, user: dict):
    text = (
        "🎉 *Abschluss der Lektion*\n\n"
        "Sie haben die Lektion *„Die Familie“* erfolgreich abgeschlossen.\n\n"
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

# -----------------------------------
# MAIN
# -----------------------------------
def main():
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