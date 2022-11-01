import os
from terminator.database import Database
from config.definitions import DB_FILE

class Admin:
    def __init__(self):
        self.db = Database()

    def uninstall(self, update, context):
        self.db.close()
        
        if os.path.exists(DB_FILE):        
            try:
                os.remove(DB_FILE)
            except OSError as e:
                print(e)

        context.bot.send_message(update.message.chat_id, f'Banco de dados removido.')

    def install(self, update, context):
        self.db.install()
        context.bot.send_message(update.message.chat_id, f'Banco de dados instalado.')
        
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
install = obj.install
uninstall = obj.uninstall