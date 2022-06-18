from django.test import TestCase
from django.utils import timezone
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