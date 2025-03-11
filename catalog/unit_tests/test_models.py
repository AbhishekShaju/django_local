from django.test import TestCase
from catalog.unit_tests.test_models import *
from django.urls import reverse

class AuthorModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Runs once for all test methods."""
        cls.author = Author.objects.create(first_name="John", last_name="Doe")

    def test_first_name_label(self):
        """Test if the label of first_name is correct."""
        author = AuthorModelTest.author
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_max_length(self):
        """Test if max_length of last_name is 100."""
        author = AuthorModelTest.author
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_get_absolute_url(self):
        """Test if get_absolute_url() method works."""
        author = AuthorModelTest.author
        self.assertEqual(author.get_absolute_url(), reverse('author-detail', args=[str(author.id)]))
