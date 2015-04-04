from hashlib import algorithms_available
import hashlib

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Robohash(object):
    DEFAULT_SIZE_X = 300
    DEFAULT_SIZE_Y = 300
    DEFAULT_HASH_ALGORITHM = 'md5'
    ALLOWED_FORMATS = ('png', 'jpg', 'bmp')
    ALLOWED_BGSETS = ('any', '1', '2', '3', 'bg1', 'bg2', 'bg3')
    ALLOWED_CREATURE_TYPES = {'robots': 1, 'zombies': 2, 'heads': 3}

    def __init__(self, **kwargs):
        self.size_x = kwargs.get('x', self.DEFAULT_SIZE_X)
        self.size_y = kwargs.get('y', self.DEFAULT_SIZE_Y)
        self.size = kwargs.get('size')
        self.format = kwargs.get('format')
        self.bgset = kwargs.get('bgset')
        self.creature_type = kwargs.get('creature_type')
        self.color = kwargs.get('color')
        self.force_hash = kwargs.get('force_hash', True)
        self.hash_algorithm = kwargs.get('hash_algorithm', 'md5')
        self.use_gravatar = kwargs.get('use_gravatar', False)
        self.gravatar_hashed = kwargs.get('gravatar_hashed', False)

        self.app = kwargs.get('app')
        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.jinja_env.filters.setdefault('robohash', self)
        app.extensions['robohash'] = self

    def __call__(self, text, **kwargs):
        # import pdb;pdb.set_trace()
        bgset = str(kwargs.get('bgset', self.bgset))
        color = kwargs.get('color', self.color)
        creature_type = kwargs.get('creature_type', self.creature_type)
        force_hash = kwargs.get('force_hash', self.force_hash)
        format = kwargs.get('format', self.format)
        gravatar_hashed = kwargs.get('gravatar_hashed', self.gravatar_hashed)
        hash_algorithm = kwargs.get('hash_algorithm', self.hash_algorithm)
        size = '{0}x{1}'.format(kwargs.get('x', self.size_x), kwargs.get('y', self.size_y)) or kwargs.get('size', self.size)
        use_gravatar = kwargs.get('use_gravatar', self.use_gravatar)

        url = 'https://robohash.org/'
        if use_gravatar or gravatar_hashed:
            url += '{0}?'.format(text)
            if gravatar_hashed:
                url += 'gravatar=hashed'
            else:
                url += 'gravatar=yes'
            return url
        elif force_hash and hash_algorithm in algorithms_available:
            hash_func = getattr(hashlib, hash_algorithm)
            text = hash_func(str(text).encode('utf-8')).hexdigest()

        url += '{0}?'.format(text)
        if format in self.ALLOWED_FORMATS:
            param = 'format={0}'.format(format)
            url += param if url.endswith('?') else '&{0}'.format(param)
        if size:
            param = 'size={0}'.format(size)
            url += param if url.endswith('?') else '&{0}'.format(param)
        if bgset in self.ALLOWED_BGSETS:
            param = 'bgset={0}'.format('bg{0}'.format(bgset) if bgset.isdigit() else bgset)
            url += param if url.endswith('?') else '&{0}'.format(param)
        if creature_type in self.ALLOWED_CREATURE_TYPES or creature_type in self.ALLOWED_CREATURE_TYPES.values():
            param = 'set={0}'.format(self.ALLOWED_CREATURE_TYPES[creature_type] if creature_type in self.ALLOWED_CREATURE_TYPES else creature_type)
            url += param if url.endswith('?') else '&{0}'.format(param)
        if color:
            param = 'color={0}'.format(color)
            url += param if url.endswith('?') else '&{0}'.format(param)
        return url
