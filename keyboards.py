from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def malumot_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Oliy", callback_data="mal:oliy")],
        [InlineKeyboardButton(text="📚 O'rta maxsus", callback_data="mal:orta_maxsus")],
        [InlineKeyboardButton(text="📖 O'rta", callback_data="mal:orta")],
    ])

def tasdiqlash_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash va Word yuklab olish", callback_data="tasdiq:ha")],
        [InlineKeyboardButton(text="✏️ Qaytadan to'ldirish", callback_data="tasdiq:yoq")],
    ])

def oila_yana_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Yana qo'shish", callback_data="oila:yana")],
        [InlineKeyboardButton(text="➡️ Davom etish", callback_data="oila:tugash")],
    ])

def skip_kb(callback="skip"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data=callback)],
    ])

def qaytish_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Qaytadan boshlash", callback_data="restart")],
    ])

def jinsi_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Erkak", callback_data="jins:erkak")],
        [InlineKeyboardButton(text="👩 Ayol", callback_data="jins:ayol")],
    ])
