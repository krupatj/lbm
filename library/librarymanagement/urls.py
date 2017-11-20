from django.conf.urls import url, include
from .Views import view_admin
from .Views.view_admin import *
from .Views.view_user import *
from .Views.authentications_view import *
from .Views import view_user
from .Views import basepages_view
from .Views import authentications_view

urlpatterns = [
   
    url(r'^$', authentications_view.Authentication.as_view(), name="sign_up_page"),
    url(r'^basepage/$', authentications_view.Authentication.as_view(), name="base_page_class"),
    url(r'^loginwindow/$', authentications_view.LoginView.as_view(), name="login_window"),
    url(r'^signup/$',  authentications_view.Authentication.as_view(), name="sign_up_page"),
    url(r'^admin_index/$', authentications_view.admin_index, name="index"),
    url(r'logoutwindow/$',  authentications_view.LogoutView.as_view(), name="logoutwindow"),

    url(r'^books_list/$', view_admin.BookList.as_view(), name = "books_page"),
    url(r'^bookdetails/(?P<pk>\d+)/$',view_admin.BookDetailsView.as_view() ,name = "book_details"),
    url(r'^authors/$', view_admin.AuthorView.as_view(), name="authors_page"),
    url(r'^lendrequests/$', view_admin.LendRequestView.as_view(), name="lend_page"),
    url(r'^borrowedbooks/$', view_admin.BorrowedBooksView.borrowed_books_list, name="borrowed_books"),
    url(r'^returnrequests/$', view_admin.ReturnRequestView.as_view(), name="return_page"),
    url(r'^addbook/$', view_admin.BookList.add_book, name="add_book"),
    url(r'^addauthor/$', view_admin.AuthorView.add_author, name="add_author"),
    url(r'^approvelendrequest/(?P<lend_id>\d+)/$', view_admin.LendRequestView.approve_lend_request, name="approve_lend_request"),
    url(r'^rejectlendrequest/(?P<lend_id>\d+)/$', view_admin.LendRequestView.reject_lend_request, name="reject_lend_request"),
    url(r'^approvereturnrequest/(?P<return_id>\d+)/$', view_admin.ReturnRequestView.approve_return_request, name="approve_return_request"),
    url(r'^rejectreturnrequest/(?P<return_id>\d+)/$', view_admin.ReturnRequestView.reject_return_request, name="reject_return_request"),


    url(r'^user_index/$', view_user.user_index, name="user_index"),
    url(r'^userlendlist/$', view_user.UserRequestsView.user_lend_list, name="user_lend_list"),
    url(r'^userborrowedbookslist/$', view_user.UserRequestsView.user_borrowed_books_list, name="user_borrowed_books_list"),
    url(r'^userreturnlist/$', view_user.UserRequestsView.user_return_list, name="user_return_list"),
    url(r'^userlendbook_class/(?P<requested_book_id>\d+)$', view_user.UserActionsView.user_lend_book, name="user_lend_book"),
    url(r'^userreturnbook/(?P<return_book_id>\d+)/(?P<lend_id>\d+)$', view_user.UserActionsView.user_return_book, name="user_return_book"),
    url(r'^userwritereview/(?P<book_id>\d+)/(?P<return_id>\d+)$', view_user.UserActionsView.user_write_review, name="user_write_review"),
    url(r'^usersubmitreview/(?P<book_id>\d+)/(?P<return_id>\d+)$', view_user.UserActionsView.user_submit_review, name="user_submit_review"),
]
