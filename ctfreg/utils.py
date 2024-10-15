import datetime

from .response_embeded import GeneralEmbed


def parse_ctftime_json(data, creating=False, username=None, password=None):
    start = int(datetime.datetime(int(data['start'][0:4]), int(data['start'][5:7]), int(data['start'][8:10]),
                                  int(data['start'][11:13]), int(data['start'][14:16]),
                                  int(data['start'][17:19])).timestamp())
    end = start + (data['duration']['hours'] + 24 * data['duration']['days']) * 3600
    ctf_fields = ['Time', 'Rating weight']
    ctf_fields_info = [
        'Start: <t:{0}:t> <t:{0}:d> (*<t:{0}:R>*)\nEnd: <t:{1}:t> <t:{1}:d> (*<t:{1}:R>*)'
        .format(str(start), str(end)), data['weight']
    ]

    if creating:
        ctf_fields.insert(0, 'Login')
        if username is not None:
            ctf_fields_info.insert(0, 'Username: ' + username + '\nPassword: ' + password)
        else:
            ctf_fields_info.insert(0, "Đang đợi ai đó /regacc...")

    fmat = data['format']
    if fmat == 'Attack-Defense':
        fmat += ' ⚔'
    elif fmat == 'Hack quest':
        fmat += ' 🌄'
    if data['onsite'] == True:
        fmat += '\nOn-site: ' + data['location']
    if data['restrictions'] != "Open":
        fmat += '\nRestricted (' + data['restrictions'] + ')'
    if fmat == 'Jeopardy':
        fmat = None
    else:
        ctf_fields.append('Format')
        ctf_fields_info.append(fmat)

    if 'discord.gg' in data['description']:
        discord_link = "https://"
        i = data['description'].find('discord.gg')
        c = data['description'][i]
        for j in range(25):
            if c not in '\r\n \t%*^$#@?=':
                discord_link += c
            i += 1
            if i == len(data['description']):
                break
            c = data['description'][i]
        ctf_fields.append('Discord')
        ctf_fields_info.append(discord_link)

    logo = data['logo']
    if len(logo) < 5:
        logo = None

    embed_var = GeneralEmbed(title=data['title'], description=data['url'], fields=ctf_fields,
                             values=ctf_fields_info, footer=data['ctftime_url'], thumbnail=logo, color=0xd50000)
    if creating:
        return data['title'], end + 1209600, embed_var  # archive after 2 weeks
    else:
        return embed_var
