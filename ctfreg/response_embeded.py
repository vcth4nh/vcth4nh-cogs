from discord import Embed


class GeneralEmbed(Embed):
    # TODO: change fields and values to dict
    def __init__(self, title=None, description=None, color=0xFCBA03, fields: list = None, values: list = None,
                 footer=None, timestamp=None, thumbnail=None):
        super().__init__()
        self.title = title
        self.description = description
        self.color = color
        self.timestamp = timestamp
        if thumbnail is not None:
            self.set_thumbnail(url=thumbnail)
        if footer is not None:
            self.set_footer(text=footer)
        if fields is not None and values is not None:
            n = len(fields)
            if n != len(values):
                print("Error - Unable to send embed: Mismatched field and value array")
                return
            for i in range(n):
                self.add_field(name=fields[i], value=values[i])


class ErrorEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__()

        self.title = kwargs.get('title', 'Error')
        self.description = kwargs.get('description', 'Không thấy j hết...')
        self.color = kwargs.get('color', 0x000000)


class LoadingEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__()

        self.title = kwargs.get('title', 'Đợi chút...')
        self.color = kwargs.get('color', 0xFEE12B)
