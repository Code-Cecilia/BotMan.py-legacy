def remove_mentions(message: str):
    message_final = message.replace(
        "@everyone", "everyone").replace("@here", "here")
    return message_final
