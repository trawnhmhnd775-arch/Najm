from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# إنشاء أزرار شفافة (بدون خلفية واضحة)
def transparent_reply_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in buttons:
        kb.row(*[KeyboardButton(text=b) for b in row])
    return kb
