import os
import urllib.parse
import urllib.request
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, BufferedInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# ==================== SOZLAMALAR ====================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ==================== TILLAR LUG'ATI ====================
LANG = {
    "en": {
        "start": "Hello! I will help you create the visual and character profile of your ideal friend.\n\nQuestion 1 (Select Country):\nChoose one of the buttons below:",
        "gender": "Question 2 (Select Gender):\nWhat is your friend's gender?",
        "name": "Question 3 (Enter Name):\nType your friend's name as text (e.g., Hasan, Amelia, Rayan).",
        "age": "Question 4 (Select Age):\nHow old is your friend?",
        "appearance": "Question 5 (Select Appearance):\n\nHair color:",
        "eye_color": "Eye color:",
        "face_shape": "Face shape:",
        "pos_traits": "Question 6: Personality\n\nSelect a positive trait:",
        "neg_traits": "Now select a negative trait:",
        "hobby": "Question 7: Interests & Hobbies\n\nSelect one of the 5 hobbies you like to do together:",
        "generating": "🎨 Generating your friend's cinematic portrait... Please wait a moment.",
        "result": "🎉 Your ideal friend's profile is ready!",
        "error": "❌ Sorry, an error occurred while generating the image. Please try again later.",
        "restart": "Type /start to begin again.",
    },
    "uz": {
        "start": "Salom! Men sizga ideal do'stingizning vizual va xarakter profilini yaratishda yordam beraman.\n\n1-savol (Davlatni tanlang):\nPastdagi tugmalardan birini tanlang:",
        "gender": "2-savol (Jinsini tanlang):\nDo'stingizning jinsi qanday?",
        "name": "3-savol (Ismini kiriting):\nDo'stingizning ismini matn ko'rinishida yozib yuboring (Masalan: Hasan, Amelia, Rayan).",
        "age": "4-savol (Yoshini tanlang):\nDo'stingiz necha yoshda?",
        "appearance": "5-savol (Tashqi ko'rinishini tanlang):\n\nSoch rangi:",
        "eye_color": "Ko'z rangi:",
        "face_shape": "Yuz shakli:",
        "pos_traits": "6-savol: Do'stning xarakteri\n\nIjobiy sifatni tanlang:",
        "neg_traits": "Endi salbiy sifatni tanlang:",
        "hobby": "7-savol: Qiziqishlar va xobbilar\n\nDo'stingiz bilan birga qilishni yoqtiradigan 5 ta qiziqishdan birini tanlang:",
        "generating": "🎨 Do'stingizning kinematografik portreti yaratilmoqda... Iltimos, biroz kuting.",
        "result": "🎉 Sizning ideal do'stingiz profili tayyor!",
        "error": "❌ Kechirasiz, rasm yaratishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.",
        "restart": "Qaytadan boshlash uchun /start buyrug'ini bosing.",
    },
    "tr": {
        "start": "Merhaba! İdeal arkadaşınızın görsel ve karakter profilini oluşturmanıza yardımcı olacağım.\n\nSoru 1 (Ülke Seçin):\nAşağıdaki düğmelerden birini seçin:",
        "gender": "Soru 2 (Cinsiyet Seçin):\nArkadaşınızın cinsiyeti nedir?",
        "name": "Soru 3 (İsim Girin):\nArkadaşınızın adını metin olarak yazın (Örn: Hasan, Amelia, Rayan).",
        "age": "Soru 4 (Yaş Seçin):\nArkadaşınız kaç yaşında?",
        "appearance": "Soru 5 (Dış Görünüm Seçin):\n\nSaç rengi:",
        "eye_color": "Göz rengi:",
        "face_shape": "Yüz şekli:",
        "pos_traits": "Soru 6: Kişilik\n\nOlumlu bir özellik seçin:",
        "neg_traits": "Şimdi olumsuz bir özellik seçin:",
        "hobby": "Soru 7: İlgi Alanları ve Hobiler\n\nBirlikte yapmayı sevdiğiniz 5 hobiden birini seçin:",
        "generating": "🎨 Arkadaşınızın sinematik portresi oluşturuluyor... Lütfen bekleyin.",
        "result": "🎉 İdeal arkadaşınızın profili hazır!",
        "error": "❌ Üzgünüm, görsel oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
        "restart": "Yeniden başlamak için /start komutunu yazın.",
    },
    "ko": {
        "start": "안녕하세요! 이상적인 친구의 시각적, 성격 프로필을 만드는 것을 도와드리겠습니다.\n\n질문 1 (국가 선택):\n아래 버튼 중 하나를 선택하세요:",
        "gender": "질문 2 (성별 선택):\n친구의 성별은 무엇인가요?",
        "name": "질문 3 (이름 입력):\n친구의 이름을 텍스트로 입력하세요 (예: Hasan, Amelia, Rayan).",
        "age": "질문 4 (나이 선택):\n친구는 몇 살인가요?",
        "appearance": "질문 5 (외모 선택):\n\n머리색:",
        "eye_color": "눈색:",
        "face_shape": "얼굴형:",
        "pos_traits": "질문 6: 성격\n\n긍정적인 특성을 선택하세요:",
        "neg_traits": "이제 부정적인 특성을 선택하세요:",
        "hobby": "질문 7: 관심사 및 취미\n\n함께 하고 싶은 5가지 취미 중 하나를 선택하세요:",
        "generating": "🎨 친구의 시네마틱 초상화를 생성 중입니다... 잠시만 기다려 주세요.",
        "result": "🎉 이상적인 친구 프로필이 준비되었습니다!",
        "error": "❌ 죄송합니다. 이미지 생성 중 오류가 발생했습니다. 나중에 다시 시도해 주세요.",
        "restart": "다시 시작하려면 /start를 입력하세요.",
    },
    "ja": {
        "start": "こんにちは！理想の友達の見た目と性格のプロフィール作成をお手伝いします。\n\n質問1（国を選択）：\n以下のボタンから1つ選んでください：",
        "gender": "質問2（性別を選択）：\n友達の性別は？",
        "name": "質問3（名前を入力）：\n友達の名前をテキストで入力してください（例：Hasan, Amelia, Rayan）。",
        "age": "質問4（年齢を選択）：\n友達は何歳ですか？",
        "appearance": "質問5（外見を選択）：\n\n髪の色：",
        "eye_color": "目の色：",
        "face_shape": "顔の形：",
        "pos_traits": "質問6：性格\n\nポジティブな特徴を選択してください：",
        "neg_traits": "次にネガティブな特徴を選択してください：",
        "hobby": "質問7：興味と趣味\n\n一緒にしたい5つの趣味から1つ選択してください：",
        "generating": "🎨 友達のシネマティックな肖像を生成しています... 少々お待ちください。",
        "result": "🎉 理想の友達のプロフィールが完成しました！",
        "error": "❌ 申し訳ありません。画像の生成中にエラーが発生しました。後でもう一度お試しください。",
        "restart": "もう一度開始するには /start と入力してください。",
    }
}

COUNTRY_TO_LANG = {
    "🇺🇿 Uzbekistan": "uz",
    "🇰🇷 South Korea": "ko",
    "🇺🇸 USA": "en",
    "🇬🇧 United Kingdom": "en",
    "🇯🇵 Japan": "ja",
    "🇹🇷 Turkey": "tr",
}

COUNTRY_TO_EN = {
    "🇺🇿 Uzbekistan": "Uzbekistan",
    "🇰🇷 South Korea": "South Korea",
    "🇺🇸 USA": "the United States",
    "🇬🇧 United Kingdom": "the United Kingdom",
    "🇯🇵 Japan": "Japan",
    "🇹🇷 Turkey": "Turkey",
}

# ==================== FSM HOLATLAR ====================
class FriendForm(StatesGroup):
    country = State()
    gender = State()
    name = State()
    age = State()
    hair_color = State()
    eye_color = State()
    face_shape = State()
    positive_traits = State()
    negative_traits = State()
    hobby = State()

# ==================== KLAVIATURALAR ====================
def get_country_kb():
    kb = ReplyKeyboardBuilder()
    for country in COUNTRY_TO_LANG.keys():
        kb.button(text=country)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_gender_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["👦 O'g'il bola", "👧 Qiz bola"],
        "tr": ["👦 Erkek", "👧 Kız"],
        "ko": ["👦 남자", "👧 여자"],
        "ja": ["👦 男の子", "👧 女の子"],
        "en": ["👦 Boy", "👧 Girl"],
    }.get(lang, ["👦 Boy", "👧 Girl"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_age_kb(lang):
    kb = ReplyKeyboardBuilder()
    for age in ["15", "16", "17", "18"]:
        suffix = {
            "uz": "yosh", "tr": "yaş", "ko": "살", "ja": "歳", "en": "years old"
        }.get(lang, "years old")
        kb.button(text=f"{age} {suffix}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_hair_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["Qora", "Jigarrang", "Sariq/Seryoqu"],
        "tr": ["Siyah", "Kahverengi", "Sarı"],
        "ko": ["검은색", "갈색", "금발"],
        "ja": ["黒", "茶色", "金髪"],
        "en": ["Black", "Brown", "Blonde"],
    }.get(lang, ["Black", "Brown", "Blonde"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_eye_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["Qora", "Jigarrang", "Yashil/Moviy"],
        "tr": ["Siyah", "Kahverengi", "Yeşil/Mavi"],
        "ko": ["검은색", "갈색", "녹색/파란색"],
        "ja": ["黒", "茶色", "緑/青"],
        "en": ["Black", "Brown", "Green/Blue"],
    }.get(lang, ["Black", "Brown", "Green/Blue"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_face_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["Oval", "Doira", "To'rtburchak"],
        "tr": ["Oval", "Yuvarlak", "Kare"],
        "ko": ["타원형", "둥근형", "사각형"],
        "ja": ["卵型", "丸型", "四角形"],
        "en": ["Oval", "Round", "Square"],
    }.get(lang, ["Oval", "Round", "Square"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_positive_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["🌟 Outgoing (Kirishimli)", "🤝 Loyal (Sadoqatli)", "⏳ Patient (Sabrli)"],
        "tr": ["🌟 Dışa dönük", "🤝 Sadık", "⏳ Sabırlı"],
        "ko": ["🌟 외향적인", "🤝 충성스러운", "⏳ 인내심 있는"],
        "ja": ["🌟 社交的", "🤝 忠実な", "⏳ 忍耐強い"],
        "en": ["🌟 Outgoing", "🤝 Loyal", "⏳ Patient"],
    }.get(lang, ["🌟 Outgoing", "🤝 Loyal", "⏳ Patient"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_negative_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": ["😠 Impatient (Be-sabr)", "😕 Dishonest (Yolg'onchi)", "🌀 Disorganized (Tartibsiz)"],
        "tr": ["😠 Sabırsız", "😕 Dürüst olmayan", "🌀 Düzensiz"],
        "ko": ["😠 성급한", "😕 부정직한", "🌀 무질서한"],
        "ja": ["😠 短気な", "😕 不誠実な", "🌀 だらしない"],
        "en": ["😠 Impatient", "😕 Dishonest", "🌀 Disorganized"],
    }.get(lang, ["😠 Impatient", "😕 Dishonest", "🌀 Disorganized"])
    for t in texts:
        kb.button(text=t)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_hobby_kb(lang):
    kb = ReplyKeyboardBuilder()
    texts = {
        "uz": [
            "⚽ Playing football (Futbol)",
            "🎬 Watching movies (Kino)",
            "🎮 Playing video games (O'yin)",
            "🎧 Listening to music (Musiqa)",
            "📚 Reading books (Kitob)",
        ],
        "tr": [
            "⚽ Futbol oynamak",
            "🎬 Film izlemek",
            "🎮 Video oyunları oynamak",
            "🎧 Müzik dinlemek",
            "📚 Kitap okumak",
        ],
        "ko": [
            "⚽ 축구하기",
            "🎬 영화 보기",
            "🎮 비디오 게임하기",
            "🎧 음악 듣기",
            "📚 책 읽기",
        ],
        "ja": [
            "⚽ サッカー",
            "🎬 映画鑑賞",
            "🎮 ゲーム",
            "🎧 音楽鑑賞",
            "📚 読書",
        ],
        "en": [
            "⚽ Playing football",
            "🎬 Watching movies",
            "🎮 Playing video games",
            "🎧 Listening to music",
            "📚 Reading books",
        ],
    }.get(lang, [
        "⚽ Playing football",
        "🎬 Watching movies",
        "🎮 Playing video games",
        "🎧 Listening to music",
        "📚 Reading books",
    ])
    for t in texts:
        kb.button(text=t)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

# ==================== YORDAMCHI FUNKSIYALAR ====================
def normalize_gender(gender_text: str) -> str:
    gender_text = gender_text.lower()
    male_markers = ["o'g'il", "og'il", "erkek", "남자", "男女の子", "boy", "male"]
    for m in male_markers:
        if m in gender_text:
            return "boy"
    return "girl"

def normalize_age(age_text: str) -> str:
    for token in age_text.split():
        if token.isdigit():
            return token
    return "16"

def translate_trait_to_en(trait: str) -> str:
    mapping = {
        "outgoing": "outgoing and sociable", "kirishimli": "outgoing and sociable",
        "dışa dönük": "outgoing and sociable", "외향적인": "outgoing and sociable",
        "社交的": "outgoing and sociable",
        "loyal": "loyal and trustworthy", "sadoqatli": "loyal and trustworthy",
        "sadık": "loyal and trustworthy", "충성스러운": "loyal and trustworthy",
        "忠実な": "loyal and trustworthy",
        "patient": "patient and calm", "sabrli": "patient and calm",
        "sabırlı": "patient and calm", "인내심 있는": "patient and calm",
        "忍耐強い": "patient and calm",
        "impatient": "impatient", "be-sabr": "impatient", "sabırsız": "impatient",
        "성급한": "impatient", "短気な": "impatient",
        "dishonest": "dishonest", "yolg'onchi": "dishonest",
        "dürüst olmayan": "dishonest", "부정직한": "dishonest", "不誠実な": "dishonest",
        "disorganized": "disorganized", "tartibsiz": "disorganized",
        "düzensiz": "disorganized", "무질서한": "disorganized", "だらしない": "disorganized",
    }
    t_lower = trait.lower()
    for key, value in mapping.items():
        if key in t_lower:
            return value
    return trait.split("(")[0].strip()

def translate_hobby_to_en(hobby: str) -> str:
    mapping = {
        "futbol": "playing football", "football": "playing football",
        "futbol oynamak": "playing football", "축구": "playing football", "サッカー": "playing football",
        "kino": "watching movies", "movies": "watching movies",
        "film izlemek": "watching movies", "영화": "watching movies", "映画": "watching movies",
        "o'yin": "playing video games", "video games": "playing video games",
        "video oyunları": "playing video games", "비디오 게임": "playing video games", "ゲーム": "playing video games",
        "musiqa": "listening to music", "music": "listening to music",
        "müzik": "listening to music", "음악": "listening to music", "音楽": "listening to music",
        "kitob": "reading books", "books": "reading books",
        "kitap": "reading books", "책": "reading books", "読書": "reading books",
    }
    h_lower = hobby.lower()
    for key, value in mapping.items():
        if key in h_lower:
            return value
    return hobby

def translate_color_to_en(color: str) -> str:
    mapping = {
        "qora": "black", "black": "black",
        "jigarrang": "brown", "brown": "brown", "kahverengi": "brown",
        "sariq": "blonde", "seryoqu": "blonde", "blonde": "blonde",
        "sarı": "blonde", "검은색": "black", "갈색": "brown", "금발": "blonde",
        "黒": "black", "茶色": "brown", "金髪": "blonde",
        "yashil": "green", "moviy": "blue", "green/blue": "green/blue",
        "yeşil/mavi": "green/blue", "녹색/파란색": "green/blue",
        "緑/青": "green/blue", "green": "green", "blue": "blue",
    }
    c_lower = color.lower()
    for key, value in mapping.items():
        if key in c_lower:
            return value
    return color

def translate_face_to_en(face: str) -> str:
    mapping = {
        "oval": "oval", "doira": "round", "round": "round",
        "to'rtburchak": "square", "square": "square",
        "yuvarlak": "round", "kare": "square",
        "타원형": "oval", "둥근형": "round", "사각형": "square",
        "卵型": "oval", "丸型": "round", "四角形": "square",
    }
    f_lower = face.lower()
    for key, value in mapping.items():
        if key in f_lower:
            return value
    return face

def create_cinematic_prompt(data: dict) -> str:
    country_en = COUNTRY_TO_EN.get(data.get("country", ""), "the world")
    gender_en = normalize_gender(data.get("gender", ""))
    age_num = normalize_age(data.get("age", ""))
    hair_en = translate_color_to_en(data.get("hair", ""))
    eye_en = translate_color_to_en(data.get("eye", ""))
    face_en = translate_face_to_en(data.get("face", ""))

    pos_en = ", ".join(translate_trait_to_en(t) for t in data.get("pos_traits", []))
    neg_en = ", ".join(translate_trait_to_en(t) for t in data.get("neg_traits", []))
    hobby_en = translate_hobby_to_en(data.get("hobby", ""))

    prompt = (
        f"Ultra-realistic cinematic portrait of a {age_num}-year-old {gender_en} from {country_en}. "
        f"Physical appearance: {hair_en} hair, {eye_en} eyes, {face_en} face shape, "
        f"natural skin texture with realistic details, expressive and friendly eyes. "
        f"Personality visible in the expression: {pos_en}, but sometimes {neg_en}. "
        f"The person loves {hobby_en}. "
        f"Shot on 85mm lens, f/1.8 aperture, golden hour lighting, soft rim light, "
        f"shallow depth of field, blurred background, warm and welcoming atmosphere. "
        f"Professional color grading, film grain, Kodak Portra 400 style, "
        f"photorealistic, 8k resolution, highly detailed, cinematic composition, "
        f"dramatic yet soft lighting, masterpiece quality."
    )
    return prompt

async def generate_image_with_pollinations(prompt: str) -> bytes | None:
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        loop = asyncio.get_event_loop()
        def fetch_url():
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.read()

        return await loop.run_in_executor(None, fetch_url)
    except Exception as e:
        logger.error("Pollinations xatoligi: %s", e)
        return None

# ==================== HANDLERLAR ====================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(lang="en")
    await message.answer(LANG["en"]["start"], reply_markup=get_country_kb())
    await state.set_state(FriendForm.country)

@dp.message(FriendForm.country)
async def process_country(message: types.Message, state: FSMContext):
    selected = message.text
    if selected not in COUNTRY_TO_LANG:
        await message.answer("Please select a country from the buttons.")
        return
    lang = COUNTRY_TO_LANG[selected]
    await state.update_data(country=selected, lang=lang)
    await message.answer(LANG[lang]["gender"], reply_markup=get_gender_kb(lang))
    await state.set_state(FriendForm.gender)

@dp.message(FriendForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(gender=message.text)
    await message.answer(LANG[lang]["name"], reply_markup=ReplyKeyboardRemove())
    await state.set_state(FriendForm.name)

@dp.message(FriendForm.name)
async def process_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(name=message.text)
    await message.answer(LANG[lang]["age"], reply_markup=get_age_kb(lang))
    await state.set_state(FriendForm.age)

@dp.message(FriendForm.age)
async def process_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(age=message.text)
    await message.answer(LANG[lang]["appearance"], reply_markup=get_hair_kb(lang))
    await state.set_state(FriendForm.hair_color)

@dp.message(FriendForm.hair_color)
async def process_hair(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(hair=message.text)
    await message.answer(LANG[lang]["eye_color"], reply_markup=get_eye_kb(lang))
    await state.set_state(FriendForm.eye_color)

@dp.message(FriendForm.eye_color)
async def process_eye(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(eye=message.text)
    await message.answer(LANG[lang]["face_shape"], reply_markup=get_face_kb(lang))
    await state.set_state(FriendForm.face_shape)

@dp.message(FriendForm.face_shape)
async def process_face(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(face=message.text, pos_traits=[], neg_traits=[])
    await message.answer(LANG[lang]["pos_traits"], reply_markup=get_positive_kb(lang))
    await state.set_state(FriendForm.positive_traits)

@dp.message(FriendForm.positive_traits)
async def process_pos_traits(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    
    # 1 ta ijobiy sifat saqlanadi
    await state.update_data(pos_traits=[message.text])

    # Birdan salbiy sifatni so'rashga o'tiladi
    await message.answer(LANG[lang]["neg_traits"], reply_markup=get_negative_kb(lang))
    await state.set_state(FriendForm.negative_traits)

@dp.message(FriendForm.negative_traits)
async def process_neg_traits(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    
    # 1 ta salbiy sifat saqlanadi
    await state.update_data(neg_traits=[message.text])

    # Birdan hobby bo'limiga o'tiladi
    await message.answer(LANG[lang]["hobby"], reply_markup=get_hobby_kb(lang))
    await state.set_state(FriendForm.hobby)

@dp.message(FriendForm.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    await state.update_data(hobby=message.text)

    data = await state.get_data()

    result_text = (
        f"{LANG[lang]['result']}\n\n"
        f"🌍 Country: {data.get('country')}\n"
        f"👤 Gender: {data.get('gender')}\n"
        f"📛 Name: {data.get('name')}\n"
        f"🎂 Age: {data.get('age')}\n"
        f"💇 Hair: {data.get('hair')}\n"
        f"👁 Eyes: {data.get('eye')}\n"
        f"😐 Face: {data.get('face')}\n"
        f"✅ Positive: {', '.join(data.get('pos_traits', []))}\n"
        f"❌ Negative: {', '.join(data.get('neg_traits', []))}\n"
        f"🎯 Hobby: {data.get('hobby')}"
    )
    await message.answer(result_text, reply_markup=ReplyKeyboardRemove())
    await message.answer(LANG[lang]["generating"])

    prompt = create_cinematic_prompt(data)
    logger.info("Prompt: %s", prompt)

    image_bytes = await generate_image_with_pollinations(prompt)

    if image_bytes:
        photo = BufferedInputFile(image_bytes, filename="friend_portrait.png")
        await message.answer_photo(
            photo=photo,
            caption=f"🎨 {data.get('name')} — {LANG[lang]['result']}"
        )
    else:
        await message.answer(LANG[lang]["error"])

    await state.clear()
    await message.answer(LANG[lang]["restart"])

# ==================== ISHGA TUSHIRISH ====================
async def main():
    logger.info("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
