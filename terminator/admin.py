from terminator.database import Database

class Admin:
    def __init__(self):
        self.db = Database()

    def flush(self, update, context):
        tabela = update.message.text.partition(' ')[2]
        self.db.flush(tabela)
        context.bot.send_message(update.message.chat_id, f'Tabela {tabela} limpa.')

    def drop(self, update, context):
        tabela = update.message.text.partition(' ')[2]
        self.db.drop(tabela)
        context.bot.send_message(update.message.chat_id, f'Tabela {tabela} apagada.')

obj = Admin()
flush = obj.flush
drop = obj.drop