import json
import os


def get_link(ctx, link_name):
    with open('./assets/global_links.json') as jsonFile:
        links_list_global = json.load(jsonFile)  # getting global links

    if not os.path.exists(f'./links/guild{ctx.guild.id}.json'):
        with open(f'./links/guild{ctx.guild.id}.json', 'w') as writeFile:
            print(f'./links/guild{ctx.guild.id}.json has been created')
            json.dump({}, writeFile)
    with open(f'./links/guild{ctx.guild.id}.json', 'r') as readFile:
        # getting guild-specific links
        guild_specific_links = json.load(readFile)

    # final links list, guild-specific links override global ones
    links_list_global.update(guild_specific_links)

    link_value = links_list_global.get(link_name)
    if link_value is None:
        link_value = "No Value Found\nCheck your spelling and/or capitalization. " \
                     "If this link does not exist, ask the server's administrators to make one."

    return link_value
