import hashlib
from unittest import mock, TestCase

from flask import Flask, render_template_string
from flask_robohash import Robohash


class RoboHashTests(TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.logger.disabled = True
        self.app = app

    def tearDown(self):
        self.app = None

    @mock.patch('flask_robohash.Robohash.init_app')
    def test_default_settings(self, patched_init_app):
        rb = Robohash()
        self.assertEqual(rb.size_x, Robohash.DEFAULT_SIZE_X)
        self.assertEqual(rb.size_y, Robohash.DEFAULT_SIZE_Y)
        self.assertIsNone(rb.size)
        self.assertIsNone(rb.format)
        self.assertIsNone(rb.bgset)
        self.assertIsNone(rb.creature_type)
        self.assertIsNone(rb.color)
        self.assertTrue(rb.force_hash)
        self.assertEqual(rb.hash_algorithm, Robohash.DEFAULT_HASH_ALGORITHM)
        self.assertFalse(rb.use_gravatar)
        self.assertFalse(rb.gravatar_hashed)
        self.assertIsNone(rb.app)
        self.assertEqual(patched_init_app.call_count, 0)

    @mock.patch('flask_robohash.Robohash.init_app')
    def test_instantantion_with_all_kwargs(self, patched_init_app):
        rb = Robohash(app=self.app, x=200,
                      y=200, size='300x300', format='jpg',
                      bgset=1, creature_type=1, color='red',
                      force_hash=False, hash_algorithm='sha1',
                      use_gravatar=True, gravatar_hashed=True
                      )
        self.assertEqual(rb.size_x, 200)
        self.assertEqual(rb.size_y, 200)
        self.assertEqual(rb.size, '300x300')
        self.assertEqual(rb.format, 'jpg')
        self.assertEqual(rb.bgset, 1)
        self.assertEqual(rb.creature_type, 1)
        self.assertEqual(rb.color, 'red')
        self.assertFalse(rb.force_hash)
        self.assertEqual(rb.hash_algorithm, 'sha1')
        self.assertTrue(rb.use_gravatar)
        self.assertTrue(rb.gravatar_hashed)
        self.assertEqual(rb.app, self.app)
        patched_init_app.assert_called_with(self.app)

    def test_call_with_only_text(self):
        rb = Robohash()
        hashed = hashlib.md5('123'.encode('utf-8')).hexdigest()
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format(hashed))

    def test_call_prioritizes_size_x_and_size_y_over_size(self):
        rb = Robohash(x=200, y=200, size='300x300', force_hash=False)
        self.assertEqual(rb('123'), 'https://robohash.org/123?size=200x200')

    def test_call_with_gravatar_kwargs(self):
        rb = Robohash(gravatar_hashed=True, use_gravatar=True)
        hashed = hashlib.md5('123'.encode('utf-8')).hexdigest()
        self.assertEqual(rb(hashed), 'https://robohash.org/{0}?gravatar=hashed'.format(hashed))

        rb.gravatar_hashed = False
        self.assertEqual(rb('anton.synd.antonov@gmail.com'), 'https://robohash.org/{0}?gravatar=yes'.format('anton.synd.antonov@gmail.com'))

    def test_call_with_specific_hash_algorithm(self):
        rb = Robohash(hash_algorithm='sha256')
        hashed = hashlib.sha256('123'.encode('utf-8')).hexdigest()
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format(hashed))

    def test_call_with_non_supported_by_python_hash_algorithm(self):
        rb = Robohash(hash_algorithm='potatorithm')
        self.assertNotIn('potatorithm', hashlib.algorithms_available)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format('123'))

    def test_call_with_allowed_format(self):
        rb = Robohash(format='png', force_hash=False)
        self.assertIn('png', Robohash.ALLOWED_FORMATS)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?format=png&size=300x300'.format('123'))

    def test_call_with_non_allowed_format(self):
        rb = Robohash(format='exe', force_hash=False)
        self.assertNotIn('exe', Robohash.ALLOWED_FORMATS)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format('123'))

    def test_call_with_allowed_bg_set(self):
        rb = Robohash(bgset='any', force_hash=False)
        self.assertIn('any', Robohash.ALLOWED_BGSETS)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300&bgset=any'.format('123'))

    def test_call_with_non_allowed_bg_set(self):
        rb = Robohash(bgset='hollywood', force_hash=False)
        self.assertNotIn('hollywood', Robohash.ALLOWED_BGSETS)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format('123'))

    def test_call_with_allowed_creature_type(self):
        rb = Robohash(creature_type='zombies', force_hash=False)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300&set=2'.format('123'))
        rb.creature_type = 1
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300&set=1'.format('123'))

    def test_call_with_non_allowed_creature_type(self):
        rb = Robohash(creature_type='vampires', force_hash=False)
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format('123'))
        rb.creature_type = 5
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?size=300x300'.format('123'))

    def test_call_with_all_kwargs_except_gravatar_ones(self):
        # Gravatar kwargs end the URL building prematurely without adding the other params.
        # That's intended due to robohash.org not supporting passing params to Gravatar redirects
        rb = Robohash(app=self.app, x=200, y=200, format='jpg',
                      bgset=1, creature_type=1, color='red',
                      force_hash=True, hash_algorithm='sha1'
                      )
        hashed = hashlib.sha1('123'.encode('utf-8')).hexdigest()
        self.assertEqual(rb('123'), 'https://robohash.org/{0}?format=jpg&size=200x200&bgset=bg1&set=1&color=red'.format(hashed))

    def test_call_with_all_kwargs_should_prioritize_gravatar_ones(self):
        rb = Robohash(app=self.app, x=200,
                      y=200, size='300x300', format='jpg',
                      bgset=1, creature_type=1, color='red',
                      force_hash=False, hash_algorithm='sha1',
                      use_gravatar=True, gravatar_hashed=False
                      )
        self.assertEqual(rb('anton.synd.antonov@gmail.com'), 'https://robohash.org/{0}?gravatar=yes'.format('anton.synd.antonov@gmail.com'))

    def test_robohash_filter_without_args(self):
        Robohash(app=self.app, force_hash=False)
        template = '{{ 123 | robohash }}'
        ctx = self.app.test_request_context()
        ctx.push()
        self.assertEqual(render_template_string(template), 'https://robohash.org/123?size=300x300')

    def test_robohash_filter_with_args(self):
        Robohash(app=self.app, force_hash=False)
        template = '{{ 123 | robohash(format=\'png\') }}'
        ctx = self.app.test_request_context()
        ctx.push()
        self.assertEqual(render_template_string(template), 'https://robohash.org/123?format=png&size=300x300')

    def test_robohash_filter_with_all_args_except_gravatar_ones(self):
        Robohash(app=self.app)
        template = '{{ 123 | robohash(format=\'jpg\', x=200, y=200, force_hash=True, hash_algorithm=\'sha1\', bgset=1, creature_type=\'robots\', color=\'red\') }}'
        hashed = hashlib.sha1('123'.encode('utf-8')).hexdigest()
        ctx = self.app.test_request_context()
        ctx.push()
        self.assertEqual(render_template_string(template), 'https://robohash.org/{0}?format=jpg&size=200x200&bgset=bg1&set=1&color=red'.format(hashed))
