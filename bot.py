import telebot
from telebot import types

# 💡 လိုအပ်သည်များကို ဤနေရာတွင် ထည့်ပါ
TOKEN = "9082926169:AAFOnxwX2BfC6P1XfiQFCxAjyzO2oZmVk3g"           # BotFather ကရတဲ့ Bot Token
CHANNEL_USERNAME = "@seriesmoviesplanet007" # ကိုယ့်ရဲ့ Telegram Channel Username

bot = telebot.TeleBot(TOKEN)

# Channel Join ပြီးပြီလား စစ်ဆေးသည့် Function
def check_user_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception as e:
        print(f"Error checking sub: {e}")
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_user_subscription(user_id):
        markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("📢 Channel သို့သွား၍ Join ရန်", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
        btn_check = types.InlineKeyboardButton("🔄 Join ပြီးပါပြီ (စစ်ဆေးရန်)", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.send_message(
            message.chat.id, 
            "⚠️ မင်္ဂလာပါ မိတ်ဆွေ...\n\n"
            f"ဤ Bot အား အသုံးပြုရန် ကျေးဇူးပြု၍ ပထမဦးစွာ ကျွန်ုပ်တို့၏ Channel ({CHANNEL_USERNAME}) ကို Join ပေးပါရန် တောင်းဆိုအပ်ပါသည်။ Join ပြီးပါက 'Join ပြီးပါပြီ' ခလုတ်ကို နှိပ်ပါ။",
            reply_markup=markup
        )
        return

    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    welcome_text = (
        "မင်္ဂလာပါ မိတ်ဆွေ..👋\n"
        "ကျွန်တော်ကတော့ Nasspar's bot ပဲဖြစ်ပါတယ်..🤖\n\n"
        "သင်သိလိုသော အကြောင်းအရာများအား အောက်တွင် ဖော်ပြထားသော ခလုတ်များကို နှိပ်၍ လေ့လာနိုင်ပါတယ် ခင်ဗျာ..✨\n"
        "(သို့မဟုတ်) Ashita No Joe အကြောင်းနှင့် ပတ်သက်သည်များကို စာတိုပေးပို့၍ မေးမြန်းနိုင်ပါသည် 🧠။"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🔵 Ashita No Joe Series အကြောင်း လေ့လာရန်", callback_data="q1")
    btn2 = types.InlineKeyboardButton("🟢 Ashita No Joe အတွက် ငွေပေးချေရန်", callback_data="q2")
    btn3 = types.InlineKeyboardButton("🟡 Nasspar's Premium Channel အကြောင်း", callback_data="q3")
    
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check_sub":
        if check_user_subscription(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Channel ထဲသို့ ရောက်ရှိကြောင်း အတည်ပြုပြီးပါပြီ။")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ ကျေးဇူးပြု၍ Channel ကို အရင် Join ပေးပါခင်ဗျာ။", show_alert=True)
        return

    bot.answer_callback_query(call.id)
    
    if call.data == "q1":
        answer = """Ashita No Joe ခေါ် Tomorrow's Joe က Season အားဖြင့် ၂ ခု ထိ ထွက်ရှိထားပါတယ်။

•Season 1 - Episode 79
•Season 2 - Episode 47
•Total Episode: 126

•Released Date: (1970 - 1981)
•IMDb 8.2/10
•Running Time: Avg 25 min

👑 Member ကြေး ၅၀၀၀ကျပ် (5k)

[⚠️Ashita No Joe Series တစ်ခုတည်း အတွက်သာ ဖြစ်သည်။]"""
        bot.send_message(call.message.chat.id, answer, parse_mode="Markdown")
        
    elif call.data == "q2":
        answer = """Member ကြေးပေးချေရန်..⬇️⬇️

•KBZ Pay:
•Wave Pay:

[⚠️ငွေပေးချေထားသော Screen Short ဓာတ်ပုံများအား Admin Acc များထံ ပေးပို့ပေးပါရန်။❗]

•Owner Acc: @Nazzpar
•Admin Acc: @hikarikeen"""
        bot.send_message(call.message.chat.id, answer, parse_mode="Markdown")
        
    elif call.data == "q3":
        answer = "မရှိသေးပါ။📵"
        bot.send_message(call.message.chat.id, answer, parse_mode="Markdown")

# 🧠 Smart Auto-Reply / AI ပုံစံတူ မေးခွန်းစစ်ဆေးဖြေကြားပေးမည့် Handler
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_smart_chat(message):
    user_id = message.from_user.id
    
    # Channel Join ပြီးမှသာ အသုံးပြုခွင့်ပေးမည်
    if not check_user_subscription(user_id):
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပထမဦးစွာ Channel ကို အရင် Join ပေးပါခင်ဗျာ။ /start ကိုနှိပ်ပြီး Channel Join ပါ။")
        return
        
    text = message.text.lower()
    
    # Typing ပုံစံပြသခြင်း
    bot.send_chat_action(message.chat.id, 'typing')
    
    # မေးလာတဲ့ စာသားအပေါ်မူတည်ပြီး အလိုအလျောက် စမတ်ကျကျ ပြန်မည့် စည်းမျဉ်းများ
    if "joe" in text or "ဂျိုး" in text or "ashita" in text:
        reply = "🥊 Ashita No Joe (Tomorrow's Joe) ဟာ တကယ့်လက်ဝှေ့ anime လက်ရာမြောက်တစ်ခုပါ။ Season ၁ နဲ့ ၂ ပါဝင်ပြီး စုစုပေါင်း Episode 126 ထိ ရှိပါတယ်။ Member ကြေး ၅၀၀၀ ကျပ်နဲ့ ကြည့်ရှုနိုင်ပါတယ်။"
    elif "price" in text or "ဈေး" in text or "ကျပ်" in text or "ငွေ" in text:
        reply = "💰 Member ကြေးကတော့ ၅၀၀၀ ကျပ် (5k) ဖြစ်ပါတယ်။ KBZ Pay / Wave Pay တို့နဲ့ ငွေလွှဲပြီး Owner @Nazzpar ထံ Screenshot ပို့ပေးလို့ရပါတယ်ခင်ဗျာ။"
    elif "admin" in text or "owner" in text or "ဆက်သွယ်" in text:
        reply = "👨‍💻 Channel Owner ကတော့ @Nazzpar ပဲ ဖြစ်ပါတယ်။ ဆက်သွယ်စုံစမ်းလိုတာရှိရင် လွတ်လပ်စွာ မေးမြန်းနိုင်ပါတယ်။"
    elif "hi" in text or "hello" in text or "မင်္ဂလာပါ" in text:
        reply = "မင်္ဂလာပါခင်ဗျာ! Nasspar's Channel မှ ကြိုဆိုပါတယ်။ Ashita No Joe နဲ့ ပတ်သက်ပြီး ဘာများ သိလိုပါသလဲဗျ။"
    else:
        reply = f"🤖 သင့်ရဲ့မေးမြန်းချက်ကို လက်ခံရရှိပါတယ်ခင်ဗျာ။ Ashita No Joe Series သို့မဟုတ် Member ငွေပေးချေမှုအကြောင်း သိလိုပါက ပေးထားသော ခလုတ်များကို နှိပ်၍လည်း ကြည့်ရှုနိုင်ပါတယ်။"
        
    bot.reply_to(message, reply)

bot.infinity_polling()
