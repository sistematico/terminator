from functools import wraps

def is_me(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if context.bot.get_me().id != update.effective_user.id:
            return func(update, context, *args, **kwargs)
        print("Cannot apply this command to me")
        return
    return wrapped

def group(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
       
        if hasattr(update, 'message'):
            chat_type = update.message.chat.type
        elif hasattr(update, 'effective_chat'):
            chat_type = update.effective_chat.type
        else:
            return

        if chat_type != "supergroup" and chat_type != "group":
            return

        return func(update, context)
    return wrapped

def not_group(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        
        if hasattr(update, 'message'):
            chat_type = update.message.chat.type
        elif hasattr(update, 'effective_chat'):
            chat_type = update.effective_chat.type
        else:
            return

        if chat_type == "supergroup" or chat_type == "group":
            return

        return func(update, context)
    return wrapped

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        for admin in context.bot.get_chat_administrators(update.effective_chat.id):
            if admin.user.id == update.effective_user.id:
                return func(update, context, *args, **kwargs)
        return
    return wrapped