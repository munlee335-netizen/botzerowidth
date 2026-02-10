Python 3.13.12 (tags/v3.13.12:1cbe481, Feb  3 2026, 18:22:25) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> from telegram import Update
... from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
... 
... TOKEN = "8077359280:AAESVojz2GUhKbdGyVf8r6SGIqyBBB6RrO4"
... 
... # --- Кодирование ---
... def encode_zero_width(text):
...     binary = text.encode("utf-8")
...     bits = "".join(f"{byte:08b}" for byte in binary)
...     return "".join("\u200B" if bit == "0" else "\u200C" for bit in bits)
... 
... # --- Декодирование ---
... def decode_zero_width(text):
...     bits = ""
...     for char in text:
...         if char == "\u200B":
...             bits += "0"
...         elif char == "\u200C":
...             bits += "1"
... 
...     bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
...     decoded_bytes = bytearray()
... 
...     for byte in bytes_list:
...         if len(byte) == 8:
...             decoded_bytes.append(int(byte, 2))
... 
...     try:
...         return decoded_bytes.decode("utf-8")
...     except:
...         return "Не удалось корректно расшифровать."
... 
... # --- /hide ---
... async def hide(update: Update, context: ContextTypes.DEFAULT_TYPE):
...     if not context.args:
...         await update.message.reply_text("Использование: /hide текст")
...         return

    secret = " ".join(context.args)
    encoded = encode_zero_width(secret)
    await update.message.reply_text(encoded)

# --- /wrap ---
async def wrap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/wrap ", "")

    if "||" not in text:
        await update.message.reply_text("Использование: /wrap видимый текст || секрет")
        return

    visible, secret = text.split("||", 1)
    encoded = encode_zero_width(secret.strip())

    # Вшиваем в конец видимого текста
    wrapped = visible.strip() + encoded

    await update.message.reply_text(wrapped)

# --- /decode ---
async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Ответь этой командой на сообщение для расшифровки.")
        return

    target_text = update.message.reply_to_message.text
    decoded = decode_zero_width(target_text)

    await update.message.reply_text(decoded)

# --- Запуск ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hide", hide))
app.add_handler(CommandHandler("wrap", wrap))
app.add_handler(CommandHandler("decode", decode))

print("Бот запущен...")
app.run_polling()
