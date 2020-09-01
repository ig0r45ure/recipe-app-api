from django.test import TestCase

from core.models import OrgUnit

import csv


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

    def test_opening_csv(self):
        """Test opening CSV-like structure (list object)"""
        csv_list = [
            'Lp,Grupa_usług_IT,Typ_usługi_IT,Lokalizacja_EK,\
            Id_usługi_IT,Kod_aplikacji,Nazwa_usługi_IT,Wersja_usługi_IT,\
            Opis_celu_świadczenia_usługi',
            '1,UZ,ALE,,AAR#00,ARS,\
            Udostępnianie aplikacji ARS-Automatyczne Rozliczanie Składek ZUS,\
            Celem usługi jest udostępnienie narzędzia wspomagającego \
            umożliwiającego prowadzenie ewidencji kont płatników (m.in. dla \
            spraw przyjętych z UE oraz zagranicznych spraw Oddziałów)']

        csv_reader = csv.reader(csv_list, delimiter=',')
        index = 1
        for row in csv_reader:
            self.assertEqual(row, csv_list[index])
            index = + 1
