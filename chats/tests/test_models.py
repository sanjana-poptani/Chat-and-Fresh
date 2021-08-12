from django.core.checks import messages
from django.db.models.fields import EmailField
from django.forms.fields import ImageField
from django.test import TestCase
from chats.models import *

class TestModels(TestCase):
    @classmethod
    def setUp(self):
        self.profile = Profile.objects.create(
            username = 'test',
            email = 'test@gmail.com',
            password = 'test',
        )

        self.groupModel = groupModel.objects.create(
            Admin = self.profile,
            groupName = 'abc',
            groupDesc = 'test',
        )

        self.usergrps = UserGroups.objects.create(
            userRef = self.profile,
            group = self.groupModel
        )

        self.grpmsge = GrpMsges.objects.create(
            message = 'hello',
            sender = self.profile,
            group = self.groupModel
        )

        self.msge = Message.objects.create(
            sender = self.profile,
            receiver = self.profile,
            message = 'hello',
        )

        self.frnds = Friends.objects.create(
            sender = self.profile,
            receiver = self.profile
        )

        self.fdbk = Feedback.objects.create(
            feedback = 'nice',
            user = self.profile
        )

        self.brdcst = Broadcast.objects.create(
            notification = 'update',
        )

    def test_fields_profile(self):
        self.assertIsInstance(self.profile.username,str)
        self.assertIsInstance(self.profile.email,str)
        self.assertIsInstance(self.profile.password,str)
        # self.assertIsInstance(self.profile.last_login,datetime)
        # self.profile.last_login.return_value = datetime.date(2021,8,11)
        # self.assertEquals(self.profile.last_login,datetime.datetime.now)
        self.assertIsInstance(self.profile.is_verified,bool)

    def test_fields_groupModel(self):
        self.assertIsInstance(self.groupModel.Admin,Profile)
        self.assertIsInstance(self.groupModel.groupName,str)
        self.assertIsInstance(self.groupModel.groupDesc,str)
        # self.assertIsInstance(self.groupModel.groupImg,ImageField)

    def test_fields_userGroup(self):
        self.assertIsInstance(self.usergrps.userRef,Profile)
        self.assertIsInstance(self.usergrps.group,groupModel)

    def test_fields_grpMsges(self):
        self.assertIsInstance(self.grpmsge.message,str)
        # self.assertIsInstance(self.grpmsge.timestamp,datetime)
        self.assertIsInstance(self.grpmsge.sender,Profile)
        self.assertIsInstance(self.grpmsge.group,groupModel)
    
    def test_fields_msges(self):
        self.assertIsInstance(self.msge.message,str)
        # self.assertIsInstance(self.msge.timestamp,datetime)
        self.assertIsInstance(self.msge.sender,Profile)
        self.assertIsInstance(self.msge.receiver,Profile)
        self.assertIsInstance(self.msge.is_read,bool)

    def test_fields_frnds(self):
        self.assertIsInstance(self.frnds.sender,Profile)
        self.assertIsInstance(self.frnds.receiver,Profile)
        self.assertIsInstance(self.frnds.is_friend,bool)
        self.assertIsInstance(self.frnds.is_req,bool)

    def test_fields_fdbk(self):
        self.assertIsInstance(self.fdbk.feedback,str)
        self.assertIsInstance(self.fdbk.user,Profile)

    def test_fields_brdcst(self):
        self.assertIsInstance(self.brdcst.notification,str)
        # self.assertIsInstance(self.brdcst.date,datetime)