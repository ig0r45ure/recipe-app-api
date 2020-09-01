from django.test import TestCase

from core.models import OrgUnit


class ImportCSVTests(TestCase):

    def test_org_unit_str(self):
        """Test the Organizational Unit string representation"""
        org_unit = OrgUnit.objects.create(
            name='Departament Kontrolingu',
            acronym='DKK'
        )

        self.assertEqual(str(org_unit), org_unit.name)

    def test_org_unit_with_null_str(self):
        """Test the Organizational Unit without acronym string"""
        org_unit = OrgUnit.objects.create(
            name='Prezes Zakładu',
        )

        self.assertEqual(str(org_unit), org_unit.name)
