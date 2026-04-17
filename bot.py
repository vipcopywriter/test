import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8579303242:AAE_BImQsA5-rv5sYPPocibMvV99J8OQqxA"

QUESTIONS = [
    {
        "block": "Ощущения",
        "text": "Ты чувствуешь облегчение, когда партнёр уезжает или задерживается?",
        "opts": [
            ("Да, честно говоря, да", 0),
            ("Иногда, но это нормально", 1),
            ("Нет, скучаю и жду", 2),
        ]
    },
    {
        "block": "Ощущения",
        "text": "Вы с партнёром можете говорить о важном — честно, без страха реакции?",
        "opts": [
            ("Нет, я заранее выбираю слова и момент", 0),
            ("Иногда получается, иногда нет", 1),
            ("Да, говорим открыто", 2),
        ]
    },
    {
        "block": "Отношения",
        "text": "Когда ты думаешь о следующих 5 годах в этих отношениях — что чувствуешь?",
        "opts": [
            ("Тревогу или усталость", 0),
            ("Неопределённость, не знаю чего хотеть", 1),
            ("Спокойствие и желание идти дальше", 2),
        ]
    },
    {
        "block": "Отношения",
        "text": "Ты остаёшься в отношениях потому что хочешь — или потому что страшно уйти?",
        "opts": [
            ("Скорее страшно уйти", 0),
            ("И то и другое одновременно", 1),
            ("Потому что хочу быть рядом", 2),
        ]
    },
    {
        "block": "Дети и дом",
        "text": "Дети видят в вашем доме живых и счастливых родителей — или напряжение и молчание?",
        "opts": [
            ("Чаще напряжение и молчание", 0),
            ("По-разному, зависит от дня", 1),
            ("Видят нас живыми и в контакте", 2),
        ]
    },
    {
        "block": "Ощущения",
        "text": "Ты помнишь, когда последний раз чувствовал(а) себя собой рядом с партнёром?",
        "opts": [
            ("Давно, уже не помню", 0),
            ("Иногда бывает, но редко", 1),
            ("Да, это моё обычное состояние рядом с ним/ней", 2),
        ]
    },
    {
        "block": "Кризис",
        "text": "Измена или серьёзное предательство в ваших отношениях было?",
        "opts": [
            ("Да, и это не проработано до сих пор", 0),
            ("Было, но мы через это прошли", 1),
            ("Нет, не было", 2),
        ]
    },
    {
        "block": "Отношения",
        "text": "Ты обсуждал(а) с партнёром то, что тебя по-настоящему не устраивает?",
        "opts": [
            ("Нет, бесполезно или страшно", 0),
            ("Пробовал(а), но ничего не меняется", 1),
            ("Да, мы работаем над этим вместе", 2),
        ]
    },
    {
        "block": "Кризис",
        "text": "Ты чувствуешь, что в этих отношениях ты на последнем месте — после всех и всего?",
        "opts": [
            ("Да, именно так", 0),
            ("Иногда так кажется", 1),
            ("Нет, я чувствую себя важным/важной", 2),
        ]
    },
    {
        "block": "Кризис",
        "text": "Если бы ты мог(ла) нажать кнопку и оказаться в другой жизни — нажал(а) бы?",
        "opts": [
            ("Да, не задумываясь", 0),
            ("Наверное да, но страшно", 1),
            ("Нет, моя жизнь здесь", 2),
        ]
    },
    {
        "block": "Кризис",
        "text": "Когда вы ссоритесь — это разговор двух взрослых или война, после которой становится только хуже?",
        "opts": [
            ("Чаще война, примирение ничего не решает", 0),
            ("По-разному, иногда находим выход", 1),
            ("Умеем слышать друг друга даже в конфликте", 2),
        ]
    },
    {
        "block": "Ощущения",
        "text": "Ты замечаешь, что тело реагирует на возвращение домой — напрягается, а не расслабляется?",
        "opts": [
            ("Да, дома я не отдыхаю", 0),
            ("Иногда бывает такое ощущение", 1),
            ("Дома мне спокойно и хорошо", 2),
        ]
    },
    {
        "block": "Дети и дом",
        "text": "Ты когда-нибудь ловил(а) себя на зависти к тем, кто уже прошёл через развод?",
        "opts": [
            ("Да, и это меня самого пугает", 0),
            ("Иногда такая мысль мелькает", 1),
            ("Нет, не завидую", 2),
        ]
    },
    {
        "block": "Отношения",
        "text": "Вы с партнёром близкие люди — или просто живёте под одной крышей?",
        "opts": [
            ("Скорее соседи с общим бытом", 0),
            ("Где-то между, бывает по-разному", 1),
            ("Близкие, есть настоящий контакт", 2),
        ]
    },
    {
        "block": "Отношения",
        "text": "Ты можешь честно сказать, что доверяешь партнёру — полностью, без оговорок?",
        "opts": [
            ("Нет, доверие давно подорвано", 0),
            ("Частично, в чём-то да, в чём-то нет", 1),
            ("Да, доверяю полностью", 2),
        ]
    },
]

MAX_SCORE = len(QUESTIONS) * 2


def get_result(score):
    if score <= 10:
        return (
            "🔴 В ваших отношениях много тревожных сигналов",
            "Ответы показывают серьёзное напряжение, которое давно накопилось. "
            "Это не приговор — но честный разговор с собой давно назрел. "
            "Такие ситуации не разрешаются сами, они только нарастают."
        )
    elif score <= 20:
        return (
            "🟡 Вы в зоне неопределённости",
            "Что-то держит, что-то тянет в другую сторону. "
            "Именно в этой точке важно разобраться честно — пока не стало больнее. "
            "Половина ответов говорит о реальных проблемах, которые стоит не игнорировать."
        )
    else:
        return (
            "🟢 В ваших отношениях есть живая основа",
            "Большинство ответов указывают на то, что контакт между вами сохранён. "
            "Но если вы всё равно прошли этот тест — значит что-то беспокоит. "
            "Стоит понять что именно, пока оно не стало больше."
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q"] = 0
    context.user_data["score"] = 0
    await update.message.reply_text(
        "Привет. Это тест на состояние отношений — 15 вопросов, честно и без лишних слов.\n\n"
        "Отвечай так, как есть на самом деле, а не как хотелось бы. "
        "В конце получишь результат и сможешь задать вопросы.\n\n"
        "Начинаем 👇"
    )
    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_idx = context.user_data["q"]
    q = QUESTIONS[q_idx]
    total = len(QUESTIONS)

    progress = "▓" * (q_idx + 1) + "░" * (total - q_idx - 1)
    header = f"*{q['block']}* · Вопрос {q_idx + 1} из {total}\n{progress}\n\n"

    keyboard = [
        [InlineKeyboardButton(text, callback_data=str(score))]
        for text, score in q["opts"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text(
            header + q["text"],
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            header + q["text"],
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    score = int(query.data)
    context.user_data["score"] = context.user_data.get("score", 0) + score
    context.user_data["q"] = context.user_data.get("q", 0) + 1

    q_idx = context.user_data["q"]

    if q_idx >= len(QUESTIONS):
        total_score = context.user_data["score"]
        title, text = get_result(total_score)

        keyboard = [
            [InlineKeyboardButton("Написать Павлу в Instagram →", url="https://instagram.com/busygin.pavel")],
            [InlineKeyboardButton("Написать в Telegram →", url="https://t.me/busygin_pavel")],
            [InlineKeyboardButton("Пройти тест заново", callback_data="restart")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            f"*Результат: {total_score} из {MAX_SCORE} баллов*\n\n"
            f"{title}\n\n{text}\n\n"
            "Если хочешь поговорить о своей ситуации честно — я здесь.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["q"] = 0
        context.user_data["score"] = 0
    else:
        await send_question(update, context)


async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_restart, pattern="^restart$"))
    app.add_handler(CallbackQueryHandler(handle_answer))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
