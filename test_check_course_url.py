from unittest import TestCase
from check_course_url import extract_urls

class Test(TestCase):

    def test_extract_urls(self):
        text = "This is a test with a URL https://www.google.com"
        urls = extract_urls(text)
        assert urls == ["https://www.google.com"]

    def test_extract_urls_2(self):
        text = "[Course information=http://www.soci.canterbury.ac.nz/courses/promo/ANTH103.shtml]"
        urls = extract_urls(text)
        assert urls == ["http://www.soci.canterbury.ac.nz/courses/promo/ANTH103.shtml"]

    def test_extract_urls_3(self):
        text = "http://canterbury.libguides.com/engl (Image: [From Unsplash= https://unsplash.com/photos/s9CC2SKySJM].)"
        urls = extract_urls(text)
        assert urls == ["http://canterbury.libguides.com/engl", "https://unsplash.com/photos/s9CC2SKySJM"]
