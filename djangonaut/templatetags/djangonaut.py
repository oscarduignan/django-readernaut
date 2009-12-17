from django.template import Library, Node, TemplateSyntaxError, Variable
from django.core.exceptions import ImproperlyConfigured
from xml.etree import ElementTree as ET
import urllib2

try:
    import readernaut
except ImportError:
    raise ImproperlyConfigured("djangonaut depends on the pyreadernaut library")


def parse_tag(token, options):
    """
    Parses a template tag.

    Arguments:
        token   - template tag token string
        options - a dict of the options your tag accepts and their defaults.

    >>> token = 'get_rating for post.author as author_rating'
    >>> parse_tag(token, {'for': None, 'as': 'object_rating'})
    {'as': 'author_rating', 'tag_name': 'get_rating', 'for': 'post.author'}

    """
    bits = token.split(' ')
    bits_len = len(bits)
    options['tag_name'] = bits.pop(0)
    for index, bit in enumerate(bits):
        bit = bit.strip()
        if bit in options:
            if bits_len != index-1:
                options[bit] = bits[index+1]
    return options


class BooksNode(Node):
    def __init__(self, username, var_name, category='""', order_by='"created"'):
        self.username = Variable(username)
        self.category = Variable(category)
        self.order_by = Variable(order_by)
        self.var_name = var_name

    def render(self, context):
        username = self.username.resolve(context)
        category = self.category.resolve(context)
        data = {'order': self.order_by.resolve(context)}
        context[self.var_name] = readernaut.get_books(username, category, data)
        return ''


def do_get_books(parser, token):
    """
    Wraps pyreadernaut get_books function.

    (all books)
    {% get_books for "username" as book_list %}

    (only books they are reading, with last modified first)
    {% get_books for "username" from "reading" order "-modified" as book_list %}

    """
    tag_options = {'as': None, 'for': None, 'from': '""', 'order': '"created"'}
    tag = parse_tag(token.contents, tag_options)
    if not tag['as'] or not tag['for']:
        raise TemplateSyntaxError("Incorrect syntax for 'get_books' tag. "
                                  "Basic usage: {% get_books for \"username\" "
                                  "as book_list %}.")
    return BooksNode(tag['for'], tag['as'], tag['from'], tag['order'])


register = Library()
register.tag('get_books', do_get_books)
