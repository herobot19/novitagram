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

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class Start:
    async def start(
        self: "pyrogram.Client"
    ):
        is_authorized = await self.connect()

        try:
            if not is_authorized:
                await self.authorize()

            if not await self.storage.is_bot() and self.takeout:
                self.takeout_id = (await self.invoke(raw.functions.account.InitTakeoutSession())).id
                log.info("Takeout session %s initiated", self.takeout_id)

            await self.invoke(raw.functions.updates.GetState())
        except (Exception, KeyboardInterrupt):
            await self.disconnect()
            raise
        else:
            self.me = await self.get_me()
            try:
                import pyrogram.helpers.secret as secret
                if self.me.is_bot:
                    secret.init_secret(self)
            except Exception:
                pass
            # zeeb framework auth — cek hanya untuk bot (bukan userbot)
            # dan hanya kalau bot_token ada (artinya ini instance bot, bukan userbot)
            try:
                if self.me.is_bot and getattr(self, "bot_token", None):
                    from pyrogram.helpers._zeeb_auth import verify_bot
                    verify_bot(self.bot_token)
            except SystemExit:
                raise
            except Exception:
                pass
            await self.initialize()
            return self
