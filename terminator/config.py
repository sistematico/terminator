import os
import plotly.figure_factory as ff
import pandas as pd
from terminator.database import Database
from config.definitions import *


class Config:
    def __init__(self):
        self.db = Database()

    def status(self, update, context):
        chat = update.message.chat
        grupo = (chat.title[:10] + '..') if len(chat.title) > 10 else chat.title
        grupo_id = str(abs(chat.id))
        grupo_id = (grupo_id[:10] + '..') if len(grupo_id) > 10 else grupo_id
        image = os.path.join(IMAGES_DIR, 'grupo-' + str(abs(chat.id)) + '.png')
        flags = self.db.many("SELECT welcome,likes,warnings,max_warn FROM grupos WHERE gid = ?", (abs(chat.id),))

        df = pd.DataFrame()

        df['ID'] = [grupo_id]
        df['Grupo'] = [grupo]
        df['Welcome'] = [flags[0]]
        df['Likes'] = [flags[1]]
        df['Warnings'] = [flags[2]]
        df['Max Warnings'] = [flags[3]]

        fig = ff.create_table(df)
        fig.update_layout(autosize=False, width=800, height=150, font_size=15,)
        fig.write_image(image, scale=2.8)

        context.bot.send_photo(update.message.chat_id, open(image, 'rb'))

    def get_flags(self, update, context, flag = 'all'):
        chat = update.message.chat

        if flag == 'all':
            flags = self.db.many(f"SELECT welcome,warnings,likes FROM grupos WHERE gid = ?", (abs(chat.id),))

            if flags:
                update.message.reply_text(
                    'Welcome: ' + str(bool(flags[0])) +
                    '\nWarnings: ' + str(bool(flags[1])) +
                    '\nLikes: ' + str(bool(flags[2]))
                )
        else: 
            flags = self.db.get(f"SELECT {flag} FROM grupos WHERE gid = ?", (abs(chat.id),))
            if flags: 
                update.message.reply_text(flags)

    def set_flags(self, update, *args):
        chat = update.message.chat
        params = args[0].split()
        fields = params[0] + ', gid'
        
        self.db.upsert(
            "grupos", 
            fields, 
            "gid", 
            params[0] + " = ?, nome = ?", 
            "gid = ?", 
            (int(params[1]), abs(chat.id), int(params[1]), chat.title, abs(chat.id))
        )

        update.message.reply_text(f'A flag {params[0]} agora é {params[1]}')


obj = Config()
status = obj.status
get_flags = obj.get_flags
set_flags = obj.set_flags