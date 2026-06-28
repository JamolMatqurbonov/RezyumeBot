from aiogram.fsm.state import State, StatesGroup

class RezyumeState(StatesGroup):
    # Shaxsiy ma'lumotlar
    familya         = State()
    ism             = State()
    otasining_ismi  = State()
    tugilgan_sana   = State()
    tugilgan_joy    = State()
    millati         = State()
    partiya         = State()
    manzil          = State()
    telefon         = State()
    email           = State()

    # Ta'lim
    malumot         = State()   # Oliy / O'rta maxsus / O'rta
    okuw_joyi       = State()   # Qaysi muassasa
    tamomlagan      = State()   # Qaysi yil
    mutaxassislik   = State()   # Mutaxassislik

    # Tillar
    tillar          = State()   # Qaysi tillarni biladi

    # Mehnat faoliyati
    ish_joyi        = State()   # Joriy/oxirgi ish joyi
    lavozim         = State()   # Lavozim
    ish_yillari     = State()   # Qaysi yildan qaysi yilgacha

    # Qo'shimcha
    mukofotlar      = State()   # Mukofotlar
    qoshimcha       = State()   # Qo'shimcha ma'lumot

    # Oila a'zolari
    oila_boshi      = State()   # Ota/ona/aka/uka...
    oila_ismi       = State()
    oila_yili       = State()
    oila_ish        = State()
    oila_manzil     = State()
    oila_yana       = State()   # Yana qo'shish?

    # Rasm
    rasm            = State()

    # Tasdiqlash
    tasdiqlash      = State()
