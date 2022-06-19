from urllib import response
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

def question_creator(qt,d):
    time = timezone.now() + datetime.timedelta(days=d)
    question = Question.objects.create(question_text=qt, pub_date=time)
    return question

def response_creator(self):
    response = self.client.get(reverse("polls:index"))
    return response

class QuestionIndexViewTests(TestCase): 

    def test_no_questions(self):
        response = response_creator(self)
        #If no questions, an approppiate mesage should appear
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_only_past_questions(self):
        question = question_creator("Test1",10)
        response = response_creator(self)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(question ,response.context["latest_question_list"])
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions_revealed(self):
        question = question_creator("Test2",-10)
        response = response_creator(self)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        past_question = question_creator("Test3", -10)
        future_question = question_creator("Test4", 10)
        response = response_creator(self)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        question1 = question_creator("Test5", -10)
        question2 = question_creator("Test6", -20)
        response = response_creator(self)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question1,question2])

    def test_two_future_questions(self):
        question1 = question_creator("Test7", 10)
        question1 = question_creator("Test8", 10)
        response = response_creator(self)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        question = question_creator("Test9", 10)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        question = question_creator("Test10", -10)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, question.question_text)

#Create Results views tests


#Create test for questions without choices (error)