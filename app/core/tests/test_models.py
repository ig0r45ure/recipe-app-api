from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import OrgUnit, Process


def sample_process():
    manager = OrgUnit.objects.create(
        name='Prezes Zakładu',
    )
    megaprocess = Process.objects.create(
        name='Zarządzanie Zakładem',
        proc_id='10',
        is_megaprocess=True,
        type='ZARZĄDZANIA',
        owner=manager,
    )
    return Process.objects.create(
        name='Zarządzanie strategiczne',
        proc_id='10.1',
        is_megaprocess=False,
        type='ZARZĄDZANIA',
        owner=OrgUnit.objects.create(
            name='Departament Kontrolingu',
            acronym='DKK'
        ),
        parent=megaprocess,
    )


class ModelTests(TestCase):

    def test_create_user_with_email_succesfull(self):
        """Test creating a new user with an email is succesfull"""
        email = 'testisthebest@test.com'
        password = 'Testpass1230'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for new user is normalized"""
        email = "igor.ziniewicz@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "test1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test1234")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="Testpass1234"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_org_unit_str(self):
        """Test the Organizational Unit string representation"""
        org_unit = OrgUnit.objects.create(
            name='Departament Kontrolingu',
            acronym='DKK'
        )

        self.assertEqual(
            str(org_unit),
            '%s - %s' % (org_unit.name, org_unit.acronym),
        )

    def test_org_unit_with_null_str(self):
        """Test the Organizational Unit without acronym string"""
        org_unit = OrgUnit.objects.create(
            name='Prezes Zakładu',
        )

        self.assertEqual(str(org_unit), org_unit.name)

    def test_process_str(self):
        """Test the process string representation"""
        manager = OrgUnit.objects.create(
            name='Prezes Zakładu',
        )
        megaprocess = Process.objects.create(
            name='Zarządzanie Zakładem',
            proc_id='10',
            is_megaprocess=True,
            type='ZARZĄDZANIA',
            owner=manager,
        )
        process = Process.objects.create(
            name='Zarządzanie strategiczne',
            proc_id='10.1',
            is_megaprocess=False,
            type='ZARZĄDZANIA',
            owner=OrgUnit.objects.create(
                name='Departament Kontrolingu',
                acronym='DKK'
            ),
            parent=megaprocess,
        )

        self.assertEqual(
            str(megaprocess),
            '%s %s' % (megaprocess.proc_id, megaprocess.name),
        )
        self.assertEqual(
            str(process),
            '%s %s' % (process.proc_id, process.name),
        )
