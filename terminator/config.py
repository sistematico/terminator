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
        grupo = (chat.title[:15] + '..') if len(chat.title) > 15 else chat.title
        image = os.path.join(IMAGES_DIR, 'grupo-' + str(abs(chat.id)) + '.png')

        df = pd.DataFrame()

        df['ID'] = [chat.id]
        df['Grupo'] = [grupo]
        df['Warnings'] = [3]
        df['Flags'] = [111]

        fig = ff.create_table(df)
        fig.update_layout(autosize=False, width=600, height=150, font_size=16,)
        fig.write_image(image, scale=2.8)

        context.bot.send_photo(update.message.chat_id, open(image, 'rb'))

obj = Config()
status = obj.status