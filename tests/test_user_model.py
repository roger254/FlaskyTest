import unittest
import time
from app import create_app, db
from app.models import User, Permission, AnonymousUser, Role
from datetime import datetime


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='test')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='test')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='test')
        self.assertTrue(u.verify_password('test'))
        self.assertFalse(u.verify_password('test123'))

    def test_password_salts_are_random(self):
        u = User(password='test')
        u2 = User(password='test')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='test123')
        u2 = User(password='test254')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='test254')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_password_token(self):
        u = User(password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'horse'))
        self.assertTrue(u.verify_password('horse'))

    def test_invalid_reset_password_token(self):
        u = User(password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'a', 'test123'))
        self.assertTrue(u.verify_password('test'))

    def test_valid_email_change_token(self):
        u = User(email='test@example.com', password='test123')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('test123@example.com')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'test123@example.com')

    def test_invalid_email_change_token(self):
        u1 = User(email='test@example.com', password='test')
        u2 = User(email='test123@example.com', password='test123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('ken@exmaple.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'test123@example.com')

    def test_user_role(self):
        u = User(email='test@example.com', password='test')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        a = Role.query.filter_by(name='Administrator').first()
        u = User(email='test@example.com', password='test', role=a)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        m = Role.query.filter_by(name='Moderator').first()
        u = User(email='test@example.com', password='test', role=m)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_timestamps(self):
        u = User(password='test')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.member_sice).total_seconds() < 3
        )
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3
        )

    def test_ping(self):
        u = User(password='test')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)
