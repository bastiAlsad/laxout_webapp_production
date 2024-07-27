from django.urls import path
from . import views, openAi, befund_logik
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    #favivon
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico')),
    path("", views.home, name="home" ),
    path("logout/", views.logout_view, name="logout"),
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("home/", views.home, name="home"),
    path("create-user/", views.create_user, name="create-user"),
    path("home/create-user/", views.create_user, name="create-user"),
    # path("create-analog-user/", views.create_analog_user, name="create-analog-user"),
    # path("home/create-analog-user/", views.create_analog_user, name="create-analog-user"),
    path("home/delete-user/<int:id>/", views.delete_user, name= "delete-user"),
    path("delete-user/<int:id>/", views.delete_user, name= "delete-user"),
    path("home/edit-user/<int:id>", views.edit_user, name="edit-user"),
    path("edit-user/<int:id>", views.edit_user, name="edit-user"),
    path("home/edit-user/edit-user-workout/", views.edit_user_workout, name="edit-user"),
    path("edit-user/edit-user-workout/", views.edit_user_workout, name="edit-user"),
    path("home/edit-user/delete-user-workout/", views.delete_user_workout, name="edit-user"),
    path("edit-user/delete-user-workout/", views.delete_user_workout, name="edit-user"),
    path("home/edit-user/add-exercises/<int:id>/", views.add_exercises, name="add-exercises"),
    path("edit-user/add-exercises/<int:id>/", views.add_exercises, name="add-exercises"),
    path("home/edit-user/add-exercises/<int:first>/<int:second>/", views.add_exercises, name="add-exercises"),
    path("edit-user/add-exercises/<int:first>/<int:second>/", views.add_exercises, name="add-exercises"),
    path("laxout/show-login-code/<str:logintoken>/", views.display_login_code, name="show-login-code"),
    path("analyses", views.analyses, name="analyses"),
    path("home/analyses", views.analyses, name="analyses"),
    path("home/edit-user/post-user-instruction/<int:id>/", views.post_user_instruction, name="edit-user"),
    path("edit-user/post-user-instruction/<int:id>/", views.post_user_instruction, name="edit-user"),
    path("new-exercise/", views.create_exercise, name="new-exercise"),
    path("home/new-exercise/", views.create_exercise, name="new-exercise"),
    path("home/trigger-admin-power", views.admin_power, name="home"),
    path("trigger-admin-power", views.admin_power, name="home"),
    path("home/edit-user/<int:id>/move-up/", views.move_up, name="edit-user"),
    path("home/edit-user/<int:id>/move-down/", views.move_down, name="edit-user"),
    path("edit-user/<int:id>/move-down/", views.move_down, name="edit-user"),
    path("edit-user/<int:id>/move-up/", views.move_up, name="edit-user"),
    path("home/edit-user/post-user-instruction-int/", views.set_instruction_int, name="edit-user"),
    path("edit-user/post-user-instruction-int/", views.set_instruction_int, name="edit-user"),
    path("home/edit-user/post-user-mail/<int:id>/", views.post_user_mail, name="edit-user"),
    path("edit-user/post-user-mail/<int:id>/", views.post_user_mail, name="edit-user"),
    path("chats/", views.chats, name="chats"),
    path("home/chats", views.chats, name="chats"),
    path("home/chats/<int:id>/", views.personal_chat, name="personal-chat"),
    path("chats/<int:id>/", views.personal_chat, name="personal-chat"), 
    path("home/chats/<int:id>/sendmessage/", views.post_message, name="personal-chat"),
    path("chats/<int:id>/sendmessage/", views.post_message, name="personal-chat"),
    path("home/chats/<int:id>/set-admin-has-seen/", views.admin_has_seen, name="personal-chat"),
    path("chats/<int:id>/set-admin-has-seen/", views.admin_has_seen, name="personal-chat"),
    path("edit-plans/", views.edit_plans, name="edit-plans"),
    path("home/edit-plans/", views.edit_plans, name="edit-plans"),
    path("edit-plans/delete-plan/<int:id>/", views.delete_plan, name="edit-plans"),
    path("home/edit-plans/delete-plan/<int:id>/", views.delete_plan, name="edit-plans"),
    path("edit-plans/edit-plan/<int:id>/", views.edit_plan, name="edit-plans"),
    path("home/edit-plans/edit-plan/<int:id>/", views.edit_plan, name="edit-plans"),
    path("edit-plans/edit-plan/<int:id>/", views.edit_plan, name="edit-plans"),
    path("home/edit-plans/edit-plan/<int:id>/", views.edit_plan, name="edit-plans"),
    path("edit-plans/edit-plan/<int:id>/add-exercises/", views.add_exercises_plan, name="edit-plans"),
    path("home/edit-plans/edit-plan/<int:id>/add-exercises/", views.add_exercises_plan, name="edit-plans"),
    path("home/edit-plans/add-exercises/<int:first>/<int:second>/", views.add_exercises_plan, name="add-exercises"),
    path("edit-plans/add-exercises/<int:first>/<int:second>/", views.add_exercises_plan, name="add-exercises"),
    path("home/edit-plans/edit-plan/<int:id>/delete-plan-exercise/", views.delete_plan_exercise, name="delete-exercise"),
    path("edit-plans/edit-plan/<int:id>/delete-plan-exercise/", views.delete_plan_exercise, name="delete-exercise"),
    path("home/edit-plans/edit-plan/<int:id>/edit-plan-exercise/", views.edit_plan_exercise, name="edit-plan"),
    path("edit-plans/edit-plan/<int:id>/edit-plan-exercise/", views.edit_plan_exercise, name="edit-plan"),
    path("edit-plans/edit-plan/<int:id>/move-down/",views.move_down_plan),
    path("home/edit-plans/edit-plan/<int:id>/move-down/",views.move_down_plan),   
    
    # path("edit-plans/edit-plan/<int:id>/update-plan-ai/",openAi.update_ai_plan),
    # path("home/edit-plans/edit-plan/<int:id>/update-plan-ai/",openAi.update_ai_plan), 

    path("edit-plans/edit-plan/<int:id>/move-up/",views.move_up_plan),
    path("home/edit-plans/edit-plan/<int:id>/move-up/",views.move_up_plan),
    # path("create-plan/", views.create_ai_training_data, name="create-plan"),
    # path("home/create-plan/", views.create_ai_training_data, name="create-plan"),
    path("edit-user/<int:id>/dokumentation/", views.patient_dokumentieren, name = "dokumentation"),
    path("home/edit-user/<int:id>/dokumentation/", views.patient_dokumentieren, name = "dokumentation"),
    path("edit-user/<int:id>/dokumentation/new-doku", views.new_doku, name = "neue dokumentation"),
    path("home/edit-user/<int:id>/dokumentation/new-doku", views.new_doku, name = "neue dokumentation"),
    path("edit-user/<int:id>/dokumentation/add-doku", views.add_doku, name = "dokumentation speichern"),
    path("edit-user/<int:id>/dokumentation/delete-doku/<int:docuId>/", views.delete_doku, name = "dokumentation löschen"),
    path("edit-user/<int:id>/dokumentation/edit-doku/<int:docuId>/", views.update_doku, name = "dokumentation bearbeiten"),
    # path("ai-power/", openAi.prompt),
    path("create-user/<int:id>/befund/", befund_logik.befund, name="befund"),
    path("home/create-user/<int:id>/befund/", befund_logik.befund, name="befund"),
    path("befund/<int:id>/", befund_logik.befund, name= "befund"),
    path('personal-befund/<int:id>/', befund_logik.personal_befund, name='personal_befund'),
    path('personal-befund/<int:id>/update/<str:befund>/<int:befundId>/', befund_logik.update_personal_befund, name='personal_befund'),
    path('personal-befund/<int:id>/new-befund/',befund_logik.new_personal_befund, name = "new-befund"),
    path('personal-befund/<int:id>/delete-befund/<int:befundId>/', befund_logik.delete_personal_befund, name = "delete-befund"),
    path('personal-befund/<int:id>/ki-diagnose/',openAi.get_diagnosis, name = "ki-diagnose"),
    path('home/personal-befund/<int:id>/', befund_logik.personal_befund, name='personal_befund'),
    path('home/personal-befund/<int:id>/update/<str:befund>/<int:befundId>/', befund_logik.update_personal_befund, name='personal_befund'),
    path('home/personal-befund/<int:id>/new-befund/',befund_logik.new_personal_befund, name = "new-befund"),
    path('home/personal-befund/<int:id>/delete-befund/<int:befundId>/', befund_logik. delete_personal_befund, name = "delete-befund"),
    path('home/personal-befund/<int:id>/ki-diagnose/',openAi.get_diagnosis, name = "ki-diagnose"),
    path('home/personal-befund/<int:id>/ki-formulierung/',openAi.ki_formulieren, name = "ki-formulieren"),
    path('personal-befund/<int:id>/ki-formulierung/',openAi.ki_formulieren, name = "ki-formulieren"),
    path('edit-user/<int:id>/dokumentation/ki-formulierung/',openAi.ki_formulieren, name = "ki-formulieren"),
    path('home/edit-user/<int:id>/dokumentation/ki-formulierung/',openAi.ki_formulieren, name = "ki-formulieren"),

    # path("home/create-analog-user/edit-analog-user/<int:id>/", views.edit_analog_user, name="edit-analog-user"),
    # path("create-analog-user/edit-analog-user/<int:id>/", views.edit_analog_user, name="edit-analog-user"),
    # path("home/create-analog-user/edit-analog-user/<int:id>/move-up/", views.move_up_analog, name="move_up_analog"),
    # path("create-analog-user/edit-analog-user/<int:id>/move-up/", views.move_up_analog, name="move_up_analog"),
    # path("home/create-analog-user/edit-analog-user/<int:id>/move-down/", views.move_down_analog, name="move_down_analog"),
    # path("create-analog-user/edit-analog-user/<int:id>/move-down/", views.move_down_analog, name="move_down_analog"),
    # path("create-analog-user/edit-analog-user/<int:id>/delete-user-workout/", views.delete_user_workout_analog, name="delete_user_workout_analog"),
    # path("create-analog-user/edit-analog-user/<int:id>/delete-user-workout/", views.delete_user_workout_analog, name="delete_user_workout_analog"),
    # path("api/<str:partner>/assistant-chat/", openAi.chatApplication, name = "assistant-chat"),
    # path("api/<str:partner>/assistant-chat/sendmessage/", openAi.chatApplication, name = "assistant-chat"),
    # path("api/<str:partner>/anamnese-chat/", openAi.anamnese_chat_applikation, name = "anamnese-chat"),
    # path("api/<str:partner>/anamnese-chat/sendmessage/", openAi.anamnese_chat_applikation, name = "anamnese-chat"),
]