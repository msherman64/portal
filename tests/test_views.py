from datetime import datetime
from unittest import mock

from django.test import TestCase

from ..models import Artifact, Author, Label
from ..views import artifacts_from_form, make_author, upload_artifact


def sorted_list_ids(alist):
    """
    Helper function to turn a list of items into a sorted list of ids
    """
    new_list = list(map(lambda x: x.id, list(alist)))
    new_list.sort()
    return new_list

class UploadArtifactTest(TestCase):
    # For the purpose of these tests, put all names
    # into first_name for each author
    def make_simple_author(name_string):
        a = Author(title='', first_name=name_string, last_name='')
        a.save()
        return a.pk

    @mock.patch('sharing.views.dev', True)
    @mock.patch('sharing.views.make_author', make_simple_author)
    @mock.patch('sharing.views.get_rec_id')
    def test_dev_success(self, mock_id):
        mock_id.return_value = "361518"
        pk = upload_artifact("doi")
        artifact = Artifact.objects.get(pk=pk)
        self.assertEqual(artifact.title, "Sample Title")
        self.assertEqual(artifact.description, "This is a description")
        self.assertEqual(len(list(artifact.authors.all())), 1)
        self.assertEqual(artifact.authors.all()[0].first_name, "Some Name")

    @mock.patch('sharing.views.dev', False)
    @mock.patch('sharing.views.make_author', make_simple_author)
    @mock.patch('sharing.views.get_rec_id')
    def test_non_dev_success(self, mock_id):
        mock_id.return_value = "3357455"
        pk = upload_artifact("doi")
        artifact = Artifact.objects.get(pk=pk)
        self.assertEqual(artifact.title,  ("Modelling and Simulation of Water"
                                           " Networks based on Loop Method"))
        self.assertIn("Simulator algorithm for water networks", 
                      artifact.description)
        self.assertEqual(len(list(artifact.authors.all())), 1)
        self.assertEqual(artifact.authors.all()[0].first_name, "Arsene, Corneliu")
    
    @mock.patch('sharing.views.dev', True)
    @mock.patch('sharing.views.make_author', make_simple_author)
    @mock.patch('sharing.views.get_rec_id')
    def test_failed_request(self, mock_id):
        # Should fail gracefully when given a bad id
        mock_id.return_value = "notadoi"
        pk = upload_artifact("doi")
        self.assertIsNone(pk)

    @mock.patch('sharing.views.dev', True)
    @mock.patch('sharing.views.make_author', make_simple_author)
    @mock.patch('sharing.views.get_rec_id')
    def test_dev_multiple_authors(self, mock_id):
        mock_id.return_value = "361531"
        pk = upload_artifact("doi")
        artifact = Artifact.objects.get(pk=pk)
        self.assertEqual(artifact.title, "A title")
        self.assertEqual(artifact.description, "A thing")
        self.assertEqual(len(artifact.authors.all()), 2)
        self.assertEqual(artifact.authors.all()[0].first_name, "A person")
        self.assertEqual(artifact.authors.all()[1].first_name, "Second person")


class MakeAuthorTest(TestCase):
    def test_title_fname_lname(self):
        author_str = "Dr. Albert Einstein"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, "Dr.") 
        self.assertEqual(a.first_name, "Albert") 
        self.assertEqual(a.last_name, "Einstein") 

    def test_simple_with_comma(self):
        author_str = "Skywalker, Luke"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '') 
        self.assertEqual(a.first_name, "Luke") 
        self.assertEqual(a.last_name, "Skywalker") 

    def test_multiple_with_comma(self):
        author_str = "Potter, Harry James"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '') 
        self.assertEqual(a.first_name, "Harry James") 
        self.assertEqual(a.last_name, "Potter") 

    def test_five_names(self):
        author_str = "Adam Albert John Jacob Samuels"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '')
        self.assertEqual(a.first_name, author_str) 
        self.assertEqual(a.last_name, '')

    def test_fname_lname(self):
        author_str = "Fred Astaire"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '')
        self.assertEqual(a.first_name, "Fred") 
        self.assertEqual(a.last_name, "Astaire") 

    def test_three_names_no_title(self):
        author_str = "Sir Isaac Newton"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '')
        self.assertEqual(a.first_name, "Sir Isaac") 
        self.assertEqual(a.last_name, "Newton") 

    def test_one_name(self):
        author_str = "Sting"
        author_pk = make_author(author_str)    
        a = Author.objects.get(pk=author_pk)
        self.assertEqual(a.title, '')
        self.assertEqual(a.first_name, "Sting") 
        self.assertEqual(a.last_name, '')


class ArtifactsFromFormTest(TestCase):
    def setUp(self):
        now = datetime.now()
        self.a = Artifact.objects.create(
                    title='Test Case Artifact a is cool',
                    description="Apple",
                    short_description="a vowel",
                    created_at=now,
                    updated_at=now,
        )    
        self.b = Artifact.objects.create(
                    title='Test Case Artifact b',
                    description="Banana",
                    created_at=now,
                    updated_at=now,
        )    
        self.c = Artifact.objects.create(
                    title='Test Case Artifact c',
                    description="Carrot",
                    created_at=now,
                    updated_at=now,
        )    
        self.d = Artifact.objects.create(
                    title='Test Case Artifact d',
                    description="Dinosaur",
                    created_at=now,
                    updated_at=now,
        )    
        self.e = Artifact.objects.create(
                    title='Test Case Artifact e',
                    description="Elephant",
                    short_description="a vowel",
                    created_at=now,
                    updated_at=now,
        )    
        self.f = Artifact.objects.create(
                    title='cool Test Case Artifact f',
                    created_at=now,
                    updated_at=now,
        )    

        # Adding labels to their multiples
        self.label1 = Label.objects.create(label='label1')
        self.label2 = Label.objects.create(label='label2')
        self.label3 = Label.objects.create(label='label3')
        self.label4 = Label.objects.create(label='label4')
        self.label5 = Label.objects.create(label='label5')
        self.a.labels.set([self.label1])
        self.b.labels.set([self.label1, self.label2])
        self.c.labels.set([self.label1, self.label3])
        self.d.labels.set([self.label1, self.label4])
        self.e.labels.set([self.label1, self.label5])
        self.f.labels.set([self.label1, self.label2, self.label3])

        # Give Einstein's initials an author
        albert = Author.objects.create(
                    title="Mr.",
                    first_name="Albert",
                    last_name="Einstein"
        )
        self.a.authors.set([albert])
        self.e.authors.set([albert])

    def test_empty_label(self):
        data = {
            'labels': [800000000],
            'search': '',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([])
        self.assertEqual(filtered, goal)
        
    def test_duplicate_matches_or(self):
        data = {
            'labels': [self.label1.id, self.label2.id, self.label3.id],
            'search': '',
            'is_or': True
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a, self.b, self.c, self.d, self.e, self.f])
        self.assertEqual(filtered, goal)
        
    def test_some_partial_matches_and(self):
        data = {
            'labels': [self.label1.id, self.label3.id],
            'search': '',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.c, self.f])
        self.assertEqual(filtered, goal)
        
    def test_keywords_title(self):
        data = {
            'labels': [],
            'search': 'cool',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a, self.f])
        self.assertEqual(filtered, goal)
        
    def test_keywords_author(self):
        data = {
            'labels': [],
            'search': 'Albert Einstein',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a, self.e])
        self.assertEqual(filtered, goal)

    def test_keywords_desc(self):
        data = {
            'labels': [],
            'search': 'Apple',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a])
        self.assertEqual(filtered, goal)

    def test_keywords_short_desc_no_isor(self):
        data = {
            'labels': [],
            'search': 'voWel',
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a, self.e])
        self.assertEqual(filtered, goal)

    def test_keywords_and_label(self):
        data = {
            'labels': [self.label5.id],
            'search': 'vowel',
            'is_or': False
        }
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.e])
        self.assertEqual(filtered, goal)

    def test_empty_form(self):
        data = {}
        filtered = sorted_list_ids(artifacts_from_form(data))
        goal = sorted_list_ids([self.a, self.b, self.c, self.d, self.e, self.f])
        self.assertEqual(filtered, goal)
