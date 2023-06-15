from django.urls import path
from .views import director as director_views
from .views import manager as manager_views

urlpatterns = [
    # Директор
    path('director/', director_views.DirectorHomeView.as_view(), name='director_home'),
    path('director/user-list/', director_views.DirectorUsersListView.as_view(), name='director_create_employee'),
    path('director/user-list/<int:pk>/', director_views.DirectorUpdateUserView.as_view(), name='director_get_user_permissions'),
    path('director/list-empl/', director_views.DirectorListEmployeeView.as_view(), name='director_list_employee_view'),
    path('director/list-empl/<int:pk>/', director_views.DirectorEmployeeDetailView.as_view(), name='director_detail_employee_view'),
    path('director/user-list/', director_views.DirectorUsersListView.as_view(), name='director_create_employee'),
    path('director/call-app-list/', director_views.DirectorListCallApplicationView.as_view(), name='director_list_call_app'),
    path('director/call-app-list/<int:pk>/', director_views.DirectorDetailCallApplicationView.as_view(), name='director_detail_call_app'),
    # Reports
    path('director/report-gen/', director_views.generate_report, name='report_generate'),
    path('director/report-users/', director_views.generate_report_users, name='report_users'),
    # Reference
    path('director/list-address/', director_views.DirectorListAddressView.as_view(), name='director_list_address'),
    path('director/list-address/<int:pk>/', director_views.DirectorEditAddressView.as_view(), name='director_edit_address'),
    path('director/create-address/', director_views.DirectorCreateAddressView.as_view(), name='director_create_address'),

    path('director/list-period/', director_views.DirectorListPeriodView.as_view(), name='director_list_period'),
    path('director/list-period/<int:pk>/', director_views.DirectorEditPeriodView.as_view(),name='director_edit_period'),
    path('director/create-period/', director_views.DirectorCreatePeriodView.as_view(), name='director_create_period'),

    path('director/list-quantity/', director_views.DirectorListQuantityView.as_view(), name='director_list_quantity'),
    path('director/list-quantity/<int:pk>/', director_views.DirectorEditQuantityView.as_view(),
         name='director_edit_quantity'),
    path('director/create-quantity/', director_views.DirectorCreateQuantityView.as_view(), name='director_create_quantity'),

    path('director/list-size/', director_views.DirectorListSizeView.as_view(), name='director_list_size'),
    path('director/list-size/<int:pk>/', director_views.DirectorEditSizeView.as_view(),
         name='director_edit_size'),
    path('director/create-size/', director_views.DirectorCreateSizeView.as_view(), name='director_create_size'),
    # Test
    path("director/filter-options/", director_views.get_filter_options, name="chart-filter-options"),
    path("director/<int:year>/", director_views.get_sales_chart, name="chart-sales"),

    # Менеджер
    path('manager/', manager_views.ManagerHomeView.as_view(), name='manager_home'),
    path('manager/order-crete', manager_views.ManagerCreateOrderView.as_view(), name='manager_create_order_view'),
    path('manager/order-list/', manager_views.ManagerOrdersListView.as_view(), name='manager_orders_list_view'),
    path('manager/order-list/<int:pk>/', manager_views.ManagerDetailOrderView.as_view(), name='manager_detail_order_view'),
    path('manager/create-user', manager_views.ManagerCreateUserView.as_view(), name='manager_create_user_view'),
    path('manager/user-list/', manager_views.ManagerUsersListView.as_view(), name='manager_users_list_view'),
    path('manager/user-list/<int:pk>/', manager_views.ManagerDetailUserView.as_view(), name='manager_detail_user_view'),

]
