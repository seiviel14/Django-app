from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
import datetime

from .models import Question

#Usually testing models and views

class QuestionModelTests(TestCase):

    #Function used for instantiate the common requeriments in every test of this class
    def setUp(self):
        self.question = Question(question_text="")

    def test_was_published_recently_with_future_questions(self):
        #was_published_recently returns False for questions with a future pub_date
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        time = timezone.now() - datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("polls:index"))
        self.question = Question(question_text="")

    def test_no_questions(self):
        #If no questions, an approppiate mesage should appear
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, "No polls are available.")
        self.assertQuerysetEqual(self.response.context["latest_question_list"], [])

    def test_only_past_questions(self):
        self.question.pub_date = timezone.now() + datetime.timedelta(days=30)
        self.assertEqual(self.response.status_code, 200)
        self.assertNotIn(self.question ,self.response.context["latest_question_list"])
