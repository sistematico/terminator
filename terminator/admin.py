import os
from terminator.database import Database
from terminator.config import DB_FILE

class Admin:
    def __init__(self):
        self.db = Database()

    def install(self, update, context):
        self.db.close()

        if os.path.exists('./data/database.db'):        
            try:
                os.remove('./data/database.db')
            except OSError as e:
                print(e)

        try:
            self.db.install()
            context.bot.send_message(update.message.chat_id, f'O banco foi instalado')
        except:
            context.bot.send_message(update.message.chat_id, f'Erro ao instalar banco.')

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