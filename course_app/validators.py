import re
from rest_framework.serializers import ValidationError


class VideoUrlValidator:

    def __init__(self, fields):
        self.fields = fields
        self.message = 'Поле содержит недопустимые ссылки.'

    def __call__(self, data):
        for field in self.fields:
            value = data.get(field)
            if value is not None:
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+',
                                   value)
                if any('youtube.com' not in link for link in links):
                    raise ValidationError(self.message)
