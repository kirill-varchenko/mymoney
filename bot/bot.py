import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from models import Account, Currency, Session, Transaction
from pydantic_models import ExpenseModel
from settings import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def check_user(func):
    def helper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id != settings.my_user_id:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Мне нельзя разговаривать с незнакомцами!")
        else:
            return func(update, context)

    return helper


updater = Updater(token=settings.bot_token, use_context=True)

dispatcher = updater.dispatcher

@check_user
def accounts(update: Update, context: CallbackContext):
    with Session() as session:
        accounts = session.query(Account).order_by(Account.id).all()
    lines = ['Счета:']
    lines.extend(f"{account.id:3d}. {account.name} ({account.currency.id})" for account in accounts)
    text = '\n'.join(lines)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@check_user
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{user['first_name']}, привет!")

@check_user
def expense(update: Update, context: CallbackContext):
    fields = ['from_account_id', 'from_amount', 'from_currency_id', 'to_account_id', 'to_amount', 'to_currency_id']
    if not context.args:
        text = 'Формат:\n' + ' '.join(fields)
    else:
        expense = ExpenseModel(**dict(zip(fields, context.args)))
        try:
            with Session() as session:
                transaction = Transaction(**expense.dict())
                session.add(transaction)
                session.commit()
                text = str(expense)
        except:
            logging.exception('Error during expense save')
            text = 'Какая-то ошибка'

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)

expense_handler = CommandHandler('expense', expense)
start_handler = CommandHandler('start', start)
accounts_handler = CommandHandler('accounts', accounts)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(accounts_handler)
dispatcher.add_handler(expense_handler)
updater.start_polling()

updater.idle()
