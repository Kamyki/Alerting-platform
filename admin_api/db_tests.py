import unittest

DEBUG = False # must be before including to surpress 
from mongo import *

class TestServicePopulate(unittest.TestCase):
    def test_populate_services(self):
        populate_services(read_yaml(SERVICES_YAML_PATH))
        services = get_services()
        self.assertEqual(len(list(services)), 2)

    def test_populate_admins(self):
        populate_admins(read_yaml(ADMINS_YAML_PATH))
        admins = get_admins()
        self.assertEqual(len(list(admins)), 2)

    def test_retrieve_admin_emails(self):
        populate_services(read_yaml(SERVICES_YAML_PATH))
        services = list(get_services())

        a1 = get_first_admin_email(services[0])
        a2 = get_second_admin_email(services[0])

        self.assertTrue("bieganski.m@wp.pl" in  [a1, a2])

    def test_populate_incidents(self):
        populate_incidents(read_yaml_incidents())
        # put_incident("http://www.google.com")
        incidents = get_incidents()
        self.assertEqual(len(list(incidents)), 2)
    
    def test_deactivate_incident(self):
        populate_incidents(read_yaml_incidents())
        admin_deactivate_alert("http://www.google.com")
        maybe_false = db[INCIDENTS_COLLECTION_NAME].find_one({"url": "http://www.google.com"}, {"active"})['active']
        self.assertFalse(maybe_false)

    def test_should_report_second_admin(self):
        populate_services(read_yaml(SERVICES_YAML_PATH))
        populate_incidents(read_yaml_incidents())

        URL = "http://www.google.com"
        put_incident(URL)

        # from pprint import pprint
        # pprint(get_incidents())

        # incident reported to admin1, but allowed_response_time not exceeded
        should = should_report_second_admin(URL)
        self.assertFalse(should)

        # allowed_response_time exceeded
        allowed_response_time = 1
        import time
        time.sleep(allowed_response_time)
        should = should_report_second_admin(URL)
        self.assertTrue(should)

        # admin1 or admin2 deactivated
        admin_deactivate_alert(URL)
        should = should_report_second_admin(URL)
        self.assertFalse(should)




if __name__ == '__main__':
    unittest.main()