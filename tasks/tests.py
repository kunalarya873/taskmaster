from django.test import TestCase
from .models import Task
from django.urls import reverse

class TaskListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task1 = Task.objects.create(title="Task 1", description="Description 1", due_date="2024-09-10", priority=1, status="To Do")
        cls.task2 = Task.objects.create(title="Task 2", description="Description 2", due_date="2024-09-15", priority=2, status="Done")
        cls.task3 = Task.objects.create(title="Task 3", description="Description 3", due_date="2024-09-12", priority=3, status="In Progress")

    def test_filter_by_status(self):
        response = self.client.get(reverse('task_list') + '?status=Done')
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context['tasks'])
        self.assertListEqual(tasks, [self.task2])

    def test_sort_by_priority(self):
        response = self.client.get(reverse('task_list') + '?sort_by=priority')
        tasks = list(response.context['tasks'])
        self.assertEqual(tasks[0], self.task1)
        self.assertEqual(tasks[1], self.task2)
        self.assertEqual(tasks[2], self.task3)


class TaskCreationTests(TestCase):
    def test_create_task(self):
        response = self.client.post(reverse('task_list'), {
            'title': 'New Task',
            'description': 'Description for new task',
            'due_date': '2024-09-20',
            'priority': 1,
            'status': 'To Do',
        })

        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_form_display(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'Create Task')