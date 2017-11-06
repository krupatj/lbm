from django.conf.urls import url, include
from librarymanagement import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^basepage/$', views.basepage, name="base_page"),
    url(r'^signup/$', views.signup, name="sign_up_page"),
    url(r'^loginwindow/$', views.login_window, name="login_window"),
    #url(r'^account_created/$', views.account_created, name="account_created"),
    url(r'logoutwindow/$', views.logout_window, name="logoutwindow"),
    url(r'^index/$', views.index, name="index"),
    url(r'^user_index/$', views.user_index, name="user_index"),
    url(r'^books/$', views.books ,name = "books_page"),
    url(r'^bookdetails(?P<books_id>\d+)/$', views.book_details ,name = "book_details"),
    url(r'^addbook/$', views.add_book, name="add_book"),
    url(r'^authors/$', views.authors, name="authors_page"),
    url(r'^addauthor/$', views.add_author, name="add_author"),
    url(r'^lendrequest/$', views.lend_request, name="lend_page"),
    url(r'^approverequest/$', views.approve_request, name="approve_request"),
    url(r'^returnrequest/$', views.return_request, name="return_page"),
    url(r'^approvelendrequest/(?P<lend_id>\d+)/$', views.approve_lend_request, name="approve_lend_request"),
    url(r'^rejectlendrequest/(?P<lend_id>\d+)/$', views.reject_lend_request, name="reject_lend_request"),
    url(r'^approvereturnrequest/(?P<return_id>\d+)/$', views.approve_return_request, name="approve_return_request"),
    url(r'^rejectreturnrequest/(?P<return_id>\d+)/$', views.reject_return_request, name="reject_return_request"),
    url(r'^userlendbook/(?P<requested_book_id>\d+)$', views.user_lend_book, name="user_lend_book"),
    url(r'^usertlendlist/$', views.user_lend_list, name="user_lend_list"),
    url(r'^userborrowedbookslist/$', views.user_borrowed_books_list, name="user_borrowed_books_list"),
    url(r'^userreturnbook/(?P<return_book_id>\d+)$', views.user_return_book, name="user_return_book"),
    url(r'^userreturnlist/$', views.user_return_list, name="user_return_list"),
    url(r'^userwritereview/(?P<book_id>\d+)$', views.user_write_review, name="user_write_review"),
    url(r'^usersubmitreview/(?P<book_id>\d+)$', views.user_submit_review, name="user_submit_review"),

]
