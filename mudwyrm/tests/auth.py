import unittest
from pyramid.config import Configurator
from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from mudwyrm.models import initialize_sql, DBSession, transaction
    from mudwyrm.models.auth import User, Group
    from sqlalchemy.exc import IntegrityError
    initialize_sql(create_engine('sqlite://'))
    users_group = Group('users')
    DBSession.add(users_group)
    user = User(name='foo', password='bar', email='foo@bar.com',
                groups=[users_group])
    DBSession.add(user)
    transaction.commit()
    return DBSession
    

class TestLoginView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.db = _initTestingDB()

    def tearDown(self):
        self.db.remove()
        testing.tearDown()

    def test_get(self):
        from mudwyrm.views.auth import login
        request = testing.DummyRequest()
        result = login(request)
        self.assertEqual(result['auth_failed'], False)
    
    def test_wrong_password(self):
        from mudwyrm.views.auth import login
        request = testing.DummyRequest(
            post = dict(
                name = 'foo',
                password = 'wrong password'
            )
        )
        result = login(request)
        self.assertEqual(result['auth_failed'], True)
        
    def test_wrong_user(self):
        from mudwyrm.views.auth import login
        request = testing.DummyRequest(
            post = dict(
                name = 'wrong user',
                password = 'bar'
            )
        )
        result = login(request)
        self.assertEqual(result['auth_failed'], True)
        
    def test_auth_success(self):
        from mudwyrm.views.auth import login
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            params = dict(
                came_from = '/test'
            ),
            post = dict(
                name = 'foo',
                password = 'bar'
            )
        )
        result = login(request)
        self.assertIsInstance(result, HTTPFound)
        self.assertEquals(result.location, '/test')


class TestLogoutView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        
    def test_success(self):
        from mudwyrm.views.auth import logout
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest()
        result = logout(request)
        self.assertIsInstance(result, HTTPFound)
        self.assertEquals(result.location, '/')
 

class TestForbiddenView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        
    def test_authenticated(self):
        from mudwyrm.views.auth import forbidden
        self.config.testing_securitypolicy(userid='foo', permissive=False)
        request = testing.DummyRequest()
        result = forbidden(request)
        self.assertEquals(result, {})
        
    def test_not_authenticated(self):
        from mudwyrm.views.auth import forbidden
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest()
        result = forbidden(request)
        self.assertIsInstance(result, HTTPFound)
        assert result.location.startswith('/login')

class TestRegisterView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.db = _initTestingDB()

    def tearDown(self):
        self.db.remove()
        testing.tearDown()

    def test_get(self):
        from mudwyrm.views.auth import register
        request = testing.DummyRequest()
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].all_errors(), [])

    def test_success(self):
        from mudwyrm.views.auth import register
        from mudwyrm.models import DBSession
        from mudwyrm.models.auth import User, Group
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = 'user',
                password = 'password',
                password_confirmation = 'password',
                email = 'user@server.com'
            )
        )
        request.route_url = lambda r: '/' if r == 'root' else None
        result = register(request)
        self.assertIsInstance(result, HTTPFound)
        self.assertEquals(result.location, request.route_url('root'))
        user = DBSession.query(User).filter(User.name == 'user').first()
        self.assertIsNotNone(user)
        self.assertEquals(user.name, 'user')
        self.assertTrue(user.validate_password('password'))
        self.assertEquals(user.email, 'user@server.com')
        self.assertEquals(user.groups[0].name, 'users')
        
    def test_existing_username(self):
        from mudwyrm.views.auth import register
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = 'foo',
                password = 'password',
                password_confirmation = 'password',
                email = 'user@server.com'
            )
        )
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].errors_for('name'),
                          ['That username is already taken'])

    def test_too_short_password(self):
        from mudwyrm.views.auth import register
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = 'user',
                password = 'pass',
                password_confirmation = 'pass',
                email = 'user@server.com'
            )
        )
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].errors_for('password'),
                          ['Enter a value at least 6 characters long'])
        
    def test_not_matching_passwords(self):
        from mudwyrm.views.auth import register
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = 'user',
                password = 'password',
                password_confirmation = 'different password',
                email = 'user@server.com'
            )
        )
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].errors_for('password_confirmation'),
                          ['Fields do not match'])
        
    def test_empty_name(self):
        from mudwyrm.views.auth import register
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = '',
                password = 'password',
                password_confirmation = 'password',
                email = 'user@server.com'
            )
        )
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].errors_for('name'),
                          ['Please enter a value'])
        
    def test_empty_email(self):
        from mudwyrm.views.auth import register
        from pyramid.httpexceptions import HTTPFound
        request = testing.DummyRequest(
            post = dict(
                name = 'user',
                password = 'password',
                password_confirmation = 'password',
                email = ''
            )
        )
        result = register(request)
        self.assertIn('form', result)
        self.assertEquals(result['form'].errors_for('email'),
                          ['Please enter an email address'])