from django.test import TestCase
from django.urls import reverse
from catalog.unit_tests.test_models import * 

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create 5 authors for pagination tests."""
        number_of_authors = 5
        for author_id in range(number_of_authors):
            Author.objects.create(first_name=f'John {author_id}', last_name=f'Doe {author_id}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/author_list.html')

    def test_pagination(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
