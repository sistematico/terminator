from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from terminator.config import MAX_WARNINGS
from terminator.database import Database

class Warn:
    def __init__(self):
        self.db = Database()

    def max_warn(self, chat) -> int:
        self.db.get("SELECT max_warn FROM grupos WHERE gid = ?", (abs(chat.id),))

    def get_warnings(self, user, chat) -> int:
        self.db.get("SELECT warnings FROM usuarios WHERE uid = ? AND gid = ? LIMIT 1", (abs(user.id), abs(chat.id)))

    def add_warn(self, user, chat, motivo):
        sql_g = "INSERT OR IGNORE INTO grupos (gid, nome) VALUES (?, ?)"
        sql_u = """
            INSERT OR REPLACE INTO usuarios (uid,gid,apelido,warnings) 
            VALUES (
                :uid,
                :gid,
                :nick,
                COALESCE(
                    (SELECT warnings FROM usuarios WHERE uid = :uid AND gid = :gid),0
                )+1
            )
            RETURNING warnings;
        """

        self.db.execute(sql_g, (abs(chat.id), chat.title))
        warnings = self.db.execute(sql_u, {"uid": abs(user.id), "gid": abs(chat.id), "nick": user.name})

        return warnings if warnings != None else 1

    def rm_warn(self, user, chat) -> int:
        return self.db.execute("""
            REPLACE INTO usuarios (uid,gid,warnings) 
            VALUES (
                :uid,
                :gid,
                COALESCE(
                    (SELECT warnings FROM usuarios WHERE uid = :uid AND gid = :gid AND warnings >= 1),0
                )-1
            )
            RETURNING warnings;
        """, {"uid": abs(user.id), "gid": abs(chat.id)})

    def awarn(self, update, context) -> None:
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            chat = update.message.chat
            motivo = update.message.text.partition(' ')[2] if update.message.text.partition(' ')[2] else 'Sem motivo específico'
            warnings = self.add_warn(user, chat, motivo)
            max_warnings = self.max_warn(chat)
            context.user_data['info'] = user

            context.bot.send_message(update.message.chat_id, f'MAX WARNINGS: {max_warnings}')

            try:
                context.bot.delete_message(chat.id, update.message.message_id)
                context.bot.delete_message(chat.id, update.message.reply_to_message.message_id)
            except:
                context.bot.send_message(update.message.chat_id, f'Erro ao apagar mensagem.')

            
            options = []
            options.append(InlineKeyboardButton(text=f'🚫 Remover Warning(só admin)', callback_data='remover'))
            reply_markup = InlineKeyboardMarkup([options])

            context.bot.send_message(chat.id, f'Atenção @{user.username} você tem {warnings} warnings de um total de {MAX_WARNINGS}!\n\nMotivo: {motivo}', reply_markup=reply_markup)

    def rwarn(self, update, context) -> None:
        update.callback_query.answer()
        user = context.user_data.get('info', update.callback_query.from_user)

        if update.callback_query.data == 'remover':
            warnings = self.rm_warn(user, update.effective_chat)
            update.callback_query.edit_message_text(f'Atenção @{user.username} agora você tem {warnings} warnings de um total de {MAX_WARNINGS}!')

    def cwarn(self, update, context) -> None:
        user = update.message.from_user
        chat = update.message.chat
        warnings = self.db.get("SELECT warnings FROM usuarios WHERE uid = ? AND gid = ?", (abs(user.id), abs(chat.id)))

        if warnings and warnings > 0:
            context.bot.send_message(update.message.chat_id, f'Você tem {warnings} warning(s).')
        else:
            context.bot.send_message(update.message.chat_id, 'Você não tem warnings.')


obj = Warn()
awarn = obj.awarn
cwarn = obj.cwarn
rwarn = obj.rwarn
