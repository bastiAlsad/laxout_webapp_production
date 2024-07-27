from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from string import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from . import forms

# Test

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ExerciseForm
from .models import (
    LaxoutUser,
    Laxout_Exercise,
    IndexesLaxoutUser,
    IndexesPhysios,
    DoneWorkouts,
    SkippedExercises,
    DoneExercises,
    Coupon,
    LaxoutUserPains,
    PhysioIndexCreationLog,
    Uebungen_Models,
)
from . import models
from .leistungsnachweise import pdf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
import random
import string
from django.contrib.auth import logout, authenticate, login
from datetime import datetime
import json
from django.utils import timezone
from uuid import uuid4
from laxout import lax_ai
from django.urls import reverse


class ExercisesModel:
    def __init__(
        self,
        new_execution,
        new_name,
        new_dauer,
        new_videoPath,
        new_looping,
        new_added,
        new_instruction,
        new_timer,
        new_required,
        new_imagePath,
        new_appId,
        new_skippedAmount,
        new_id,
    ):
        self.execution = new_execution
        self.name = new_name
        self.dauer = new_dauer
        self.videoPath = new_videoPath
        self.looping = new_looping
        self.added = new_added
        self.instruction = new_instruction
        self.timer = new_timer
        self.required = new_required
        self.imagePath = new_imagePath
        self.appId = new_appId
        self.skippedAmount = new_skippedAmount
        self.id = new_id


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect(
            "login"
        )  # Hier 'login' durch den Namen deiner Login-URL ersetzen
    else:
        # Du könntest hier auch eine eigene Logout-Seite rendern
        # return render(request, 'logout.html')
        pass


def random_string(length=100):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def display_login_code(request, logintoken=None):
    return render(request, "laxout_app/display_code.html", {"login_token": logintoken})


# Create your views here.
@login_required(login_url="login")
def home(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    print("Active Admin id{}".format(active_admin_user.is_superuser))
    users_filtert = LaxoutUser.objects.filter(created_by=request.user)
    user_amount = users_filtert.count()

    active_user_amount = 0
    for user in users_filtert:
        print(str(user.last_login.date) + "Last Login date")
        if days_between_today_and_date(user.last_login) < 14:
            active_user_amount += 1

    users = LaxoutUser.objects.all()
    user_list = []
    for user in users:
        if user.created_by == request.user:
            user_list.append(user)

    context = {
        "users": user_list,
        "user_amount": user_amount,
        "active_user_amount": active_user_amount,
        "is_superuser": active_admin_user.is_superuser,
    }
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, "laxout_app/home_mobil.html", context)
    elif user_agent.is_tablet:
        return render(request, "laxout_app/home_mobil.html", context)
    else:
        return render(request, "laxout_app/home.html", context)


@login_required(login_url="login")
def create_exercise(request):
    if request.method == "POST":
        try:
            first = request.POST.get("first")
            second = request.POST.get("second")
        except json.JSONDecodeError as e:
            print("Error in Json Decode")

        form = ExerciseForm(request.POST)

        if form.is_valid():
            print("krass")
            exercise_instance = form.save(commit=False)
            exercise_instance.save()

            # Add First and Second instances
            if first is not None:
                exercise_instance.first.add(models.First.objects.create(first=first))
            if second is not None:
                exercise_instance.second.add(
                    models.Second.objects.create(second=second)
                )
            exercise_instance.second.add(models.Second.objects.create(second=7))

            print(exercise_instance)
            return redirect("/")  # Redirect to the exercise list view
    else:
        form = ExerciseForm()

    return render(request, "laxout_app/create_exercise.html", {"form": form})


def set_exercises_user(user_id, predicted_exercises):
    user = models.LaxoutUser.objects.get(id=user_id)
    for i in predicted_exercises:
        user.exercises.add(i)
    user.save()
    print("Hich")
    print(user.exercises.all())


def send_user_welcome_email(email, user_uid):
    # SMTP-Verbindungsinformationen
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "laxoutapp@gmail.com"
    smtp_password = "jezm nesb fhpj tvrv"

    # E-Mail-Inhalte
    sender_email = "laxoutapp@gmail.com"
    receiver_email = email
    subject = "Herzlich Willkommen"
    link = f"https://dashboardlaxout.eu.pythonanywhere.com/laxout/show-login-code/{user_uid}"

    # HTML-Inhalt der E-Mail
    html_template = Template(
        """
    <!DOCTYPE html>
    <html lang="de">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Willkommen bei Unsere Firma</title>
        <style>
            .wave {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: auto;
                z-index: -1;
            }
        </style>
    </head>

    <body style="font-family: Arial, sans-serif; position: relative;">

        <!-- Wellenförmige Trennlinie -->
        <svg class="wave" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
            <path fill="rgb(243, 242, 244)" fill-opacity="1"
                d="M0,224L48,234.7C96,245,192,267,288,240C384,213,480,139,576,138.7C672,139,768,213,864,229.3C960,245,1056,203,1152,170.7C1248,139,1344,117,1392,106.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1048,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z">
            </path>
        </svg>
        <!-- Firmenlogo -->
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://laxoutapp.com/wp-content/uploads/elementor/thumbs/Original-on-Transparent-2-Kopie-qdvaef4t4wosp4blnwuth1860qdc3tupxko88fkwvo.png"
                    alt="Firmenlogo" style="max-width: 200px;">
            </div>

            <!-- Willkommensnachricht -->
            <div style="text-align: center; margin-bottom: 20px;">
                <h1>Willkommen!</h1>
                <p>Vielen Dank für Ihre Anmeldung bei Laxout. Wir freuen uns, Sie als Nutzer unserer App begrüßen zu dürfen.
                </p>
                <p>Sie können die App 2 Wochen kostenlos und unverbindlich benutzen. Nach der 2 wöchigen Testphase werden wir Sie fragen, ob Sie die App für einmalig 29€ weiternutzen möchten.</p>
                <p>Wenn Sie darauf nicht antworten, oder Sie sich gegen die weitere Nutzung entscheiden, werden wir Ihre Daten löschen und Ihr Zugang wird ungültig. </p>
                <p>Drücken Sie nun bitte auf den <a href="${link}" style=" color: blue;">Loslegen</a> Button, um mit Ihrem Training beginnen!</p>
                <div style="text-align: center; margin: 50px;">
                    <button
                        style="height: 50px; width: 140px; border-radius: 10px; background-color: rgb(176, 224, 230); color: black; cursor: pointer; border: none;">
                        <a href="${link}" style="text-decoration: none; color: white;">Loslegen</a>
                    </button>
                </div>
                <p>Viel Spaß wünscht Ihnen</p>
                <br>
                <p>Ihr Laxout-Team</p>
            </div>

            <!-- Social-Media-Icons -->
            <div style="display: flex; justify-content: center; margin: 40px;">
                <div style="margin-right: 20px;">
                    <a href="https://www.linkedin.com/company/laxout/">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor"
                            class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path fill="rgb(0,0,0)"
                                d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                        </svg>
                    </a>
                </div>
                <div>
                    <a href="https://www.instagram.com/laxoutapp/">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor"
                            class="bi bi-instagram" viewBox="0 0 16 16">
                            <path fill="rgb(0,0,0)"
                                d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334" />
                        </svg>
                    </a>
                </div>
            </div>

            <!-- Footer-Text -->
            <small style="text-align: center; margin-bottom: 50px;">©2024 Laxout, Steffen Friedrich, Firmensitz: Brünnsteinstraße 49, 85435
                Erding. Alle Rechte vorbehalten.</small>
        </div>


    </body>

    </html>
    """
    )

    # Erstellen der MIME-Multipart-Nachricht
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Hinzufügen des HTML-Inhalts zur Nachricht
    html_content = html_template.substitute(link=link)
    msg.attach(MIMEText(html_content, "html"))
    # billing_model, created = models.BillingCount.objects.get_or_create(id=1)
    # billing_count = str(billing_model.billing_count)
    # new_billing_count = billing_model.billing_count+1
    # billing_model.billing_count = new_billing_count
    # billing_model.save()
    # current_billing_id = ""
    # how_many_zeros = 12-len(billing_count)

    # for i in range(how_many_zeros):
    #     current_billing_id+= "0"
    # current_billing_id+= billing_count
    # #Produktion
    # #/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/
    # #Dev
    # #D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/
    # print(f"Current billing Id {current_billing_id}")
    # input_pdf_path = "/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_vorlage.pdf"  # Passe den Pfad zur vorhandenen PDF-Datei an D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/leistungsnachweis
    # output_pdf_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"  # Passe den Pfad für die neu erstellte PDF-Datei an
    # pdf.modifyPdf(input_pdf_path,output_pdf_path,current_billing_id)

    # # Pfad zur PDF-Datei
    # pdf_attachment_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"

    # # Hinzufügen der PDF-Datei als Anhang
    # with open(pdf_attachment_path, 'rb') as pdf_attachment:
    #     part = MIMEApplication(pdf_attachment.read(), 'pdf')
    #     part.add_header('Content-Disposition', f'attachment; filename= {pdf_attachment_path}')
    #     msg.attach(part)

    # SMTP-Verbindung und Versenden der E-Mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    # sender = "laxoutapp@gmail.com"
    # password = "aliy rfnz mtmx xwif"
    # subject = "Herzlich Willkommen bei Laxout"
    # link = f"https://dashboardlaxout.eu.pythonanywhere.com/laxout/show-login-code/{user_uid}"
    # body = f"Hallo, \nschön dass sie sich für Laxout entschieden haben ! \nSie erhalten Ihr individuelles Workout, indem Sie die App über folgenden Link herunterladen:\n{link} \nAußerdem benötigt Laxout während des Anmeldeprozesses außerdem Zugriff auf Ihre Zwischenablage des Smartphones.\n \nViel Erfolg wünscht Ihnen Ihr Laxout-Team "
    # reciever = email
    # message = MIMEMultipart()
    # message["From"] = sender
    # message["Subject"] = subject
    # message.attach(MIMEText(body, "plain"))
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(sender, password)
    # text = message.as_string()
    # server.sendmail(sender, reciever, text)
    # server.quit()


@login_required(login_url="login")
def create_user(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            insteance = form.save(commit=False)
            befund = form.cleaned_data["befund"]

            insteance.created_by = request.user
            tree = models.LaxTree.objects.create()
            insteance.lax_tree_id = tree.id
            new_user_uid = str(uuid4())
            while LaxoutUser.objects.filter(user_uid=new_user_uid).exists():
                new_user_uid = str(uuid4())
            insteance.user_uid = new_user_uid
            email = form.cleaned_data.get("email_adress")
            note = request.POST.get("selected_illness")
            insteance.note = note
            insteance.save()
            if befund == True:
                return redirect(f"{insteance.id}/befund/")
            # lax_ai.train_model(request.user.id)
            # predicted_exercises_ids = lax_ai.predict_exercise(note)

            exercises = []
            print(f"note{note}")

            ai_training_data = models.AiTrainingDataGlobal.objects.filter(
                illness=note
            ).last()

            # , created_by=request.user.id

            if ai_training_data != None:
                list_order_objects = (
                    models.Laxout_Exercise_Order_For_User.objects.filter(
                        laxout_user_id=ai_training_data.id
                    )
                )
                # print("LIST Skipped LENGTH {}".format(skipped_exercises))
                sorted_list = sorted(
                    list_order_objects, key=lambda x: x.order
                )  # Werden der größe nach Sotiert
                # print("Sorted List {}".format(sorted_list))
                related_exercises_rigth_order = []

                for i in sorted_list:
                    related_exercises_rigth_order.append(
                        models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
                    )

                for i in related_exercises_rigth_order:
                    user_instance = insteance
                    # es wird geschaut, ob es schon eine Reihenfolge gibt

                    exercise_to_add = Laxout_Exercise.objects.create(
                        execution=Uebungen_Models.objects.get(id=i.appId).execution,
                        name=Uebungen_Models.objects.get(id=i.appId).name,
                        dauer=Uebungen_Models.objects.get(id=i.appId).dauer,
                        videoPath=Uebungen_Models.objects.get(id=i.appId).videoPath,
                        looping=Uebungen_Models.objects.get(id=i.appId).looping,
                        added=False,
                        instruction="",
                        timer=Uebungen_Models.objects.get(id=i.appId).timer,
                        required=Uebungen_Models.objects.get(id=i.appId).required,
                        imagePath=Uebungen_Models.objects.get(id=i.appId).imagePath,
                        appId=Uebungen_Models.objects.get(id=i.appId).id,
                        onlineVideoPath=Uebungen_Models.objects.get(
                            id=i.appId
                        ).onlineVideoPath,
                    )
                    exercises.append(exercise_to_add)

            set_exercises_user(insteance.id, exercises)
            print("ZZZ")
            print(exercises)
            print(insteance.id)
            # print(lax_ai.predict_exercise(note))
            send_user_welcome_email(email, insteance.user_uid)
            models.ChatDataModel.objects.create(
                message="Willkommen bei der Laxout Chat funktion. Sollten Sie Fragen zur App oder zu Übungen haben, können Sie diese hier stellen. Viel Spaß beim benutzen der App!",
                created_by=insteance.id,
                admin_id=request.user.id,
            )
            return redirect(f"/edit-user/{insteance.id}")

    else:
        ilness_list_obj = models.AiTrainingDataGlobal.objects.all()
        ilness_list = []
        for i in ilness_list_obj:
            if i.illness not in ilness_list:
                filterd_objects = ilness_list_obj.filter(illness=i.illness)
                item = filterd_objects.last()
                print(item.illness)
                ilness_list.append(item.illness)

        # for i in ilness_list_obj:
        #     ilness_list.append(i.illness)
        form = UserForm()
        return render(
            request,
            "laxout_app/create_user.html",
            {
                "form": form,
                "is_superuser": active_admin_user.is_superuser,
                "illness_list": ilness_list,
            },
        )


@login_required(login_url="login")
def delete_user(request, id=None):
    if id != None:
        object_to_delte = LaxoutUser.objects.get(id=id)
        if request.user == object_to_delte.created_by:
            for exercis in object_to_delte.exercises.all():
                exercis.delete()
            for index in IndexesLaxoutUser.objects.filter(created_by=id).all():
                index.delete()
            for coupon in object_to_delte.coupons.all():
                coupon.delete()
            for doneWorkout in DoneWorkouts.objects.filter(laxout_user_id=id).all():
                doneWorkout.delete()
            for skippedExercise in SkippedExercises.objects.filter(
                laxout_user_id=id
            ).all():
                skippedExercise.delete()
            for doneExercise in DoneExercises.objects.filter(laxout_user_id=id).all():
                doneExercise.delete()
            for doneWorkout in DoneWorkouts.objects.filter(laxout_user_id=id).all():
                doneWorkout.delete()
            for order in models.Laxout_Exercise_Order_For_User.objects.filter(
                laxout_user_id=id
            ).all():
                order.delete()
            for pain in models.LaxoutUserPains.objects.filter(created_by=id).all():
                pain.delete()
            models.SuccessControll.objects.filter(created_by=id).delete()
            object_to_delte.delete()
        return redirect("/home")
    return redirect("/home")


@login_required(login_url="login")
def edit_user(request, id=None):
    user = LaxoutUser.objects.get(id=id)

    if request.method == "POST":
        user.last_meet = timezone.datetime.today()
        user.save()

    last_meet = user.last_meet.strftime("%Y-%m-%d")
    indexes = []
    workouts_instance = []
    workout_dates = []

    for index in IndexesLaxoutUser.objects.all():
        if index.created_by == id:
            indexes.append(index)

    for workout in DoneWorkouts.objects.all():
        if workout.laxout_user_id == id:
            workouts_instance.append(workout)

    workout_dates = [date.date.strftime("%Y-%m-%d") for date in workouts_instance]
    labels = []
    count = 0
    to_put = 0
    store = []
    users_indexes = []
    unique_w_d = set(workout_dates)
    workout_dates = list(unique_w_d)

    for index in indexes:
        if index.creation_date not in labels:
            labels.append(index.creation_date)

    for i in labels:
        for z in indexes:
            if i == z.creation_date:
                count += z.index
                store.append(z)

        to_put = count / len(store)
        count = 0
        store = []
        users_indexes.append(to_put)

    ###skip logik###

    current_exercises = user.exercises.all()

    current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )  # es wird geschaut, ob es schon eine Reihenfolge gibt

    print(f"ids der geradigen order:")
    for i in current_order_objects:
        print(i.laxout_exercise_id)

    if len(current_order_objects) == 0 and len(current_exercises) != 0:
        print("There was a diffenrence")
        order = 1
        for i in current_exercises:
            models.Laxout_Exercise_Order_For_User.objects.create(
                laxout_user_id=id, laxout_exercise_id=i.id, order=order
            )

            order += 1
        print("length")
        print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

    lenght_order_objects_list = len(current_order_objects)

    print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

    users_exercises_skipped = []

    skipped_exercises = models.SkippedExercises.objects.filter(laxout_user_id=id)

    list_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )
    # print("LIST Skipped LENGTH {}".format(skipped_exercises))
    sorted_list = sorted(
        list_order_objects, key=lambda x: x.order
    )  # Werden der größe nach Sotiert
    # print("Sorted List {}".format(sorted_list))
    exercise_ids = []

    for i in sorted_list:
        exercise_ids.append(i.laxout_exercise_id)
    skipped_amount = 0

    for order in sorted_list:
        # print("RELEVANT ERROR ID")
        # print(order.laxout_exercise_id)
        try:
            exercise = models.Laxout_Exercise.objects.get(id=order.laxout_exercise_id)
            for skipped_exercis in skipped_exercises:

                if exercise.id == skipped_exercis.skipped_exercise_id:
                    skipped_amount += 1
                    print(skipped_amount)

            users_exercises_skipped.append(
                ExercisesModel(
                    new_added=exercise.added,
                    new_appId=exercise.appId,
                    new_dauer=exercise.dauer,
                    new_execution=exercise.execution,
                    new_imagePath=exercise.imagePath,
                    new_instruction=exercise.instruction,
                    new_looping=exercise.looping,
                    new_name=exercise.name,
                    new_required=exercise.required,
                    new_timer=exercise.timer,
                    new_videoPath=exercise.videoPath,
                    new_skippedAmount=skipped_amount,
                    new_id=exercise.id,
                )
            )
            skipped_amount = 0

            skipped_amount = 0
        except:
            print("EXEPTION THROUGH DELETE AFTER AI GENERATION OF EXERCISES")

    print(
        "LENGHT EXERCISE LIST {}".format(users_exercises_skipped)
    )  # sie heißen nur skipped weil die skipped logik drinnen steckt, sind aber die ganz normalen Übungen
    print("Exercise ids from user with note:{}".format(user.note))
    for i in users_exercises_skipped:
        print(i.appId)
    laxout_user_pains_instances = models.LaxoutUserPains.objects.filter(created_by=id)
    index_labels = []
    month_year_instances = []
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    for she in laxout_user_pains_instances:
        append_she = True
        for i in month_year_instances:
            if i.for_month == she.for_month and i.for_year == she.for_year:
                append_she = False

        if append_she:
            index_labels.append(she.for_month)
            month_year_instances.append(she)

    for i in month_year_instances:
        current_pains = models.LaxoutUserPains.objects.filter(
            created_by=i.created_by, for_month=i.for_month, for_year=i.for_year
        )
        six_eight = 0
        zero_two = 0
        three_five = 0
        nine_ten = 0
        for ii in current_pains:
            six_eight = six_eight + ii.six_eight
            zero_two = zero_two + ii.zero_two
            three_five = three_five + ii.theree_five
            nine_ten = nine_ten + ii.nine_ten
        zero_two_pain.append(zero_two)
        theree_five_pain.append(three_five)
        six_eight_pain.append(six_eight)
        nine_ten_pain.append(nine_ten)

    average_pain_list_user = []
    for i in range(len(zero_two_pain)):
        average_pain = 0
        average_pain += zero_two_pain[i]
        average_pain += theree_five_pain[i]
        average_pain += six_eight_pain[i]
        average_pain += nine_ten_pain[i]
        average_pain = average_pain / 4
        average_pain_list_user.append(average_pain)

    better_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=True)
    )
    worse_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=False)
    )

    # Train ai with the new data
    # lax_ai.train_model(request.user.id)

    context = {
        "user": user,
        "users": user,
        "workouts": users_exercises_skipped,
        "userIndexes": json.dumps(users_indexes),
        "labels": json.dumps(labels),
        "workoutDates": json.dumps(workout_dates),
        "lastMeet": json.dumps(last_meet),
        "index_labels": json.dumps(index_labels),
        # "test": json.dumps(indexes),
        "zero_two_pain": json.dumps(zero_two_pain),
        "three_five_pain": json.dumps(theree_five_pain),
        "six_eight_pain": json.dumps(six_eight_pain),
        "nine_ten_pain": json.dumps(nine_ten_pain),
        "int": user.instruction_in_int,
        "better": better_success_controll_count,
        "worse": worse_success_controll_count,
    }

    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, "laxout_app/edit_user_mobile.html", context)
    elif user_agent.is_tablet:
        return render(request, "laxout_app/edit_user_mobile.html", context)
    else:
        return render(request, "laxout_app/edit_user.html", context)


def get_workout_list(first, second):
    to_return = []
    uebungen_to_append = []
    exercises_to_browse = models.Uebungen_Models.objects.all()
    # Nacken
    if first == 0 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)

    if first == 0 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 0 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 0 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Schultern
    if first == 1 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # mittlerer Rücken
    if first == 2 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # bauch rumpf
    if first == 3 and second == 0:
        uebungen_to_append = []
    if first == 3 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 3 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 3 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Unterer Rücken
    if first == 4 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 4 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 4 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)

    if first == 4 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Beine Füße
    if first == 5 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Arme Hände

    if first == 6 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 6 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 6 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)

    if first == 6 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)

    return to_return


@login_required(login_url="login")
def add_exercises(request, id=None, first=0, second=0):
    print("ececuted")
    workout_list = []
    if request.method == "GET":
        first = request.GET.get("first", 0)
        second = request.GET.get("second", 0)
        print(first)
        print(second)
        workout_list = get_workout_list(int(first), int(second))
        print("handled request")
        print(workout_list)
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            return render(
                request,
                "laxout_app/add_exercises_mobile.html",
                {"workouts": workout_list},
            )
        elif user_agent.is_tablet:
            return render(
                request,
                "laxout_app/add_exercises_mobile.html",
                {"workouts": workout_list},
            )
        else:
            return render(
                request, "laxout_app/add_exercises.html", {"workouts": workout_list}
            )

    if request.method == "POST":
        new_execution = request.POST.get("execution")
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        new_id = request.POST.get("id")
        print(new_dauer)
        if new_dauer == "":
            new_dauer = Uebungen_Models.objects.get(id=new_id).dauer

        user_instance = LaxoutUser.objects.get(id=id)

        current_exercises = user_instance.exercises.all()
        if len(current_exercises) != 0:
            models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
        current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
            laxout_user_id=id
        )  # es wird geschaut, ob es schon eine Reihenfolge gibt
        if len(current_order_objects) == 0 and len(current_exercises) != 0:
            print("There was a diffenrence")
            order = 1
            for i in current_exercises:
                models.Laxout_Exercise_Order_For_User.objects.create(
                    laxout_user_id=id, laxout_exercise_id=i.id, order=order
                )
                order += 1
            print("length")
            print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

        lenght_order_objects_list = len(current_order_objects)

        print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

        exercise_to_add = Laxout_Exercise.objects.create(
            execution=new_execution,
            name=Uebungen_Models.objects.get(id=new_id).name,
            dauer=new_dauer,
            videoPath=Uebungen_Models.objects.get(id=new_id).videoPath,
            looping=Uebungen_Models.objects.get(id=new_id).looping,
            added=False,
            instruction="",
            timer=Uebungen_Models.objects.get(id=new_id).timer,
            required=Uebungen_Models.objects.get(id=new_id).required,
            imagePath=Uebungen_Models.objects.get(id=new_id).imagePath,
            appId=new_id,
            onlineVideoPath=Uebungen_Models.objects.get(id=new_id).onlineVideoPath,
        )
        order_new_exercise = len(current_order_objects) + 1

        print(f"ID der hinzugefügten Übung {exercise_to_add.id}")

        models.Laxout_Exercise_Order_For_User.objects.create(
            laxout_user_id=id,
            laxout_exercise_id=exercise_to_add.id,
            order=order_new_exercise,
        )

        print(exercise_to_add.dauer)
        exercise_to_add.save()
        user_instance.exercises.add(exercise_to_add)
        if request.user == user_instance.created_by:
            user_instance.save()

    workout_list = get_workout_list(0, 0)
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, "laxout_app/add_exercises_mobile.html", {"workouts": workout_list, "userId": id})
    elif user_agent.is_tablet:
        return render(request, "laxout_app/add_exercises_mobile.html", {"workouts": workout_list, "userId": id})
    else:
        return render(request, "laxout_app/add_exercises.html", {"workouts": workout_list, "userId": id})

@login_required(login_url="login")
def edit_user_workout(
    request,
    id=None,
):
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        print("new execution:{}".format(new_execution))
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        new_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        print("new dauer:{}".format(new_dauer))
        print("new id:{}".format(new_id))
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(id=new_id)
        if new_execution:
            exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        user_instance.save()
        models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, "laxout_app/edit_user_mobile.html")
    elif user_agent.is_tablet:
        return render(request, "laxout_app/edit_user_mobile.html")
    else:
        return render(request, "laxout_app/edit_user.html")




@login_required(login_url="login")
def delete_user_workout(
    request,
    id=None,
):
    if request.method == "POST":
        to_delete_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(
            id=to_delete_id
        )  # <---- kann ich so auf die Übung zugreifen, die ich bearbeiten möchte ?
        if request.user == user_instance.created_by:
            exercise_to_edit.delete()
            user_instance.save()
            print("to delete id")
            print(to_delete_id)
            to_delete = models.Laxout_Exercise_Order_For_User.objects.get(
                laxout_exercise_id=to_delete_id, laxout_user_id=user_id
            )
            to_delete.delete()

            list_order_exercises = models.Laxout_Exercise_Order_For_User.objects.filter(
                laxout_user_id=id
            )
            if len(list_order_exercises) != 0:
                right_order_exercises = []
                for i in list_order_exercises:
                    right_order_exercises.append(
                        models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
                    )

                sorted_list = sorted(right_order_exercises, key=lambda x: x.order)
                order = 1
                for i in sorted_list:
                    instance = models.Laxout_Exercise_Order_For_User.objects.get(
                        laxout_exercise_id=i.laxout_exercise_id,
                        laxout_user_id=i.laxout_user_id,
                    ).order = order
                    instance.save()
                    order += 1
            models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, "laxout_app/edit_user_mobile.html")
    elif user_agent.is_tablet:
        return render(request, "laxout_app/edit_user_mobile.html")
    else:
        return render(request, "laxout_app/edit_user.html")


def days_between_today_and_date(input_datetime):
    # Assuming last_login_2 is stored in the same timezone as the server
    input_datetime = input_datetime.replace(tzinfo=None)  # Make it naive
    current_datetime = datetime.now()

    time_difference = current_datetime - input_datetime
    days_difference = time_difference.days

    return days_difference


@login_required(login_url="login")
def analyses(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    # how many users
    users = LaxoutUser.objects.filter(created_by=request.user)
    user_amount = users.count()
    user_indexes = IndexesLaxoutUser.objects.filter(
        created_by=request.user.id, creation_date=datetime.now().month
    )
    devide_by = len(user_indexes)
    devide = 0

    for user_index in user_indexes:
        devide += user_index.index

    if devide == 0:
        physio_index = 0

    else:
        physio_index = devide / devide_by

    if physio_index == None:
        physio_index = 0
        print("physio index was none")

    active_user_amount = 0

    for user in users:
        print(str(user.last_login_2.date) + "Last Login date")
        if days_between_today_and_date(user.last_login_2) < 14:
            active_user_amount += 1

    all_physio_indexes = IndexesPhysios.objects.filter(
        for_month=datetime.now().month,
        created_by=request.user.id,
        for_year=datetime.now().year,
    )

    if len(all_physio_indexes) != 0:
        current_physio_index_object = all_physio_indexes[len(all_physio_indexes) - 1]
    if len(all_physio_indexes) == 0:
        try:
            PhysioIndexCreationLog.objects.get(
                created_by=request.user.id,
                for_month=datetime.now().month,
                for_year=datetime.now().year,
            )
        except:
            current_physio_index_object = IndexesPhysios.objects.create(
                for_month=datetime.now().month, created_by=request.user.id
            )
            PhysioIndexCreationLog.objects.create(created_by=request.user.id)

    current_physio_index_object.indexs = physio_index
    current_physio_index_object.save()

    logins = current_physio_index_object.logins
    tests = current_physio_index_object.tests
    # tests = 0
    # logins = 0

    all_instances = IndexesPhysios.objects.filter(created_by=request.user.id)

    substitude_instances = []
    counter = 0
    if len(all_instances) > 10:
        for insteance in all_instances:
            if counter > len(all_instances) - 10:
                substitude_instances.append(insteance)
            counter += 1
        all_instances = substitude_instances

    indexes = []
    index_labels = []
    laxout_user_pains_instances = LaxoutUserPains.objects.filter(
        admin_id=request.user.id
    )
    month_year_instances = []
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    print("LENGHT Pains LIST {}".format(len(laxout_user_pains_instances)))

    for she in laxout_user_pains_instances:
        append_month_year = True
        for i in month_year_instances:
            if i.for_month == she.for_month and i.for_year == she.for_year:
                append_month_year = False

        if append_month_year:
            month_year_instances.append(she)
            index_labels.append(she.for_month)

    for i in month_year_instances:
        current_pains = models.LaxoutUserPains.objects.filter(
            created_by=i.created_by, for_month=i.for_month, for_year=i.for_year
        )
        six_eight = 0
        zero_two = 0
        three_five = 0
        nine_ten = 0

        for ii in current_pains:
            six_eight = six_eight + ii.six_eight
            zero_two = zero_two + ii.zero_two
            three_five = three_five + ii.theree_five
            nine_ten = nine_ten + ii.nine_ten
        zero_two_pain.append(zero_two)
        theree_five_pain.append(three_five)
        six_eight_pain.append(six_eight)
        nine_ten_pain.append(nine_ten)

    print("9-10{}".format(nine_ten_pain))
    print("8-6{}".format(six_eight_pain))
    print("3-5{}".format(theree_five_pain))
    print("0-2{}".format(zero_two_pain))

    context = {
        "user_amount": user_amount,
        "active_user_amount": active_user_amount,
        "logins": logins,
        "tests": tests,
        "index_labels": json.dumps(index_labels),
        "test": json.dumps(indexes),
        "zero_two_pain": json.dumps(zero_two_pain),
        "three_five_pain": json.dumps(theree_five_pain),
        "six_eight_pain": json.dumps(six_eight_pain),
        "nine_ten_pain": json.dumps(nine_ten_pain),
        "is_superuser": active_admin_user.is_superuser,
    }
    return render(request, "laxout_app/analyses.html", context)


@login_required(login_url="login")
def post_user_instruction(request, id=None):
    new_instruction = request.POST.get("instruction")
    user_insance = LaxoutUser.objects.get(id=id)
    user_insance.instruction = new_instruction
    user_insance.save()
    return HttpResponse("All clear")


@login_required(login_url="login")
def post_user_mail(request, id=None):
    new_mail = request.POST.get("mail")
    user_insance = LaxoutUser.objects.get(id=id)
    user_insance.email_adress = new_mail
    user_insance.save()
    return HttpResponse("All clear")


# from . import signals


class UebungList:
    def __init__(
        self,
        looping,
        timer,
        execution,
        name,
        videoPath,
        dauer,
        imagePath,
        added,
        instruction,
        required,
        onlineVidePath,
    ):
        self.looping = looping
        self.timer = timer
        self.execution = execution
        self.name = name
        self.videoPath = videoPath
        self.dauer = dauer
        self.imagePath = imagePath
        self.added = added
        self.instruction = instruction
        self.required = required
        self.onlineVidePath = onlineVidePath


additionalUebungList2 = []


uebungen_to_append00 = []  # Nacken
uebungen_to_append01 = []
uebungen_to_append02 = []
uebungen_to_append07 = []
uebungen_to_append10 = []  # Schultern
uebungen_to_append11 = []
uebungen_to_append12 = []
uebungen_to_append17 = []
uebungen_to_append20 = []  # Mittlerer Rücken
uebungen_to_append21 = []
uebungen_to_append22 = []
uebungen_to_append27 = []
uebungen_to_append30 = []  # Bauch Rumpf
uebungen_to_append31 = []
uebungen_to_append32 = []
uebungen_to_append37 = []
uebungen_to_append40 = []  # Unterer Rücken
uebungen_to_append41 = []
uebungen_to_append42 = []
uebungen_to_append47 = []
uebungen_to_append50 = []  # Beine Füße
uebungen_to_append51 = []
uebungen_to_append52 = []
uebungen_to_append57 = []
uebungen_to_append60 = []  # Arme Hände
uebungen_to_append61 = []
uebungen_to_append62 = []
uebungen_to_append67 = [254, 255, 256, 257]


def inizialize_first_second(
    debugValue,
):  # Falls die Ids in der Datenbank durch löschungen verzogen werden kommt ein debugValue hinzu, der die Ids anpasst ab Übung 210 wird der wert relevant (387)
    for i in uebungen_to_append00:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append01:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append02:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append07:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append10:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append11:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append12:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append17:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append20:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append21:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append22:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append27:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append30:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append31:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append32:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append37:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append40:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append41:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append42:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append47:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append50:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append51:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append52:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append57:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append60:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append61:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append62:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append67:
        instance_exercise = models.Uebungen_Models.objects.get(id=i + debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()


@login_required(login_url="login")
def admin_power(request):
    ##Update Executions
    # id = 1
    # all_exercises = models.Uebungen_Models.objects.all()
    # print("Test")
    # print(len(uebungen))
    # print(len(all_exercises))
    # for i in uebungen:
    #     exercise = models.Uebungen_Models.objects.get(id=id)
    #     exercise.execution = i.execution
    #     exercise.save()
    #     id += 1
    # print("done")

    # Create new Exercises
    for i in additionalUebungList2:
        Uebungen_Models.objects.create(
            looping=i.looping,
            timer=i.timer,
            execution=i.execution,
            name=i.name,
            videoPath=i.videoPath,
            dauer=i.dauer,
            imagePath=i.imagePath,
            added=i.added,
            instruction=i.instruction,
            required=i.required,
            onlineVideoPath=i.onlineVidePath,
        )
    inizialize_first_second(
        0
    )  # auf pythonanywhere ist dieser wert aktuell 387 erklärung bei 'def' inizialize..

    # models.Uebungen_Models.objects.all().delete()
    # models.First.objects.all().delete()
    # models.Second.objects.all().delete()

    # from . import signals
    # for i in signals.uebungen:
    #             Uebungen_Models.objects.create(
    #                 looping=i.looping,
    #                 timer=i.timer,
    #                 execution=i.execution,
    #                 name=i.name,
    #                 videoPath=i.videoPath,
    #                 dauer=i.dauer,
    #                 imagePath=i.imagePath,
    #                 added=i.added,
    #                 instruction=i.instruction,
    #                 required=i.required,
    #                 onlineVideoPath = i.onlineVidePath

    #             )
    # inizialize_first_second()

    # for i in models.LaxoutUser.objects.all():
    #     laxout_tree = models.LaxTree.objects.create()
    #     i.lax_tree_id = laxout_tree.id
    #     i.save()

    return HttpResponse("all clear")


@login_required(login_url="login")
def move_up(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        user = models.LaxoutUser.objects.get(id=id)
        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_up.order == 1:
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")
        order_to_move_up = item_to_move_up.order
        order_to_move_down = item_to_move_up.order - 1
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_down
        )
        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()
        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": user.exercises.all()}
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
           return render(request, "laxout_app/edit_user_mobile.html",context)
        elif user_agent.is_tablet:
           return render(request, "laxout_app/edit_user_mobile.html",context)
        else:
            return render(request, "laxout_app/edit_user.html",context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def move_down(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        user = models.LaxoutUser.objects.get(id=id)
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_down.order == len(
            models.Laxout_Exercise_Order_For_User.objects.filter(laxout_user_id=id)
        ):
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")

        order_to_move_down = item_to_move_down.order
        order_to_move_up = item_to_move_down.order + 1

        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_up
        )

        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()

        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": user.exercises.all()}
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
           return render(request, "laxout_app/edit_user_mobile.html",context)
        elif user_agent.is_tablet:
           return render(request, "laxout_app/edit_user_mobile.html",context)
        else:
            return render(request, "laxout_app/edit_user.html",context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def set_instruction_int(request):
    try:
        user = models.LaxoutUser.objects.get(id=request.POST.get("id"))
        print(user.id)
        instruction_int = request.POST.get("int")
        print(instruction_int)
        user.instruction_in_int = instruction_int
        user.save()
        return HttpResponse("OK 2_0_0")
    except:
        print(Exception)
        print("Kacke")
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def chats(request):
    users = models.LaxoutUser.objects.filter(created_by=request.user.id)

    return render(request, "laxout_app/chats.html", {"users": users})


@login_required(login_url="login")
def personal_chat(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    personal_chat = models.ChatDataModel.objects.filter(created_by=id)
    print(f"Länge des Chats{len(personal_chat)}")
    return render(
        request,
        "laxout_app/personal-chat.html",
        {"user": user, "personal_chat": personal_chat},
    )


@login_required(login_url="login")
def post_message(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    message = request.POST.get("message")
    is_sender = request.POST.get("is_sender")
    user.user_has_seen_chat = False
    user.save()
    models.ChatDataModel.objects.create(
        message=message, is_sender=False, created_by=id, admin_id=request.user.id
    )
    return HttpResponse("OK")


@login_required(login_url="login")
def admin_has_seen(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    user.admin_has_seen_chat = True
    user.save()
    return HttpResponse("OK")


@login_required(login_url="login")
def edit_plans(request):
    plans_list = models.AiTrainingDataGlobal.objects.all()
    print(f"plans_list{plans_list}")
    return render(
        request,
        "laxout_app/plaene.html",
        {
            "plans_list": plans_list,
        },
    )


@login_required(login_url="login")
def delete_plan(request, id=None):
    if id != None:
        print("id nicht none")
        plan_to_delete = models.AiTrainingDataGlobal.objects.get(id=id)
        if plan_to_delete.created_by == request.user.id:
            print("gelöscht")
            plan_to_delete.delete()
    return render(request, "laxout_app/plaene.html")


@login_required(login_url="login")
def edit_plan(request, id=None):

    plan = models.AiTrainingDataGlobal.objects.get(id=id)

    related_exercises = plan.related_exercises.all()

    related_exercises = []

    current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )  # es wird geschaut, ob es schon eine Reihenfolge gibt

    print(f"ids der geradigen order:")
    for i in current_order_objects:
        print(i.laxout_exercise_id)

    if len(current_order_objects) == 0 and len(related_exercises) != 0:
        print("There was a diffenrence")
        order = 1
        for i in related_exercises:
            models.Laxout_Exercise_Order_For_User.objects.create(
                laxout_user_id=id, laxout_exercise_id=i.id, order=order
            )

            order += 1
        print("length")
        print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

    print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

    list_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )
    # print("LIST Skipped LENGTH {}".format(skipped_exercises))
    sorted_list = sorted(
        list_order_objects, key=lambda x: x.order
    )  # Werden der größe nach Sotiert
    # print("Sorted List {}".format(sorted_list))
    related_exercises_rigth_order = []

    for i in sorted_list:
        related_exercises_rigth_order.append(
            models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
        )

    return render(
        request,
        "laxout_app/edit_plan.html",
        {"related_exercises": related_exercises_rigth_order, "plan": plan},
    )


@login_required(login_url="login")
def add_exercises_plan(request, id=None, first=0, second=0):
    print("ececuted")
    workout_list = []
    if request.method == "GET":
        first = request.GET.get("first", 0)
        second = request.GET.get("second", 0)
        print(first)
        print(second)
        workout_list = get_workout_list(int(first), int(second))
        print("handled request")
        print(workout_list)
        return render(
            request, "laxout_app/add_exercises.html", {"workouts": workout_list}
        )

    if request.method == "POST":
        new_execution = request.POST.get("execution")
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        new_id = request.POST.get("id")
        print(new_dauer)
        if new_dauer == "":
            new_dauer = models.Uebungen_Models.objects.get(id=new_id).dauer

        programm_instance = models.AiTrainingDataGlobal.objects.get(id=id)
        current_exercises = programm_instance.related_exercises.all()

        current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
            laxout_user_id=id
        )
        if len(current_order_objects) == 0 and len(current_exercises) != 0:
            print("There was a diffenrence")
            order = 1
            for i in current_exercises:
                models.Laxout_Exercise_Order_For_User.objects.create(
                    laxout_user_id=id, laxout_exercise_id=i.id, order=order
                )
                order += 1

        exercise_to_add = models.Laxout_Exercise.objects.create(
            execution=new_execution,
            name=models.Uebungen_Models.objects.get(id=new_id).name,
            dauer=new_dauer,
            videoPath=models.Uebungen_Models.objects.get(id=new_id).videoPath,
            looping=models.Uebungen_Models.objects.get(id=new_id).looping,
            added=False,
            instruction="",
            timer=models.Uebungen_Models.objects.get(id=new_id).timer,
            required=models.Uebungen_Models.objects.get(id=new_id).required,
            imagePath=models.Uebungen_Models.objects.get(id=new_id).imagePath,
            appId=new_id,
            onlineVideoPath=models.Uebungen_Models.objects.get(
                id=new_id
            ).onlineVideoPath,
        )
        order_new_exercise = len(current_order_objects) + 1

        print(f"ID der hinzugefügten Übung {exercise_to_add.id}")

        models.Laxout_Exercise_Order_For_User.objects.create(
            laxout_user_id=id,
            laxout_exercise_id=exercise_to_add.id,
            order=order_new_exercise,
        )

        print(exercise_to_add.dauer)
        exercise_to_add.save()

        if request.user.id == programm_instance.created_by:
            programm_instance.related_exercises.add(exercise_to_add)
            programm_instance.save()

    workout_list = get_workout_list(0, 0)

    return render(
        request,
        "laxout_app/add_exercises.html",
        {"workouts": workout_list, "userId": id},
    )


@login_required(login_url="login")
def edit_plan_exercise(
    request,
    id=None,
):
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        print("new execution:{}".format(new_execution))
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        exercise_to_edit_id = request.POST.get("id")
        plan_id = request.POST.get("planId")
        print("plan_id:{}".format(plan_id))
        programm_instance = models.AiTrainingDataGlobal.objects.get(id=plan_id)
        exercise_to_edit = programm_instance.related_exercises.get(
            id=exercise_to_edit_id
        )
        if new_execution:
            exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        programm_instance.save()
    return render(
        request,
        "laxout_app/edit_plan.html",
    )


@login_required(login_url="login")
def delete_plan_exercise(
    request,
    id=None,
):
    if request.method == "POST":
        print("ANGEKOMMEN")
        to_delete_id = request.POST.get("id")
        print(f"to delet id {to_delete_id}")
        instance = models.AiTrainingDataGlobal.objects.get(id=id)
        exercise_to_delete = models.Laxout_Exercise.objects.get(id=to_delete_id)

        if request.user.id == instance.created_by:
            exercise_to_delete.delete()
            instance.save()
            print("to delete id")
            print(to_delete_id)
            to_delete = models.Laxout_Exercise_Order_For_User.objects.get(
                laxout_exercise_id=to_delete_id, laxout_user_id=id
            )
            to_delete.delete()

            list_order_exercises = models.Laxout_Exercise_Order_For_User.objects.filter(
                laxout_user_id=id
            )
            if len(list_order_exercises) != 0:
                right_order_exercises = []
                for i in list_order_exercises:
                    right_order_exercises.append(
                        models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
                    )

                sorted_list = sorted(right_order_exercises, key=lambda x: x.order)
                order = 1
                for i in sorted_list:
                    instance = models.Laxout_Exercise_Order_For_User.objects.get(
                        laxout_exercise_id=i.laxout_exercise_id,
                        laxout_user_id=i.laxout_user_id,
                    ).order = order
                    instance.save()
                    order += 1

    return render(
        request,
        "laxout_app/edit_plan.html",
    )


@login_required(login_url="login")
def create_ai_training_data(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    if request.method == "POST":
        form = forms.TrainingDataForm(request.POST)
        print("OK")
        if form.is_valid():
            illness = form.cleaned_data.get("illness")
            print(f"illness{illness}")
            models.AiTrainingDataGlobal.objects.get_or_create(
                illness=illness, created_by=request.user.id
            )
            # print(lax_ai.predict_exercise(note))
        return redirect("/home")

    else:
        form = forms.TrainingDataForm
        return render(
            request,
            "laxout_app/create_trainingdata.html",
            {
                "form": form,
                "is_superuser": active_admin_user.is_superuser,
            },
        )


@login_required(login_url="login")
def move_up_plan(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        plan = models.AiTrainingDataGlobal.objects.get(id=id)
        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_up.order == 1:
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")
        order_to_move_up = item_to_move_up.order
        order_to_move_down = item_to_move_up.order - 1
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_down
        )
        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()
        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": plan.related_exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def move_down_plan(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        plan = models.AiTrainingDataGlobal.objects.get(id=id)
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_down.order == len(
            models.Laxout_Exercise_Order_For_User.objects.filter(laxout_user_id=id)
        ):
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")

        order_to_move_down = item_to_move_down.order
        order_to_move_up = item_to_move_down.order + 1

        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_up
        )

        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()

        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": plan.related_exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


####befund logik
@login_required(login_url="login")
def befund(request, id=None):
    test_list_json = request.POST.get("test_list")
    if test_list_json:
        test_list = json.loads(
            test_list_json
        )  # Decode the JSON string to a Python list
        models.StandartBefund.objects.get_or_create(
            created_by=request.user, created_for=id
        )
        models.Befund.objects.get_or_create(created_for=id, befund="standart_befund")
        for test in test_list:
            if test == "fragenevaluation_icf":
                models.FragenevaluationNachICFKategorien.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="fragenevaluation_icf"
                )
            if test == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
                models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id,
                    befund="fragenevaluation_bio_psycho_sozial_krankheitsmodell",
                )
            if test == "w_fragen":
                models.FragenevaluationenNachDen7WFragen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="w_fragen")
            if test == "stand_reha_phase":
                models.StandDerReHaPhase.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="stand_reha_phase")
            if test == "nebenerkrankungen_medikamente":
                models.NebenerkrankungenMedikamente.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="nebenerkrankungen_medikamente"
                )
            if test == "historia_morbis":
                models.HistoriaMorbis.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="historia_morbis")

            if test == "nrs_numeric_rating_scale":
                models.NrsNumericRatingScale.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="nrs_numeric_rating_scale"
                )
            if test == "aktive_beweglichkeit":
                models.AktiveBeweglichkeit.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="aktive_beweglichkeit"
                )
            if test == "passive_beweglichkeit":
                models.PassiveBeweglichkeit.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="passive_beweglichkeit"
                )
            if test == "beweglichkeitsmessung":
                models.BeweglichkeitsmessungKnie.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="beweglichkeitsmessung"
                )
            if test == "isometrischer_krafttest":
                models.IsometrischerKrafttest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="isometrischer_krafttest"
                )
            if test == "muskelfunktionspruefung":
                models.Muskelfunktionspruefung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="muskelfunktionspruefung"
                )
            if test == "einbeinstand_60_sekunden":
                models.Einbeinstand60Sekunden.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="einbeinstand_60_sekunden"
                )
            if test == "einbeinstand_30_sekunden_geschlossene_augen":
                models.Einbeinstand30SekundenGeschlosseneAugen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="einbeinstand_30_sekunden_geschlossene_augen"
                )
            if test == "alltagsfunktionen":
                models.Alltagsfunktionen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="alltagsfunktionen")
            if test == "beinlaengenmessung":
                models.Beinlaengenmessung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="beinlaengenmessung"
                )
            if test == "quadriceps_dehnungstest":
                models.QuadricepsDehnungstest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="quadriceps_dehnungstest"
                )
            if test == "m_rectus_dehnungstest":
                models.MRectusDehnungstest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="m_rectus_dehnungstest"
                )
            if test == "hamstringtest":
                models.Hamstringtest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="hamstringtest")
            if test == "umfangsmessung":
                models.Umfangsmessung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="umfangsmessung")
            if test == "tanzende_patella":
                models.TanzendePatella.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="tanzende_patella")
            if test == "mini_erguss_test":
                models.MiniErgussTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="mini_erguss_test")
            if test == "glide_test":
                models.GlideTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="glide_test")
            if test == "tilt_test":
                models.TiltTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="tilt_test")
            if test == "aprehension_test":
                models.AprehensionTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="aprehension_test")
            if test == "zohlen_zeichen":
                models.ZohlenZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="zohlen_zeichen")
            if test == "facettendruckschmerztest":
                models.Facettendruckschmerztest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="facettendruckschmerztest"
                )
            if test == "valgus_test":
                models.ValgusTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="valgus_test")
            if test == "varus_test":
                models.VarusTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="varus_test")
            if test == "lachmann_test":
                models.LachmannTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="lachmann_test")
            if test == "vordere_schublade":
                models.VordereSchublade.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="vordere_schublade")
            if test == "pivot_shift_test":
                models.PivotShiftTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="pivot_shift_test")
            if test == "hintere_schublade":
                models.HintereSchublade.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="hintere_schublade")
            if test == "gravitiy_sign":
                models.GravitiySign.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="gravitiy_sign")
            if test == "loomers_test":
                models.LoomersTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="loomers_test")
            if test == "steinmann1":
                models.Steinmann1.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="steinmann1")
            if test == "steinmann3":
                models.Steinmann3.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="steinmann3")
            if test == "theslay_test":
                models.TheslayTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="theslayTest")
            if test == "mac_murray_test":
                models.MacMurrayTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="mac_murray_test")
            if test == "payr_zeichen":
                models.PayrZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="payr_zeichen")
            if test == "apley_zeichen":
                models.ApleyZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="apley_zeichen")
            if test == "medio_patellarer_plica_test":
                models.MedioPatellarerPlicaTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="medio_patellarer_plica_test"
                )
            if test == "hughston_plica_test":
                models.HughstonPlicaTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="hughston_plica_test"
                )

        return redirect(
            "personal_befund", id=id
        )  # Use the name of the URL pattern and pass the id
    befunde = models.Befund.objects.filter(created_for=id)
    befunde_strings = []
    for i in befunde:
        befunde_strings.append(i.befund)
    context = {"already_added": befunde_strings}
    print("jasfkjasfjkasgf")
    print(befunde_strings)
    return render(request, "laxout_app/befund.html", context)


@login_required(login_url="login")
def personal_befund(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)

    # Define your models here
    fragenevaluation_icf_list = models.FragenevaluationNachICFKategorien.objects.filter(
        created_for=id
    )
    fragenevaluation_bio_list = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.filter(
        created_for=id
    )
    wfragen_list = models.FragenevaluationenNachDen7WFragen.objects.filter(
        created_for=id
    )
    rehaPhase_list = models.StandDerReHaPhase.objects.filter(created_for=id)
    nebenerkrankung_list = models.NebenerkrankungenMedikamente.objects.filter(
        created_for=id
    )
    historia_morbis_list = models.HistoriaMorbis.objects.filter(created_for=id)
    standartbefund_list = models.StandartBefund.objects.filter(created_for=id)
    nrs_numeric_rating_scale_list = models.NrsNumericRatingScale.objects.filter(
        created_for=id
    )
    aktive_beweglichkeit_list = models.AktiveBeweglichkeit.objects.filter(
        created_for=id
    )
    passive_beweglichkeit_list = models.PassiveBeweglichkeit.objects.filter(
        created_for=id
    )
    beweglichkeitsmessung_list = models.BeweglichkeitsmessungKnie.objects.filter(
        created_for=id
    )
    isometrischer_krafttest_list = models.IsometrischerKrafttest.objects.filter(
        created_for=id
    )
    muskelfunktionspruefung_list = models.Muskelfunktionspruefung.objects.filter(
        created_for=id
    )
    einbeinstand60_sekunden_list = models.Einbeinstand60Sekunden.objects.filter(
        created_for=id
    )
    einbeinstand30_sekunden_geschlossene_augen_list = (
        models.Einbeinstand30SekundenGeschlosseneAugen.objects.filter(created_for=id)
    )
    alltagsfunktionen_list = models.Alltagsfunktionen.objects.filter(created_for=id)
    beinlaengenmessung_list = models.Beinlaengenmessung.objects.filter(created_for=id)
    quadriceps_dehnungstest_list = models.QuadricepsDehnungstest.objects.filter(
        created_for=id
    )
    m_rectus_dehnungstest_list = models.MRectusDehnungstest.objects.filter(
        created_for=id
    )
    hamstringtest_list = models.Hamstringtest.objects.filter(created_for=id)
    umfangsmessung_list = models.Umfangsmessung.objects.filter(created_for=id)
    tanzende_patella_list = models.TanzendePatella.objects.filter(created_for=id)
    mini_ergurs_test_list = models.MiniErgussTest.objects.filter(created_for=id)
    glide_test_list = models.GlideTest.objects.filter(created_for=id)
    tilt_test_list = models.TiltTest.objects.filter(created_for=id)
    aprehension_test_list = models.AprehensionTest.objects.filter(created_for=id)
    zohlen_zeichen_list = models.ZohlenZeichen.objects.filter(created_for=id)
    facettendruckschmerztest_list = models.Facettendruckschmerztest.objects.filter(
        created_for=id
    )
    valgus_test_list = models.ValgusTest.objects.filter(created_for=id)
    varus_test_list = models.VarusTest.objects.filter(created_for=id)
    lachmann_test_list = models.LachmannTest.objects.filter(created_for=id)
    vordere_Schublade_list = models.VordereSchublade.objects.filter(created_for=id)
    pivot_shift_test_list = models.PivotShiftTest.objects.filter(created_for=id)
    hintere_schublade_list = models.HintereSchublade.objects.filter(created_for=id)
    gravity_sign_list = models.GravitiySign.objects.filter(created_for=id)
    loomers_test_list = models.LoomersTest.objects.filter(created_for=id)
    steinmann1_list = models.Steinmann1.objects.filter(created_for=id)
    steinmann3_list = models.Steinmann3.objects.filter(created_for=id)
    theslay_test_list = models.TheslayTest.objects.filter(created_for=id)
    mac_murry_test_list = models.MacMurrayTest.objects.filter(created_for=id)
    payr_zeichen_list = models.PayrZeichen.objects.filter(created_for=id)
    apley_zeichen_list = models.ApleyZeichen.objects.filter(created_for=id)
    medio_patellarer_plica_test_list = models.MedioPatellarerPlicaTest.objects.filter(
        created_for=id
    )
    hughston_pica_test_list = models.HughstonPlicaTest.objects.filter(created_for=id)

    # Initialize context dictionary
    context = {"user": user}

    # Function to add list to context if it exists
    def add_list_to_context(list_obj, context_key):
        if list_obj.exists():
            context[context_key] = list_obj
            ids_list_script = [item.id for item in list_obj]
            context[f"{context_key}_ids"] = ids_list_script

    # Add lists to context using the function
    add_list_to_context(standartbefund_list, "standartbefund_list")
    add_list_to_context(nrs_numeric_rating_scale_list, "nrs_numeric_rating_scale_list")
    add_list_to_context(aktive_beweglichkeit_list, "aktive_beweglichkeit_list")
    add_list_to_context(passive_beweglichkeit_list, "passive_beweglichkeit_list")
    add_list_to_context(beweglichkeitsmessung_list, "beweglichkeitsmessung_list")
    add_list_to_context(isometrischer_krafttest_list, "isometrischer_krafttest_list")
    add_list_to_context(muskelfunktionspruefung_list, "muskelfunktionspruefung_list")
    add_list_to_context(einbeinstand60_sekunden_list, "einbeinstand60_sekunden_list")
    add_list_to_context(
        einbeinstand30_sekunden_geschlossene_augen_list,
        "einbeinstand30_sekunden_geschlossene_augen_list",
    )
    add_list_to_context(alltagsfunktionen_list, "alltagsfunktionen_list")
    add_list_to_context(beinlaengenmessung_list, "beinlaengenmessung_list")
    add_list_to_context(quadriceps_dehnungstest_list, "quadriceps_dehnungstest_list")
    add_list_to_context(m_rectus_dehnungstest_list, "m_rectus_dehnungstest_list")
    add_list_to_context(hamstringtest_list, "hamstringtest_list")
    add_list_to_context(umfangsmessung_list, "umfangsmessung_list")
    add_list_to_context(tanzende_patella_list, "tanzende_patella_list")
    add_list_to_context(mini_ergurs_test_list, "mini_ergurs_test_list")
    add_list_to_context(glide_test_list, "glide_test_list")
    add_list_to_context(tilt_test_list, "tilt_test_list")
    add_list_to_context(aprehension_test_list, "aprehension_test_list")
    add_list_to_context(zohlen_zeichen_list, "zohlen_zeichen_list")
    add_list_to_context(facettendruckschmerztest_list, "facettendruckschmerztest_list")
    add_list_to_context(valgus_test_list, "valgus_test_list")
    add_list_to_context(varus_test_list, "varus_test_list")
    add_list_to_context(lachmann_test_list, "lachmann_test_list")
    add_list_to_context(vordere_Schublade_list, "vordere_Schublade_list")
    add_list_to_context(pivot_shift_test_list, "pivot_shift_test_list")
    add_list_to_context(hintere_schublade_list, "hintere_schublade_list")
    add_list_to_context(gravity_sign_list, "gravity_sign_list")
    add_list_to_context(loomers_test_list, "loomers_test_list")
    add_list_to_context(steinmann1_list, "steinmann1_list")
    add_list_to_context(steinmann3_list, "steinmann3_list")
    add_list_to_context(theslay_test_list, "theslay_test_list")
    add_list_to_context(mac_murry_test_list, "mac_murry_test_list")
    add_list_to_context(payr_zeichen_list, "payr_zeichen_list")
    add_list_to_context(apley_zeichen_list, "apley_zeichen_list")
    add_list_to_context(
        medio_patellarer_plica_test_list, "medio_patellarer_plica_test_list"
    )
    add_list_to_context(hughston_pica_test_list, "hughston_pica_test_list")
    add_list_to_context(fragenevaluation_bio_list, "fragenevaluation_bio_list")
    add_list_to_context(fragenevaluation_icf_list, "fragenevaluation_icf_list")
    add_list_to_context(wfragen_list, "wfragen_list")
    add_list_to_context(rehaPhase_list, "rehaPhase_list")
    add_list_to_context(nebenerkrankung_list, "nebenerkrankung_list")
    add_list_to_context(historia_morbis_list, "historia_morbis_list")

    print(context)

    return render(request, "laxout_app/personal_befund.html", context)


@login_required(login_url="login")
def update_personal_befund(request, id=None, befund=None, befundId=None):
    if id == None:
        return HttpResponse("Not valid")
    if befund == "ananmese":
        selected_befund = models.AnanmenseBefund.objects.get(id=befundId)
        disability = request.POST.get("disability")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        selected_befund.disability = disability
        selected_befund.name = name
        selected_befund.surname = surname
        selected_befund.save()

    if befund == "fragenevaluation_icf":
        selected_befund = models.FragenevaluationNachICFKategorien.objects.get(
            id=befundId
        )
        # op = request.POST.get("op")
        # if op == "1":
        #     op = True
        #     print("TRUE")
        # else:
        #     op = False
        #     aktueller_gesundheitszustand = models.CharField(default="", max_length=20000)
        # struktur_funktion = models.CharField(default="", max_length=20000)
        # aktivitaet = models.CharField(default="", max_length=20000)
        # partizipation = models.CharField(default="", max_length=20000)
        # kontextfaktoren = models.CharField(default="", max_length=20000)
        aktueller_gesundheitszustand = request.POST.get("aktueller_gesundheitszustand")
        struktur_funktion = request.POST.get("struktur_funktion")
        aktivitaet = request.POST.get("aktivitaet")
        partizipation = request.POST.get("partizipation")
        kontextfaktoren = request.POST.get("kontextfaktoren")

        selected_befund.aktueller_gesundheitszustand = aktueller_gesundheitszustand
        selected_befund.struktur_funktion = struktur_funktion
        selected_befund.aktivitaet = aktivitaet
        selected_befund.partizipation = partizipation
        selected_befund.kontextfaktoren = kontextfaktoren

        selected_befund.save()

    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        selected_befund = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.get(
            id=befundId
        )

        koerperliche_beschwerden = request.POST.get("koerperliche_beschwerden")
        psychisch_gelagerte_eschwerden = request.POST.get(
            "psychisch_gelagerte_eschwerden"
        )
        probleme_mit_aktiver_teilhabe_am_sozialen_Leben = request.POST.get(
            "probleme_mit_aktiver_teilhabe_am_sozialen_Leben"
        )

        selected_befund.koerperliche_beschwerden = koerperliche_beschwerden
        selected_befund.psychisch_gelagerte_eschwerden = psychisch_gelagerte_eschwerden
        selected_befund.probleme_mit_aktiver_teilhabe_am_sozialen_Leben = (
            probleme_mit_aktiver_teilhabe_am_sozialen_Leben
        )

        selected_befund.save()

    if befund == "w_fragen":
        selected_befund = models.FragenevaluationenNachDen7WFragen.objects.get(
            id=befundId
        )

        hauptbeschwerden = request.POST.get("hauptbeschwerden")
        lokalisierung = request.POST.get("lokalisierung")
        provokation = request.POST.get("provokation")
        orientierung_für_Maßnahmen = request.POST.get("orientierung_für_Maßnahmen")
        schmerzqualität = request.POST.get("schmerzqualität")
        orientierung = request.POST.get("orientierung")
        beschwerdeverlauf = request.POST.get("beschwerdeverlauf")

        selected_befund.beschwerdeverlauf = beschwerdeverlauf
        selected_befund.orientierung = orientierung
        selected_befund.schmerzqualität = schmerzqualität
        selected_befund.orientierung_für_Maßnahmen = orientierung_für_Maßnahmen
        selected_befund.provokation = provokation
        selected_befund.lokalisierung = lokalisierung
        selected_befund.hauptbeschwerden = hauptbeschwerden

        selected_befund.save()

    if befund == "standart_befund":
        selected_befund = models.StandartBefund.objects.get(id=befundId)

        dropdown_aktualisierung = request.POST.get("dropdown")
        if dropdown_aktualisierung:
            geschlecht = request.POST.get("geschlecht")
            selected_befund.geschlecht = geschlecht
            selected_befund.save()
            return HttpResponse("Updated Successfully")

        # Felder einzeln aktualisieren, falls sie im POST-Request vorhanden sind
        if "name" in request.POST:
            selected_befund.name = request.POST.get("name")
        if "vorname" in request.POST:
            selected_befund.vorname = request.POST.get("vorname")
        if "alter" in request.POST:
            selected_befund.alter = request.POST.get("alter")
        if "diagnose" in request.POST:
            selected_befund.diagnose = request.POST.get("diagnose")
        if "hauptziel" in request.POST:
            selected_befund.hauptziel = request.POST.get("hauptziel")
        if "vollbelastung" in request.POST:
            selected_befund.vollbelastung = request.POST.get("vollbelastung")
        if "teilbeslastung" in request.POST:
            selected_befund.teilbeslastung = request.POST.get("teilbeslastung")
        if "lagerungstabil" in request.POST:
            selected_befund.lagerungstabil = request.POST.get("lagerungstabil")
        if "maximalpuls" in request.POST:
            selected_befund.maximalpuls = request.POST.get("maximalpuls")
        if "therapeutische_ziele_maßnahmen" in request.POST:
            selected_befund.therapeutische_ziele_maßnahmen = request.POST.get(
                "therapeutische_ziele_maßnahmen"
            )
        if "medikament_einnahme" in request.POST:
            selected_befund.medikament_einnahme = request.POST.get(
                "medikament_einnahme"
            )
        if "groeße" in request.POST:
            selected_befund.groeße = request.POST.get("groeße")
        if "gewicht" in request.POST:
            selected_befund.gewicht = request.POST.get("gewicht")
        if "konstitutionstyp" in request.POST:
            selected_befund.konstitutionstyp = request.POST.get("konstitutionstyp")
        if "beruf" in request.POST:
            selected_befund.beruf = request.POST.get("beruf")
        if "alltagsaktivitaeten" in request.POST:
            selected_befund.alltagsaktivitaeten = request.POST.get(
                "alltagsaktivitaeten"
            )
        if "op_vorliegend" in request.POST:
            selected_befund.op_vorliegend = request.POST.get("op_vorliegend")

        selected_befund.save()

    if befund == "stand_reha_phase":
        selected_befund = models.StandDerReHaPhase.objects.get(id=befundId)

        akute_phase = request.POST.get("akute_phase")
        wundheilungsphase = request.POST.get("wundheilungsphase")
        frueh_phase_ReHa = request.POST.get("frueh_phase_ReHa")
        mittlere_phase_Reha = request.POST.get("mittlere_phase_Reha")
        spaet_phase_reha = request.POST.get("spaet_phase_reha")

        selected_befund.akute_phase = akute_phase
        selected_befund.wundheilungsphase = wundheilungsphase
        selected_befund.frueh_phase_ReHa = frueh_phase_ReHa
        selected_befund.mittlere_phase_Reha = mittlere_phase_Reha
        selected_befund.spaet_phase_reha = spaet_phase_reha

        selected_befund.save()

    if befund == "nebenerkrankungen_medikamente":
        selected_befund = models.NebenerkrankungenMedikamente.objects.get(id=befundId)

        erbkrankheiten = request.POST.get("erbkrankheiten")
        metabolische_erkrankungen = request.POST.get("metabolische_erkrankungen")
        psychische_erkrankungen = request.POST.get("psychische_erkrankungen")
        herz_kreislauferkrankungen = request.POST.get("herz_kreislauferkrankungen")
        neurologische_erkrankungen = request.POST.get("neurologische_erkrankungen")
        rheumatisch_entzuendliche_erkrankungen = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen"
        )
        erkrankungen_bewegungsapparat = request.POST.get(
            "erkrankungen_bewegungsapparat"
        )
        erbkrankheiten_krankheit = request.POST.get("erbkrankheiten_krankheit")
        metabolische_erkrankungen_krankheit = request.POST.get(
            "metabolische_erkrankungen_krankheit"
        )
        psychische_erkrankungen_krankheit = request.POST.get(
            "psychische_erkrankungen_krankheit"
        )
        herz_kreislauferkrankungen_krankheit = request.POST.get(
            "herz_kreislauferkrankungen_krankheit"
        )
        neurologische_erkrankungen_krankheit = request.POST.get(
            "neurologische_erkrankungen_krankheit"
        )
        rheumatisch_entzuendliche_erkrankungen_krankheit = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen"
        )
        erkrankungen_bewegungsapparat_erkrankungen_krankheit = request.POST.get(
            "erkrankungen_bewegungsapparat_erkrankungen_krankheit"
        )
        erbkrankheiten_medikamente = request.POST.get("erbkrankheiten_medikamente")
        metabolische_erkrankungen_medikamente = request.POST.get(
            "metabolische_erkrankungen_medikamente"
        )
        psychische_erkrankungen_medikamente = request.POST.get(
            "psychische_erkrankungen_medikamente"
        )
        herz_kreislauferkrankungen_medikamente = request.POST.get(
            "herz_kreislauferkrankungen_medikamente"
        )
        neurologische_erkrankungen_medikamente = request.POST.get(
            "neurologische_erkrankungen_medikamente"
        )
        rheumatisch_entzuendliche_erkrankungen_medikamente = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen_medikamente"
        )
        erkrankungen_bewegungsapparat_erkrankungen_medikamente = request.POST.get(
            "erkrankungen_bewegungsapparat_erkrankungen_medikamente"
        )

        selected_befund.erbkrankheiten = erbkrankheiten
        selected_befund.metabolische_erkrankungen = metabolische_erkrankungen
        selected_befund.psychische_erkrankungen = psychische_erkrankungen
        selected_befund.herz_kreislauferkrankungen = herz_kreislauferkrankungen
        selected_befund.neurologische_erkrankungen = neurologische_erkrankungen
        selected_befund.rheumatisch_entzuendliche_erkrankungen = (
            rheumatisch_entzuendliche_erkrankungen
        )
        selected_befund.erkrankungen_bewegungsapparat = erkrankungen_bewegungsapparat

        selected_befund.erbkrankheiten_krankheit = erbkrankheiten_krankheit
        selected_befund.metabolische_erkrankungen_krankheit = (
            metabolische_erkrankungen_krankheit
        )
        selected_befund.psychische_erkrankungen_krankheit = (
            psychische_erkrankungen_krankheit
        )
        selected_befund.herz_kreislauferkrankungen_krankheit = (
            herz_kreislauferkrankungen_krankheit
        )
        selected_befund.neurologische_erkrankungen_krankheit = (
            neurologische_erkrankungen_krankheit
        )
        selected_befund.rheumatisch_entzuendliche_erkrankungen_krankheit = (
            rheumatisch_entzuendliche_erkrankungen_krankheit
        )
        selected_befund.erkrankungen_bewegungsapparat_erkrankungen_krankheit = (
            erkrankungen_bewegungsapparat_erkrankungen_krankheit
        )

        selected_befund.erbkrankheiten_medikamente = erbkrankheiten_medikamente
        selected_befund.metabolische_erkrankungen_medikamente = (
            metabolische_erkrankungen_medikamente
        )
        selected_befund.psychische_erkrankungen_medikamente = (
            psychische_erkrankungen_medikamente
        )
        selected_befund.herz_kreislauferkrankungen_medikamente = (
            herz_kreislauferkrankungen_medikamente
        )
        selected_befund.neurologische_erkrankungen_medikamente = (
            neurologische_erkrankungen_medikamente
        )
        selected_befund.rheumatisch_entzuendliche_erkrankungen_medikamente = (
            rheumatisch_entzuendliche_erkrankungen_medikamente
        )
        selected_befund.erkrankungen_bewegungsapparat_erkrankungen_medikamente = (
            erkrankungen_bewegungsapparat_erkrankungen_medikamente
        )

        selected_befund.save()

    if befund == "historia_morbis":
        selected_befund = models.HistoriaMorbis.objects.get(id=befundId)

        trauma_unfall = request.POST.get("trauma_unfall")
        atraumatisch = request.POST.get("atraumatisch")
        chronisch = request.POST.get("chronisch")
        progredient = request.POST.get("progredient")
        krankheitsverlauf = request.POST.get("krankheitsverlauf")
        Krankenhausaufenthalte = request.POST.get("Krankenhausaufenthalte")
        unfaelle_verletzungen_operationen = request.POST.get(
            "unfaelle_verletzungen_operationen"
        )
        schwangerschaften = request.POST.get("schwangerschaften")
        sucht_drogenverhalten = request.POST.get("sucht_drogenverhalten")

        selected_befund.trauma_unfall = trauma_unfall
        selected_befund.atraumatisch = atraumatisch
        selected_befund.chronisch = chronisch
        selected_befund.progredient = progredient
        selected_befund.krankheitsverlauf = krankheitsverlauf
        selected_befund.Krankenhausaufenthalte = Krankenhausaufenthalte
        selected_befund.unfaelle_verletzungen_operationen = (
            unfaelle_verletzungen_operationen
        )
        selected_befund.schwangerschaften = schwangerschaften
        selected_befund.sucht_drogenverhalten = sucht_drogenverhalten

        selected_befund.save()

    if befund == "nrs_numeric_rating_scale":
        selected_befund = models.NrsNumericRatingScale.objects.get(id=befundId)

        if "kein_schmerz" in request.POST:
            selected_befund.kein_schmerz = request.POST.get("kein_schmerz")

        if "sanft" in request.POST:
            selected_befund.sanft = request.POST.get("sanft")

        if "gering" in request.POST:
            selected_befund.gering = request.POST.get("gering")

        if "unbequem" in request.POST:
            selected_befund.unbequem = request.POST.get("unbequem")

        if "mittelgradig" in request.POST:
            selected_befund.mittelgradig = request.POST.get("mittelgradig")

        if "ablenkend" in request.POST:
            selected_befund.ablenkend = request.POST.get("ablenkend")

        if "quaelend" in request.POST:
            selected_befund.quaelend = request.POST.get("quaelend")

        if "starker_schmerz" in request.POST:
            selected_befund.starker_schmerz = request.POST.get("starker_schmerz")

        if "hochgradiger_schmerz" in request.POST:
            selected_befund.hochgradiger_schmerz = request.POST.get(
                "hochgradiger_schmerz"
            )

        if "unertraeglich" in request.POST:
            selected_befund.unertraeglich = request.POST.get("unertraeglich")

        if "unbeschreiblich" in request.POST:
            selected_befund.unbeschreiblich = request.POST.get("unbeschreiblich")

        selected_befund.save()

    if befund == "aktive_beweglichkeit":
        selected_befund = models.AktiveBeweglichkeit.objects.get(id=befundId)

        # Flexion Rechts
        if "flexion_rechts_oB" in request.POST:
            selected_befund.flexion_rechts_oB = request.POST.get("flexion_rechts_oB")
        if "flexion_rechts_leicht_begrenzt" in request.POST:
            selected_befund.flexion_rechts_leicht_begrenzt = request.POST.get(
                "flexion_rechts_leicht_begrenzt"
            )
        if "flexion_rechts_mittelgradig_begrenzt" in request.POST:
            selected_befund.flexion_rechts_mittelgradig_begrenzt = request.POST.get(
                "flexion_rechts_mittelgradig_begrenzt"
            )
        if "flexion_rechts_stark_begrenzt" in request.POST:
            selected_befund.flexion_rechts_stark_begrenzt = request.POST.get(
                "flexion_rechts_stark_begrenzt"
            )
        if "flexion_rechts_schmerzhaft" in request.POST:
            selected_befund.flexion_rechts_schmerzhaft = request.POST.get(
                "flexion_rechts_schmerzhaft"
            )
        if "flexion_rechts_gehemmt" in request.POST:
            selected_befund.flexion_rechts_gehemmt = request.POST.get(
                "flexion_rechts_gehemmt"
            )
        if "flexion_rechts_verzögert" in request.POST:
            selected_befund.flexion_rechts_verzögert = request.POST.get(
                "flexion_rechts_verzögert"
            )
        if "flexion_rechts_eingeschränkt" in request.POST:
            selected_befund.flexion_rechts_eingeschränkt = request.POST.get(
                "flexion_rechts_eingeschränkt"
            )
        if "flexion_rechts_unkoordiniert" in request.POST:
            selected_befund.flexion_rechts_unkoordiniert = request.POST.get(
                "flexion_rechts_unkoordiniert"
            )

        # Flexion Links
        if "flexion_links_oB" in request.POST:
            selected_befund.flexion_links_oB = request.POST.get("flexion_links_oB")
        if "flexion_links_leicht_begrenzt" in request.POST:
            selected_befund.flexion_links_leicht_begrenzt = request.POST.get(
                "flexion_links_leicht_begrenzt"
            )
        if "flexion_links_mittelgradig_begrenzt" in request.POST:
            selected_befund.flexion_links_mittelgradig_begrenzt = request.POST.get(
                "flexion_links_mittelgradig_begrenzt"
            )
        if "flexion_links_stark_begrenzt" in request.POST:
            selected_befund.flexion_links_stark_begrenzt = request.POST.get(
                "flexion_links_stark_begrenzt"
            )
        if "flexion_links_schmerzhaft" in request.POST:
            selected_befund.flexion_links_schmerzhaft = request.POST.get(
                "flexion_links_schmerzhaft"
            )
        if "flexion_links_gehemmt" in request.POST:
            selected_befund.flexion_links_gehemmt = request.POST.get(
                "flexion_links_gehemmt"
            )
        if "flexion_links_verzögert" in request.POST:
            selected_befund.flexion_links_verzögert = request.POST.get(
                "flexion_links_verzögert"
            )
        if "flexion_links_eingeschränkt" in request.POST:
            selected_befund.flexion_links_eingeschränkt = request.POST.get(
                "flexion_links_eingeschränkt"
            )
        if "flexion_links_unkoordiniert" in request.POST:
            selected_befund.flexion_links_unkoordiniert = request.POST.get(
                "flexion_links_unkoordiniert"
            )

        # Extension Rechts
        if "extension_rechts_oB" in request.POST:
            selected_befund.extension_rechts_oB = request.POST.get(
                "extension_rechts_oB"
            )
        if "extension_rechts_leicht_begrenzt" in request.POST:
            selected_befund.extension_rechts_leicht_begrenzt = request.POST.get(
                "extension_rechts_leicht_begrenzt"
            )
        if "extension_rechts_mittelgradig_begrenzt" in request.POST:
            selected_befund.extension_rechts_mittelgradig_begrenzt = request.POST.get(
                "extension_rechts_mittelgradig_begrenzt"
            )
        if "extension_rechts_stark_begrenzt" in request.POST:
            selected_befund.extension_rechts_stark_begrenzt = request.POST.get(
                "extension_rechts_stark_begrenzt"
            )
        if "extension_rechts_schmerzhaft" in request.POST:
            selected_befund.extension_rechts_schmerzhaft = request.POST.get(
                "extension_rechts_schmerzhaft"
            )
        if "extension_rechts_gehemmt" in request.POST:
            selected_befund.extension_rechts_gehemmt = request.POST.get(
                "extension_rechts_gehemmt"
            )
        if "extension_rechts_verzögert" in request.POST:
            selected_befund.extension_rechts_verzögert = request.POST.get(
                "extension_rechts_verzögert"
            )
        if "extension_rechts_eingeschränkt" in request.POST:
            selected_befund.extension_rechts_eingeschränkt = request.POST.get(
                "extension_rechts_eingeschränkt"
            )
        if "extension_rechts_unkoordiniert" in request.POST:
            selected_befund.extension_rechts_unkoordiniert = request.POST.get(
                "extension_rechts_unkoordiniert"
            )

        # Extension Links
        if "extension_links_oB" in request.POST:
            selected_befund.extension_links_oB = request.POST.get("extension_links_oB")
        if "extension_links_leicht_begrenzt" in request.POST:
            selected_befund.extension_links_leicht_begrenzt = request.POST.get(
                "extension_links_leicht_begrenzt"
            )
        if "extension_links_mittelgradig_begrenzt" in request.POST:
            selected_befund.extension_links_mittelgradig_begrenzt = request.POST.get(
                "extension_links_mittelgradig_begrenzt"
            )
        if "extension_links_stark_begrenzt" in request.POST:
            selected_befund.extension_links_stark_begrenzt = request.POST.get(
                "extension_links_stark_begrenzt"
            )
        if "extension_links_schmerzhaft" in request.POST:
            selected_befund.extension_links_schmerzhaft = request.POST.get(
                "extension_links_schmerzhaft"
            )
        if "extension_links_gehemmt" in request.POST:
            selected_befund.extension_links_gehemmt = request.POST.get(
                "extension_links_gehemmt"
            )
        if "extension_links_verzögert" in request.POST:
            selected_befund.extension_links_verzögert = request.POST.get(
                "extension_links_verzögert"
            )
        if "extension_links_eingeschränkt" in request.POST:
            selected_befund.extension_links_eingeschränkt = request.POST.get(
                "extension_links_eingeschränkt"
            )
        if "extension_links_unkoordiniert" in request.POST:
            selected_befund.extension_links_unkoordiniert = request.POST.get(
                "extension_links_unkoordiniert"
            )

        selected_befund.save()

    if befund == "passive_beweglichkeit":
        selected_befund = models.PassiveBeweglichkeit.objects.get(id=befundId)

        # Flexion Rechts
        if "flexion_rechts_oB_pb" in request.POST:

            selected_befund.flexion_rechts_oB = request.POST.get("flexion_rechts_oB_pb")
        if "flexion_rechts_leicht_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_leicht_begrenzt = request.POST.get(
                "flexion_rechts_leicht_begrenzt_pb"
            )
        if "flexion_rechts_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_mittelgradig_begrenzt = request.POST.get(
                "flexion_rechts_mittelgradig_begrenzt_pb"
            )
        if "flexion_rechts_stark_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_stark_begrenzt = request.POST.get(
                "flexion_rechts_stark_begrenzt_pb"
            )
        if "flexion_rechts_fest_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fest_elastischer_stopp = request.POST.get(
                "flexion_rechts_fest_elastischer_stopp"
            )
        if "flexion_rechts_weich_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_weich_elastischer_stopp = request.POST.get(
                "flexion_rechts_weich_elastischer_stopp"
            )
        if "flexion_rechts_hart_unelastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_hart_unelastischer_stopp = request.POST.get(
                "flexion_rechts_hart_unelastischer_stopp"
            )
        if "flexion_rechts_fester_unelastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fester_unelastischer_stopp = (
                request.POST.get("flexion_rechts_fester_unelastischer_stopp")
            )
        if "flexion_rechts_fester_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fester_elastischer_stopp = request.POST.get(
                "flexion_rechts_fester_elastischer_stopp"
            )
        if "flexion_rechts_leeres_endgefuehl" in request.POST:
            selected_befund.flexion_rechts_leeres_endgefuehl = request.POST.get(
                "flexion_rechts_leeres_endgefuehl"
            )
        if "flexion_rechts_schmerz" in request.POST:
            selected_befund.flexion_rechts_schmerz = request.POST.get(
                "flexion_rechts_schmerz"
            )

        # Flexion Links
        if "flexion_links_oB_pb" in request.POST:
            selected_befund.flexion_links_oB = request.POST.get("flexion_links_oB_pb")
        if "flexion_links_leicht_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_leicht_begrenzt = request.POST.get(
                "flexion_links_leicht_begrenzt_pb"
            )
        if "flexion_links_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_mittelgradig_begrenzt = request.POST.get(
                "flexion_links_mittelgradig_begrenzt_pb"
            )
        if "flexion_links_stark_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_stark_begrenzt = request.POST.get(
                "flexion_links_stark_begrenzt_pb"
            )
        if "flexion_links_fest_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_fest_elastischer_stopp = request.POST.get(
                "flexion_links_fest_elastischer_stopp"
            )
        if "flexion_links_weich_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_weich_elastischer_stopp = request.POST.get(
                "flexion_links_weich_elastischer_stopp"
            )
        if "flexion_links_hart_unelastischer_stopp" in request.POST:
            selected_befund.flexion_links_hart_unelastischer_stopp = request.POST.get(
                "flexion_links_hart_unelastischer_stopp"
            )
        if "flexion_links_fester_unelastischer_stopp" in request.POST:
            selected_befund.flexion_links_fester_unelastischer_stopp = request.POST.get(
                "flexion_links_fester_unelastischer_stopp"
            )
        if "flexion_links_fester_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_fester_elastischer_stopp = request.POST.get(
                "flexion_links_fester_elastischer_stopp"
            )
        if "flexion_links_leeres_endgefuehl" in request.POST:
            selected_befund.flexion_links_leeres_endgefuehl = request.POST.get(
                "flexion_links_leeres_endgefuehl"
            )
        if "flexion_links_schmerz" in request.POST:
            selected_befund.flexion_links_schmerz = request.POST.get(
                "flexion_links_schmerz"
            )

        # Extension Rechts
        if "extension_rechts_oB_pb" in request.POST:
            selected_befund.extension_rechts_oB = request.POST.get(
                "extension_rechts_oB_pb"
            )
        if "extension_rechts_leicht_begrenzt_pb" in request.POST:
            selected_befund.extension_rechts_leicht_begrenzt = request.POST.get(
                "extension_rechts_leicht_begrenzt_pb"
            )
        if "extension_rechts_mittelgradig_begrenzt_pb" in request.POST:
            print("AUFGERUFEN")
            print(request.POST.get("extension_rechts_mittelgradig_begrenzt_pb"))
            selected_befund.extension_rechts_mittelgradig_begrenztb = request.POST.get(
                "extension_rechts_mittelgradig_begrenzt_pb"
            )
        if "extension_rechts_stark_begrenzt_pb" in request.POST:
            selected_befund.extension_rechts_stark_begrenzt = request.POST.get(
                "extension_rechts_stark_begrenzt_pb"
            )
        if "extension_rechts_fest_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fest_elastischer_stopp = request.POST.get(
                "extension_rechts_fest_elastischer_stopp"
            )
        if "extension_rechts_weich_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_weich_elastischer_stopp = request.POST.get(
                "extension_rechts_weich_elastischer_stopp"
            )
        if "extension_rechts_hart_unelastischer_stopp" in request.POST:
            selected_befund.extension_rechts_hart_unelastischer_stopp = (
                request.POST.get("extension_rechts_hart_unelastischer_stopp")
            )
        if "extension_rechts_fester_unelastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fester_unelastischer_stopp = (
                request.POST.get("extension_rechts_fester_unelastischer_stopp")
            )
        if "extension_rechts_fester_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fester_elastischer_stopp = (
                request.POST.get("extension_rechts_fester_elastischer_stopp")
            )
        if "extension_rechts_leeres_endgefuehl" in request.POST:
            selected_befund.extension_rechts_leeres_endgefuehl = request.POST.get(
                "extension_rechts_leeres_endgefuehl"
            )
        if "extension_rechts_schmerz" in request.POST:
            selected_befund.extension_rechts_schmerz = request.POST.get(
                "extension_rechts_schmerz"
            )

        # Extension Links
        if "extension_links_oB_pb" in request.POST:
            selected_befund.extension_links_oB = request.POST.get(
                "extension_links_oB_pb"
            )

        if "extension_links_leicht_begrenzt_pb" in request.POST:
            selected_befund.extension_links_leicht_begrenzt = request.POST.get(
                "extension_links_leicht_begrenzt_pb"
            )
        if "extension_links_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.extension_links_mittelgradig_begrenzt = request.POST.get(
                "extension_links_mittelgradig_begrenzt_pb"
            )
        if "extension_links_stark_begrenzt_pb" in request.POST:
            selected_befund.extension_links_stark_begrenzt = request.POST.get(
                "extension_links_stark_begrenzt_pb"
            )
        if "extension_links_fest_elastischer_stopp" in request.POST:
            selected_befund.extension_links_fest_elastischer_stopp = request.POST.get(
                "extension_links_fest_elastischer_stopp"
            )
        if "extension_links_weich_elastischer_stopp" in request.POST:
            selected_befund.extension_links_weich_elastischer_stopp = request.POST.get(
                "extension_links_weich_elastischer_stopp"
            )
        if "extension_links_hart_unelastischer_stopp" in request.POST:
            selected_befund.extension_links_hart_unelastischer_stopp = request.POST.get(
                "extension_links_hart_unelastischer_stopp"
            )
        if "extension_links_fester_unelastischer_stopp" in request.POST:
            selected_befund.extension_links_fester_unelastischer_stopp = (
                request.POST.get("extension_links_fester_unelastischer_stopp")
            )
        if "extension_links_fester_elastischer_stopp" in request.POST:
            selected_befund.extension_links_fester_elastischer_stopp = request.POST.get(
                "extension_links_fester_elastischer_stopp"
            )
        if "extension_links_leeres_endgefuehl" in request.POST:
            selected_befund.extension_links_leeres_endgefuehl = request.POST.get(
                "extension_links_leeres_endgefuehl"
            )
        if "extension_links_schmerz" in request.POST:
            selected_befund.extension_links_schmerz = request.POST.get(
                "extension_links_schmerz"
            )

        selected_befund.save()

    if befund == "beweglichkeitsmessung":
        selected_befund = models.BeweglichkeitsmessungKnie.objects.get(id=befundId)

        if "extension_flexion_rechts_value_bmk" in request.POST:
            selected_befund.extension_flexion_rechts_value = request.POST.get(
                "extension_flexion_rechts_value_bmk"
            )
        if "extension_flexion_links_value_bmk" in request.POST:
            selected_befund.extension_flexion_links_value = request.POST.get(
                "extension_flexion_links_value_bmk"
            )

        selected_befund.save()

    if befund == "isometrischer_krafttest":
        selected_befund = models.IsometrischerKrafttest.objects.get(id=befundId)

        if "flexion_oB_ikk" in request.POST:
            selected_befund.flexion_oB = request.POST.get("flexion_oB_ikk")
        if "flexion_kann_nicht_gehalten_werden_ikk" in request.POST:
            selected_befund.flexion_kann_nicht_gehalten_werden = request.POST.get(
                "flexion_kann_nicht_gehalten_werden_ikk"
            )
        if "extension_oB_ikk" in request.POST:
            selected_befund.extension_oB = request.POST.get("extension_oB_ikk")
        if "extension_kann_nicht_gehalten_werden_ikk" in request.POST:
            selected_befund.extension_kann_nicht_gehalten_werden = request.POST.get(
                "extension_kann_nicht_gehalten_werden_ikk"
            )

        selected_befund.save()

    if befund == "muskelfunktionspruefung":
        selected_befund = models.Muskelfunktionspruefung.objects.get(id=befundId)

        # Update Flexion fields
        if "flexion_1_mfk" in request.POST:
            selected_befund.flexion_1 = request.POST.get("flexion_1_mfk")
        if "flexion_2_mfk" in request.POST:
            selected_befund.flexion_2 = request.POST.get("flexion_2_mfk")
        if "flexion_3_mfk" in request.POST:
            selected_befund.flexion_3 = request.POST.get("flexion_3_mfk")
        if "flexion_4_mfk" in request.POST:
            selected_befund.flexion_4 = request.POST.get("flexion_4_mfk")
        if "flexion_5_mfk" in request.POST:
            selected_befund.flexion_5 = request.POST.get("flexion_5_mfk")

        # Update Extension fields
        if "extension_1_mfk" in request.POST:
            selected_befund.extension_1 = request.POST.get("extension_1_mfk")
        if "extension_2_mfk" in request.POST:
            selected_befund.extension_2 = request.POST.get("extension_2_mfk")
        if "extension_3_mfk" in request.POST:
            selected_befund.extension_3 = request.POST.get("extension_3_mfk")
        if "extension_4_mfk" in request.POST:
            selected_befund.extension_4 = request.POST.get("extension_4_mfk")
        if "extension_5_mfk" in request.POST:
            selected_befund.extension_5 = request.POST.get("extension_5_mfk")

        selected_befund.save()

    if befund == "einbeinstand_60_sekunden":
        selected_befund = models.Einbeinstand60Sekunden.objects.get(id=befundId)

        if "oB_e6k" in request.POST:
            selected_befund.oB = request.POST.get("oB_e6k")
        if "kann_nicht_gehalten_werden_e6k" in request.POST:
            selected_befund.kann_nicht_gehalten_werden = request.POST.get(
                "kann_nicht_gehalten_werden_e6k"
            )

        selected_befund.save()

    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        selected_befund = models.Einbeinstand30SekundenGeschlosseneAugen.objects.get(
            id=befundId
        )

        if "oB_e3k" in request.POST:
            selected_befund.oB = request.POST.get("oB_e3k")
        if "kann_nicht_gehalten_werden_e3k" in request.POST:
            selected_befund.kann_nicht_gehalten_werden = request.POST.get(
                "kann_nicht_gehalten_werden_e3k"
            )

        selected_befund.save()

    if befund == "alltagsfunktionen":
        selected_befund = models.Alltagsfunktionen.objects.get(id=befundId)

        if "tiefe_hocke_ob_afk" in request.POST:
            print("Angekommen")
            print(request.POST.get("tiefe_hocke_ob_afk"))
            selected_befund.tiefe_hocke_ob = request.POST.get("tiefe_hocke_ob_afk")
        if "tiefe_hocke_auffaellig_afk" in request.POST:
            selected_befund.tiefe_hocke_auffaellig = request.POST.get(
                "tiefe_hocke_auffaellig_afk"
            )
        if "tiefe_hocke_bemerkung_afk" in request.POST:
            selected_befund.tiefe_hocke_bemerkung = request.POST.get(
                "tiefe_hocke_bemerkung_afk"
            )

        if "huepfen_einem_bein_ob_afk" in request.POST:
            selected_befund.huepfen_einem_bein_ob = request.POST.get(
                "huepfen_einem_bein_ob_afk"
            )
        if "huepfen_einem_bein_auffaellig_afk" in request.POST:
            selected_befund.huepfen_einem_bein_auffaellig = request.POST.get(
                "huepfen_einem_bein_auffaellig_afk"
            )
        if "huepfen_einem_bein_bemerkung_afk" in request.POST:
            selected_befund.huepfen_einem_bein_bemerkung = request.POST.get(
                "huepfen_einem_bein_bemerkung_afk"
            )

        if "ferstand_ob_afk" in request.POST:
            selected_befund.ferstand_ob = request.POST.get("ferstand_ob_afk")
        if "ferstand_auffaellig_afk" in request.POST:
            selected_befund.ferstand_auffaellig = request.POST.get(
                "ferstand_auffaellig_afk"
            )
        if "ferstand_bemerkung_afk" in request.POST:
            selected_befund.ferstand_bemerkung = request.POST.get(
                "ferstand_bemerkung_afk"
            )

        if "fersenfall_ob_afk" in request.POST:
            selected_befund.fersenfall_ob = request.POST.get("fersenfall_ob_afk")
        if "fersenfall_auffaellig_afk" in request.POST:
            selected_befund.fersenfall_auffaellig = request.POST.get(
                "fersenfall_auffaellig_afk"
            )
        if "fersenfall_bemerkung_afk" in request.POST:
            selected_befund.fersenfall_bemerkung = request.POST.get(
                "fersenfall_bemerkung_afk"
            )

        if "einbeinstand_ob_afk" in request.POST:
            selected_befund.einbeinstand_ob = request.POST.get("einbeinstand_ob_afk")
        if "einbeinstand_auffaellig_afk" in request.POST:
            selected_befund.einbeinstand_auffaellig = request.POST.get(
                "einbeinstand_auffaellig_afk"
            )
        if "einbeinstand_bemerkung_afk" in request.POST:
            selected_befund.einbeinstand_bemerkung = request.POST.get(
                "einbeinstand_bemerkung_afk"
            )

        if "treppe_ob_afk" in request.POST:
            selected_befund.treppe_ob = request.POST.get("treppe_ob_afk")
        if "treppe_auffaellig_afk" in request.POST:
            selected_befund.treppe_auffaellig = request.POST.get(
                "treppe_auffaellig_afk"
            )
        if "tiefe_hocke_bemerkung_afk" in request.POST:
            selected_befund.treppe_bemerkung = request.POST.get("treppe_bemerkung_afk")

        selected_befund.save()

    if befund == "beinlaengenmessung":
        selected_befund = models.Beinlaengenmessung.objects.get(id=befundId)

        # Update anatomische Messung
        if "anatomische_messung_rechts_blk" in request.POST:
            selected_befund.anatomische_messung_rechts = request.POST.get(
                "anatomische_messung_rechts_blk"
            )
        if "anatomische_messung_links_blk" in request.POST:
            selected_befund.anatomische_messung_links = request.POST.get(
                "anatomische_messung_links_blk"
            )

        # Update funktionelle Messung
        if "funktionelle_messung_rechts_blk" in request.POST:
            selected_befund.funktionelle_messung_rechts = request.POST.get(
                "funktionelle_messung_rechts_blk"
            )
        if "funktionelle_messung_links_blk" in request.POST:
            selected_befund.funktionelle_messung_links = request.POST.get(
                "funktionelle_messung_links_blk"
            )

        selected_befund.save()

    if befund == "quadriceps_dehnungstest":
        selected_befund = models.QuadricepsDehnungstest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund_qdk" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund_qdk")

        # Update positiv auffällig
        if "positiv_auffaellig_qdk" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get(
                "positiv_auffaellig_qdk"
            )

        # Update nicht durchführbar
        if "nicht_durchfuehrbar_qdk" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar_qdk"
            )

        # Update Bemerkung
        if "bemerkung_qdk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_qdk")

        selected_befund.save()

    if befund == "m_rectus_dehnungstest":
        selected_befund = models.MRectusDehnungstest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")
        else:
            selected_befund.ohne_befund = False

        # Update positiv auffällig
        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        # Update nicht durchführbar
        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        # Update Bemerkung
        if "bemerkung" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "hamstringtest":
        selected_befund = models.Hamstringtest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        # Update positiv auffällig
        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        # Update nicht durchführbar
        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        # Update Bemerkung
        if "bemerkung" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "umfangsmessung":
        selected_befund = models.Umfangsmessung.objects.get(id=befundId)

        if "messort_10cm_oberhalb_kniegelenkspalt_rechts" in request.POST:
            selected_befund.messort_10cm_oberhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_10cm_oberhalb_kniegelenkspalt_rechts")
            )

        if "messort_10cm_oberhalb_kniegelenkspalt_links" in request.POST:
            selected_befund.messort_10cm_oberhalb_kniegelenkspalt_links = (
                request.POST.get("messort_10cm_oberhalb_kniegelenkspalt_links")
            )

        if "messort_am_kniegelenkspalt_rechts" in request.POST:
            selected_befund.messort_am_kniegelenkspalt_rechts = request.POST.get(
                "messort_am_kniegelenkspalt_rechts"
            )

        if "messort_am_kniegelenkspalt_links" in request.POST:
            selected_befund.messort_am_kniegelenkspalt_links = request.POST.get(
                "messort_am_kniegelenkspalt_links"
            )

        if "messort_10cm_unterhalb_kniegelenkspalt_rechts" in request.POST:
            selected_befund.messort_10cm_unterhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_10cm_unterhalb_kniegelenkspalt_rechts")
            )

        if "messort_10cm_unterhalb_kniegelenkspalt_links" in request.POST:
            selected_befund.messort_10cm_unterhalb_kniegelenkspalt_links = (
                request.POST.get("messort_10cm_unterhalb_kniegelenkspalt_links")
            )

        if "messort_15cm_unterhalb_kniegelenkspalt_rechts" in request.POST:
            selected_befund.messort_15cm_unterhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_15cm_unterhalb_kniegelenkspalt_rechts")
            )

        if "messort_15cm_unterhalb_kniegelenkspalt_links" in request.POST:
            selected_befund.messort_15cm_unterhalb_kniegelenkspalt_links = (
                request.POST.get("messort_15cm_unterhalb_kniegelenkspalt_links")
            )

        selected_befund.save()

    if befund == "tanzende_patella":
        selected_befund = models.TanzendePatella.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "mini_erguss_test":
        selected_befund = models.MiniErgussTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "glide_test":
        selected_befund = models.GlideTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "tilt_test":
        selected_befund = models.TiltTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "aprehension_test":
        selected_befund = models.AprehensionTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "zohlen_zeichen":
        selected_befund = models.ZohlenZeichen.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "facettendruckschmerztest":
        selected_befund = models.Facettendruckschmerztest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "valgus_test":
        selected_befund = models.ValgusTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "varus_test":
        selected_befund = models.VarusTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "lachmann_test":
        selected_befund = models.LachmannTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "vordere_schublade":
        selected_befund = models.VordereSchublade.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "pivot_shift_test":
        selected_befund = models.PivotShiftTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "hintere_schublade":
        selected_befund = models.HintereSchublade.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "gravitiy_sign":
        selected_befund = models.GravitiySign.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "loomers_test":
        selected_befund = models.LoomersTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "steinmann1":
        selected_befund = models.Steinmann1.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "steinmann3":
        selected_befund = models.Steinmann3.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "theslay_test":
        selected_befund = models.TheslayTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "mac_murray_test":
        selected_befund = models.MacMurrayTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "payr_zeichen":
        selected_befund = models.PayrZeichen.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "apley_zeichen":
        selected_befund = models.ApleyZeichen.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "medio_patellarer_plica_test":
        selected_befund = models.MedioPatellarerPlicaTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    if befund == "hughston_plica_test":
        selected_befund = models.HughstonPlicaTest.objects.get(id=befundId)

        if "ohne_befund" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund")

        if "positiv_auffaellig" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get("positiv_auffaellig")

        if "nicht_durchfuehrbar" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar"
            )

        if "bemerkung" in request.POST:
            selected_befund.ohne_befund = request.POST.get("bemerkung")

        selected_befund.save()

    return HttpResponse("Updated Succesfully")


@login_required(login_url="login")
def new_personal_befund(request, id=None):
    if id == None:
        return HttpResponse("Not valid")
    befund = request.POST.get("befund")

    if befund == "fragenevaluation_icf":
        models.FragenevaluationNachICFKategorien.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "w_fragen":
        models.FragenevaluationenNachDen7WFragen.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "standart_befund":
        models.StandartBefund.objects.create(created_for=id, created_by=request.user)
    if befund == "stand_reha_phase":
        models.StandDerReHaPhase.objects.create(created_for=id, created_by=request.user)
    if befund == "nebenerkrankungen_medikamente":
        models.NebenerkrankungenMedikamente.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "historia_morbis":
        models.HistoriaMorbis.objects.create(created_for=id, created_by=request.user)
    if befund == "nrs_numeric_rating_scale":
        models.NrsNumericRatingScale.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "aktive_beweglichkeit":
        models.AktiveBeweglichkeit.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "passive_beweglichkeit":
        models.PassiveBeweglichkeit.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "beweglichkeitsmessung":
        models.BeweglichkeitsmessungKnie.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "isometrischer_krafttest":
        models.IsometrischerKrafttest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "muskelfunktionspruefung":
        models.Muskelfunktionspruefung.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "einbeinstand_60_sekunden":
        models.Einbeinstand60Sekunden.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        models.Einbeinstand30SekundenGeschlosseneAugen.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "alltagsfunktionen":
        models.Alltagsfunktionen.objects.create(created_by=request.user, created_for=id)
    if befund == "beinlaengenmessung":
        models.Beinlaengenmessung.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "quadriceps_dehnungstest":
        models.QuadricepsDehnungstest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "m_rectus_dehnungstest":
        models.MRectusDehnungstest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "hamstringtest":
        models.Hamstringtest.objects.create(created_by=request.user, created_for=id)
    if befund == "umfangsmessung":
        models.Umfangsmessung.objects.create(created_by=request.user, created_for=id)
    if befund == "tanzende_patella":
        models.TanzendePatella.objects.create(created_by=request.user, created_for=id)
    if befund == "mini_erguss_test":
        models.MiniErgussTest.objects.create(created_by=request.user, created_for=id)
    if befund == "glide_test":
        models.GlideTest.objects.create(created_by=request.user, created_for=id)
    if befund == "tilt_test":
        models.TiltTest.objects.create(created_by=request.user, created_for=id)
    if befund == "aprehension_test":
        models.AprehensionTest.objects.create(created_by=request.user, created_for=id)
    if befund == "zohlen_zeichen":
        models.ZohlenZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "facettendruckschmerztest":
        models.Facettendruckschmerztest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "valgus_test":
        models.ValgusTest.objects.create(created_by=request.user, created_for=id)
    if befund == "varus_test":
        models.VarusTest.objects.create(created_by=request.user, created_for=id)
    if befund == "lachmann_test":
        models.LachmannTest.objects.create(created_by=request.user, created_for=id)
    if befund == "vordere_schublade":
        models.VordereSchublade.objects.create(created_by=request.user, created_for=id)
    if befund == "pivot_shift_test":
        models.PivotShiftTest.objects.create(created_by=request.user, created_for=id)
    if befund == "hintere_schublade":
        models.HintereSchublade.objects.create(created_by=request.user, created_for=id)
    if befund == "gravitiy_sign":
        models.GravitiySign.objects.create(created_by=request.user, created_for=id)
    if befund == "loomers_test":
        models.LoomersTest.objects.create(created_by=request.user, created_for=id)
    if befund == "steinmann1":
        models.Steinmann1.objects.create(created_by=request.user, created_for=id)
    if befund == "steinmann3":
        models.Steinmann3.objects.create(created_by=request.user, created_for=id)
    if befund == "theslay_test":
        models.TheslayTest.objects.create(created_by=request.user, created_for=id)
    if befund == "mac_murray_test":
        models.MacMurrayTest.objects.create(created_by=request.user, created_for=id)
    if befund == "payr_zeichen":
        models.PayrZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "apley_zeichen":
        models.ApleyZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "medio_patellarer_plica_test":
        models.MedioPatellarerPlicaTest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "hughston_plica_test":
        models.HughstonPlicaTest.objects.create(created_by=request.user, created_for=id)
    return HttpResponse("Updated Succesfully")


@login_required(login_url="login")
def delete_personal_befund(request, id=None, befundId=None):
    if id == None:
        return HttpResponse("Not valid")
    befund = request.POST.get("befund")
    if befund == "fragenevaluation_icf":
        selected_befund = models.FragenevaluationNachICFKategorien.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        selected_befund = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "w_fragen":
        selected_befund = models.FragenevaluationenNachDen7WFragen.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "standart_befund":
        selected_befund = models.StandartBefund.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "stand_reha_phase":
        selected_befund = models.StandDerReHaPhase.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "nebenerkrankungen_medikamente":
        selected_befund = models.NebenerkrankungenMedikamente.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "historia_morbis":
        selected_befund = models.HistoriaMorbis.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "nrs_numeric_rating_scale":
        selected_befund = models.NrsNumericRatingScale.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "aktive_beweglichkeit":
        selected_befund = models.AktiveBeweglichkeit.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "passive_beweglichkeit":
        selected_befund = models.PassiveBeweglichkeit.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "beweglichkeitsmessung":
        selected_befund = models.BeweglichkeitsmessungKnie.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "isometrischer_krafttest":
        selected_befund = models.IsometrischerKrafttest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "muskelfunktionspruefung":
        selected_befund = models.Muskelfunktionspruefung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "einbeinstand_60_sekunden":
        selected_befund = models.Einbeinstand60Sekunden.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        selected_befund = models.Einbeinstand30SekundenGeschlosseneAugen.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "alltagsfunktionen":
        selected_befund = models.Alltagsfunktionen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "beinlaengenmessung":
        selected_befund = models.Beinlaengenmessung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "quadriceps_dehnungstest":
        selected_befund = models.QuadricepsDehnungstest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "m_rectus_dehnungstest":
        selected_befund = models.MRectusDehnungstest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hamstringtest":
        selected_befund = models.Hamstringtest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "umfangsmessung":
        selected_befund = models.Umfangsmessung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "tanzende_patella":
        selected_befund = models.TanzendePatella.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "mini_erguss_test":
        selected_befund = models.MiniErgussTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "glide_test":
        selected_befund = models.GlideTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "tilt_test":
        selected_befund = models.TiltTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "aprehension_test":
        selected_befund = models.AprehensionTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "zohlen_zeichen":
        selected_befund = models.ZohlenZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "facettendruckschmerztest":
        selected_befund = models.Facettendruckschmerztest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "valgus_test":
        selected_befund = models.ValgusTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "varus_test":
        selected_befund = models.VarusTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "lachmann_test":
        selected_befund = models.LachmannTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "vordere_schublade":
        selected_befund = models.VordereSchublade.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "pivot_shift_test":
        selected_befund = models.PivotShiftTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hintere_schublade":
        selected_befund = models.HintereSchublade.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "gravitiy_sign":
        selected_befund = models.GravitiySign.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "loomers_test":
        selected_befund = models.LoomersTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "steinmann1":
        selected_befund = models.Steinmann1.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "steinmann3":
        selected_befund = models.Steinmann3.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "theslay_test":
        selected_befund = models.TheslayTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "mac_murray_test":
        selected_befund = models.MacMurrayTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "payr_zeichen":
        selected_befund = models.PayrZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "apley_zeichen":
        selected_befund = models.ApleyZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "medio_patellarer_plica_test":
        selected_befund = models.MedioPatellarerPlicaTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hughston_plica_test":
        selected_befund = models.HughstonPlicaTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    return HttpResponse("Updated Succesfully")
