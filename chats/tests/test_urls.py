from django.test import SimpleTestCase
from django.urls import reverse,resolve
from chats.views import *

class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func,home)

    def test_msgeList_url_is_resolved(self):
        url = reverse('message-list')
        self.assertEquals(resolve(url).func,message_list)

    def test_grpList_url_is_resolved(self):
        url = reverse('message-list1')
        self.assertEquals(resolve(url).func,grp_message_list)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,login)

    def test_reg_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func,register)

    def test_chat_url_is_resolved(self):
        url = reverse('rooms1',args=[1,2])
        self.assertEquals(resolve(url).func,msge_view)

    def test_grp_chat_url_is_resolved(self):
        url = reverse('rooms2',args=[1,5])
        self.assertEquals(resolve(url).func,grp_msge_view)

    def test_msge_url_is_resolved(self):
        url = reverse('message-detail',args=[5,2])
        self.assertEquals(resolve(url).func,message_list)

    def test_grp_msge_url_is_resolved(self):
        url = reverse('message-detail1',args=[2,3])
        self.assertEquals(resolve(url).func,grp_message_list)

    def test_token_url_is_resolved(self):
        url = reverse('token_send')
        self.assertEquals(resolve(url).func,token_send)

    def test_success_url_is_resolved(self):
        url = reverse('success')
        self.assertEquals(resolve(url).func,success)

    def test_verify_url_is_resolved(self):
        url = reverse('verify',args=["token"])
        self.assertEquals(resolve(url).func,verify)

    def test_error_url_is_resolved(self):
        url = reverse('error')
        self.assertEquals(resolve(url).func,error_page)

    def test_change_pwd_url_is_resolved(self):
        url = reverse('change_pwd',args=["token"])
        self.assertEquals(resolve(url).func,change_pwd)

    def test_forget_pwd_url_is_resolved(self):
        url = reverse('forgot_pwd')
        self.assertEquals(resolve(url).func,forgot_pwd)

    def test_status_url_is_resolved(self):
        url = reverse('status')
        self.assertEquals(resolve(url).func,add_edit_status)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func,logout)

    def test_submit_fdbk_url_is_resolved(self):
        url = reverse('submitFeedback')
        self.assertEquals(resolve(url).func,submitFeedback)

    def test_fdbk_url_is_resolved(self):
        url = reverse('feedback')
        self.assertEquals(resolve(url).func,feedback)

    def test_video_url_is_resolved(self):
        url = reverse('openVideo')
        self.assertEquals(resolve(url).func,openVideo)

    def test_clear_chat_url_is_resolved(self):
        url = reverse('clearChat',args=[2,5])
        self.assertEquals(resolve(url).func,clearChat)

    def test_final_logout_url_is_resolved(self):
        url = reverse('finalLogout')
        self.assertEquals(resolve(url).func,finalLogout)

    def test_load_fdbk_url_is_resolved(self):
        url = reverse('loadfeedbacks')
        self.assertEquals(resolve(url).func,loadFeedback)

    def test_view_brdcst_url_is_resolved(self):
        url = reverse('viewBroadcast')
        self.assertEquals(resolve(url).func,view_broadcast)

    def test_brdcst_url_is_resolved(self):
        url = reverse('broadcast')
        self.assertEquals(resolve(url).func,broadcast)

    def test_notices_url_is_resolved(self):
        url = reverse('notices')
        self.assertEquals(resolve(url).func,viewNotifications)

    def test_users_url_is_resolved(self):
        url = reverse('fetchUsers')
        self.assertEquals(resolve(url).func,fetchUsers)

    def test_reqSent_url_is_resolved(self):
        url = reverse('reqSent',args=[14,52])
        self.assertEquals(resolve(url).func,reqSent)

    def test_isAccept_url_is_resolved(self):
        url = reverse('isAccept',args=[54,78])
        self.assertEquals(resolve(url).func,is_accept)

    def test_decline_url_is_resolved(self):
        url = reverse('decline',args=[65,45])
        self.assertEquals(resolve(url).func,is_decline)

    def test_newGrp_url_is_resolved(self):
        url = reverse('newGrp')
        self.assertEquals(resolve(url).func,createGrp)

    def test_newGrp2_url_is_resolved(self):
        url = reverse('newGrp2',args=[105])
        self.assertEquals(resolve(url).func,createGrp2)

    def test_grpDesc_url_is_resolved(self):
        url = reverse('grpDesc',args=[54])
        self.assertEquals(resolve(url).func,change_grp_desc)

    def test_grpImg_url_is_resolved(self):
        url = reverse('grpImg',args=[44])
        self.assertEquals(resolve(url).func,add_change_grp_icn)                                