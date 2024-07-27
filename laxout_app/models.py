from django.db import models
from django.contrib.auth.models import User
import random, string
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from datetime import datetime
from django.utils import timezone
from uuid import uuid4


def random_string(length=70):
    allowed_characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(allowed_characters) for _ in range(length))
    return random_string


def generate_rabatt_code():
    allowed_characters = string.ascii_letters + string.digits
    random_string = ""
    for _ in range(10):
        random_string += random.choice(allowed_characters)


class DoneWorkouts(models.Model):
    workout_id = models.IntegerField(default=0)
    laxout_user_id = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())


class DoneExercises(models.Model):
    exercise_id = models.IntegerField(default=0)
    laxout_user_id = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.datetime.today())


class SkippedExercises(models.Model):
    skipped_exercise_id = models.IntegerField(default=0)
    laxout_user_id = models.IntegerField(default=0)


class IndexesLaxoutUser(models.Model):
    index = models.IntegerField(default=0)
    creation_date = models.IntegerField(default=datetime.now().month)
    created_by = models.IntegerField(default=None, blank=True)


class IndexesPhysios(models.Model):
    indexs = models.IntegerField(default=0)
    logins = models.IntegerField(default=0)
    tests = models.IntegerField(default=0)
    for_month = models.IntegerField(default=datetime.now().month)
    for_year = models.IntegerField(default=datetime.now().year)
    for_week = models.IntegerField(default=datetime.now().isocalendar()[1])
    created_by = models.IntegerField(default=None, blank=True)
    zero_two = models.IntegerField(default=0)
    theree_five = models.IntegerField(default=0)
    six_eight = models.IntegerField(default=0)
    nine_ten = models.IntegerField(default=0)


class LaxoutUserPains(models.Model):
    def __str__(self):
        return f"{self.created_by}'s Pains"

    for_month = models.IntegerField(default=datetime.now().month)
    created_by = models.IntegerField(default=None, blank=True)
    for_year = models.IntegerField(default=datetime.now().year)
    zero_two = models.IntegerField(default=0)
    theree_five = models.IntegerField(default=0)
    six_eight = models.IntegerField(default=0)
    nine_ten = models.IntegerField(default=0)
    for_week = models.IntegerField(default=datetime.now().isocalendar()[1])
    admin_id = models.IntegerField(default=0, blank=True)


class Coupon(models.Model):
    coupon_name = models.CharField(default="", max_length=200)
    coupon_text = models.CharField(default="", max_length=400)
    coupon_image_url = models.CharField(default="", max_length=200)
    coupon_price = models.IntegerField(default=0)
    coupon_offer = models.CharField(default="", max_length=100)
    rabbat_code = models.CharField(default="", max_length=250)


class First(models.Model):
    first = models.IntegerField(default=0)


class Second(models.Model):
    second = models.IntegerField(default=0)


class Laxout_Exercise(models.Model):
    execution = models.CharField(max_length=10000, default="")
    name = models.CharField(max_length=40, default="")
    dauer = models.IntegerField(default=30)
    videoPath = models.CharField(max_length=100, default="")
    looping = models.BooleanField(default=False)
    added = models.BooleanField(default=False)
    instruction = models.CharField(max_length=200, default="")
    timer = models.BooleanField(default=False)
    required = models.CharField(max_length=50, default="")
    imagePath = models.CharField(max_length=50, default="")
    appId = models.IntegerField(default=0)
    onlineVideoPath = models.CharField(default="", max_length=220)


class Laxout_Exercise_Order_For_User(models.Model):
    laxout_user_id = models.IntegerField(default=0)
    laxout_exercise_id = models.IntegerField(default=0)
    order = models.IntegerField(default=0)



class LaxoutUser(models.Model):
    user_uid = models.CharField(max_length=420, default="")
    laxout_user_name = models.CharField(max_length=200, default="")
    laxout_credits = models.IntegerField(default=0)
    note = models.CharField(max_length=200, default="")
    creation_date = models.DateField(default=timezone.now())
    exercises = models.ManyToManyField(Laxout_Exercise)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    indexes = models.ManyToManyField(IndexesLaxoutUser)
    last_login = models.DateTimeField(default=timezone.datetime(2023, 11, 14))
    last_login_2 = models.DateTimeField(default=timezone.datetime(2023, 11, 14))
    coupons = models.ManyToManyField(Coupon)
    last_meet = models.DateField(default=timezone.datetime.today())
    instruction = models.CharField(default="", max_length=200)
    lax_tree_id = models.IntegerField(default=0)
    water_drops_count = models.IntegerField(default=0)
    instruction_in_int = models.IntegerField(default=0)
    email_adress = models.CharField(default="", max_length=40)
    admin_has_seen_chat = models.BooleanField(default=True)
    user_has_seen_chat = models.BooleanField(default=False)
    was_created_through_app = models.BooleanField(default=False)
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indexes = models.ManyToManyField(IndexesPhysios)


class PhysioIndexCreationLog(models.Model):
    for_month = models.IntegerField(default=datetime.now().month)
    for_year = models.IntegerField(default=datetime.now().year)
    created_by = models.IntegerField(default=None, blank=True)
    for_week = models.IntegerField(default=datetime.now().isocalendar()[1])


class LaxoutUserIndexCreationLog(models.Model):
    for_month = models.IntegerField(default=datetime.now().month)
    for_year = models.IntegerField(default=datetime.now().year)
    created_by = models.IntegerField(default=None, blank=True)
    for_week = models.IntegerField(default=datetime.now().isocalendar()[1])
    related_user_pain = models.IntegerField(default=0)


class Uebungen_Models(models.Model):
    execution = models.CharField(max_length=10000, default="")
    name = models.CharField(max_length=40, default="")
    dauer = models.IntegerField(default=30)
    videoPath = models.CharField(max_length=100, default="")
    looping = models.BooleanField(default=False)
    added = models.BooleanField(default=False)
    instruction = models.CharField(max_length=200, default="")
    timer = models.BooleanField(default=False)
    required = models.CharField(max_length=50, default="")
    imagePath = models.CharField(max_length=50, default="")
    appId = models.IntegerField(default=0)
    onlineVideoPath = models.CharField(default="", max_length=220)
    first = models.ManyToManyField(First)
    second = models.ManyToManyField(Second)


class LaxTree(models.Model):
    condition = models.IntegerField(default=0)


class SuccessControll(models.Model):
    better = models.BooleanField(default=False)
    created_by = models.IntegerField(default=0)


class AiTrainingDataGlobal(models.Model):
    def __str__(self):
        return f"{self.illness}"

    illness = models.CharField(default="", max_length=200)
    related_exercises = models.ManyToManyField(Laxout_Exercise)
    created_by = models.IntegerField(default=0)  # Physio Id


class ChatDataModel(models.Model):
    is_sender = models.BooleanField(default=False)
    message = models.CharField(max_length=2003000000, default="")
    created_by = models.IntegerField(default=0)
    admin_id = models.IntegerField(default=0)


class BillingCount(models.Model):
    billing_count = models.IntegerField(default=1)


class SovendusCustomerUid(models.Model):
    uid = models.CharField(default="", max_length=200)


class WebCodes(models.Model):
    created_by = models.IntegerField(default=0)
    code = models.CharField(default="", max_length=20)


##Old
class AiExercise(models.Model):
    exercise_id = models.IntegerField(default=0)


class AiTrainingData(models.Model):
    def __str__(self):
        return f"{self.illness}"

    illness = models.CharField(default="", max_length=200)
    related_exercises = models.ManyToManyField(AiExercise)
    created_by = models.IntegerField(default=0)  # Physio Id
    created_for = models.IntegerField(default=0)  # LaxoutUserId


# Befunde


class FragenevaluationNachICFKategorien(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    aktueller_gesundheitszustand = models.CharField(default="", max_length=2000)
    struktur_funktion = models.CharField(default="", max_length=2000)
    aktivitaet = models.CharField(default="", max_length=2000)
    partizipation = models.CharField(default="", max_length=2000)
    kontextfaktoren = models.CharField(default="", max_length=2000)


class FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    koerperliche_beschwerden = models.CharField(default="", max_length=2000)
    psychisch_gelagerte_eschwerden = models.CharField(default="", max_length=2000)
    probleme_mit_aktiver_teilhabe_am_sozialen_Leben = models.CharField(
        default="", max_length=2000
    )


class FragenevaluationenNachDen7WFragen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    hauptbeschwerden = models.CharField(
        default="", max_length=2000
    )  # Weshalb kommen Sie zur Therapie?
    lokalisierung = models.CharField(
        default="", max_length=2000
    )  # Wo sind die Beschwerden?
    provokation = models.CharField(
        default="", max_length=2000
    )  # Wann treten die Beschwerden auf ?
    orientierung_für_Maßnahmen = models.CharField(
        default="", max_length=2000
    )  # Wodurch werden die Beschwerden besser ?
    schmerzqualität = models.CharField(
        default="", max_length=2000
    )  # Wie fühlen sich die Schmerzen an ?
    orientierung = models.CharField(
        default="", max_length=2000
    )  # Was wurde bisher an Therapien durchgeführt?
    beschwerdeverlauf = models.CharField(
        default="", max_length=2000
    )  # Seit wann haben Sie die Beschwerden und was verschlimmert sie ?


class StandDerReHaPhase(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    akute_phase = models.BooleanField(default=False)
    wundheilungsphase = models.BooleanField(default=False)
    frueh_phase_ReHa = models.BooleanField(default=False)
    mittlere_phase_Reha = models.BooleanField(default=False)
    spaet_phase_reha = models.BooleanField(default=False)


class NebenerkrankungenMedikamente(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    erbkrankheiten = models.BooleanField(default=False)
    erbkrankheiten_krankheit = models.CharField(default="", max_length=1000)
    erbkrankheiten_medikamente = models.CharField(default="", max_length=1000)
    metabolische_erkrankungen = models.BooleanField(default=False)
    metabolische_erkrankungen_krankheit = models.CharField(default="", max_length=1000)
    metabolische_erkrankungen_medikamente = models.CharField(default="", max_length=1000)
    psychische_erkrankungen = models.BooleanField(default=False)
    psychische_erkrankungen_krankheit = models.CharField(default="", max_length=1000)
    psychische_erkrankungen_medikamente = models.CharField(default="", max_length=1000)
    herz_kreislauferkrankungen = models.BooleanField(default=False)
    herz_kreislauferkrankungen_krankheit = models.CharField(default="", max_length=1000)
    herz_kreislauferkrankungen_medikamente = models.CharField(default="", max_length=1000)
    neurologische_erkrankungen = models.BooleanField(default=False)
    neurologische_erkrankungen_krankheit = models.CharField(default="", max_length=1000)
    neurologische_erkrankungen_medikamente = models.CharField(default="", max_length=1000)
    rheumatisch_entzuendliche_erkrankungen = models.BooleanField(default=False)
    rheumatisch_entzuendliche_erkrankungen_krankheit = models.CharField(default="", max_length=1000)
    rheumatisch_entzuendliche_erkrankungen_medikamente = models.CharField(default="", max_length=1000)
    erkrankungen_bewegungsapparat = models.BooleanField(default=False)
    erkrankungen_bewegungsapparat_erkrankungen_krankheit = models.CharField(default="", max_length=1000)
    erkrankungen_bewegungsapparat_erkrankungen_medikamente = models.CharField(default="", max_length=1000)


class HistoriaMorbis(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    trauma_unfall = models.BooleanField(default=False)
    atraumatisch = models.BooleanField(default=False)
    chronisch = models.BooleanField(default=False)
    progredient = models.BooleanField(default=False)
    krankheitsverlauf = models.CharField(default="", max_length=2000)
    Krankenhausaufenthalte = models.CharField(default="", max_length=2000)
    unfaelle_verletzungen_operationen = models.CharField(default="", max_length=2000)
    schwangerschaften = models.CharField(default="", max_length=2000)
    sucht_drogenverhalten = models.CharField(default="", max_length=2000)


class StandartBefund(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    name = models.CharField(default="", max_length=50)
    vorname = models.CharField(default="", max_length=50)
    alter = models.IntegerField(default=0)
    diagnose = models.CharField(default="", max_length=1000)
    hauptziel = models.CharField(default="", max_length=2000)
    vollbelastung = models.BooleanField(default=False)
    teilbeslastung = models.BooleanField(default=False)
    lagerungstabil = models.BooleanField(default=False)
    maximalpuls = models.BooleanField(default=False)
    therapeutische_ziele_maßnahmen = models.CharField(default="", max_length=2000)
    op_vorliegend = models.BooleanField(default=False)
    medikament_einnahme = models.BooleanField(default=False)
    geschlecht = models.CharField(default="", max_length=100)
    groeße = models.IntegerField(default=0)
    gewicht = models.IntegerField(default=0)
    konstitutionstyp = models.CharField(default="", max_length=1000)
    beruf = models.CharField(default="", max_length=500)
    alltagsaktivitaeten= models.CharField(default="", max_length=500)


class NrsNumericRatingScale(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    kein_schmerz  = models.BooleanField(default=False)
    sanft = models.BooleanField(default=False)
    gering = models.BooleanField(default=False)
    unbequem = models.BooleanField(default=False)
    mittelgradig = models.BooleanField(default=False)
    ablenkend  = models.BooleanField(default=False)
    quaelend = models.BooleanField(default=False)
    starker_schmerz = models.BooleanField(default=False)
    hochgradiger_schmerz  = models.BooleanField(default=False)
    unertraeglich = models.BooleanField(default=False)
    unbeschreiblich  = models.BooleanField(default=False)


class AktiveBeweglichkeit(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    # Flexion Rechts
    flexion_rechts_oB = models.BooleanField(default=False)
    flexion_rechts_leicht_begrenzt = models.BooleanField(default=False)
    flexion_rechts_mittelgradig_begrenzt = models.BooleanField(default=False)
    flexion_rechts_stark_begrenzt = models.BooleanField(default=False)
    flexion_rechts_schmerzhaft = models.BooleanField(default=False)
    flexion_rechts_gehemmt = models.BooleanField(default=False)
    flexion_rechts_verzögert = models.BooleanField(default=False)
    flexion_rechts_eingeschränkt = models.BooleanField(default=False)
    flexion_rechts_unkoordiniert = models.BooleanField(default=False)

    # Flexion Links
    flexion_links_oB = models.BooleanField(default=False)
    flexion_links_leicht_begrenzt = models.BooleanField(default=False)
    flexion_links_mittelgradig_begrenzt = models.BooleanField(default=False)
    flexion_links_stark_begrenzt = models.BooleanField(default=False)
    flexion_links_schmerzhaft = models.BooleanField(default=False)
    flexion_links_gehemmt = models.BooleanField(default=False)
    flexion_links_verzögert = models.BooleanField(default=False)
    flexion_links_eingeschränkt = models.BooleanField(default=False)
    flexion_links_unkoordiniert = models.BooleanField(default=False)

    # Extension Rechts
    extension_rechts_oB = models.BooleanField(default=False)
    extension_rechts_leicht_begrenzt = models.BooleanField(default=False)
    extension_rechts_mittelgradig_begrenzt = models.BooleanField(default=False)
    extension_rechts_stark_begrenzt = models.BooleanField(default=False)
    extension_rechts_schmerzhaft = models.BooleanField(default=False)
    extension_rechts_gehemmt = models.BooleanField(default=False)
    extension_rechts_verzögert = models.BooleanField(default=False)
    extension_rechts_eingeschränkt = models.BooleanField(default=False)
    extension_rechts_unkoordiniert = models.BooleanField(default=False)

    # Extension Links
    extension_links_oB = models.BooleanField(default=False)
    extension_links_leicht_begrenzt = models.BooleanField(default=False)
    extension_links_mittelgradig_begrenzt = models.BooleanField(default=False)
    extension_links_stark_begrenzt = models.BooleanField(default=False)
    extension_links_schmerzhaft = models.BooleanField(default=False)
    extension_links_gehemmt = models.BooleanField(default=False)
    extension_links_verzögert = models.BooleanField(default=False)
    extension_links_eingeschränkt = models.BooleanField(default=False)
    extension_links_unkoordiniert = models.BooleanField(default=False)


class PassiveBeweglichkeit(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    # Flexion Rechts
    flexion_rechts_oB = models.BooleanField(default=False)
    flexion_rechts_leicht_begrenzt = models.BooleanField(default=False)
    flexion_rechts_mittelgradig_begrenzt = models.BooleanField(default=False)
    flexion_rechts_stark_begrenzt = models.BooleanField(default=False)
    
    # Flexion Rechts - Physiologisches Endgefühl
    flexion_rechts_fest_elastischer_stopp = models.BooleanField(default=False)
    flexion_rechts_weich_elastischer_stopp = models.BooleanField(default=False)
    
    # Flexion Rechts - Pathologische Endgefühle
    flexion_rechts_hart_unelastischer_stopp = models.BooleanField(default=False)
    flexion_rechts_fester_unelastischer_stopp = models.BooleanField(default=False)
    flexion_rechts_fester_elastischer_stopp = models.BooleanField(default=False)
    flexion_rechts_leeres_endgefuehl = models.BooleanField(default=False)
    flexion_rechts_schmerz = models.BooleanField(default=False)

    # Flexion Links
    flexion_links_oB= models.BooleanField(default=False)
    flexion_links_leicht_begrenzt = models.BooleanField(default=False)
    flexion_links_mittelgradig_begrenzt = models.BooleanField(default=False)
    flexion_links_stark_begrenzt = models.BooleanField(default=False)
    
    # Flexion Links - Physiologisches Endgefühl
    flexion_links_fest_elastischer_stopp = models.BooleanField(default=False)
    flexion_links_weich_elastischer_stopp = models.BooleanField(default=False)
    
    # Flexion Links - Pathologische Endgefühle
    flexion_links_hart_unelastischer_stopp = models.BooleanField(default=False)
    flexion_links_fester_unelastischer_stopp = models.BooleanField(default=False)
    flexion_links_fester_elastischer_stopp = models.BooleanField(default=False)
    flexion_links_leeres_endgefuehl = models.BooleanField(default=False)
    flexion_links_schmerz = models.BooleanField(default=False)

    # Extension Rechts
    extension_rechts_oB = models.BooleanField(default=False)
    extension_rechts_leicht_begrenzt = models.BooleanField(default=False)
    extension_rechts_mittelgradig_begrenztb = models.BooleanField(default=False)
    extension_rechts_stark_begrenzt = models.BooleanField(default=False)
    
    # Extension Rechts - Physiologisches Endgefühl
    extension_rechts_fest_elastischer_stopp = models.BooleanField(default=False)
    extension_rechts_weich_elastischer_stopp = models.BooleanField(default=False)
    
    # Extension Rechts - Pathologische Endgefühle
    extension_rechts_hart_unelastischer_stopp = models.BooleanField(default=False)
    extension_rechts_fester_unelastischer_stopp = models.BooleanField(default=False)
    extension_rechts_fester_elastischer_stopp = models.BooleanField(default=False)
    extension_rechts_leeres_endgefuehl = models.BooleanField(default=False)
    extension_rechts_schmerz = models.BooleanField(default=False)

    # Extension Links
    extension_links_oB = models.BooleanField(default=False)
    extension_links_leicht_begrenzt = models.BooleanField(default=False)
    extension_links_mittelgradig_begrenzt = models.BooleanField(default=False)
    extension_links_stark_begrenzt = models.BooleanField(default=False)
    
    # Extension Links - Physiologisches Endgefühl
    extension_links_fest_elastischer_stopp = models.BooleanField(default=False)
    extension_links_weich_elastischer_stopp = models.BooleanField(default=False)
    
    # Extension Links - Pathologische Endgefühle
    extension_links_hart_unelastischer_stopp = models.BooleanField(default=False)
    extension_links_fester_unelastischer_stopp = models.BooleanField(default=False)
    extension_links_fester_elastischer_stopp = models.BooleanField(default=False)
    extension_links_leeres_endgefuehl = models.BooleanField(default=False)
    extension_links_schmerz = models.BooleanField(default=False)


class BeweglichkeitsmessungKnie(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    extension_flexion_rechts_value = models.CharField(default="", max_length=100)
    extension_flexion_links_value = models.CharField(default="", max_length=100)

class IsometrischerKrafttest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    flexion_oB = models.BooleanField(default=False)
    flexion_kann_nicht_gehalten_werden = models.BooleanField(default=False)
    extension_oB = models.BooleanField(default=False)
    extension_kann_nicht_gehalten_werden = models.BooleanField(default=False)

class Muskelfunktionspruefung(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    # Flexion
    flexion_1 = models.BooleanField(default=False)
    flexion_2 = models.BooleanField(default=False)
    flexion_3 = models.BooleanField(default=False)
    flexion_4 = models.BooleanField(default=False)
    flexion_5 = models.BooleanField(default=False)

    # Extension
    extension_1 = models.BooleanField(default=False)
    extension_2 = models.BooleanField(default=False)
    extension_3 = models.BooleanField(default=False)
    extension_4 = models.BooleanField(default=False)
    extension_5 = models.BooleanField(default=False)


class Einbeinstand60Sekunden(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    oB = models.BooleanField(default=False)  # ohne Befund
    kann_nicht_gehalten_werden = models.BooleanField(default=False)


class Einbeinstand30SekundenGeschlosseneAugen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    oB = models.BooleanField(default=False)  # ohne Befund
    kann_nicht_gehalten_werden = models.BooleanField(default=False)

class Alltagsfunktionen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    # Tiefe Hocke
    tiefe_hocke_ob = models.BooleanField(default=False)  # ohne Befund
    tiefe_hocke_auffaellig = models.BooleanField(default=False)
    tiefe_hocke_bemerkung = models.CharField(max_length=755, default="")

    # Hüpfen auf einem Bein
    huepfen_einem_bein_ob = models.BooleanField(default=False)  # ohne Befund
    huepfen_einem_bein_auffaellig = models.BooleanField(default=False)
    huepfen_einem_bein_bemerkung = models.CharField(max_length=755, default="")

    # Ferstand
    ferstand_ob = models.BooleanField(default=False)  # ohne Befund
    ferstand_auffaellig = models.BooleanField(default=False)
    ferstand_bemerkung = models.CharField(max_length=755, default="")

    # Fersenfall
    fersenfall_ob = models.BooleanField(default=False)  # ohne Befund
    fersenfall_auffaellig = models.BooleanField(default=False)
    fersenfall_bemerkung = models.CharField(max_length=755, default="")

    # Einbeinstand
    einbeinstand_ob = models.BooleanField(default=False)  # ohne Befund
    einbeinstand_auffaellig = models.BooleanField(default=False)
    einbeinstand_bemerkung = models.CharField(max_length=755, default="")

    # Treppe
    treppe_ob = models.BooleanField(default=False)  # ohne Befund
    treppe_auffaellig = models.BooleanField(default=False)
    treppe_bemerkung = models.CharField(max_length=755, default="")


class Beinlaengenmessung(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    # Anatomische Messung
    anatomische_messung_rechts = models.IntegerField(default=0)
    anatomische_messung_links = models.IntegerField(default=0)

    # Funktionelle Messung
    funktionelle_messung_rechts = models.IntegerField(default=0)
    funktionelle_messung_links = models.IntegerField(default=0)

class QuadricepsDehnungstest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class MRectusDehnungstest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class Hamstringtest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class Umfangsmessung(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    messort_10cm_oberhalb_kniegelenkspalt_rechts = models.IntegerField(default=0)
    messort_10cm_oberhalb_kniegelenkspalt_links = models.IntegerField(default=0)
    messort_am_kniegelenkspalt_rechts = models.IntegerField(default=0)
    messort_am_kniegelenkspalt_links = models.IntegerField(default=0)
    messort_10cm_unterhalb_kniegelenkspalt_rechts = models.IntegerField(default=0)
    messort_10cm_unterhalb_kniegelenkspalt_links = models.IntegerField(default=0)
    messort_15cm_unterhalb_kniegelenkspalt_rechts = models.IntegerField(default=0)
    messort_15cm_unterhalb_kniegelenkspalt_links = models.IntegerField(default=0)

class TanzendePatella(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class MiniErgussTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class GlideTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")


class TiltTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class AprehensionTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class ZohlenZeichen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class Facettendruckschmerztest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class ValgusTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class VarusTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class LachmannTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class VordereSchublade(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class PivotShiftTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class HintereSchublade(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class GravitiySign(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class LoomersTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class Steinmann1(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class Steinmann3(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class TheslayTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class MacMurrayTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class PayrZeichen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class ApleyZeichen(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class MedioPatellarerPlicaTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")

class HughstonPlicaTest(models.Model):
    created_for = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.datetime.today())
    ohne_befund = models.BooleanField(default=False)
    positiv_auffaellig = models.BooleanField(default=False)
    nicht_durchfuehrbar = models.BooleanField(default=False)
    bemerkung = models.CharField(max_length=755, default="")
    

class Befund(models.Model):
    befund = models.CharField(default="", max_length=200)
    created_for = models.IntegerField(default=0)