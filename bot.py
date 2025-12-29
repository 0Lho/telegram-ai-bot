"""
Умный Telegram бот с ИИ (Wikipedia + математика)
Версия для Render.com (24/7)
"""

import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== НАСТРОЙКИ ДЛЯ RENDER ==========
# Токен из переменных окружения Render
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8529839070:AAGnIAZpogj-KDUlsDSZONqPupYgu4U2Yd0")

# Убираем keep_alive - на Render не нужно
# try:
#     from keep_alive import keep_alive
#     keep_alive()
# except:
#     pass

# ========== НАСТРОЙКА ЛОГОВ ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),  # Логи в консоль Render
        logging.FileHandler('bot.log')      # Логи в файл
    ]
)
logger = logging.getLogger(__name__)

# ========== ИМПОРТ ИИ ==========
try:
    from smart_ai import smart_ai
    AI_AVAILABLE = True
    logger.info("✅ Модуль smart_ai загружен успешно")
except Exception as e:
    AI_AVAILABLE = False
    logger.error(f"❌ Ошибка загрузки smart_ai: {e}")

# ========== КОМАНДЫ БОТА ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "🧠 **Умный ИИ-помощник (24/7 на облаке)**\n\n"
        "✨ *Что я умею:*\n"
        "• 🔢 Решать математические задачи\n"
        "• 📚 Искать информацию в Wikipedia\n"
        "• 💡 Давать ответы с источниками\n"
        "• ⚡ Работать всегда онлайн\n\n"
        "**Просто задайте вопрос!**\n\n"
        "*Примеры:*\n"
        "• 'сколько будет 15% от 200'\n"
        "• 'что такое искусственный интеллект'\n"
        "• 'реши уравнение 2x + 5 = 15'",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - проверка работы бота"""
    await update.message.reply_text(
        "✅ *Бот работает нормально!*\n\n"
        "🌐 *Хостинг:* Render.com\n"
        "⏰ *Режим:* 24/7\n"
        "🤖 *AI модуль:* " + ("Активен ✓" if AI_AVAILABLE else "Не доступен ✗"),
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка всех сообщений"""
    try:
        user_text = update.message.text
        logger.info(f"📩 Сообщение от {update.effective_user.id}: {user_text[:50]}...")
        
        if AI_AVAILABLE:
            answer = smart_ai.get_answer(user_text)
        else:
            answer = "🤖 *AI модуль временно недоступен*\n\nПопробуйте позже или используйте команду /start"
        
        # Обрезаем если слишком длинное (Telegram ограничение)
        if len(answer) > 4000:
            answer = answer[:4000] + "\n\n... (сообщение обрезано)"
            
        await update.message.reply_text(answer, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки сообщения: {e}")
        await update.message.reply_text(
            "⚠️ *Произошла ошибка*\n\n"
            "Попробуйте:\n"
            "1. Переформулировать вопрос\n"
            "2. Использовать команду /start\n"
            "3. Подождать 1-2 минуты",
            parse_mode='Markdown'
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    logger.error(f"Ошибка в обработчике: {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text("❌ Внутренняя ошибка бота")

# ========== ЗАПУСК БОТА ==========
def main():
    """Основная функция запуска"""
    print("=" * 50)
    print("🤖 ЗАПУСК TELEGRAM БОТА НА RENDER.COM")
    print(f"🔑 Токен: {TOKEN[:10]}...")
    print("🌐 Режим: Polling (24/7)")
    print("=" * 50)
    
    if not TOKEN or TOKEN == "8529839070:AAGnIAZpogj-KDUlsDSZONqPupYgu4U2Yd0":
        print("⚠️ ВНИМАНИЕ: Используется дефолтный токен!")
        print("⚠️ На Render добавьте переменную TELEGRAM_TOKEN")
    
    try:
        # Создаем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Обработчик ошибок
        app.add_error_handler(error_handler)
        
        print("✅ Бот запущен и слушает сообщения...")
        print("⚡ Работает 24/7 на Render.com")
        print("🔄 Для остановки на Render: остановите сервис")
        
        # Запускаем бота
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
        
    except Exception as e:
        logger.error(f"Критическая ошибка запуска: {e}")
        print(f"❌ Бот упал с ошибкой: {e}")
        print("🔄 Render автоматически перезапустит через несколько секунд")

if __name__ == '__main__':
    main()