#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from ..object import Object

# Default ButtonStyle — fallback ke None kalau tidak ada
try:
    _DEFAULT_STYLE = enums.ButtonStyle.DEFAULT
except AttributeError:
    _DEFAULT_STYLE = None


class InlineKeyboardButton(Object):
    """One button of an inline keyboard.

    Parameters:
        text (``str``):
            Label text on the button.

        callback_data (``str`` | ``bytes``, *optional*):
            Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes.

        url (``str``, *optional*):
            HTTP url to be opened when button is pressed.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            Web App that will be launched when button is pressed.

        login_url (:obj:`~pyrogram.types.LoginUrl`, *optional*):
            HTTP URL for automatic authorization.

        user_id (``int``, *optional*):
            User id, for links to the user profile.

        switch_inline_query (``str``, *optional*):
            Prompt user to select chat and insert bot username + query.

        switch_inline_query_current_chat (``str``, *optional*):
            Insert bot username + query in current chat's input field.

        callback_game (:obj:`~pyrogram.types.CallbackGame`, *optional*):
            Description of the game that will be launched.

        copy_text (``str``, *optional*):
            A button that copies specified text to clipboard.

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Button color style. PRIMARY=blue, DANGER=red, SUCCESS=green.
    """

    def __init__(
        self,
        text: str,
        callback_data: Union[str, bytes] = None,
        url: str = None,
        web_app: "types.WebAppInfo" = None,
        login_url: "types.LoginUrl" = None,
        user_id: int = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        callback_game: "types.CallbackGame" = None,
        copy_text: Optional[str] = None,
        style: "enums.ButtonStyle" = _DEFAULT_STYLE,
    ):
        super().__init__()

        self.text = str(text)
        self.callback_data = callback_data
        self.url = url
        self.web_app = web_app
        self.login_url = login_url
        self.user_id = user_id
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.copy_text = copy_text
        self.style = style

    def _get_raw_style(self):
        """Convert ButtonStyle enum ke raw.types.KeyboardButtonStyle."""
        try:
            ButtonStyle = enums.ButtonStyle
            KBS = raw.types.KeyboardButtonStyle
            if self.style == ButtonStyle.PRIMARY:
                return KBS(bg_primary=True)
            elif self.style == ButtonStyle.DANGER:
                return KBS(bg_danger=True)
            elif self.style == ButtonStyle.SUCCESS:
                return KBS(bg_success=True)
        except (AttributeError, Exception):
            pass
        return None

    @staticmethod
    def read(b: "raw.base.KeyboardButton"):
        # Parse style dari raw button
        raw_style = getattr(b, "style", None)
        button_style = _DEFAULT_STYLE
        if raw_style is not None:
            try:
                ButtonStyle = enums.ButtonStyle
                if getattr(raw_style, "bg_primary", False):
                    button_style = ButtonStyle.PRIMARY
                elif getattr(raw_style, "bg_danger", False):
                    button_style = ButtonStyle.DANGER
                elif getattr(raw_style, "bg_success", False):
                    button_style = ButtonStyle.SUCCESS
            except (AttributeError, Exception):
                pass

        if isinstance(b, raw.types.KeyboardButtonCallback):
            try:
                data = b.data.decode()
            except UnicodeDecodeError:
                data = b.data
            return InlineKeyboardButton(
                text=b.text,
                callback_data=data,
                style=button_style
            )

        if isinstance(b, raw.types.KeyboardButtonUrl):
            return InlineKeyboardButton(text=b.text, url=b.url)

        if isinstance(b, raw.types.KeyboardButtonUrlAuth):
            return InlineKeyboardButton(text=b.text, login_url=types.LoginUrl.read(b))

        if isinstance(b, raw.types.KeyboardButtonUserProfile):
            return InlineKeyboardButton(text=b.text, user_id=b.user_id)

        if isinstance(b, raw.types.KeyboardButtonSwitchInline):
            if b.same_peer:
                return InlineKeyboardButton(text=b.text, switch_inline_query_current_chat=b.query)
            else:
                return InlineKeyboardButton(text=b.text, switch_inline_query=b.query)

        if isinstance(b, raw.types.KeyboardButtonGame):
            return InlineKeyboardButton(text=b.text, callback_game=types.CallbackGame())

        if isinstance(b, raw.types.KeyboardButtonWebView):
            return InlineKeyboardButton(text=b.text, web_app=types.WebAppInfo(url=b.url))

        if isinstance(b, raw.types.KeyboardButtonCopy):
            return InlineKeyboardButton(text=b.text, copy_text=b.copy_text)

        if isinstance(b, raw.types.KeyboardButton):
            return InlineKeyboardButton(text=b.text)

    async def write(self, client: "pyrogram.Client"):
        if self.callback_data is not None:
            data = bytes(self.callback_data, "utf-8") if isinstance(self.callback_data, str) else self.callback_data
            return raw.types.KeyboardButtonCallback(
                text=self.text,
                data=data,
                style=self._get_raw_style()
            )

        if self.url is not None:
            return raw.types.KeyboardButtonUrl(text=self.text, url=self.url)

        if self.login_url is not None:
            return self.login_url.write(
                text=self.text,
                bot=await client.resolve_peer(self.login_url.bot_username or "self")
            )

        if self.user_id is not None:
            return raw.types.InputKeyboardButtonUserProfile(
                text=self.text,
                user_id=await client.resolve_peer(self.user_id)
            )

        if self.switch_inline_query is not None:
            return raw.types.KeyboardButtonSwitchInline(
                text=self.text,
                query=self.switch_inline_query
            )

        if self.switch_inline_query_current_chat is not None:
            return raw.types.KeyboardButtonSwitchInline(
                text=self.text,
                query=self.switch_inline_query_current_chat,
                same_peer=True
            )

        if self.callback_game is not None:
            return raw.types.KeyboardButtonGame(text=self.text)

        if self.web_app is not None:
            return raw.types.KeyboardButtonWebView(text=self.text, url=self.web_app.url)

        if self.copy_text is not None:
            return raw.types.KeyboardButtonCopy(text=self.text, copy_text=self.copy_text)
