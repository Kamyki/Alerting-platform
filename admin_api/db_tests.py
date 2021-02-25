import unittest
from mongo import *


class TestServicePopulate(unittest.TestCase):
    def test_populate_services(self):
        populate_services(read_yaml(SERVICES_YAML_PATH))
        services = get_services()
        self.assertEqual(len(services), 2)

    def test_populate_admins(self):
        populate_admins(read_yaml(ADMINS_YAML_PATH))
        admins = get_admins()
        self.assertEqual(len(admins), 2)

    def test_retrieve_admin_emails(self):
        populate_services(read_yaml(SERVICES_YAML_PATH))
        services = get_services()

        a1 = get_first_admin_email(services[0])
        a2 = get_second_admin_email(services[0])

        self.assertTrue("bieganski.m@wp.pl" in  [a1, a2])


if __name__ == '__main__':
    unittest.main()
