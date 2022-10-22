from telegram.ext import MessageFilter

class FilterAwesome(MessageFilter):
    def filter(self, message):
        return 'prune' in message.text

filter_awesome = FilterAwesome()