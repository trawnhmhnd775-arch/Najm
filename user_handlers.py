from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from db import DB
from keyboards import transparent_reply_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, db: DB):
    # التأكد من أن المستخدم موجود في قاعدة البيانات
    await db.ensure_user(message.from_user)

    # نص الرسالة الترحيبية
    welcome_text = "<b>🎮 مرحبًا بك في بوت الشحن!</b>\nاختر من الأزرار أدناه."

    # أزرار شفافة: القناة الرسمية والتواصل مع الدعم
    transparent_buttons = [
        ['🌐 القناة الرسمية للمتجر', '💬 التواصل مع الدعم']
    ]
    transparent_kb = transparent_reply_keyboard(transparent_buttons)

    # إرسال الرسالة الترحيبية مع الأزرار الشفافة
    await message.answer(welcome_text, reply_markup=transparent_kb, parse_mode="HTML")

@router.message(lambda message: message.text == "🌐 القناة الرسمية للمتجر")
async def redirect_to_channel(message: Message):
    # عند الضغط على الزر الأول، يتم تحويل المستخدم إلى القناة الرسمية للمتجر
    await message.answer("🔗 تحولت إلى القناة الرسمية للمتجر.", reply_markup=ReplyKeyboardRemove())
    # إرسل رابط القناة الرسمية
    await message.answer("اضغط هنا للانتقال إلى القناة: https://t.me/X_MAX_STOR")

@router.message(lambda message: message.text == "💬 التواصل مع الدعم")
async def redirect_to_support(message: Message):
    # عند الضغط على الزر الثاني، يتم تحويل المستخدم إلى دعم المتجر
    await message.answer("🔗 تم تحويلك إلى الدعم.", reply_markup=ReplyKeyboardRemove())
    # إرسل رابط الدعم
    await message.answer("للتواصل مع الدعم، اضغط هنا: https://t.me/XMAX_SUPPORTbot")
