from random import choice
from andrebotpy.toxingar import curses
from  telebot.types import Message,User
from telebot.async_telebot import AsyncTeleBot
def type_cast_args(args:list[str]) -> None:
    return [(int(el) if el.isdecimal() else el)  for el in args]



def get_ofense():
    return choice(curses)




class Author:
    def __init__(self, user: User):
        self.name = user.username or user.full_name
    def __repr__(self):
        return self.name

class Telegram_Context_Adapter:
    """builds the context object"""
    def __init__(self, app: AsyncTeleBot, message: Message):
        self.message = message
        self.app = app
        self.args = message.text.split(" ")[1:]
        self.author = Author(message.from_user)
        self.message.author = self.author

    async def send(self, *args):
        #temporary filter for wordlewinners while
        #i dont fix the database
        if args and type(args[0]) == type(dict()):
            nd = dict()
            for name,wins in args[0].items():
                newname = get_ofense() if name != "Andrebot" else name
                while newname in nd:
                    newname = get_ofense()
                nd[newname] = wins
            args = (nd,) + args[1:]



        text = " ".join(map(str, args))
        await self.app.reply_to(self.message, text)


class Telegram_Interface:
    """this interface converts whatever api is being used to an api that provides for each function
    a context argument, through which it's possible to obtain any informations relative to the context
    of the message, as well as answer any incoming messages"""
    def __init__(self, app: AsyncTeleBot, decorator):
        self.decorator = decorator
        self.context_adapter = Telegram_Context_Adapter
        self.app = app
        self.HELP_TEXT = ""

    def interface_middleware_decorator(self):
        def decor(f):
            #print("im running")
            if f.__doc__: self.HELP_TEXT += f.__doc__
            @self.decorator(func = lambda message: message.text.split(" ")[0] == ("/" + f.__name__))
            async def f2(ctx, *args):
                

                
                ctx = self.context_adapter(self.app, ctx)
                args = ctx.args
                #args = type_cast_args(args)

                return await f(ctx, *args)
        return decor