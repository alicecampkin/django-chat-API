from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Message, Conversation

USER_MODEL = get_user_model()


class TestConversation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bob = USER_MODEL.objects.create(
            email='bob@test.com',
            full_name='Bob Bennington',
            password='pass123'
        )
        cls.jane = USER_MODEL.objects.create(
            email='jane@test.com',
            full_name='Jane Deux',
            password='pass456',
        )
        cls.susan = USER_MODEL.objects.create(
            email='susan@test.com',
            full_name='Susan Shaw',
            password='pass789'
        )

    def test_conversation_instance(self):
        conversation = Conversation.objects.create(
            owner=self.bob.profile,
            user_with=self.jane.profile
        )

        self.assertEqual(conversation.owner, self.bob.profile)
        self.assertEqual(conversation.user_with, self.jane.profile)

    def test_bobs_conversations(self):
        Conversation.objects.create(
            owner=self.bob.profile,
            user_with=self.jane.profile
        )
        Conversation.objects.create(
            owner=self.bob.profile,
            user_with=self.susan.profile
        )
        bobs_conversations = self.bob.profile.conversations.all()

        self.assertEqual(bobs_conversations.count(), 2)


class TestMessage(TestCase):
    '''
    Things to test:
    - Can I create a message between two users?
    - Does the message have a timestamp?
    -
    '''

    @classmethod
    def setUpTestData(cls):
        cls.bob = USER_MODEL.objects.create(
            full_name='Bob Bennington',
            email='bob@test.com',
            password='password123'
        )
        cls.jane = USER_MODEL.objects.create(
            full_name='Jane Deux',
            email='janedeux@test.com',
            password='password456'
        )
        cls.susan = USER_MODEL.objects.create(
            full_name='Susan Shaw',
            email='susanshaw@test.com',
            password='password789'
        )
        cls.conversation_jane_bob = Conversation.objects.create(
            owner=cls.jane.profile,
            user_with=cls.bob.profile
        )
        cls.conversation_jane_susan = Conversation.objects.create(
            owner=cls.jane.profile,
            user_with=cls.susan.profile
        )

    def test_create_message(self):
        message = Message.objects.create(
            user_from=self.bob.profile,
            user_to=self.jane.profile,
            conversation=self.conversation_jane_bob,
            content="Hi Jane, this is Bob."
        )

        self.assertTrue(hasattr(message, 'sent'))
        self.assertEqual(message.user_from.user.full_name, 'Bob Bennington')
        self.assertEqual(message.content, 'Hi Jane, this is Bob.')

    def test_janes_messages(self):
        bobs_first_message = Message.objects.create(
            user_from=self.bob.profile,
            user_to=self.jane.profile,
            conversation=self.conversation_jane_bob,
            content='Hi Jane, this is Bob'
        )
        bobs_second_message = Message.objects.create(
            user_from=self.bob.profile,
            user_to=self.jane.profile,
            conversation=self.conversation_jane_bob,
            content='Hi Jane, this is Bob again.'
        )
        susans_message = Message.objects.create(
            user_from=self.susan.profile,
            user_to=self.jane.profile,
            conversation=self.conversation_jane_susan,
            content='Hi Jane, this is Susan'
        )
        janes_message_to_bob = Message.objects.create(
            user_from=self.jane.profile,
            user_to=self.bob.profile,
            conversation=self.conversation_jane_bob,
            content='Hey Bob.'
        )

        janes_messages = self.jane.profile.messages.all().order_by('-sent')
        self.assertEqual(janes_messages.count(), 3)

        most_recent_message = janes_messages[0]
        self.assertEqual(most_recent_message.content, 'Hi Jane, this is Susan')

        janes_messages_from_bob = self.jane.profile.messages.filter(
            user_from=self.bob.profile)
        self.assertEqual(janes_messages_from_bob.count(), 2)

        unread_messages = self.jane.profile.messages.filter(read=False)
        self.assertEqual(unread_messages.count(), 3)

        janes_sent_messages = self.jane.profile.sent_messages.all()
        self.assertEqual(janes_sent_messages.count(), 1)

    def test_conversation_messages(self):

        Message.objects.create(
            user_from=self.bob.profile,
            user_to=self.jane.profile,
            conversation=self.conversation_jane_bob,
            content='Hi Jane, this is Bob'
        )
        Message.objects.create(
            user_from=self.jane.profile,
            user_to=self.bob.profile,
            conversation=self.conversation_jane_bob,
            content='Hey Bob.'
        )

        messages = self.conversation_jane_bob.messages.all().order_by('-sent')

        self.assertEqual(messages.count(), 2)
