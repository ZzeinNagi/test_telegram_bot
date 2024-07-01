import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логгирования для отладки и мониторинга
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Список для хранения задач
tasks = []

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}! Я твой бот для управления задачами. Чтобы узнать доступные '
                              f'команды используй /help')

# Обработчик команды /add
def add_task(update: Update, context: CallbackContext) -> None:
    task_description = ' '.join(context.args)
    if task_description:
        # Добавление новой задачи в список
        tasks.append({"description": task_description, "completed": False})
        update.message.reply_text(f'Задача добавлена: {task_description}')
    else:
        update.message.reply_text('Пожалуйста, укажите описание задачи после команды /add.')

# Обработчик команды /list
def list_tasks(update: Update, context: CallbackContext) -> None:
    if tasks:
        message = 'Список задач:\n'
        # Перебор всех задач и формирование сообщения
        for i, task in enumerate(tasks, start=1):
            status = '✅' if task["completed"] else '❌'
            message += f'{i}. {task["description"]} {status}\n'
        update.message.reply_text(message)
    else:
        update.message.reply_text('Список задач пуст.')

# Обработчик команды /done
def done_task(update: Update, context: CallbackContext) -> None:
    try:
        task_index = int(context.args[0]) - 1
        if 0 <= task_index < len(tasks):
            # Отметка задачи как выполненной
            tasks[task_index]["completed"] = True
            update.message.reply_text(f'Задача выполнена: {tasks[task_index]["description"]}')
        else:
            update.message.reply_text('Неверный номер задачи.')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите номер задачи после команды /done.')

# Обработчик команды /help
def help_task(update: Update, context: CallbackContext) -> None:
    help_message = """
    Все доступные команды:
/start - Приветственное сообщение от бота
/add - Добавление задачи
/list - Просмотр списка задач
/done - Отметка выполненных задач
    """
    update.message.reply_text(help_message)

# Главная функция для запуска бота
def main() -> None:
    # Получение токена бота из переменных окружения
    TOKEN = os.getenv('TOKEN')

    # Создание Updater и передача ему токена бота
    updater = Updater(TOKEN, use_context=True)

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_task))
    dispatcher.add_handler(CommandHandler("list", list_tasks))
    dispatcher.add_handler(CommandHandler("done", done_task))
    dispatcher.add_handler(CommandHandler("help", help_task))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запуск главной функции при запуске скрипта
if __name__ == '__main__':
    main()