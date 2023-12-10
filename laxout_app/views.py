from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import LaxoutUser, Laxout_Exercise
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
import random
import string
from django.contrib.auth import logout, authenticate, login


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')  # Hier 'login' durch den Namen deiner Login-URL ersetzen
    else:
        # Du könntest hier auch eine eigene Logout-Seite rendern
        # return render(request, 'logout.html')
        pass




def random_string(length=100):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def display_login_code(request, logintoken= None):
    return render(request, 'laxout_app/display_code.html', {"login_token": logintoken})

# Create your views here.
@login_required(login_url="login")
def home(request):
    users = LaxoutUser.objects.all()
    user_list = []
    for user in users:
        if user.created_by == request.user:
            user_list.append(user)
    return render(
        request,
        "laxout_app/home.html",
        {"users": user_list},
    )


@login_required(login_url="login")
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            insteance = form.save(commit=False)
            insteance.created_by = request.user
            insteance.save()
            return redirect("/home")

    else:
        form = UserForm()
        return render(request, "laxout_app/create_user.html", {"form": form})


@login_required(login_url="login")
def delete_user(request, id=None):
    if id != None:
        object_to_delte = LaxoutUser.objects.get(id=id)
        if request.user == object_to_delte.created_by:
            object_to_delte.delete()
        return redirect("/home")
    return redirect("/home")


@login_required(login_url="login")
def edit_user(request, id=None):
    users = LaxoutUser.objects.get(id=id)
    return render(
        request,
        "laxout_app/edit_user.html",
        {"users": users},
    )


def get_workout_list(first, second):
    to_return = []
    uebungen_to_append = []
    if first == 0 and second == 0:
        uebungen_to_append = [1, 2, 3, 23, 48, 49]
    if first == 0 and second == 1:
        uebungen_to_append = [24, 25, 27, 28]
    if first == 0 and second == 2:
        uebungen_to_append = [4, 5, 19, 20, 21, 22]
    if first == 1 and second == 0:
        uebungen_to_append = [1, 29, 30, 31, 41, 43, 44, 45, 46, 47, 48, 49, 67]
    if first == 1 and second == 1:
        uebungen_to_append = [26, 29, 37, 38, 39, 41, 42, 43, 64, 65, 66, 68, 69, 70]
    if first == 1 and second == 2:
        uebungen_to_append = [6, 7, 8, 9, 32, 33, 34, 35, 36]
    if first == 2 and second == 0:
        uebungen_to_append = [14, 117, 18, 105, 106, 107, 108, 109, 110]
    if first == 2 and second == 1:
        uebungen_to_append = [38, 96, 10, 103]
    if first == 2 and second == 2:
        uebungen_to_append = [15, 16, 94, 95]
    if first == 3 and second == 0:
        uebungen_to_append = []
    if first == 3 and second == 1:
        uebungen_to_append = [
            66,
            97,
            102,
            119,
            120,
            121,
            122,
            123,
            124,
            125,
            126,
            127,
            128,
            141,
        ]
    if first == 3 and second == 2:
        uebungen_to_append = [92, 93, 94, 95, 96, 112, 113, 114, 115, 116, 117, 118]
    if first == 4 and second == 0:
        uebungen_to_append = [
            10,
            11,
            105,
            106,
            107,
            108,
            134,
            142,
            143,
            144,
            145,
            146,
            147,
            158,
            165,
            166,
        ]
    if first == 4 and second == 1:
        uebungen_to_append = [
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            124,
            135,
            136,
            137,
            138,
            139,
            140,
            141,
            158,
            165,
            166,
        ]
    if first == 4 and second == 2:
        uebungen_to_append = [
            12,
            13,
            94,
            95,
            112,
            113,
            114,
            115,
            117,
            118,
            129,
            130,
            131,
            132,
            133,
            134,
            148,
            149,
        ]
    if first == 5 and second == 0:
        uebungen_to_append = [40, 67, 104, 156, 158, 161, 162, 163, 164, 165]
    if first == 5 and second == 1:
        uebungen_to_append = [
            123,
            139,
            156,
            157,
            158,
            159,
            160,
            161,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
        ]
    if first == 5 and second == 2:
        uebungen_to_append = [148, 149, 150, 151, 152, 153, 154, 155, 166, 168]
    if first == 6 and second == 0:
        uebungen_to_append = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 63, 169]
    if first == 6 and second == 1:
        uebungen_to_append = [64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77]
    if first == 6 and second == 2:
        uebungen_to_append = [
            60,
            61,
            67,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            111,
        ]

    uebungen = Laxout_Exercise.objects.all()
    for i in uebungen:
        for z in uebungen_to_append:
            if i.id == z:
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
        return render(
            request, "laxout_app/add_exercises.html", {"workouts": workout_list}
        )

    if request.method == "POST":
        new_execution = request.POST.get("execution")
        new_dauer = request.POST.get("dauer") #.objects.get(id=new_id)
        new_id = request.POST.get("id")
        print(new_dauer)
        user_instance = LaxoutUser.objects.get(id=id)
        exercise_to_add = Laxout_Exercise()
        exercise_to_add.execution = new_execution
        exercise_to_add.name = Laxout_Exercise.objects.get(id=new_id).name
        exercise_to_add.dauer = Laxout_Exercise.objects.get(id=new_id).dauer
        exercise_to_add.videoPath = Laxout_Exercise.objects.get(id=new_id).videoPath
        exercise_to_add.looping = Laxout_Exercise.objects.get(id=new_id).looping
        exercise_to_add.added = Laxout_Exercise.objects.get(id=new_id).added
        exercise_to_add.instruction = Laxout_Exercise.objects.get(id=new_id).instruction
        exercise_to_add.timer = Laxout_Exercise.objects.get(id=new_id).timer
        exercise_to_add.required = Laxout_Exercise.objects.get(id=new_id).required
        exercise_to_add.imagePath = Laxout_Exercise.objects.get(id=new_id).imagePath
        if new_dauer:
            exercise_to_add.dauer = new_dauer
        print(exercise_to_add.dauer)
        exercise_to_add.save()
        user_instance.exercises.add(exercise_to_add)
        if request.user == user_instance.created_by:
            user_instance.save()

    workout_list = get_workout_list(0, 0)
    return render(request, "laxout_app/add_exercises.html", {"workouts": workout_list})


@login_required(login_url="login")
def edit_user_workout(request, id=None,):
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        new_dauer = request.POST.get("dauer") #.objects.get(id=new_id)
        new_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        print(new_dauer)
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(id=new_id)#<---- kann ich so auf die Übung zugreifen, die ich bearbeiten möchte ?
        if new_execution:
           exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        if request.user == user_instance.created_by:
            user_instance.save()
    return render(request, "laxout_app/edit_user.html",)

@login_required(login_url="login")
def delete_user_workout(request, id=None,):
    if request.method == "POST":
        new_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(id=new_id)#<---- kann ich so auf die Übung zugreifen, die ich bearbeiten möchte ?
        if request.user == user_instance.created_by:
            exercise_to_edit.delete()
            user_instance.save()
    return render(request, "laxout_app/edit_user.html",)



           
# @login_required(login_url="login")
# def execute_data_transfer(request):
#     for i in uebungen:
#         uebung = Laxout_Exercise()
#         uebung.looping = i.looping
#         uebung.timer = i.timer
#         uebung.execution = i.execution
#         uebung.name = i.name
#         uebung.videoPath = i.videoPath
#         uebung.dauer = i.dauer
#         uebung.imagePath = i.imagePath
#         uebung.added = i.added
#         uebung.instruction = i.instruction
#         uebung.required = i.required
#         uebung.save()
#     # uebungenToDelete = Laxout_Exercise.objects.all()
#     # for i in uebungenToDelete:
#     #     i.delete()
 


