"""
URL configuration for laxout project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("laxout_app.routing")),
    path("", include("django.contrib.auth.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path("autorise", api_views.autorise_laxout_user),
    re_path("api/test", api_views.get_username),
    re_path("uebungen", api_views.get_exercises),
    re_path("indexpost", api_views.post_leistungs_index),
    re_path("coinsget", api_views.get_laxcoins_amount),
    re_path("painsadd", api_views.post_pain_level),
    re_path("couponsget", api_views.get_coupons),
    re_path("couponbuy", api_views.buy_coupon),
    re_path("coupongetuser", api_views.get_coupons_for_user),
    re_path("coupondeleteuser", api_views.delete_coupon_user),
    re_path("exercisefinish", api_views.finish_exercise),
    re_path("exerciseskip", api_views.skip_exercise),
    re_path("workoutfinish", api_views.finish_workout),
    re_path("instructionget", api_views.get_intruction),
    re_path("progressweekget", api_views.get_progress_week),
    re_path("getindividualindexes", api_views.get_individual_indexes),
]
