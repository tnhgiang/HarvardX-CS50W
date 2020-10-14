from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.check_watchlist, name="check_watchlist"),
    path("purchase_list", views.check_purchase_list, name="check_purchase_list"),
    path("listing/<str:id>", views.manipulate_listing, name="manipulate_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.show_category, name="show_category")
]
