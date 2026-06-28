import os, json, subprocess, asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from states import RezyumeState
from keyboards import (
    malumot_kb, tasdiqlash_kb, oila_yana_kb, skip_kb, qaytish_kb
)

router = Router()

DOCX_SCRIPT = os.path.join(os.path.dirname(__file__), "generate_docx.js")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════
# /start
# ═══════════════════════════════════════════════════
@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RezyumeState.familya)
    await msg.answer(
        "👋 <b>Rezyume (MA'LUMOTNOMA) bot</b>ga xush kelibsiz!\n\n"
        "Men sizning ma'lumotlaringizni yig'ib, <b>rasmiy Word hujjati</b> tayyorlab beraman.\n\n"
        "Boshlaylik! 📝\n\n"
        "1️⃣ <b>Familyangizni</b> kiriting (masalan: Maткурбонов):",
        parse_mode="HTML"
    )

@router.callback_query(F.data == "restart")
async def restart(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(RezyumeState.familya)
    await cb.message.answer(
        "🔄 Qaytadan boshlaymiz!\n\n1️⃣ <b>Familyangizni</b> kiriting:",
        parse_mode="HTML"
    )

# ═══════════════════════════════════════════════════
# SHAXSIY MA'LUMOTLAR
# ═══════════════════════════════════════════════════
@router.message(RezyumeState.familya)
async def q_familya(msg: Message, state: FSMContext):
    await state.update_data(familya=msg.text.strip())
    await state.set_state(RezyumeState.ism)
    await msg.answer("2️⃣ <b>Ismingizni</b> kiriting:", parse_mode="HTML")

@router.message(RezyumeState.ism)
async def q_ism(msg: Message, state: FSMContext):
    await state.update_data(ism=msg.text.strip())
    await state.set_state(RezyumeState.otasining_ismi)
    await msg.answer("3️⃣ <b>Otangizning ismini</b> kiriting:", parse_mode="HTML")

@router.message(RezyumeState.otasining_ismi)
async def q_otaismi(msg: Message, state: FSMContext):
    await state.update_data(otasining_ismi=msg.text.strip())
    await state.set_state(RezyumeState.tugilgan_sana)
    await msg.answer("4️⃣ <b>Tug'ilgan sanangizni</b> kiriting:\n<i>Masalan: 19.05.2004</i>", parse_mode="HTML")

@router.message(RezyumeState.tugilgan_sana)
async def q_sana(msg: Message, state: FSMContext):
    await state.update_data(tugilgan_sana=msg.text.strip())
    await state.set_state(RezyumeState.tugilgan_joy)
    await msg.answer("5️⃣ <b>Tug'ilgan joyingizni</b> kiriting:\n<i>Masalan: Xorazm viloyati, Bog'ot tumani</i>", parse_mode="HTML")

@router.message(RezyumeState.tugilgan_joy)
async def q_joy(msg: Message, state: FSMContext):
    await state.update_data(tugilgan_joy=msg.text.strip())
    await state.set_state(RezyumeState.millati)
    await msg.answer("6️⃣ <b>Millatingizni</b> kiriting:\n<i>Masalan: o'zbek, rus, qozoq</i>", parse_mode="HTML")

@router.message(RezyumeState.millati)
async def q_millat(msg: Message, state: FSMContext):
    await state.update_data(millati=msg.text.strip())
    await state.set_state(RezyumeState.partiya)
    await msg.answer(
        "7️⃣ <b>Partiyaviyligingiz:</b>\n<i>Masalan: partiyasiz, yoki partiya nomi</i>",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:partiya")
    )

@router.callback_query(F.data == "skip:partiya")
async def skip_partiya(cb: CallbackQuery, state: FSMContext):
    await state.update_data(partiya="партиясиз")
    await state.set_state(RezyumeState.manzil)
    await cb.message.answer("8️⃣ <b>Yashash manzilingizni</b> kiriting:\n<i>Masalan: Toshkent sh., Mirzo Ulug'bek t., Xislat ko'chasi 11-uy</i>", parse_mode="HTML")

@router.message(RezyumeState.partiya)
async def q_partiya(msg: Message, state: FSMContext):
    await state.update_data(partiya=msg.text.strip())
    await state.set_state(RezyumeState.manzil)
    await msg.answer("8️⃣ <b>Yashash manzilingizni</b> kiriting:", parse_mode="HTML")

@router.message(RezyumeState.manzil)
async def q_manzil(msg: Message, state: FSMContext):
    await state.update_data(manzil=msg.text.strip())
    await state.set_state(RezyumeState.telefon)
    await msg.answer("9️⃣ <b>Telefon raqamingiz:</b>", parse_mode="HTML")

@router.message(RezyumeState.telefon)
async def q_telefon(msg: Message, state: FSMContext):
    await state.update_data(telefon=msg.text.strip())
    await state.set_state(RezyumeState.email)
    await msg.answer(
        "1️⃣0️⃣ <b>E-mail manzilingiz</b> (ixtiyoriy):",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:email")
    )

@router.callback_query(F.data == "skip:email")
async def skip_email(cb: CallbackQuery, state: FSMContext):
    await state.update_data(email="—")
    await _malumot_savol(cb.message, state)

@router.message(RezyumeState.email)
async def q_email(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text.strip())
    await _malumot_savol(msg, state)

# ═══════════════════════════════════════════════════
# TA'LIM
# ═══════════════════════════════════════════════════
async def _malumot_savol(msg: Message, state: FSMContext):
    await state.set_state(RezyumeState.malumot)
    await msg.answer("📚 <b>Ma'lumotingiz:</b>", parse_mode="HTML", reply_markup=malumot_kb())

@router.callback_query(F.data.startswith("mal:"))
async def q_malumot(cb: CallbackQuery, state: FSMContext):
    val = {"mal:oliy": "олий", "mal:orta_maxsus": "ўрта махсус", "mal:orta": "ўрта"}
    await state.update_data(malumot=val.get(cb.data, "олий"))
    await state.set_state(RezyumeState.okuw_joyi)
    await cb.message.answer("🏫 <b>O'qigan muassasangiz nomini kiriting:</b>\n<i>Masalan: Toshkent davlat yuridik instituti</i>", parse_mode="HTML")

@router.message(RezyumeState.okuw_joyi)
async def q_okuw(msg: Message, state: FSMContext):
    await state.update_data(okuw_joyi=msg.text.strip())
    await state.set_state(RezyumeState.tamomlagan)
    await msg.answer("📅 <b>Qaysi yili tamomlagan/tamomlaydigan yilni</b> kiriting:\n<i>Masalan: 2026</i>", parse_mode="HTML")

@router.message(RezyumeState.tamomlagan)
async def q_tamomlagan(msg: Message, state: FSMContext):
    await state.update_data(tamomlagan=msg.text.strip())
    await state.set_state(RezyumeState.mutaxassislik)
    await msg.answer("🎯 <b>Mutaxassisligingiz:</b>\n<i>Masalan: huquqshunos, iqtisodchi, muhandis</i>", parse_mode="HTML")

@router.message(RezyumeState.mutaxassislik)
async def q_mutaxassis(msg: Message, state: FSMContext):
    await state.update_data(mutaxassislik=msg.text.strip())
    await state.set_state(RezyumeState.tillar)
    await msg.answer("🌐 <b>Qaysi tillarni bilasiz?</b>\n<i>Masalan: rus tili, ingliz tili (o'rta daraja)</i>", parse_mode="HTML")

# ═══════════════════════════════════════════════════
# MEHNAT FAOLIYATI
# ═══════════════════════════════════════════════════
@router.message(RezyumeState.tillar)
async def q_tillar(msg: Message, state: FSMContext):
    await state.update_data(tillar=msg.text.strip())
    await state.set_state(RezyumeState.ish_joyi)
    await msg.answer(
        "💼 <b>Joriy yoki oxirgi ish joyingiz:</b>\n<i>Masalan: OOO 'Imkon Pro' yoki 'Talaba (hali ishlamagan)'</i>",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:ish")
    )

@router.callback_query(F.data == "skip:ish")
async def skip_ish(cb: CallbackQuery, state: FSMContext):
    await state.update_data(ish_joyi="", lavozim="", ish_yillari="")
    await _mukofot_savol(cb.message, state)

@router.message(RezyumeState.ish_joyi)
async def q_ish(msg: Message, state: FSMContext):
    await state.update_data(ish_joyi=msg.text.strip())
    await state.set_state(RezyumeState.lavozim)
    await msg.answer("💼 <b>Lavozimingiz:</b>\n<i>Masalan: yurist, dasturchi, buxgalter</i>", parse_mode="HTML")

@router.message(RezyumeState.lavozim)
async def q_lavozim(msg: Message, state: FSMContext):
    await state.update_data(lavozim=msg.text.strip())
    await state.set_state(RezyumeState.ish_yillari)
    await msg.answer("📅 <b>Qaysi yillardan beri ishlaysiz?</b>\n<i>Masalan: 2022–2026 yoki 2024-hozir</i>", parse_mode="HTML")

@router.message(RezyumeState.ish_yillari)
async def q_yillar(msg: Message, state: FSMContext):
    await state.update_data(ish_yillari=msg.text.strip())
    await _mukofot_savol(msg, state)

# ═══════════════════════════════════════════════════
# MUKOFOTLAR
# ═══════════════════════════════════════════════════
async def _mukofot_savol(msg, state):
    await state.set_state(RezyumeState.mukofotlar)
    await msg.answer(
        "🏆 <b>Davlat mukofotlari yoki yutuqlaringiz</b> (ixtiyoriy):\n<i>Masalan: yo'q, yoki Olimpiada g'olibi 2023</i>",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:mukofoot")
    )

@router.callback_query(F.data == "skip:mukofoot")
async def skip_mukofot(cb: CallbackQuery, state: FSMContext):
    await state.update_data(mukofotlar="йўқ")
    await _oila_boshlash(cb.message, state)

@router.message(RezyumeState.mukofotlar)
async def q_mukofot(msg: Message, state: FSMContext):
    await state.update_data(mukofotlar=msg.text.strip())
    await _oila_boshlash(msg, state)

# ═══════════════════════════════════════════════════
# OILA A'ZOLARI
# ═══════════════════════════════════════════════════
async def _oila_boshlash(msg, state):
    await state.update_data(oila=[])
    await state.set_state(RezyumeState.oila_boshi)
    await msg.answer(
        "👨‍👩‍👧‍👦 <b>Oila a'zolari haqida ma'lumot</b>\n\n"
        "Birinchi a'zo — <b>qanday qarindosh?</b>\n<i>Masalan: Otasi, Onasi, Akasi, Ukasi, Singlisi, Opasi, Rafiqasi, Eri</i>",
        parse_mode="HTML"
    )

@router.message(RezyumeState.oila_boshi)
async def q_oila_boshi(msg: Message, state: FSMContext):
    data = await state.get_data()
    joriy = data.get("_joriy_oila", {})
    joriy["qarindoshligi"] = msg.text.strip()
    await state.update_data(_joriy_oila=joriy)
    await state.set_state(RezyumeState.oila_ismi)
    await msg.answer("👤 <b>Familya, ism, otasining ismi:</b>", parse_mode="HTML")

@router.message(RezyumeState.oila_ismi)
async def q_oila_ismi(msg: Message, state: FSMContext):
    data = await state.get_data()
    joriy = data.get("_joriy_oila", {})
    joriy["ismi"] = msg.text.strip()
    await state.update_data(_joriy_oila=joriy)
    await state.set_state(RezyumeState.oila_yili)
    await msg.answer("📅 <b>Tug'ilgan yili va joyi:</b>\n<i>Masalan: 1982 yil, Bog'ot tumani</i>", parse_mode="HTML")

@router.message(RezyumeState.oila_yili)
async def q_oila_yili(msg: Message, state: FSMContext):
    data = await state.get_data()
    joriy = data.get("_joriy_oila", {})
    joriy["yili"] = msg.text.strip()
    await state.update_data(_joriy_oila=joriy)
    await state.set_state(RezyumeState.oila_ish)
    await msg.answer("💼 <b>Ish joyi va lavozimi:</b>\n<i>Masalan: Davlat xavfsizlik xizmati, talaba, uy bekasi</i>", parse_mode="HTML")

@router.message(RezyumeState.oila_ish)
async def q_oila_ish(msg: Message, state: FSMContext):
    data = await state.get_data()
    joriy = data.get("_joriy_oila", {})
    joriy["ish_joyi"] = msg.text.strip()
    await state.update_data(_joriy_oila=joriy)
    await state.set_state(RezyumeState.oila_manzil)
    await msg.answer("📍 <b>Yashash manzili:</b>", parse_mode="HTML")

@router.message(RezyumeState.oila_manzil)
async def q_oila_manzil(msg: Message, state: FSMContext):
    data = await state.get_data()
    joriy = data.get("_joriy_oila", {})
    joriy["manzil"] = msg.text.strip()
    oila = data.get("oila", [])
    oila.append(joriy)
    await state.update_data(oila=oila, _joriy_oila={})
    await state.set_state(RezyumeState.oila_yana)
    await msg.answer(
        f"✅ {joriy.get('qarindoshligi', 'A\'zo')} qo'shildi.\n\nYana oila a'zosi qo'shasizmi?",
        reply_markup=oila_yana_kb()
    )

@router.callback_query(F.data == "oila:yana")
async def oila_yana(cb: CallbackQuery, state: FSMContext):
    await state.set_state(RezyumeState.oila_boshi)
    await cb.message.answer("Keyingi a'zo — <b>qanday qarindosh?</b>", parse_mode="HTML")

@router.callback_query(F.data == "oila:tugash")
async def oila_tugash(cb: CallbackQuery, state: FSMContext):
    await state.set_state(RezyumeState.qoshimcha)
    await cb.message.answer(
        "📝 <b>Qo'shimcha ma'lumot</b> (ixtiyoriy):\n<i>Ko'nikma, maqsad, hobby va h.k.</i>",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:qoshimcha")
    )

@router.callback_query(F.data == "skip:qoshimcha")
async def skip_qoshimcha(cb: CallbackQuery, state: FSMContext):
    await state.update_data(qoshimcha="")
    await _rasm_savol(cb.message, state)

@router.message(RezyumeState.qoshimcha)
async def q_qoshimcha(msg: Message, state: FSMContext):
    await state.update_data(qoshimcha=msg.text.strip())
    await _rasm_savol(msg, state)

# ═══════════════════════════════════════════════════
# RASM
# ═══════════════════════════════════════════════════
async def _rasm_savol(msg, state):
    await state.set_state(RezyumeState.rasm)
    await msg.answer(
        "📸 <b>Rasm yuboring</b> (hujjat uchun foto, ixtiyoriy):\n<i>Pasport yoki 3×4 foto</i>",
        parse_mode="HTML",
        reply_markup=skip_kb("skip:rasm")
    )

@router.callback_query(F.data == "skip:rasm")
async def skip_rasm(cb: CallbackQuery, state: FSMContext):
    await state.update_data(rasm_path=None)
    await _ko_rsatish(cb.message, state)

@router.message(RezyumeState.rasm, F.photo)
async def q_rasm(msg: Message, state: FSMContext, bot: Bot):
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    rasm_path = os.path.join(TEMP_DIR, f"{msg.from_user.id}_photo.jpg")
    await bot.download_file(file.file_path, destination=rasm_path)
    await state.update_data(rasm_path=rasm_path)
    await _ko_rsatish(msg, state)

@router.message(RezyumeState.rasm)
async def rasm_emas(msg: Message, state: FSMContext):
    await state.update_data(rasm_path=None)
    await _ko_rsatish(msg, state)

# ═══════════════════════════════════════════════════
# MA'LUMOTLARNI KO'RSATISH
# ═══════════════════════════════════════════════════
async def _ko_rsatish(msg, state):
    data = await state.get_data()
    await state.set_state(RezyumeState.tasdiqlash)

    oila_text = ""
    for a in data.get("oila", []):
        oila_text += f"\n  • {a.get('qarindoshligi')}: {a.get('ismi')} ({a.get('yili')})"

    preview = (
        f"📋 <b>Kiritilgan ma'lumotlar:</b>\n\n"
        f"👤 <b>F.I.O:</b> {data.get('familya')} {data.get('ism')} {data.get('otasining_ismi')}\n"
        f"🗓 <b>Tug'ilgan:</b> {data.get('tugilgan_sana')} — {data.get('tugilgan_joy')}\n"
        f"🌍 <b>Millati:</b> {data.get('millati')} | {data.get('partiya')}\n"
        f"📍 <b>Manzil:</b> {data.get('manzil')}\n"
        f"📞 <b>Telefon:</b> {data.get('telefon')} | {data.get('email')}\n\n"
        f"🎓 <b>Ma'lumot:</b> {data.get('malumot')} — {data.get('okuw_joyi')} ({data.get('tamomlagan')} y.)\n"
        f"🎯 <b>Mutaxassislik:</b> {data.get('mutaxassislik')}\n"
        f"🌐 <b>Tillar:</b> {data.get('tillar')}\n\n"
        f"💼 <b>Ish:</b> {data.get('ish_joyi') or '—'} — {data.get('lavozim') or '—'} ({data.get('ish_yillari') or '—'})\n"
        f"🏆 <b>Mukofotlar:</b> {data.get('mukofotlar')}\n"
        f"\n👨‍👩‍👧 <b>Oila a'zolari:</b>{oila_text or ' —'}\n"
    )

    await msg.answer(preview, parse_mode="HTML", reply_markup=tasdiqlash_kb())

# ═══════════════════════════════════════════════════
# TASDIQLASH VA DOCX YARATISH
# ═══════════════════════════════════════════════════
@router.callback_query(F.data == "tasdiq:yoq")
async def qayta(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(RezyumeState.familya)
    await cb.message.answer("🔄 Qaytadan boshlaymiz!\n\n1️⃣ <b>Familyangizni</b> kiriting:", parse_mode="HTML")

@router.callback_query(F.data == "tasdiq:ha")
async def yaratish(cb: CallbackQuery, state: FSMContext, bot: Bot):
    await cb.message.edit_text("⏳ <b>Hujjat tayyorlanmoqda...</b>", parse_mode="HTML")
    data = await state.get_data()

    uid = cb.from_user.id
    json_path = os.path.join(TEMP_DIR, f"{uid}_data.json")
    docx_path = os.path.join(TEMP_DIR, f"{uid}_rezyume.docx")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Node.js orqali DOCX yaratish
    result = subprocess.run(
        ["node", DOCX_SCRIPT, json_path, docx_path],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode != 0 or not os.path.exists(docx_path):
        await cb.message.answer(
            "❌ Hujjat yaratishda xatolik.\n\n" + result.stderr,
            reply_markup=qaytish_kb()
        )
        return

    d = data
    filename = f"{d.get('familya','')}{d.get('ism','')[0] if d.get('ism') else ''}_malumotnoma.docx"

    doc_file = FSInputFile(docx_path, filename=filename)
    await bot.send_document(
        cb.from_user.id,
        doc_file,
        caption=(
            f"✅ <b>Hujjatingiz tayyor!</b>\n\n"
            f"👤 {d.get('familya')} {d.get('ism')} {d.get('otasining_ismi')}\n"
            f"📄 Rasmiy MA'LUMOTNOMA formati\n\n"
            "Hujjatni Word da ochib, zarur bo'lsa ozgina tahrirlashingiz mumkin."
        ),
        parse_mode="HTML"
    )

    # Fayllarni tozalash
    for p in [json_path, docx_path]:
        try: os.remove(p)
        except: pass

    await state.clear()

    await cb.message.answer(
        "🎉 Muvaffaqiyat! Yana rezyume yaratmoqchi bo'lsangiz /start bosing.",
        reply_markup=qaytish_kb()
    )
