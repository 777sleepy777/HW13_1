import unittest
from datetime import date, datetime
from unittest.mock import MagicMock

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, Email, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(name="test", surname="surnametest", birthday=datetime.strptime('2020-09-20 00:00:00', '%Y-%m-%d %H:%M:%S'), description="test contact", emails=[1, 2])
        emails = [Email(id=1, email='qwe@tre.yy', user_id=1), Email(id=2, email='qwer@trye.yyy', user_id=1)]
        self.session.query().filter().all.return_value = emails

        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertListEqual(result.emails, emails)
        self.assertTrue(hasattr(result, "id"))


    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(name="test", surname="surnametest", birthday=datetime.strptime('2020-09-20 00:00:00', '%Y-%m-%d %H:%M:%S'), description="test contact", emails=[1, 2])
        emails = [Email(id=1, user_id=1), Email(id=5, user_id=1)]
        contact = Contact(emails=emails)
        self.session.query().filter().first.return_value = contact
        self.session.query().filter().all.return_value = emails
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(name="test", surname="surnametest", birthday=datetime.strptime('2020-09-20 00:00:00', '%Y-%m-%d %H:%M:%S'), description="test contact", emails=[1, 2])
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
