
from  telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
def type_cast_args(args:list[str]) -> None:
    return [(int(el) if el.isdecimal() else el)  for el in args]

class Telegram_Context_Adapter:
    """builds the context object"""
    def __init__(self, app: AsyncTeleBot, message: Message):
        self.message = message
        self.app = app
        self.args = message.text.split(" ")[1:]
        self.author = message.from_user.full_name
    async def send(self, *args):
        text = " ".join(args)
        await self.app.reply_to(self.message, text)

class Telegram_Interface:
    """this interface converts whatever api is being used to an api that provides for each function
    a context argument, through which it's possible to obtain any informations relative to the context
    of the message, as well as answer any incoming messages"""
    def __init__(self, app: AsyncTeleBot, decorator):
        self.decorator = decorator
        self.context_adapter = Telegram_Context_Adapter
        self.app = app

    def interface_middleware_decorator(self):
        def decor(f):
            #print("im running")
            @self.decorator(commands=[f.__name__])
            async def f2(ctx, *args):
                

                
                ctx = self.context_adapter(self.app, ctx)
                args = ctx.args
                #args = type_cast_args(args)

                return await f(ctx, *args)
        return decor