import openai
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.conf import settings
from openai import OpenAI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
