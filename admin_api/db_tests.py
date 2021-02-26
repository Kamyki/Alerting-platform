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
        URL = "http://www.google.com"
        db[INCIDENTS_COLLECTION_NAME].drop()
        put_incident(URL)

        token = get_incident_token_first_admin(URL)
        admin_deactivate_alert(URL, token)
        maybe_false = db[INCIDENTS_COLLECTION_NAME].find_one({"url": URL}, {"active"})['active']
        self.assertFalse(maybe_false)

    def test_should_report_second_admin(self):
        services_dict = read_yaml(SERVICES_YAML_PATH)
        populate_services(services_dict)
        # populate_incidents(read_yaml_incidents())

        db[INCIDENTS_COLLECTION_NAME].drop()
        db[ADMINS_REACTION_COLLECTION_NAME].drop()

        URL = "http://www.google.com"
        put_incident(URL)

        # incident reported to admin1, but allowed_response_time not exceeded
        should = should_report_second_admin(URL)
        self.assertFalse(should)

        # allowed_response_time exceeded
        allowed_response_time = services_dict[0]['alerting_window']
        import time
        time.sleep(allowed_response_time)
        should = should_report_second_admin(URL)
        self.assertTrue(should)

        # admin1 (or admin2, whatever) deactivated
        token = get_incident_token_first_admin(URL)
        admin_deactivate_alert(URL, token)
        should = should_report_second_admin(URL)
        self.assertFalse(should)


if __name__ == '__main__':
    unittest.main()
