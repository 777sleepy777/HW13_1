import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Email, User
from src.schemas import EmailModel
from src.repository.emails import (
    get_emails,
    get_email,
    create_email,
    remove_email,
    update_email,
)


class TestEmails(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_emails(self):
        emails = [Email(), Email(), Email()]
        user = User()
        self.session.query().filter().offset().limit().all.return_value = emails
        result = await get_emails(skip=0, limit=10, user=user, db=self.session)
        self.assertEqual(result, emails)

    async def test_get_email_found(self):
        email = Email()
        user = User()
        self.session.query().filter().first.return_value = email
        result = await get_email(email_id=1, user=user, db=self.session)
        self.assertEqual(result, email)

    async def test_get_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_email(email_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_email(self):
        body = EmailModel(email='qwe@tre.yy')
        result = await create_email(body=body, user=self.user, db=self.session)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, "id"))


    async def test_remove_email_found(self):
        email = Email()
        self.session.query().filter().first.return_value = email
        result = await remove_email(email_id=1, user=self.user, db=self.session)
        self.assertEqual(result, email)

    async def test_remove_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_email(email_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_email_found(self):
        body = EmailModel(email="test@dfghg.hygf")
        email = Email()
        self.session.query().filter().first.return_value = email
        self.session.commit.return_value = None
        result = await update_email(email_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, email)

    async def test_update_email_not_found(self):
        body = EmailModel(email="test@dfghg.hygf")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_email(email_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
