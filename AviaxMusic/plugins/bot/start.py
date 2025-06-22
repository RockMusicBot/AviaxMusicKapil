@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # SAFER: Split only once, get the argument safely
    parts = message.text.strip().split(None, 1)
    if len(parts) > 1:
        name = parts[1].strip().lower()

        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                protect_content=True,
                reply_markup=keyboard,
            )

        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} just started the bot to check <b>sudo list</b>.\n\n<b>User ID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
                )
            return

        elif name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} just started the bot to check <b>track information</b>.\n\n<b>User ID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
                )

    else:
        # No argument: normal start
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(
                message.from_user.mention, app.mention, UP, DISK, CPU, RAM
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"{message.from_user.mention} just started the bot.\n\n<b>User ID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
            )
