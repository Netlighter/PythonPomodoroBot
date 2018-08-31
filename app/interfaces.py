from telegram import (
    ext, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)


class RegexHandler(ext.RegexHandler):
    """Class-based handler for regular expressions."""
    class MarkupType:
        INLINE = 'INLINE'
        REGULAR = 'REGULAR'

    # List of lists of strings (or of dictionaries if markup_type is INLINE)
    # which represents menu matrix.
    markup_keyboard = None
    markup_type = MarkupType.REGULAR
    markup_kwargs = {'resize_keyboard': True}

    # Message text which send to user.
    reply_text = ''

    # The handler which must be executed after current handler execution end.
    chained_handler = None

    def __init__(self, pattern='', *args, **kwargs):
        super().__init__(pattern, callback=self.callback, *args, **kwargs)

    def extend_self(self, update, dispatcher):
        """Extend self with usefull shortcuts."""
        self.update = update
        self.dispatcher = dispatcher
        self.bot = dispatcher.bot
        self.message = update.effective_message
        self.user = update.effective_message.from_user

    def handle_update(self, update, dispatcher):
        """Extend self, handle update, reply message."""
        self.extend_self(update, dispatcher)

        state = super().handle_update(update, dispatcher)
        self.reply_message()
        chained_handler_state = self.run_chained_handler()

        # TODO: Add a HUGE warning.
        # Prefer chained_handler_state.
        # Do not use None as "KEEP_CURRENT_STATE" logic implementation, instead
        # create own constants for this behaviour.
        state = chained_handler_state or state

        return state

    def run_chained_handler(self):
        """
        Run chained handler handle_update with current update and dispatcher
        credentials.
        """
        handler = self.get_chained_handler()
        if handler is not None:
            return handler.handle_update(self.update, self.dispatcher)
        else:
            return None

    def get_chained_handler(self):
        """Return handler object"""
        return self.chained_handler

    def callback(self, bot, update):
        """
        Force main handler logic. Return state.

        'bot' and 'update' arguments are decalred for back compatibility with
        ext.RegularHandler.
        """
        raise NotImplementedError

    # Reply message text etc.

    def reply_message(self):
        """Reply message."""
        self.message.reply_text(
            text=self.get_reply_text(),
            reply_markup=self.get_markup_object())

    def get_reply_text(self):
        """Return reply message text."""
        if self.reply_text == '':
            raise NotImplementedError

        return self.reply_text

    # Markups

    def get_markup_kwargs(self):
        """Get markup keyword arguments."""
        return self.markup_kwargs

    def get_markup(self):
        """Get telegram lib regular markup object."""
        return ReplyKeyboardMarkup(
            self.get_markup_keyboard(), **self.get_markup_kwargs())

    def get_inline_markup(self):
        """Get telegram lib inline markup object."""
        keyboard = []
        for sublist in self.get_markup_keyboard():
            for inline_kwargs in sublist:
                keyboard.append([InlineKeyboardButton(**inline_kwargs)])

        return InlineKeyboardMarkup(keyboard, **self.get_markup_kwargs())

    def get_markup_keyboard(self):
        """Get markup keyboard."""
        return self.markup_keyboard

    def get_markup_object(self):
        """Get markup object depend on declared markup_type."""
        if self.get_markup_keyboard() is None:
            return None

        if self.markup_type == self.MarkupType.INLINE:
            return self.get_inline_markup()
        elif self.markup_type == self.MarkupType.REGULAR:
            return self.get_markup()
        else:
            raise ValueError(f'Wrong markup type defined for {self}')

    #
