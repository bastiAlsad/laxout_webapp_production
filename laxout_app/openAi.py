import openai
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from laxout import settings
from openai import OpenAI, AssistantEventHandler, AzureOpenAI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models, signals
import json
from typing_extensions import override
from uuid import uuid4

client = OpenAI(api_key=settings.OPENAI_API_KEY)

client_azure = AzureOpenAI(
    api_key=settings.AZURE_API_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=settings.AZURE_END_POINT,
)


@login_required(login_url="login")
def get_diagnosis(request, id=None):
    if request.method == "POST":
        body = None
        patient_info = ""
        ananmnnese_list = models.AnanmenseBefund.objects.filter(created_for=id)
        schmerz_list = models.SchmerzBefund.objects.filter(created_for=id)

        for i in ananmnnese_list:
            patient_info += i.disability + f"Stand({i.created_at})"

        for i in schmerz_list:
            patient_info += i.opinion_patient + f"Stand({i.created_at})"
            patient_info += f"Aktuelles Schmerzlevel: (Stand {i.created_at})" + str(
                i.current_pain_level
            )

        # patient_info += f"Aktuelles Schmerzlevel: (Stand {i.created_at})" +i.current_pain_level
        # medikamente_list = models.MedikamentBefund.objects.filter(created_for=id)
        # test1_list = models.Test1Befund.objects.filter(created_for=id)
        # test2_list = models.Test2Befund.objects.filter(created_for=id)
        # test3_list = models.Test3Befund.objects.filter(created_for=id)

        if not patient_info:
            return JsonResponse(
                {"error": "No patient information provided"}, status=400
            )

        def generate():
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Du bist ein erfahrener Physiotherapeut und sollst eine Diagnose aufgrund der folgenden Patienteninformationen stellen. Deine Antwort soll nur die mögliche Diagnose enthalten, ohne Behandlungsvorschläge. Formuliere es schön aus.",
                    },
                    {
                        "role": "user",
                        "content": f"Hier sind die Informationen: {patient_info}. Welche Diagnose könnte der Patient haben?",
                    },
                ],
                stream=True,
            )

            response_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    last_period_index = response_text.rfind(".")
                    if last_period_index != -1:
                        # Yield the complete sentence up to the last period
                        yield response_text[: last_period_index + 1].strip()
                        response_text = response_text[last_period_index + 1 :]

        return StreamingHttpResponse(generate(), content_type="text/event-stream")
    return render(request, "laxout_app/diagnose.html")


@login_required(login_url="login")
def ki_formulieren(request, id=None):
    if request.method == "POST":

        if request.method == "POST":

            data = json.loads(request.body)

            befund = data.get("befund")
            textfeld = data.get("textfeld")
            value = data.get("value")

            if befund is None or textfeld is None:
                return HttpResponse("Fehler: Befund oder Textfeld fehlen.")

            def generate():
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[
                        {
                            "role": "system",
                            "content": f"Du bist ein erfahrener Physiotherapeut und sollst folgende Bruchstücke von Sätzen bzw. Schlagwörter in einen sich schön anhörenden Text mit korrekter Grammatik und Rechtschreibung umformulieren. Mache nach jedem Punkt ein Leerzeichen. Verwende Fachsprache und achte auf logische Zusammenhänge. Der Text soll für das Textfeld {textfeld} eines {befund} Befundes sein.",
                        },
                        {
                            "role": "user",
                            "content": f"Hier ist der umzuformulierende Text: {value}",
                        },
                    ],
                    stream=True,
                )

                response_text = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        response_text += chunk.choices[0].delta.content
                        last_period_index = response_text.rfind(".")
                        if last_period_index != -1:
                            # Yield the complete sentence up to the last period
                            yield response_text[: last_period_index + 1].strip()
                            response_text = response_text[last_period_index + 1 :]

            return StreamingHttpResponse(generate(), content_type="text/event-stream")
    return HttpResponse("OK")


# def make_pre_call(illness, plan_info):
#     category_ids = [
#         {"id": 1, "category": "Nacken/HWS"},
#         {"id": 2, "category": "Schultern"},
#         {"id": 3, "category": "Mittlerer Rücken/BWS"},
#         {"id": 4, "category": "Bauch/Rumpf"},
#         {"id": 5, "category": "Unterer Rücken/LWS/Hüfte"},
#         {"id": 6, "category": "Beine/Knie/Füße"},
#         {"id": 7, "category": "Arme/Ellenbogen/Handgelenke"},
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": "provide your answer in valid json",
#             },
#             {
#                 "role": "system",
#                 "content": "Du bist ein augebildeter Sportwissenschaftler und Physio uns sollt mir bei der Erstellung von Trainingsplänen assistieren. Hierfür musst du mir bitte sagen, welche Kategorie von Körperbereichen bzw. deren IDs bei der Erstellung eines trainingsplans relevant sind. Deine Antwort, einen array 'category_list' aus category ids gibts du in form valid JSON response zurück. Es sollen nicht mehr wie 3 ids in der Antwort enthalten sein. Ich gebe dir 200€ wenn du es gut machst.",
#             },
#             {
#                 "role": "system",
#                 "content": f"Hier sind die Kategorien mit den dazugehörigen Ids:{category_ids}",
#             },
#             {
#                 "role": "user",
#                 "content": f"Hier die Info zu dem Plan {illness} Gib mir nur JSON zurück mit der category_list!",
#             },
#         ],
#         stream=False,
#     )
#     content = response.choices[0].message.content
#     try:
#         json_data = json.loads(content)
#         category_list = json_data.get("category_list", [])
#     except:
#         category_list = []

#     return category_list


# def create_ai_plan(illness, plan_info, fine_tuning_object):
#     context_ai = []
#     category_list_labels = []
#     category_list = make_pre_call(illness=illness, plan_info=plan_info)

#     for i in category_list:
#         if i == 1:
#             category_list_labels.append("nacken/hws")
#             for id in signals.uebungen_to_append00:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append01:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append02:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 2:
#             category_list_labels.append("schulter")
#             for id in signals.uebungen_to_append10:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append11:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append12:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 3:
#             category_list_labels.append("mittlerer Rücken/BWS")
#             for id in signals.uebungen_to_append20:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append21:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append22:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 4:
#             category_list_labels.append("bauch/Rumpf")
#             for id in signals.uebungen_to_append30:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append31:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append32:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 5:
#             category_list_labels.append("unterer Rücken/hüfte")
#             for id in signals.uebungen_to_append40:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append41:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append42:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 6:
#             category_list_labels.append("knie/beine")
#             for id in signals.uebungen_to_append50:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append51:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append52:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 7:
#             category_list_labels.append("ellenbogen/arme/hände")
#             for id in signals.uebungen_to_append60:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append61:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append62:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#     response = client.chat.completions.create(
#         response_format={"type": "json_object"},
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "provide your answer in valid json",
#             },
#             {
#                 "role": "system",
#                 "content": "du bist ein studierter und hochangesehener Sportwissenschaftler und Physiotherapeu uns sollt mir bei der Erstellung von Trainingsplänen assistieren. Deine Antwort, einen array 'uebung_list' aus Übungs ids gibts du in form einer JSON Antwort zurück. Der Plan soll nicht zu lang werden. INFO: Jede Übung die du hinzufügst dauert ca. 30 sek. Mache Übungen bei denen es rechts/links gibt hintereinander. Fange mit Mobilisationsübungen an, dann Kräftiung dann Dehnung. ",
#             },
#             {
#                 "role": "user",
#                 "content": f"Name Trainingsplan{illness}, Infos Plan{plan_info}, übungen, aus denen du nur die ids auswählen sollst: {context_ai}",
#             },
#         ],
#         stream=False,
#     )
#     counter = 0
#     for category in category_list_labels:
#         interpreted_category = models.InterpretedCategory.objects.create(category = category, category_id = category_list[counter])
#         fine_tuning_object.interpreted_categorys.add(interpreted_category)
#         counter += 1
#     fine_tuning_object.save()

#     content = response.choices[0].message.content
#     try:
#         json_data = json.loads(content)
#         uebung_list = json_data.get("uebung_list", [])
#         print(content)

#     except:
#         uebung_list = []

#     return uebung_list


# @login_required(login_url="login")
# def update_ai_plan(request, id=None):
#     ai_training_data_object = models.AiTrainingDataGlobal.objects.get(id=id)
    
#     prompt = request.POST.get("")
    
#     fine_tuning_object = models.FineTuningTrainingData.objects.get(created_for = ai_training_data_object.id)
#     categorys = fine_tuning_object.interpreted_categorys.all()

#     category_list = [category.category_id for category in categorys]
    
#     category_context = {"category_list": [category_list]}

#     category_ids = [
#         {"id": 1, "category": "Nacken/HWS"},
#         {"id": 2, "category": "Schultern"},
#         {"id": 3, "category": "Mittlerer Rücken/BWS"},
#         {"id": 4, "category": "Bauch/Rumpf"},
#         {"id": 5, "category": "Unterer Rücken/LWS/Hüfte"},
#         {"id": 6, "category": "Beine/Knie/Füße"},
#         {"id": 7, "category": "Arme/Ellenbogen/Handgelenke"},
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": "provide your answer in valid json",
#             },
#             {
#                 "role": "system",
#                 "content": "Du bist ein augebildeter Sportwissenschaftler und Physio uns sollt mir bei der Erstellung von Trainingsplänen assistieren. Hierfür musst du mir bitte sagen, welche Kategorie von Körperbereichen bzw. deren IDs bei der Erstellung eines trainingsplans relevant sind. Deine Antwort, einen array 'category_list' aus category ids gibts du in form valid JSON response zurück. Ich gebe dir 200€ wenn du es gut machst.",
#             },
#             {
#                 "role": "system",
#                 "content": f"Hier sind die Kategorien mit den dazugehörigen Ids:{category_ids}",
#             },
#             {
#                 "role": "user",
#                 "content": f"Hier die Info zu dem Plan {fine_tuning_object.plan_name} Gib mir nur JSON zurück mit der category_list!",
#             },
#             {
#                 "role": "assistant",
#                 "content": f"{category_context}",
#             },
#             {
#                 "role": "user",
#                 "content": f"{prompt} Treffe nun mit meiner Anweisung erneut eine Auswahl und gib Sie in der JSON response in 'category_list' zurück.",
#             },
#         ],
#         stream=False,
#     )

#     response_category_list = response.choices[0].message.content
#     try:
#         json_data = json.loads(response_category_list)
#         finished_category_list = json_data.get("category_list", [])
#         print(response_category_list)

#     except:
#         finished_category_list = []

#     context_ai = []

#     for i in finished_category_list:
#         if i == 1:
#             for id in signals.uebungen_to_append00:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append01:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append02:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "nacken/hws",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 2:
#             for id in signals.uebungen_to_append10:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append11:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append12:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "schulter",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 3:
#             for id in signals.uebungen_to_append20:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append21:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append22:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "mittlerer Rücken/BWS",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 4:
#             for id in signals.uebungen_to_append30:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append31:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append32:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "bauch/Rumpf",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#         if i == 5:
#             for id in signals.uebungen_to_append40:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append41:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )

#             for id in signals.uebungen_to_append42:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "unterer Rücken/hüfte",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 6:
#             for id in signals.uebungen_to_append50:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append51:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append52:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "knie/beine",
#                         "kategorie": "dehnübung",
#                     }
#                 )
#         if i == 7:
#             for id in signals.uebungen_to_append60:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "mobilisationsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append61:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "kräftigungsübung",
#                     }
#                 )
#             for id in signals.uebungen_to_append62:
#                 context_ai.append(
#                     {
#                         "id": id,
#                         "name": models.Uebungen_Models.objects.get(id=id).name,
#                         "körperbereich": "ellenbogen/arme/hände",
#                         "kategorie": "dehnübung",
#                     }
#                 )

#     uebung_list_objects = fine_tuning_object.related_exercise_ids.all()
#     uebung_list = [uebung.exercise_id for uebung in uebung_list_objects]
#     uebung_list_context = {"uebung_list":uebung_list}

#     response2 = client.chat.completions.create(
#         response_format={"type": "json_object"},
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "provide your answer in valid json",
#             },
#             {
#                 "role": "system",
#                 "content": "du bist ein studierter und hochangesehener Sportwissenschaftler und Physiotherapeu uns sollt mir bei der Erstellung von Trainingsplänen assistieren. Deine Antwort, einen array 'uebung_list' aus Übungs ids gibts du in form einer JSON Antwort zurück. Der Plan soll nicht zu lang werden. INFO: Jede Übung die du hinzufügst dauert ca. 30 sek. Mache Übungen bei denen es rechts/links gibt hintereinander. Fange mit Mobilisationsübungen an, dann Kräftiung dann Dehnung. ",
#             },
#             {
#                 "role": "user",
#                 "content": f"Name Trainingsplan{fine_tuning_object.plan_name}, Infos Plan{fine_tuning_object.plan_info}",
#             },
#             {
#                 "role": "assistant",
#                 "content": f"{uebung_list_context}",
#             },
#             {
#                 "role": "user",
#                 "content": f"{prompt} Passe die Uebung list nun nach meinen Wünschen an und gibt mir nur die JSON response mit der 'uebung_list'!",
#             },
#         ],
#         stream=False,
#     )


#     response_uebung_list= response2.choices[0].message.content
#     try:
#         json_data = json.loads(response_uebung_list)
#         finished_uebung_list = json_data.get("uebung_list", [])
#         print(response_uebung_list)
#     except:
#         finished_uebung_list = []



    

#     print(f"Finished Ubeung List {finished_uebung_list}")

#     return render(request, "laxout_app/edit_plan.html")


# def create_training_data():
#     jsonl_file_path = "fine_tuning_data.jsonl"
#     with open(jsonl_file_path, "w") as file:
#         fine_tuning_objects = models.FineTuningTrainingData.objects.all()

#         # Gemeinsame System-Nachricht für alle Einträge
#         system_message = {
#             "role": "system",
#             "content": "Du bist ein Sportwissenschaftler der basierend auf der Körperregion und zusätzlichen Informationen Trainingspläne für Patienten aus vorgegebenen Übungen erstellt. Du gibst eine Antwort im JSON Format. Diese antwort enhält eine 'uebung_list' mit den IDs der Übungen. Diese IDs gehen von 1-257.",
#         }

#         for i in fine_tuning_objects:
#             current_uebung_list = []
#             exercise_id_objects = i.related_exercise_ids.all()
#             for obj in exercise_id_objects:
#                 current_uebung_list.append(obj.exercise_id)

#             # Erstellen des JSON-Strings für die 'uebung_list'
#             uebung_list_json = json.dumps({"uebung_list": current_uebung_list})

#             # Erstellen der Benutzer- und Assistent-Nachrichten
#             user_message = {
#                 "role": "user",
#                 "content": f"Name Trainingsplan {i.plan_name}, Infos Plan {i.plan_info}",
#             }
#             assistant_message = {"role": "assistant", "content": uebung_list_json}

#             # Schreiben der vollständigen Nachricht in die JSONL-Datei
#             file.write(
#                 json.dumps(
#                     {"messages": [system_message, user_message, assistant_message]}
#                 )
#                 + "\n"
#             )

#     return HttpResponse("OK")


# def generate_image(prompt):
#     try:
#         # Bild generieren

#         response = client.images.generate(
#             model="dall-e-3",
#             prompt=prompt,
#             size="1024x1024",
#             quality="standard",
#             n=1,
#         )


#         image_url = response.data[0].url
#         return image_url
#     except Exception as e:
#         print(f"Fehler bei der Bildgenerierung: {e}")
#         return None
from django.shortcuts import get_object_or_404
from openai import OpenAI


# @login_required(login_url="login")
# def create_assistant(request, partner_name=None):

#     assistant = client.beta.assistants.create(
#         name="Physiotherapist",
#         instructions="You are a helpful assistant for a Physiotherapy Practice named 'Therapiezentrum Wörndl'. You give patients information about opening times, and so on.",
#         model="gpt-4o",
#         tools=[{"type": "file_search"}],
#     )

#     vector_store = client.beta.vector_stores.create(name="praxis_woernld_laxout")

#     file_paths = ["infos_woerndl.txt"]
#     file_streams = [open(path, "rb") for path in file_paths]

#     # Use the upload and poll SDK helper to upload the files, add them to the vector store,
#     # and poll the status of the file batch for completion.
#     file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#         vector_store_id=vector_store.id, files=file_streams
#     )

#     assistant = client.beta.assistants.update(
#         assistant_id=assistant.id,
#         tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
#     )

#     # Create a thread
#     message_file = client.files.create(
#         file=open("infos_woerndl.txt", "rb"), purpose="assistants"
#     )

#     # Create a thread and attach the file to the message
#     thread = client.beta.threads.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Wer ist inhaber der Praxis Woerndl? ",
#                 # Attach the new file to the message.
#                 "attachments": [
#                     {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
#                 ],
#             }
#         ]
#     )

#     # Run the thread
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread.id, assistant_id=assistant.id
#     )

#     messages = list(
#         client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
#     )

#     message_content = messages[0].content[0].text
#     annotations = message_content.annotations
#     citations = []
#     for index, annotation in enumerate(annotations):
#         message_content.value = message_content.value.replace(
#             annotation.text, f"[{index}]"
#         )
#         if file_citation := getattr(annotation, "file_citation", None):
#             cited_file = client.files.retrieve(file_citation.file_id)
#             citations.append(f"[{index}] {cited_file.filename}")

#     print(message_content.value)
#     print("\n".join(citations))

#     print(
#         f"###################################################################################{assistant.id}###########################################################################"
#     )
#     chat_assistant, creatred = models.ChatAssistant.objects.get_or_create(
#         created_for=request.user
#     )
#     chat_assistant.assistant_id = assistant.id
#     chat_assistant.partner_name = partner_name
#     chat_assistant.save()

#     return HttpResponse("OK")


# import time


# def chatApplication(request, partner=None):
#     if request.method == "POST":
#         try:
#             # Hole den ChatAssistant Eintrag basierend auf dem Partner
#             assistant_instance = models.ChatAssistant.objects.get(partner_name=partner)

#             # Extrahiere die Frage aus der POST-Anfrage
#             question = request.POST.get("message")
#             thread = client.beta.threads.create(
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": question,
#                         # Attach the new file to the message.
#                     }
#                 ]
#             )

#             run = client.beta.threads.runs.create_and_poll(
#                 thread_id=thread.id, assistant_id=assistant_instance.assistant_id
#             )

#             messages = list(
#                 client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
#             )

#             message_content = messages[0].content[0].text

#             print(message_content.value)

#             return JsonResponse({"answer_chat_assistant": message_content.value})
#         except Exception as e:
#             # Allgemeine Fehlerbehandlung
#             return JsonResponse({"error": str(e)}, status=500)

#     return render(request, "laxout_app/assistant_chat.html")


# def api_call_anamnese_chat(user_input, anamnese_chat, questions, index):
#     message_object = models.AnamneseMessage.objects.create(
#         message=user_input, bot_message=False
#     )
#     anamnese_chat.messages.add(message_object)

#     completion = client.chat.completions.create(
#         model="ft:gpt-3.5-turbo-0125:laxout::9pIq31Ai",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant who assists users in understanding and completing an anamnesis form. Your task is to determine whether the user is asking a question because they do not understand something or if they are providing an answer to the form.If the user asks a question or indicates confusion, explain the relevant part to them.Respond in valid JSON format with:'answer_on_users_question': Your explanation or answer to the user's question, if necessary.'user_asked_question': A boolean indicating whether the user asked a question in their input.",
#             },
#             {
#                 "role": "user",
#                 "content": f"Frage aus dem Fragebogen: {questions[index]} User input zu dieser Frage: {user_input}.",
#             },
#         ],
#     )
#     print(f"Frage Fragebogen:{questions[index]}")
#     print(f"User Input:{user_input}")
#     print(completion.choices[0].message)
#     content = completion.choices[0].message.content
#     return content


# def anamnese_chat_applikation(request, partner=None):
#     index = request.POST.get("index")
#     print(f"Empfangener index {index}")
#     if index is None:
#         index = 0
#         print("Index got reset")
#     else:
#         index = int(index)

#     uid = request.POST.get("uid")
#     if uid is None:
#         uid = str(uuid4())
#         while models.AnamneseChat.objects.filter(uid=uid).exists():
#             uid = str(uuid4())
#         anamnese_chat = models.AnamneseChat.objects.create(uid=uid)
#     else:
#         anamnese_chat = models.AnamneseChat.objects.get(uid=uid)

#     questions = [
#         "Wie heißen Sie mit Vor- und Nachnamen?",
#         "Wie heißen Sie mit Vor- und Nachnamen?",
#         "In welcher Stadt leben Sie ?",
#         "Was ist Ihre Adresse?",
#         "Welchen Beruf haben Sie?",
#         "Haben Sie Hobbys oder treiben Sie Sport? Wenn ja was tun Sie ?"
#         "Welche Diagnose liegt bei Ihnen vor?",
#         "Bei welcher Versicherung sind Sie versichert?",
#         "Wie alt sind Sie ?",
#         "Welche Therapiemaßnahmen hat der Artzt Ihnen verschrieben? (z.B. Krankengymnastik)",
#         "Haben Sie ohne bekannte Ursache an Gewicht verloren?",
#         "Leiden Sie unter Schmerzen, die Sie nachts wach halten?",
#         "Haben Sie Veränderungen in Ihrer Blasen-/Darmkontrolle bemerkt?",
#         "Fühlen Sie Taubheit oder Kribbeln in bestimmten Körperregionen?",
#         "Hatten Sie kürzlich Fieber oder andere Infektionssymptome? Wenn ja, welche?",
#         "Ist Ihnen eine ungewöhnliche Schwellung oder Rötung an einer Körperstelle aufgefallen? Wenn ja, wo?",
#         "Haben Sie Schwierigkeiten beim Gehen oder bei der Koordination Ihrer Bewegungen?",
#         "Sind Ihre Schmerzen nach einem Trauma oder Unfall aufgetreten? Wenn ja, welche?",
#         "Haben Sie Schmerzen, die nicht auf Medikamente ansprechen? Wenn ja, welche?",
#         "Haben Sie eine Vorgeschichte mit Krebserkrankungen? Wenn ja, welche?",
#         "Erleben Sie eine plötzliche Schwäche in den Armen oder Beinen?",
#         "Liegt eine plötzliche Veränderung der Sehkraft vor?",
#         "Erleben Sie bei Anstrengungen Atemnot oder Brustschmerzen?",
#         "Liegen Schluckbeschwerden oder Sprachveränderungen vor?",
#         "Leiden Sie unter anhaltenden Kopfschmerzen?",
#         "Fühlen Sie sich in Ihrem Alltag stark eingeschränkt?",
#         "Haben Sie das Gefühl, dass Stress Ihre Schmerzen/Beschwerden verschlimmert?",
#         "Leiden Sie unter Schlafstörungen aufgrund Ihrer Schmerzen/Beschwerden?",
#         "Empfinden Sie Ihre Schmerzen/Beschwerden als unerträglich oder überwältigend?",
#         "Machen Sie sich häufig Sorgen um Ihre Gesundheit?",
#         "Vermeiden Sie Aktivitäten, die Sie früher genossen haben?",
#         "Fühlen Sie sich oft hoffnungslos und deprimiert?",
#         "Haben Sie das Gefühl, dass Ihre Lebensqualität durch Ihre Schmerzen stark beeinträchtigt ist?",
#         "Haben Sie von Ihren Ärzten einen Arztbericht, Röntgenaufnahmen, Unterlagen oder einen Nachbehandlungsplan bekommen?",
#         "Gibt es eine ärztliche Anweisung, für die eine Belastungsstufe, die Sie einhalten müssen bzw. hat Ihr Arzt eine Belastungsstufe für Sie festgelegt, die wir beachten sollten?",
#         "Benötigen Sie Hilfsmittel im Alltag? Z.B.Orthesen, Schiene, Gips, Bandagen, Gehstützen, Schuheinlagen, Rollator, Rollstuhl, Orthopädische Schuhe etc.",
#     ]

#     if request.method == "POST":
#         user_input = request.POST.get("message")
#         if index == 0:
#             if user_input.lower() == "ja":
#                 index += 1
#                 message_object = models.AnamneseMessage.objects.create(
#                     message="Super! Dann lassen Sie uns doch mit einer kurzen Vorstellung beginnen. Mein Name ist Laxo und ich bin der Chat Assistent von Laxout. Wie heißen Sie mit vor und Nachnamen?",
#                     bot_message=True,
#                 )
#                 anamnese_chat.messages.add(message_object)
#                 return JsonResponse(
#                     {
#                         "answer_chat_assistant": "Super! Dann lassen Sie uns doch mit einer kurzen Vorstellung beginnen. Mein Name ist Laxo und ich bin der Chat Assistent von Laxout. Wie heißen Sie mit vor und Nachnamen?",
#                         "index": index,
#                     }
#                 )
#             else:
#                 message_object = models.AnamneseMessage.objects.create(
#                     message="Bitte antworten Sie bei dieser Frage mit 'Ja', ansonsten kann die Patientenbefragung nicht durchgeführt werden. Haben Sie Fragen dann können Sie diese im Assistant Chat stellen. Akzeptieren Sie die AGB und Datenschutzbestimmungen?",
#                     bot_message=True,
#                 )
#                 anamnese_chat.messages.add(message_object)
#                 return JsonResponse(
#                     {
#                         "answer_chat_assistant": "Bitte antworten Sie bei dieser Frage mit 'Ja', ansonsten kann die Patientenbefragung nicht durchgeführt werden. Haben Sie Fragen dann können Sie diese im Assistant Chat stellen. Akzeptieren Sie die AGB und Datenschutzbestimmungen?",
#                         "index": index,
#                     }
#                 )
#         else:
#             content = api_call_anamnese_chat(
#                 user_input, anamnese_chat, questions, index
#             )
#             try:
#                 json_data = json.loads(content)
#                 user_asked_question = json_data.get("user_asked_question", False)
#                 answer_on_users_question = json_data.get(
#                     "answer_on_users_question",
#                     "Bitte kontaktieren Sie hierfür Ihren Therapeuten.",
#                 )
#                 print(content)
#             except:
#                 print("Error in ApI call")
#                 content = api_call_anamnese_chat(
#                     user_input, anamnese_chat, questions, index
#                 )
#                 try:
#                     json_data = json.loads(content)
#                     user_asked_question = json_data.get("user_asked_question", False)
#                     answer_on_users_question = json_data.get(
#                         "answer_on_users_question",
#                         "Bitte kontaktieren Sie hierfür Ihren Therapeuten.",
#                     )
#                     print(content)
#                 except:
#                     print("Error in ApI call2")
#                     content = api_call_anamnese_chat(
#                         user_input, anamnese_chat, questions, index
#                     )
#                     try:
#                         json_data = json.loads(content)
#                         user_asked_question = json_data.get(
#                             "user_asked_question", False
#                         )
#                         answer_on_users_question = json_data.get(
#                             "answer_on_users_question",
#                             "Bitte kontaktieren Sie hierfür Ihren Therapeuten.",
#                         )
#                         print(content)
#                     except:
#                         print("Error in ApI call2")
#                         user_asked_question = False
#                         answer_on_users_question = ""

#             if user_asked_question == False:
#                 index += 1
#                 answer_chat_assistant = ""
#             else:
#                 answer_chat_assistant = answer_on_users_question

#             if answer_chat_assistant == "":
#                 if index < len(questions):
#                     answer_chat_assistant = questions[index]
#                 else:
#                     answer_chat_assistant = "Sehr gut! Vielen Dank für Ihre Zeit. Ihre Eingaben werden nun von der LaxAi ausgewertet und ein Trainingsplan wird generiert. Haben Sie bitte kurz Geduld..."

#             return JsonResponse(
#                 {"index": index, "answer_chat_assistant": answer_chat_assistant}
#             )

#     return render(
#         request,
#         "laxout_app/anamnese_chat.html",
#         {"uid": uid, "anamnese_messages": anamnese_chat.messages.all(), "index": index},
#     )
