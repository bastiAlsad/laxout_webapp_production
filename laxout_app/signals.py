# in signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Uebungen_Models
from . import models


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


# Liste von Übungen
uebungen = [
    UebungList(
        looping=True,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den linken Fuß wie gezeigt auf den rechten Oberschenkel. Versuchen Sie Ihr linkes Knie soweit wie möglich nach unten zu drücken.",
        name="Schulterblattkreisen",
        videoPath="assets/videos/schuterblattkreisen.mp4",
        dauer=30,
        imagePath="assets/images/schulterblattkreisen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath= "https://youtu.be/jFGkSAmt3jI",
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Wichtig ist dass du aufrecht an der Stuhlkante sitzt und deine Schultern hängen lässt. Führe die Übung bitte langsam aus.",
        name="Halbkreise Links",
        videoPath="assets/videos/Halbkreisnackenlinks.mp4",
        dauer=30,
        imagePath="assets/images/halbkreiseLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/44v3LKOQkVs"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Wichtig ist dass du aufrecht an der Stuhlkante sitzt und deine Schultern hängen lässt. Führe die Übung bitte langsam aus.",
        name="Halbkreise Rechts",
        videoPath="assets/videos/HalbkreisNackenrechts.mp4",
        dauer=30,
        imagePath="assets/images/halbkreiseRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/VtZs7yu_dyI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehe langsam in die Dehnung, halte sie und bewege deine Schultern nicht. Außerdem ist es gut, wenn du aufrecht sitzt. Bist du fertig mit der Übung, verlasse die Dehnung nicht zu schnell.",
        name="Dehnung Links Hinten",
        videoPath="assets/videos/nackenLinksHinten.mp4",
        dauer=30,
        imagePath="assets/images/nackenLinksHinten.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/gWu3B5UqHjU",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehe langsam in die Dehnung, halte sie und bewege deine Schultern nicht. Außerdem ist es gut, wenn du aufrecht sitzt. Bist du fertig mit der Übung, verlasse die Dehnung nicht zu schnell.",
        name="Dehnung Rechts Hinten",
        videoPath="assets/videos/nackenRechtsHinten.mp4",
        dauer=30,
        imagePath="assets/images/nackenRechtsHinten.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/x752jP5KfyU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege deine Hände im geschätzen 45 Grad Winkel wie gezeigt an die Wand. Dannach machst du einen Ausfallschritt und verlagerst dein Gewicht langsam nach vorne.",
        name="Schulterdehnung 45 Grad",
        videoPath="assets/videos/schulterdehnung.mp4",
        dauer=30,
        imagePath="assets/images/schulterdehnug45.png",
        added=False,
        instruction="",
        required="Wandecke",
        onlineVidePath="https://youtu.be/0xQiN5FbLEY",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege deine Hände so hoch wie möglich an die Wand, wie als ob dich jemand nach oben zieht. Dannach machst du einen Ausfallschritt und verlagerst dein Gewicht langsam nach vorne.",
        name="Schulterdehnung 90 Grad",
        videoPath="assets/videos/schulterdehnungGerade.mp4",
        dauer=30,
        imagePath="assets/images/schulterdehnung90.png",
        added=False,
        instruction="",
        required="Wand/Tür",
        onlineVidePath="https://youtu.be/N9lxp4sA5EM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lasse deinen Nacken locker, wärend deine Hände sich auf Arschhöhre verschränken. Deine Schultern gehen nun hinten zusammen, während die Hände nach unten gezogen werden.",
        name="Aufrichten",
        videoPath="assets/videos/aufrichtenoberkoerper.mp4",
        dauer=30,
        imagePath="assets/images/aufrichten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/zqBmTOsSaO8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Deine Hände sind auf Brusthöhe, während du dich nach vorne neigst, als ob jemand an deinen Unterarmen zieht. Stell dir vor du willst etwas vor dir umarmen.",
        name="Bagger",
        videoPath="assets/videos/bagger.mp4",
        dauer=30,
        imagePath="assets/images/bagger.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/CgCJbMCpuU4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setze dich aufrecht an die Stuhlkante und beginne mit dem Becken zu kreisen. Der Oberkörper muss möglichst ruhig bleiben.",
        name="Bewegung Unterer Rücken",
        videoPath="assets/videos/beckenschaukel.mp4",
        dauer=30,
        imagePath="assets/images/bewegungUntererRuecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/oIpWIe1oeMU"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Du schaust gerade nach oben zur Decke. Lege deine Beine langsam und abwechselnd links und rechts zur Seite ab. Dabei bewegt sich dein Oberkörper nicht.",
        name="Plumpsen",
        videoPath="assets/videos/Plumpsenrechtslinks.mp4",
        dauer=30,
        imagePath="assets/images/plumpsen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/NxWtZWNRwx0"
    ),

    UebungList(# kein Video
        looping=False,
        timer=True,
        execution="Du schaust gerade nach oben zur Decke. Dannach legst du deine Beine langsam zur Seite ab und hältst die Dehnung. Dabei bewegt sich dein Oberkörper nicht.",
        name="Dehnung Unterer Rücken rechts",
        videoPath="assets/videos/untererRueckenrechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnunUnterRueckenR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Imm4kNNWtr8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Du schaust gerade nach oben zur Decke. Dannach legst du deine Beine langsam zur Seite ab und hältst die Dehnung. Dabei bewegt sich dein Oberkörper nicht",
        name="Dehnung Unterer Rücken links",
        videoPath="assets/videos/untererRueckenlinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungUntererRueckenL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/N3jNoQSuoos"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setze dich so an die Stuhlkante, dass deine Knie auseinander sind und du aufrecht sitzt. Bei der Drehnung darf sich dein Becken und dein Kopf nicht bewegen. Tipp nehme hierfür deine Hände, wie gezeigt vor die Brust.",
        name="Rotation Oberkörper",
        videoPath="assets/videos/rotationMittlererR.mp4",
        dauer=30,
        imagePath="assets/images/RotationOberkoerper.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/bM5QIh9G2hc"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setze dich so an die Stuhlkante, dass deine Knie auseinander sind und du aufrecht sitzt. Neige dich nun mit ausgestrecktem Arm zur Seite und versuche tief zu atmen. Schau dabei auf den Boden, der gerade vor dir ist.",
        name="Seitliche Dehnung links",
        videoPath="assets/videos/seitlicheDehnunglins.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungLS.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/IZ0yEvc5SoU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setze dich so an die Stuhlkante, dass deine Knie auseinander sind und du aufrecht sitzt. Neige dich nun mit ausgestrecktem Arm zur Seite und versuche tief zu atmen. Schau dabei auf den Boden, der gerade vor dir ist.",
        name="Seitliche Dehnung rechts",
        videoPath="assets/videos/seitlicheDehnungm.rechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungRS.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/LdaT-uqtkuA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege dir für diese Übung am besten ein Kissen wie gezeigt unter. Dannach geht der ausgestreckte Arm zur anderen Seite, während du ihm nachschaust und dein Kopf sich mit ihm mitbewegt.",
        name="Brustwirbelsäule links",
        videoPath="assets/videos/brustwirbelsauleLinks.mp4",
        dauer=30,
        imagePath="assets/images/BrustwirbelsauleL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/v4GZpH6C0uI"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege dir für diese Übung am besten ein Kissen wie gezeigt unter. Dannach geht der ausgestreckte Arm zur anderen Seite, während du ihm nachschaust und dein Kopf sich mit ihm mitbewegt.",
        name="Brustwirbelsäule rechts",
        videoPath="assets/videos/brustwirbelsauleRechts.mp4",
        dauer=30,
        imagePath="assets/images/BrustwirbelsauleR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/NKQts1Ebsfw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht auf einen Stuhl. Legen Sie Ihre Hände an den Hinterkopf. Beugen Sie Ihren Nacken nach vorne und spüren Sie eine leichte Dehnung im Bereich der Halswirbelsäule.",
        name="Dehnung HWS hinten",
        videoPath="assets/videos/DehnungHwsHinten.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsHinten.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/ZVfJk2vkmJY"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie rechte Hand ans linke Schlüsselbein. Neigen Sie Ihren Kopf langsam nach rechts hinten und spüren Sie die Dehnung im Bereich der Halswirbelsäule. Achten Sie auf einen geraden Rücken.",
        name="Dehnung HWS links vorne",
        videoPath="assets/videos/DehnungHwsLinksVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsLinksVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/nVhWy_Zo44A"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie die linke Hand ans rechte Schlüsselbein. Neigen Sie Ihren Kopf langsam nach links hinten und spüren Sie die Dehnung im Bereich der Halswirbelsäule. Achten Sie auf einen geraden Rücken.",
        name="Dehnung HWS rechts vorne",
        videoPath="assets/videos/DehnungHwsRechtsVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsRechtsVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/KfnRkpDCNeM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie eine Hand auf die Stirn. Neigen Sie Ihren Kopf langsam und vorsichtig nach hinten, um eine Dehnung im Bereich der Halswirbelsäule zu spüren. Achten Sie auf einen geraden Rücken. Seien Sie vorsichtig, um Schwindel zu vermeiden, und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung HWS vorne",
        videoPath="assets/videos/DehnungHwsVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/eBDLpqOF5Go"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sitzen Sie aufrecht oder stehen Sie gerade. Neigen Sie den Kopf zur rechten Schulter, so weit wie es bequem ist, und halten Sie diese Position für 5 Sekunden. Gehen Sie zurück zur Ausgangsposition und wiederholen Sie die Übung auf der linken Seite. Führen Sie die Übung in der Geschwindigkeit wie vorgemacht aus und machen Sie die Übung 15 mal.",
        name="Nacken seitliche Neigungen",
        videoPath="assets/videos/NackenSeitlicheNeigungen.mp4",
        dauer=15,
        imagePath="assets/images/NackenSeitlicheNeigungen.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/7mz1mrMjQrw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Drücken Sie Ihre Handfläche gegen die Stirn und halten Sie den Kopf dabei stabil. Halten Sie den Widerstand für 5-10 Sekunden. Wiederholen Sie dies, indem Sie die Handflächen gegen die Seiten des Kopfes und den Hinterkopf drücken.",
        name="Nacken Kräftigung Drücken",
        videoPath="assets/videos/NackenDruecken.mp4",
        dauer=15,
        imagePath="assets/images/NackenKraeftigungDruecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/IhsZRVPnG_E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie 2 Wasserflaschen in die Hände. Sitzen Sie aufrecht. Ziehen Sie Ihre Schultern in 2-3 Sekunden ca. 30-mal hoch und lassen Sie sie langsam absenken.",
        name="Schultern Hochziehen",
        videoPath="assets/videos/SchulternHochziehen.mp4",
        dauer=30,
        imagePath="assets/images/SchulternHochziehen.png",
        added=False,
        instruction="",
        required="2 Wasserflaschen",
        onlineVidePath="https://youtu.be/zWFyKhItfow"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Hinsetzen und nach vorne lehnen. Der Oberkörper bildet einen Winkel von ca. 45 Grad zu den Beinen. Heben Sie Ihre Arme beidseitig wie ein Vogel gerade nach oben. Führen Sie die Übung langsam aus. Optional: Verwenden Sie Gewichte.",
        name="Kräftigung Rotatoren",
        videoPath="assets/videos/KraeftigungRotatoren.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungRotatoren.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/OOTxwlqru78"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie Ihre rechte Hand auf einen Tisch. Stellen Sie Ihren Fuß auf der Seite, wo die Hand ist, einen Schritt nach vorne. Halten Sie eine Gewicht/Wasserflasche in der anderen Hand. Lehnen Sie sich leicht nach vorne. Ziehen Sie den Arm mit dem Gewicht möglichst nah am Körper und möglichst gerade zur Decke hoch.",
        name="Trapez Muskulatur links",
        videoPath="assets/videos/TrapezMuskulaturL.mp4",
        dauer=20,
        imagePath="assets/images/TrapezMuskulaturL.png",
        added=False,
        instruction="",
        required="Gewicht/Wasserflasche",
        onlineVidePath="https://youtu.be/UncBhm17jNg"

    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie Ihre linke Hand auf einen Tisch. Stellen Sie Ihren Fuß auf der Seite, wo die Hand ist, einen Schritt nach vorne. Halten Sie eine Gewicht/Wasserflasche in der anderen Hand. Lehnen Sie sich leicht nach vorne. Ziehen Sie den Arm mit dem Gewicht möglichst nah am Körper und möglichst gerade zur Decke hoch.",
        name="Trapez Muskulatur rechts",
        videoPath="assets/videos/TrapezMuskulaturR.mp4",
        dauer=20,
        imagePath="assets/images/TrapezMuskulaturR.png",
        added=False,
        instruction="",
        required="Gewicht/Wasserflasche",
        onlineVidePath="https://youtu.be/P8HFabQdJ54"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Die linke Schulter beginnt nun Kreise nach hinten zu machen. Leicht versetzt davon macht auch die rechte Schulter Kreise indem sie erst nach Oben, dann nach Hinten, dann nach unten und dann wieder zurück geht.",
        name="Schulterkreisen größer werden",
        videoPath="assets/videos/SchGroesser.mp4",
        dauer=30,
        imagePath="assets/images/SchulterkreisenGroeßerWerden.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/_-mvpirfTMU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Eine Hand (z.B. die linke Hand) berührt die rechte Schulter, während die andere Hand (rechts) den Bauch etwas oberhalb der Hüfte umfasst. Die Arme sind also wie bei einer Umarmung. Anschließend wechselt die linke Hand zum Bauch, während die rechte Hand die Schulter berührt. Diese Übung kann auch im Sitzen durchgeführt werden.",
        name="Verschränken Mobilisation Schultergürtel",
        videoPath="assets/videos/VerschraenkenMobilisationSchulterguertel.mp4",
        dauer=60,
        imagePath="assets/images/VerschraenkenMobilisationSchulterguertel.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/sEN1lli6lUo"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Machen Sie ein leichtes Hohlkreuz, wobei Sie das Brustbein anheben. Die Arme gehen nach oben, und die Unterarme bilden einen 90-Grad-Winkel mit den Oberarmen. Die Ellbogen verlaufen parallel zum Körper, und die Handflächen zeigen in einer offenen Position nach vorne und in einer geschlossenen Position zum Kopf. Atmen Sie beim Auseinanderbewegen der Ellenbogen ein und beim Zusammenführen der Ellenbogen aus. Im Verlauf der Übung können Sie das Tempo leicht steigern.",
        name="Mobilisation Schultergürtel",
        videoPath="assets/videos/MobilisationSchulterguertel.mp4",
        dauer=60,
        imagePath="assets/images/MobilisationSchulterguertel.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/gngSnM56xdM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf den Boden. Ihre Arme gehen hinter den Rücken auf den Boden, als ob Sie sich abstützen würden. Halten Sie Ihre Füße leicht angewinkelt. Ihre Ellenbogen bleiben gerade, während Sie Ihre Hände langsam nach hinten tippeln, bis sie eine Dehnung spürem. Dann drücken sie die Hände gegen den Boden, bis sie eine leichte bis mittelstarke Dehnung spüren. Führen Sie die Übung etwa 60 Sekunden lang aus.",
        name="Dehnung im Halbliegen",
        videoPath="assets/videos/DehnungImHalbliegen.mp4",
        dauer=60,
        imagePath="assets/images/DehnungImHalbliegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/YKStW6oT8bQ"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Liegen Sie mit dem Bauch auf einer Matte. Ihr Kopf ist nach rechts, oder links gedreht, und Ihre Arme sind etwa 45 Grad vom Körper seitlich ausgestreckt. Ziehen Sie Ihre Schultern nach außen aus den Schultergelenken, indem Sie mit den Fingerspitzen nach außen tippeln. Führen Sie die Übung etwa 60 Sekunden lang aus.",
        name="Dehnung in Bauchlage",
        videoPath="assets/videos/DehnungInBauchlage.mp4",
        dauer=60,
        imagePath="assets/images/DehnungInBauchlage.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/cmi1bekkkuE"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Ihr Ziel ist es jetzt, dass sich die Hände hinter dem Rücken berühren: Ihre linke Hand kommt von unten, und die rechte Hand, die von oben kommt, versucht, die linke Handfläche, wenn möglich, hinter dem Rücken zu berühren. Dehnen Sie nicht zu stark.",
        name="Dehnung Rechte Schulter",
        videoPath="assets/videos/DehnungRechteSchulter.mp4",
        dauer=40,
        imagePath="assets/images/DehnungRechteSchulter.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/R0NmFKcFB1Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Ihr Ziel ist es jetzt, dass sich die Hände hinter dem Rücken berühren: Ihre rechte Hand kommt von unten, und die linke Hand, die von oben kommt, versucht, die linke Handfläche, wenn möglich, hinter dem Rücken zu berühren. Dehnen Sie nicht zu stark.",
        name="Dehnung Linke Schulter",
        videoPath="assets/videos/DehnungLinkeSchulter.mp4",
        dauer=40,
        imagePath="assets/images/DehnungLinkeSchulter.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/5cyxyTi_gss"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Machen Sie es dann wie eine Katze, lassen Sie ihren Oberkörper nach vorne absinken, bleiben sie mit den Knien und den Füßen am Boden und strecken sie ihre Hände soweit wie möglich nach vorne aus. Schieben sie ihren Oberkörper dann nach hinten um eine leichte Dehnung im Bereich der Schultern zu spüren.",
        name="Kinderstellung",
        videoPath="assets/videos/Kinderstellung.mp4",
        dauer=30,
        imagePath="assets/images/Kinderstellung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/4uMgVmPnl9E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie aufrecht, Ellenbogen sind am Rumpf des Körpers. Ober zu unter Arme sind im 90 Grad Winkel. Ellenbogen gehen nun seitlich nach oben bis sich eine Waagerechte zwischen linkem Oberarm, Schultern und rechtem Oberarm bildet. Wichtig: Nacken entspannen, langsam ausführen, leicht in die Kniee und Rücken Gerade lassen.",
        name="Schulterkräftigung im Stehen",
        videoPath="assets/videos/SchulterkraeftigungStehen.mp4",
        dauer=30,
        imagePath="assets/images/SchulterkraeftigungImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/vAozR51VE-k"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie zunächst aufrecht und beugen Sie sich dann mit geradem Rücken leicht nach vorne. Ellenbogen sind wieder eng am Rumpf und es ist ein 90 Grad Winkel zwischen Ober- und Unterarmen. Die Ellenbogen gehen nun nah am Rumpf schräg nach oben und dann wieder nach unten, als würden Sie etwas vom Boden schräg hochziehen und wieder hinunterstoßen. Strecken Sie ihre Arme, wenn Sie in der 'hinunterstoßen'-Phase sind kurz ganz aus.",
        name="Ellenbogenhochziehen",
        videoPath="assets/videos/Ellenbogenhochziehen.mp4",
        dauer=30,
        imagePath="assets/images/Ellenbogenhochziehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/w06qcM8N_lE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht mit den Händen vor Ihrem Körper ausgestreckt. Die Handflächen sollten nach unten zeigen. Führen Sie schnelle, auf- und abgehende Bewegungen durch. Dabei sollten die Arme vollständig ausgestreckt sein. Achten Sie darauf, dass der Nacken entlastet bleibt.",
        name="Paddeln",
        videoPath="assets/videos/Paddeln.mp4",
        dauer=30,
        imagePath="assets/images/Paddeln.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/ILpL1uiaLkc"

    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Mobilisation Sprunggelenk links: Setzen Sie sich auf eine Matte, ein Bett oder eine Liege. Strecken Sie Ihre Füße aus. Die Fußspitzen zeigen nach oben. Kippen Sie nun Ihr linkes Fußgelenk nach vorne, soweit es geht, und Das ganz langsam. Achten Sie darauf, dass Ihr Bein und der Fuß gerade sind und nicht zur Seite wegkippen. Gehen Sie mit Ihrem Fußgelenk anschließend in die Ausgangsstellung und kippen Sie ihn dann wieder nach vorne. Der Vorgang des Vorkippens dauert ca. einen langen Ausatmer. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Sprunggelenk links",
        videoPath="assets/videos/MSprunglelenkLinks.mp4",
        dauer=20,
        imagePath="assets/images/mspruL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/cGe7uvkSAQ4"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ihre Arme befinden sich im 90-Grad-Winkel zum Rumpf und waagerecht zu den Schultern. Die Handflächen zeigen zum Boden, und die Arme sind ausgestreckt. Rotieren Sie in aufrechter Haltung nun Ihre Handflächen. Halten Sie die Arme dabei oben, für etwa 45 Sekunden.",
        name="Schulterkreiseln",
        videoPath="assets/videos/Schulterkreiseln.mp4",
        dauer=45,
        imagePath="assets/images/Schulterkreiseln.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/21EYxRuNwZ0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie aufrecht und halten Sie eine Hantel/ Wasserflasche in jeder Hand, während Ihre Arme seitlich herabhängen. Heben Sie nun langsam beide Arme vor sich bis auf Schulterhöhe und senken Sie sie kontrolliert zurück. Der Rücken sollte gerade sein, der Blick nach vorne gerichtet und Sie gehen sie leicht in die Knie wobei sie den Bauch für die Stabilität und zur Entlastung des Rückens leicht anspannen. Wiederholen Sie diese Bewegung 10 bis 15 Mal. Die Hanteln sind hierbei erforderlich.",
        name="Vorderes Schulterheben",
        videoPath="assets/videos/VorderesSchulterheben.mp4",
        dauer=30,
        imagePath="assets/images/VorderesSchulterheben.png",
        added=False,
        instruction="",
        required="Hanteln/ Waserflasche",
        onlineVidePath="https://youtu.be/zLcK8hDzoqU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien, und legen Sie Ihre Arme gestreckt übereinander vor Ihrem Körper. Bewegen Sie dann Ihre Arme auseinander und dann jeweils hinter Ihren Rücken und versuchen Sie, sie so nah wie möglich aneinander zu bringen. Führen Sie diese Bewegung kontinuierlich aus und achten Sie auf einen geraden Rücken.",
        name="Schere",
        videoPath="assets/videos/Schere.mp4",
        dauer=60,
        imagePath="assets/images/Schere.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/f7hleF7Eqjk"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich mit leicht gespreizten Beinen und leicht nach vorne gebeugtem Oberkörper hin. Beugen Sie den Rücken leicht nach vorne und legen Sie Ihren linken Arm auf den Oberschenkel. Ihr rechter Arm hängt locker. Durch Gewichtsverlagerung bringen Sie den rechten Arm in eine Pendelbewegung. Der Rücken sollte gerade sein.",
        name="Schulterpendeln Rechts",
        videoPath="assets/videos/SchulterpendelnRechts.mp4",
        dauer=60,
        imagePath="assets/images/SchulterpendelnRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/JmBxk3XZolw"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich mit leicht gespreizten Beinen und leicht nach vorne gebeugtem Oberkörper hin. Beugen Sie den Rücken leicht nach vorne und legen Sie Ihren rechten Arm auf den Oberschenkel. Ihr linker Arm hängt locker. Durch Gewichtsverlagerung bringen Sie den rechten Arm in eine Pendelbewegung. Der Rücken sollte gerade sein.",
        name="Schulterpendeln Links",
        videoPath="assets/videos/SchulterpendelnLinks.mp4",
        dauer=60,
        imagePath="assets/images/SchulterpendelnLinks2.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/dIm3wSRUx3w"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien. Lassen Sie Ihre Arme wie eine Windmühle nach vorne kreisen, während Ihr Kopf nach vorne schaut. Der Rücken sollte gerade bleiben und der Oberkörper sich möglichst wenig mitbewegen.",
        name="Armkreisen/ Windmühle nach vorne",
        videoPath="assets/videos/WindmuehleVorne.mp4",
        dauer=60,
        imagePath="assets/images/WindmuehleVorne.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/9Hqb4qGZG3w"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien. Lassen Sie Ihre Arme wie eine Windmühle nach hinten kreisen, während Ihr Kopf nach vorne schaut.",
        name="Armkreisen/ Windmühle nach hinten",
        videoPath="assets/videos/WindmuehleHinten.mp4",
        dauer=60,
        imagePath="assets/images/WindmuehleHinten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/QcTXvtULl3I"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ziehen Sie Ihre Schultern zuerst nach oben und führen Sie dann kleine Kreisbewegungen mit Ihren Schultern nach hinten aus. Hierbei bewegen sich die Schultern auch nach unten. Beginnen Sie von vorne. Der Nacken ist dabei entspannt und sie stehen aufrecht, leicht in den Knien.",
        name="Schulterkreisen nach hinten",
        videoPath="assets/videos/SchulterkreisenHinten.mp4",
        dauer=40,
        imagePath="assets/images/SchulterkreisenHinten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/VatSJUlsR7s"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ziehen Sie Ihre Schultern zuerst nach oben und führen Sie dann eine Kreisbewegung mit Ihren Schultern nach vorne aus. Danach gehen Ihre Schultern nach unten und daraufhin zurück auf ihre Ausgangsposition. Beginnen Sie von vorne. Der Nacken ist dabei entspannt und sie stehen aufrecht, leicht in den Knien.",
        name="Schulterkreisen nach vorne",
        videoPath="assets/videos/SchulterkreisenVorne.mp4",
        dauer=40,
        imagePath="assets/images/SchulterkreisenVorne.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/6ytDZ0al-yA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht und strecken Sie Ihren rechten Arm aus, woraufhin der Arm leicht nach unten geht, sodass der Arm nun schräg nach unten zeigt. Die Handfläche zeigt nach vorne. Ihre linke Hand geht nun unter dem rechten Arm durch und greift den rechten Daumen, um ihn sanft zum Körper zu ziehen. Achten Sie darauf, dass sie nur eine leichte Dehnung spüren und den Daumen nicht zu stark zu sich ziehen.",
        name="Daumendehnung rechts",
        videoPath="assets/videos/DaumenDehnungRechts.mp4",
        dauer=30,
        imagePath="assets/images/DaumenDehnungRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Zm1skfJizG4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehen Sie zunächst in den Vierfüßlerstand mit einem geraden Rücken. Drehen Sie dann Ihre Fingerspitzen nach außen, sodass sie in Richtung Ihrer Knie zeigen, um eine leichte Dehnung in den Unterarmen zu fühlen. Lehnen Sie sich dabei vorsichtig nach hinten, soweit es möglich ist, ohne Schmerzen zu spüren.",
        name="Dehnung Unterarme",
        videoPath="assets/videos/DehnugUnterarme.mp4",
        dauer=40,
        imagePath="assets/images/DehnugUnterarme.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/D9YnMFANEjI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Strecken Sie den linken Arm nach vorne aus. Umschließen sie dann den Daumen mit der Faust. Knicken sie nun das Handgelenk nahch unten ab und halten sie mit ihrer rechten Hand die linke Hand in der Faustposition. Stützen sie sich nun auf dem linken Handrücken vorsichtig und langsam ab, wenn sie in die abgewandte Position des Vierfüßlerstandes gehen. Achten sie auf einen geraden Rücken. ",
        name="Dehnung Handgelenk links",
        videoPath="assets/videos/DehnungHandgelenkLinks3.mp4",
        dauer=40,
        imagePath="assets/images/DehnungHandgelenkLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/sHdsLWoDblw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Strecken Sie den rechten Arm nach vorne aus. Umschließen sie dann den Daumen mit der Faust. Knicken sie nun das Handgelenk nahch unten ab und halten sie mit ihrer rechten Hand die linke Hand in der Faustposition. Stützen sie sich nun auf dem linken Handrücken vorsichtig und langsam ab, wenn sie in die abgewandte Position des Vierfüßlerstandes gehen. Achten sie auf einen geraden Rücken. ",
        name="Dehnung Handgelenk rechts",
        videoPath="assets/videos/DehnungHandgelenkRechts.mp4",
        dauer=40,
        imagePath="assets/images/DehnungHandgelenkRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/VTXvLgJQvI0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Strecken Sie Ihren rechten Arm aus und legen Sie die Handfläche an die Wand. Drehen Sie diese Hand nach rechts, sodass die Fingerspitzen nach unten zeigen. Schieben Sie Ihren Oberkörper in Richtung der Wand, um eine leichte Dehnung zu spüren. Lassen Sie ihren Arm durchgestreckt.",
        name="Rechte Unterarmdehnung",
        videoPath="assets/videos/UnterarmRechts.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmRechtsWand.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/FAXsQ8zay8U"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Strecken Sie Ihren linken Arm aus und legen Sie die Handfläche an die Wand. Drehen Sie diese Hand nach links, sodass die Fingerspitzen nach unten zeigen. Schieben Sie Ihren Oberkörper in Richtung der Wand, um eine leichte Dehnung zu spüren. Lassen Sie ihren Arm durchgestreckt.",
        name="Linke Unterarmdehnung",
        videoPath="assets/videos/UnterarmLinks.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmLinksWand.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/2e8yCIb5PLY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stellen Sie sich vor eine Wand und ballen Sie mit der linken Hand eine Faust. Strecken sie den linken Arm aus und rotieren Sie die Faust, sodass der Daumen zum Boden zeigt. Knicken Sie dann das Handgelenk nach außen ab und drücken Sie den Handrücken anschließen vorsichtig und langsam gegen die Wand, bis ein 90-Grad-Winkel zwischen Unterarm und Handrücken entsteht. Führen Sie diese Bewegung mit gestreckten Arm aus uns stehen sie seitlich zur Wand ",
        name="Dehnung Handrücken Rechts",
        videoPath="assets/videos/DehnungHandrueckenRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHandrueckenRechts.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/V_f61S10Et4"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stellen Sie sich vor eine Wand und ballen Sie mit der linken Hand eine Faust. Strecken sie den linken Arm aus und rotieren Sie die Faust, sodass der Daumen zum Boden zeigt. Knicken Sie dann das Handgelenk nach außen ab und drücken Sie den Handrücken anschließen vorsichtig und langsam gegen die Wand, bis ein 90-Grad-Winkel zwischen Unterarm und Handrücken entsteht. Führen Sie diese Bewegung mit gestreckten Arm aus uns stehen sie seitlich zur Wand ",
        name="Dehnung Handrücken Links",
        videoPath="assets/videos/DehnungHandrueckenLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHandrueckenLinks.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/EyS7f2zBXSA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Ihre rechte Hand berührt Ihre rechte hintere Schulter, und die Unterseite des Oberarms ist an der Wand angelehnt. Ihre linke Hand zieht mit den Fingern Ihre rechte Hand am Handgelenk in Richtung Boden. Achten Sie darauf, dass der Ellenbogen gerade nach oben zeigt und nicht zur Seite abknickt. Dehnen Sie nicht zu stark und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung für Tennisarm rechts",
        videoPath="assets/videos/DehnungTennisarmRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungTennisarmRechts.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/40HuYS6Fh0U"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Ihre linke Hand berührt Ihre linke hintere Schulter, und die Unterseite des Oberarms ist an der Wand angelehnt. Ihre rechte Hand zieht mit den Fingern Ihre linke Hand am Handgelenk in Richtung Boden. Achten Sie darauf, dass der Ellenbogen gerade nach oben zeigt und nicht zur Seite abknickt. Dehnen Sie nicht zu stark und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung für Tennisarm links",
        videoPath="assets/videos/DehungTennisarmLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehungTennisarmLinks.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/H78nspGhd-k"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich aufrecht hin. Heben Sie den linken Arm nun seitlich an, bis ein ca. 30 Grad großer Winkel zwischen Rumpf und Arm entsteht. Der Handrückem zeigt nach vorne und Sie nehmen Ihrnen Daumen nun in die Handfläche als würden Sie eine 4 zeigen. Die linke Schulter geht nun soweit wie möglich nach unten, wobei der Arm seitlich ausgestreckt bleibt. Wenn Sie noch keine Dehnung sprüren Versetzen Sie den Arm weiter nach hinten und heben Sie ihn seitlich leicht an. Neigen Sie den Kopf nach rechts und spüren Sie eine sanfte Dehnung im Bereich des Arms. Drehen Sie den Arm nun 3 mal sodass der Handrücken zunächst nach vorne und dann nach hintern zeigt. Anschließend halten Sie die Dehnung für ein paar Sekunden und routiren ihren Arm dann anschließen aus dem Schultergelenk 3 mal. Dann halten Sie die Dehnung wieder kurz. Zum Schluß ziehen sie die Schulter nocheinmal 3 mal nach oben und senken sie wieder ab. Der Handrücken zeigt außer bei der Drehung des Armes immer nach vorne und der Daumen verlässt seine Position nicht. Gehen Sie nicht über 5 auf einer Schmerzskala. ",
        name="Armnerven Mobilisation links",
        videoPath="assets/videos/ArmnervenmobilisationLinks2.mp4",
        dauer=50,
        imagePath="assets/images/ArmnervenmobilisationLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/bzyosU-Y55o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich aufrecht hin. Heben Sie den rechten Arm nun seitlich an, bis ein ca. 30 Grad großer Winkel zwischen Rumpf und Arm entsteht. Der Handrückem zeigt nach vorne und Sie nehmen Ihrnen Daumen nun in die Handfläche als würden Sie eine 4 zeigen. Die rechte Schulter geht nun soweit wie möglich nach unten, wobei der Arm seitlich ausgestreckt bleibt. Wenn Sie noch keine Dehnung sprüren Versetzen Sie den Arm weiter nach hinten und heben Sie ihn seitlich leicht an. Neigen Sie den Kopf nach links und spüren Sie eine sanfte Dehnung im Bereich des Arms. Drehen Sie den Arm nun 3 mal sodass der Handrücken zunächst nach vorne und dann nach hintern zeigt. Anschließend halten Sie die Dehnung für ein paar Sekunden und routiren ihren Arm dann anschließen aus dem Schultergelenk 3 mal. Dann halten Sie die Dehnung wieder kurz. Zum Schluß ziehen sie die Schulter nocheinmal 3 mal nach oben und senken sie wieder ab. Der Handrücken zeigt außer bei der Drehung des Armes immer nach vorne und der Daumen verlässt seine Position nicht. Gehen Sie nicht über 5 auf einer Schmerzskala. ",
        name="Armnerven Mobilisation rechts",
        videoPath="assets/videos/ArmnervenmobilisationRechts3.mp4",
        dauer=50,
        imagePath="assets/images/ArmnervenmobilisationRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Nmy27Q0Kitw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht oder stehen Sie aufrecht. Ihre rechte Hand geht nun zwischen die Schulterblätter. Versuchen Sie ihre rechten Fingerspitzen so nah wie möglich zum Boden zu bekommen und achten Sie darauf, dass die Handfläche möglichst mitig und wirklich zwischen den Schulterblättern ist. Ihre linke Hand zieht vorsichtig den rechten Ellenbogen nach links. Achten Sie darauf, die Dehnung sanft und kontrolliert auszuführen, um den Trizeps zu dehnen. Halten Sie die Position und atmen Sie ruhig. Falls Sie Schmerzen verspüren, brechen Sie die Übung sofort ab.",
        name="Trizepsdehnung rechts",
        videoPath="assets/videos/TrizepsDehnungRechts.mp4",
        dauer=40,
        imagePath="assets/images/TrizepsDehnungRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Pz2PSdm7XJI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht oder stehen Sie aufrecht. Ihre linke Hand geht nun zwischen die Schulterblätter.Versuchen Sie ihre rechten Fingerspitzen so nah wie möglich zum Boden zu bekommen und achten Sie darauf, dass die Handfläche möglichst mitig und wirklich zwischen den Schulterblättern ist. Ihre rechte Hand zieht vorsichtig den linken Ellenbogen nach rechts. Achten Sie darauf, die Dehnung sanft und kontrolliert auszuführen, um den Trizeps zu dehnen. Halten Sie die Position und atmen Sie ruhig. Falls Sie Schmerzen verspüren, brechen Sie die Übung sofort ab.",
        name="Trizepsdehnung links",
        videoPath="assets/videos/TrizepsDehnungLinks.mp4",
        dauer=40,
        imagePath="assets/images/TrizepsDehnungLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/cfYr1iIllFc"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und bewahren Sie eine aufrechte Haltung. Breiten Sie Ihre Arme seitlich aus und strecken Sie sie, sodass eine waagerechte Linie zwischen Ihren Schultern und Armen entsteht. Zu Beginn zeigen Handflächen und Kopf nach oben. Halten Sie Ihren Rücken während der gesamten Übung gerade. Drehen Sie nun Handflächen und Kopf nach vorne, soweit es geht, und kehren Sie zur Ausgangsposition zurück. Halten Sie Ihre Finger während der Übung möglichst gespreizt.",
        name="Armkräftigung",
        videoPath="assets/videos/Armkraeftigung3.mp4",
        dauer=60,
        imagePath="assets/images/Armkraeftigung.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/MTU4B5bv0UU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Nehmen Sie eine aufrechte Sitzposition ein. Imitieren Sie die Armbewegungen eines Kaktus: Ihr linker Arm bildet einen 90-Grad-Winkel zwischen Ober- und Unterarm und zeigt zum Boden, während Ihre Handfläche nach hinten gerichtet ist. Ihr rechter Arm bildet ebenfalls einen 90-Grad-Winkel zwischen Ober- und Unterarm, zeigt zur Decke und die Handfläche ist nach vorne gerichtet. Der rechte Arm geht nun in die Position des linken Arms und umgekehrt. Dabei sollten die Oberarme parallel zum Boden bleiben und sich möglichst nicht bewegen. Die 90 Grad Winkel sollten möglichst dauerhaft erhalten bleiben.",
        name="Kaktus",
        videoPath="assets/videos/Kaktus.mp4",
        dauer=60,
        imagePath="assets/images/Kaktus.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/eZ1Qbc1UkQk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Begeben Sie sich in die Position für einen Liegestütz, allerdings stützen sie ihr Gewicht auf den Knien ab und nicht wie beim normalen Liegestütz auf den Füßen. Ihr Rücken sollte während der Übung gerade sein, und Ihre Hände sollten sich etwa auf Höhe der Schultern am Boden befinden. Beim Hochkommen aus der Liegestützposition atmen Sie aus und beim runtergehen Atmen Sie ein.",
        name="Abgewandte Liegestütz",
        videoPath="assets/videos/AbgewandterLiegestuetz2.mp4",
        dauer=15,
        imagePath="assets/images/AbgewandterLiegestuetz.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/m74EFFeDNDE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Beginnen Sie in aufrechter Haltung, stehen Sie mit den Füßen zusammen und die Arme an den Seiten. Springen Sie in die Luft und spreizen Sie die Beine zur Seite, während Sie gleichzeitig die Arme über den Kopf heben. Landen Sie wieder in einer aufrechten Position und führen Sie die Beine und Arme wieder zusammen.",
        name="Hampelmann",
        videoPath="assets/videos/Hampelmann.mp4",
        dauer=60,
        imagePath="assets/images/Hampelmann.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/IXYwjyezEoY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Legen Sie sich auf die linke Seite. Ihr rechter Arm stützt Sie und Ihr Oberkörper ist leicht verdreht, während Ihr linker Arm sie umarmt. Der stützende Arm sollte etwa auf Schulterhöhe sein, und ihre Beine sollten die ganze Zeit am Boden bleiben und sind versetzt zueinander. Senken Sie Ihren Oberkörper seitlich ab, sodass Ihr rechter Arm unter Belastung steht. Drücken Sie sich mit dem rechten Arm wieder nach oben. Achten Sie darauf, die Bewegung kontrolliert auszuführen und atmen Sie ruhig. Die Übung erfordert Stabilität und Kraft in den seitlichen Muskeln.",
        name="Armkräftigung Seitlicher Liegestütz rechts",
        videoPath="assets/videos/SeitlicherLiegestuetzR.mp4",
        dauer=15,
        imagePath="assets/images/ArmkraeftigungSeitlicherLiegestuetzR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/F7s8RS4bJs8"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Legen Sie sich auf die rechte Seite. Ihr linker Arm stützt Sie und Ihr Oberkörper ist leicht verdreht, während Ihr rechter Arm sie umarmt. Der stützende Arm sollte etwa auf Schulterhöhe sein, und ihre Beine sollten die ganze Zeit am Boden bleiben und sind versetzt zueinander. Senken Sie Ihren Oberkörper seitlich ab, sodass Ihr linker Arm unter Belastung steht. Drücken Sie sich mit dem linken Arm wieder nach oben. Achten Sie darauf, die Bewegung kontrolliert auszuführen und atmen Sie ruhig. Die Übung erfordert Stabilität und Kraft in den seitlichen Muskeln.",
        name="Armkräftigung Seitlicher Liegestütz links",
        videoPath="assets/videos/SeitlicherLiegestuetzL.mp4",
        dauer=15,
        imagePath="assets/images/ArmkraeftigungSeitlicherLiegestuetzL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/q1V5v-_Fgrc"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie sich aufrecht auf eine Matte. Setzen Sie Ihre Hände hinter Ihrem Rücken ab, sodass sie Sie stützen. Drehen Sie Ihre Fingerspitzen so, dass sie in Richtung Ihres Gesäßes zeigen. Drücken Sie sich aus den Schultern heraus nach oben, sodass ihr Gesäß über dem Boden schwebt und sie den Boden nur mit den Versen und ihren Handflächen berühren. Senken Sie ihr Gesäß nun wieder in Richtung Boden ab und heben Sie es wieder, als würden Sie Dips für den Trizeps machen. Spannen Sie während der Übung Ihren Bauch an und achten Sie darauf, dass Ihre Beine und Ihr Oberkörper eine möglichst gerade Linie bilden. Achten Sie außerdem darauf, die Bewegung kontrolliert auszuführen und atmen Sie gleichmäßig. Diese Übung stärkt Ihre Trizeps-Muskulatur und erfordert Stabilität im Oberkörper.",
        name="Trizeps Dips im Liegenden Sitz",
        videoPath="assets/videos/TrizepsDipsImLiegen.mp4",
        dauer=12,
        imagePath="assets/images/TrizepsDipsImLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3p41QJQ0PGQ"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche sollte dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training Ihres linken Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps links",
        videoPath="assets/videos/BizepsLinks2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsLinks.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/uTh6OeySo4A"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche sollte dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training Ihres rechten Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps rechts",
        videoPath="assets/videos/BizepsRechts2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsRechts.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/DVdEktILMf4"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand und eine in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihre Ellenbogen während der Übung nah am Körper, während Sie die Wasserflaschen nach oben bewegen. Die Flaschen sollten dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training beider Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps beidseitig",
        videoPath="assets/videos/BizepsBeidseitig2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsBeidseitig.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/4tbXggIXm7M"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und beugen Sie sich nach vorne, sodass Ihr linker Ellenbogen auf Ihrem linken Oberschenkel ruht. Nehmen Sie eine Wasserflasche in die linke Hand. Heben und senken Sie Ihr Handgelenk, während Ihr Rücken gerade ist und der Ellenbogen am Oberschenkel bleibt. Führen Sie diese Bewegung etwa 40 Sekunden lang im gezeigten Tempo aus, um Ihre Unterarmmuskulatur zu stärken.",
        name="Unterarm links",
        videoPath="assets/videos/UnterarmLinks.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmLinks.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/2TAcpv-MNbY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und beugen Sie sich nach vorne, sodass Ihr rechter Ellenbogen auf Ihrem rechten Oberschenkel ruht. Nehmen Sie eine Wasserflasche in die rechte Hand. Heben und senken Sie Ihr Handgelenk, während Ihr Rücken gerade ist und der Ellenbogen am Oberschenkel bleibt. Führen Sie diese Bewegung etwa 40 Sekunden lang im gezeigten Tempo aus, um Ihre Unterarmmuskulatur zu stärken.",
        name="Unterarm rechts",
        videoPath="assets/videos/UnterarmRechts.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmRechts.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/DVruqdMzhzc"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Ihr Rücken sollte gerade sein, und Sie können leicht in die Knie gehen, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche ist anfangs nach vorne gerichtet (parallel zu Fußspitzen) und dreht sich während des Hochbewegens so, dass sie in der Endposition parallel zum Boden ist. Diese Übung zielt auf die Kräftigung des linken Bizeps und Trizeps ab und verbessert die Kraft und Ausdauer in diesen Muskelgruppen.",
        name="Bizeps und Trizeps links",
        videoPath="assets/videos/BizepsTrizepsLinks2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsTrizepsLinks.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/c7OFz_3dxfg"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Ihr Rücken sollte gerade sein, und Sie können leicht in die Knie gehen, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche ist anfangs nach vorne gerichtet (parallel zu Fußspitzen) und dreht sich während des Hochbewegens so, dass sie in der Endposition parallel zum Boden ist. Diese Übung zielt auf die Kräftigung des rechten Bizeps und Trizeps ab und verbessert die Kraft und Ausdauer in diesen Muskelgruppen.",
        name="Bizeps und Trizeps rechts",
        videoPath="assets/videos/BizepsTrizepsRechts.mp4",
        dauer=20,
        imagePath="assets/images/BizepsTrizepsRechts.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/qhGDiUV_z5w"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie gerade oder setzen Sie sich aufrecht hin. Strecken Sie den linken Arm aus, ballen Sie eine Faust und halten Sie mit der rechten Hand Ihren Bizeps fest. Der Handrücken schaut zunächst nach unten. Führen Sie einen Ellenbogenkreis im Uhrzeigersinn aus, indem die Faust zum Kinn geht und dann so weit wie möglich außen zurück zur ausgestreckten Position. Jetzt sollte der Handrücken nach unten zeigen. Während der Kreisbewegung drehen Sie den Bizeps leicht nach links. Drehen Sie nun anschließend ihre Hand um 180 Grad, sodass diese sich wieder in der Position vom Anfang befindet. Beginnen Sie von vorn.",
        name="Mobilisierung Elle links",
        videoPath="assets/videos/MobilisationElleLinks.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationElleLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/TJBmoiZJHm0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie gerade oder setzen Sie sich aufrecht hin. Strecken Sie den rechten Arm aus, ballen Sie eine Faust und halten Sie mit der linken Hand Ihren Bizeps fest. Der Handrücken schaut zunächst nach unten. Führen Sie einen Ellenbogenkreis gegen den Uhrzeigersinn aus, indem die Faust zum Kinn geht und dann so weit wie möglich außen zurück zur ausgestreckten Position. Jetzt sollte der Handrücken nach unten zeigen. Während der Kreisbewegung drehen Sie den Bizeps leicht nach links. Drehen Sie nun anschließend ihre Hand um 180 Grad, sodass diese sich wieder in der Position vom Anfang befindet. Beginnen Sie von vorn.",
        name="Mobilisierung Elle rechts",
        videoPath="assets/videos/MobilisationElleRechts.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationElleRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/YwqVTiQQE74"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf den Boden und legen Sie Ihren Unterarm auf einer Tischkante ab, sodass Ihr Handgelenk freischwebt. Sie können sich auch auf einen Stuhl setzen, allerdings brauchen Sie dann einen höheren Tisch. Beugen Sie das Handgelenk nach oben und halten Sie die Position für einige Sekunden. Beugen Sie das Handgelenk dann nach unten und halten Sie erneut. Achten Sie darauf, nicht zu stark zu dehnen.",
        name="Handgelenkflexion und -Extension Rechts",
        videoPath="assets/videos/HandgelenkFlexionRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkFlexionRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/acN2yuFGOKs"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und halten Sie Ihren Oberarm nach vorne ausgestreckt. Beugen Sie den Ellenbogen auf der linken Seite, indem Sie die Handfläche zur rechten Schulter bringen, und strecken Sie den Arm anschließend wieder nach vorne aus. Machen Sie dasselbe für die andere Seite.",
        name="Ellenbogen beugen, strecken",
        videoPath="assets/videos/EllenbogenBeugenStrecken.mp4",
        dauer=30,
        imagePath="assets/images/EllenbogenBeugenStrecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Gi4DyesJXR4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Halten Sie Ihre Hände gerade vor sich, mit ausgestreckten Fingern. Bewegen Sie Ihre Handgelenke in einer Kreisbewegung im Uhrzeigersinn und dann gegen den Uhrzeigersinn. Fangen Sie zunächst mit einem langsamen Tempo an und werden Sie dann ein wenig schneller.",
        name="Kreissäge mit den Händen",
        videoPath="assets/videos/KreissaegeMitHaenden.mp4",
        dauer=30,
        imagePath="assets/images/KreissaegeMitHaenden.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/DjbDmPpoQL0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den rechten Arm aus. Zeigen Sie nun mit den Fingerspitzen zur Decke, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung oben rechts",
        videoPath="assets/videos/HandgelenkDehnungObenRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungObenRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/GEt3XifhExE"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den linken Arm aus. Zeigen Sie nun mit den Fingerspitzen zur Decke, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung oben links",
        videoPath="assets/videos/HandgelenkDehnungObenLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungObenLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/FMA2BekeJl0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den linken Arm aus. Zeigen Sie nun mit den Fingerspitzen zum Boden, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung unten links",
        videoPath="assets/videos/HandgelenkDehnungUntenLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungUntenLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/eAff2QhVFDs"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den rechten Arm aus. Zeigen Sie nun mit den Fingerspitzen zum Boden , bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung unten rechts",
        videoPath="assets/videos/HandgelenkDehnungUntenRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungUntenRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/y79A_grklp4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Sie können die Übung bei Bedarf abbrechen.Mobilisation Speiche links: Stellen Sie sich aufrecht hin (auch im aufrechten Sitzen möglich). Strecken Sie den linken Arm seitlich aus. Der Daumen ist so, als würden Sie eine 4 zeigen und die Handfläche zeigt zunächst nach oben. Führen Sie die Fingerspitzen in einer abwärts Kreisbewegung zur Taille. Die Schulter darf nicht zu weit nach vorne gehen. Fixieren Sie sie daher mit der freien Hand. Versuchen Sie den Kreis zu vollenden, sodass die Handfläche am Ende wieder nach oben zeigt. Drehen Sie die Handfläche, sodass sie wieder in der Ausgangsposition ist und beginnen Sie von vorne.",
        name="Mobilisation Speiche rechts",
        videoPath="assets/videos/MobilisationSpeicheRechts.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationSpeicheRechts.png",
        added=False,
        instruction="",
        required="Optional Stuhl",
        onlineVidePath="https://youtu.be/2shtAOYyX_Y"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Sie können die Übung bei Bedarf abbrechen.Mobilisation Speiche links: Stellen Sie sich aufrecht hin (auch im aufrechten Sitzen möglich). Strecken Sie den rechten Arm seitlich aus. Der Daumen ist so, als würden Sie eine 4 zeigen und die Handfläche zeigt zunächst nach oben. Führen Sie die Fingerspitzen in einer abwärts Kreisbewegung zur Taille. Die Schulter darf nicht zu weit nach vorne gehen. Fixieren Sie sie daher mit der freien Hand. Versuchen Sie den Kreis zu vollenden, sodass die Handfläche am Ende wieder nach oben zeigt. Drehen Sie die Handfläche, sodass sie wieder in der Ausgangsposition ist und beginnen Sie von vorne.",
        name="Mobilisation Speiche links",
        videoPath="assets/videos/MobilisationSpeicheLinks.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationSpeicheLinks.png",
        added=False,
        instruction="",
        required="Optional Stuhl",
        onlineVidePath="https://youtu.be/mJ_raWeOUvE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Armmobilisation links (Tennisarm): Stellen Sie sich aufrecht hin oder sitzen Sie aufrecht. Strecken Sie den linken Arm seitlich aus. Senken Sie den Arm nun so, dass er nur noch leicht vom Körper absteht (ca. 30 Grad Winkel). Bringen Sie den Daumen in eine Position, sodass Sie ihn mit den restlichen Fingern umschließen könnten, als ob Sie eine 4 zeigen würden. Drehen Sie den Arm nach hinten, sodass der Daumen nach hinten zeigt. Fassen Sie mit der rechten Hand auf Ihre Schulter und senken Sie die Schulter ab. Der Oberkörper bleibt gerade. Neigen Sie Ihren Kopf nach rechts und heben Sie den Arm seitlich, bis Sie eine 4 auf der Schmerzskala von 1-10 fühlen. Schulter und Arm bleiben unten.",
        name="Armmobilisation links (Tennisarm)",
        videoPath="assets/videos/ArmmobilisationTennisarmLinks2.mp4",
        dauer=40,
        imagePath="assets/images/ArmmobilisationTennisarmLinks.png",
        added=False,
        instruction="",
        required="Optional: Stuhl",
        onlineVidePath="https://youtu.be/5Is-XsSKPeY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Armmobilisation rechts (Tennisarm): Stellen Sie sich aufrecht hin oder sitzen Sie aufrecht. Strecken Sie den rechten Arm seitlich aus. Senken Sie den Arm nun so, dass er nur noch leicht vom Körper absteht (ca. 30 Grad Winkel). Bringen Sie den Daumen in eine Position, sodass Sie ihn mit den restlichen Fingern umschließen könnten, als ob Sie eine 4 zeigen würden. Drehen Sie den Arm nach hinten, sodass der Daumen nach hinten zeigt. Fassen Sie mit der linken Hand auf Ihre Schulter und senken Sie die Schulter ab. Der Oberkörper bleibt gerade. Neigen Sie Ihren Kopf nach rechts und heben Sie den Arm seitlich, bis Sie eine 4 auf der Schmerzskala von 1-10 fühlen. Schulter und Arm bleiben unten.",
        name="Armmobilisation rechts (Tennisarm)",
        videoPath="assets/videos/ArmmobilisationTennisarmRechts2.mp4",
        dauer=40,
        imagePath="assets/images/ArmmobilisationTennisarmRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/gB292C-2RFM"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Handgelenke Mobilisieren: Setzen Sie sich aufrecht hin oder stehen Sie aufrecht. Verschränken Sie die Hände wie bei einem Gebet. Beginnen Sie nun die Handgelenke zu bewegen und kreisförmige Bewegungen mit den Händen zu machen. Versuchen Sie möglichst aufrecht zu stehen und beginnen Sie mit kleinen Kreisen und einer langsamen Frequenz. Werden Sie im Verlauf der Übung ein wenig schneller und machen Sie immer größere Kreise",
        name="Handgelenke Mobilisieren",
        videoPath="assets/videos/HandgelenkeMobilisieren.mp4",
        dauer=20,
        imagePath="assets/images/HandgelenkeMobilisieren.png",
        added=False,
        instruction="",
        required="Optional: Stuhl",
        onlineVidePath="https://youtu.be/GGMBnpa7s30"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Seitliche Rumpfdehnung rechts: Sitzen Sie aufrecht und heben Sie den rechten Arm nach ausgestreckt oben. Beugen Sie Ihren Oberkörper sanft zur linken Seite, während Sie die rechte Hand über den Kopf ziehen und die andere nach unten richtung Boden bewegen. Halten Sie die Dehnung für 30 Sekunden und achten Sie darauf, dass ihr Rücken gerade bleibt und die Hüfte sich nicht bewegt.",
        name="Seitliche Rumpfdehnung rechts",
        videoPath="assets/videos/seitlicheDehnungmRechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfDehnugRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/EuHs16lRh_Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Seitliche Rumpfdehnung links: Sitzen Sie aufrecht und heben Sie den linken Arm ausgestreckt nach oben. Beugen Sie Ihren Oberkörper sanft zur rechten Seite, während Sie die linke Hand über den Kopf ziehen und die andere nach unten richtung Boden bewegen. Halten Sie die Dehnung für 30 Sekunden und achten Sie darauf, dass ihr Rücken gerade bleibt und die Hüfte sich nicht bewegt.",
        name="Seitliche Rumpfdehnung links",
        videoPath="assets/videos/SeitlicheRumpfDehnugLinks.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/c0eLPrqEloU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Thorakale Drehung links: Setzen Sie sich auf einen Stuhl, Rücken gerade. Legen Sie die linke Hand auf die rechte Außenseite Ihres rechten Oberschenkels. Drehen Sie Ihren Oberkörper nach rechts und benutzen Sie Ihre rechte Hand, um den Boden hinter Ihnen zu greifen. Halten Sie die Drehung für 15-20 Sekunden. Versuchen Sie die Hüfte nicht zu verrutschen und bleiben Sie während der gesamten Übung mit Ihrem Rücken gerade.",
        name="Thorakale Drehung links",
        videoPath="assets/videos/ThorakaleDenungLinks.mp4",
        dauer=30,
        imagePath="assets/images/ThorakaleDenungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/54MWXbEI608"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Thorakale Drehung rechts: Setzen Sie sich auf einen Stuhl, Rücken gerade. Legen Sie die rechte Hand auf die linke Außenseite Ihres linken Oberschenkels. Drehen Sie Ihren Oberkörper nach links und benutzen Sie Ihre linke Hand, um den Boden hinter Ihnen zu greifen. Halten Sie die Drehung für 15-20 Sekunden. Versuchen Sie die Hüfte nicht zu verrutschen und bleiben Sie während der gesamten Übung mit Ihrem Rücken gerade.",
        name="Thorakale Drehung rechts",
        videoPath="assets/videos/ThorakaleDenungRechts.mp4",
        dauer=30,
        imagePath="assets/images/ThorakaleDenungRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Y6xEdoEQbg4"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Katzen-Kuh-Dehnung: Beginnen Sie die Übung auf Händen und Knien im Vierfüßlerstand, mit den Händen unter den Schultern und den Knien unter den Hüften. Bei der Einatmung senken Sie den Rücken nach unten, heben den Kopf und schauen nach oben (Kuh-Haltung). Bei der Ausatmung runden Sie den Rücken, ziehen das Kinn zur Brust und schieben den Rücken nach oben (Katzenhaltung). Verwenden Sie eine Matte. Halten Sie jede Position für ca. 10 Sekunden",
        name="Katzen-Kuh-Dehnung",
        videoPath="assets/videos/KatzenKuhDehnung.mp4",
        dauer=30,
        imagePath="assets/images/KatzenKuhDehnung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/kbN_1oDYkqA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Erleichterte Plank: Stützen Sie sich mit den Händen und den Knien auf einer Matte ab. Ihr Rücken ist gerade, der Kopf schaut nach vorne. Strecken Sie nun abwechselnd den linken und dann den rechten Arm für eine kurze Zeit nach vorne/oben aus. Halten Sie die Plank mit nur einer Hand und versuchen stabil zu bleiben. Strecken Sie den Arm, der oben ist, voll aus.",
        name="Erleichterte Plank",
        videoPath="assets/videos/ErleichtertePlank.mp4",
        dauer=40,
        imagePath="assets/images/ErleichtertePlank.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/JUK4Y4mGMLg"
    ),
    UebungList(
        looping=False,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Heben/Senken: Legen Sie sich mit dem Bauch auf eine Matte. Winkeln Sie die Arme seitlich an. Der Kopf schaut in den Boden. Heben Sie nun Ihren Oberkörper nach oben und senken ihn langsam wieder ab. Die Arme sind die ganze Zeit in der Luft. Vergessen Sie nicht zu atmen.",
        name="Heben/Senken",
        videoPath="assets/videos/HebenSenken.mp4",
        dauer=20,
        imagePath="assets/images/HebenSenken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EIEfU7KiwIU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung Rücken: Legen Sie sich mit dem Bauch auf eine Matte. Heben Sie die Arme leicht an, halten Sie sie nah am Körper und zeigen Sie mit den Fingerspitzen nach hinten. Heben Sie Ihren Oberkörper leicht an. Halten Sie diese Position und beginnen Sie die Beine anzuwinkeln und wieder abzusenken. Der Blick ist nach unten gerichtet.",
        name="Kräftigung Unterer Rücken",
        videoPath="assets/videos/KraeftigungUntererRuecken.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/wdyW0yIUTzY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Fliegen: Legen Sie sich mit dem Bauch auf eine Matte. Strecken Sie Ihre Arme seitlich aus, mit 90 Grad zwischen Oberkörper und Armen. Der Kopf schaut in den Boden. Heben Sie nun Ihre Arme mit dem Oberkörper nach oben, als würden Sie mit den Flügeln schlagen, und senken ihn langsam wieder ab. Die Arme sind die ganze Zeit in der Luft. Vergessen Sie nicht zu atmen.",
        name="Fliegen",
        videoPath="assets/videos/Fliegen.mp4",
        dauer=30,
        imagePath="assets/images/Fliegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3hUW6XvQn4Y"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung im Vierfüßler Stand: Gehen Sie in den Vierfüßler Stand auf einer Matte. Ihr Rücken muss gerade sein. Strecken Sie nun abwechselnd das rechte Bein und den linken Arm und das linke Bein und den rechten Arm aus. Strecken Sie so weit, dass sich eine Waagerechte zwischen Rücken, Arm und Bein bildet.",
        name="Kräftigung im Vierfüßler Stand",
        videoPath="assets/videos/Vierfuesslerstand.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungImViefueßlerstand.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EcKsFt7XfmI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung Rücken/Bauch: Gehen Sie auf einer Matte in den Liegestütz (Hände ca. unter den Schultern Füße nah beieinander, Blick leicht nach vorne). Schieben Sie Ihren Oberkörper nun mit geradem Rücken und Kopf langsam leicht nach vorne, und wieder zurück. Versuchen Sie, stabil zu bleiben. Wenn Ihnen die Übung zu schwer fällt können sie sich auch auf den Knien abstützen. Achten Sie aber bitte die ganze Zeit darauf, dass ihr Rücken gerade ist.",
        name="Kräftigung Rücken und Bauch",
        videoPath="assets/videos/KraeftigungRueckenUndBauch.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungRueckenUndBauch.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/YcQeV6q-PD0"
    ),
    UebungList(
        looping=False,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Ruderübung mit Theraband: Befestigen Sie ein Theraband an einem festen Punkt, ca auf Bauchnabelhöhe. Nehmen Sie die Enden des Therabands in beide Hände und stehen Sie mit leicht gebeugten Knien. Ziehen Sie das Theraband zu sich, während Sie den Rücken gerade halten und die Ellbogen eng am Körper behalten. Spannen Sie den Bauch dabei an. Diese Übung stärkt die Muskeln im oberen und mittleren Rücken, was zur Entlastung des unteren Rückens beiträgt.",
        name="Ruderübung mit Theraband",
        videoPath="assets/videos/RuderuebungMitTheraband.mp4",
        dauer=30,
        imagePath="assets/images/RuderuebungMitTheraband.png",
        added=False,
        instruction="",
        required="Theraband",
        onlineVidePath="https://youtu.be/27Ouh_6GGj0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Mobilisation Sprunggelenk rechts: Setzen Sie sich auf eine Matte, ein Bett oder eine Liege. Strecken Sie Ihre Füße aus. Die Fußspitzen zeigen nach oben. Kippen Sie nun Ihr rechtes Fußgelenk nach vorne, soweit es geht, und Das ganz langsam. Achten Sie darauf, dass Ihr Bein und der Fuß gerade sind und nicht zur Seite wegkippen. Gehen Sie mit Ihrem Fußgelenk anschließend in die Ausgangsstellung und kippen Sie ihn dann wieder nach vorne. Der Vorgang des Vorkippens dauern ca. einen langen Ausatmer. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Sprunggelenk rechts",
        videoPath="assets/videos/MSprunglelenkRechts.mp4",
        dauer=20,
        imagePath="assets/images/mspru.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/CsUOtiueZtQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Vierfüßler Stand links: Gehen Sie in den Vierfüßler Stand. Strecken Sie nun Ihr rechtes Bein nach hinten aus. Drehen Sie Ihren linken Arm nach außen und stützen Sie sich mit der rechten Hand ab. Schauen Sie dem Arm hinterher. Führen Sie die Bewegung langsam aus. Tauchen Sie dann ab, indem Ihr linker Arm unter Ihrem Körper hindurchgeht und Ihr Oberkörper sich leicht verknotet. Gehen Sie zurück in die Grundstellung und führen Sie diese Übung für 1 Minute aus.",
        name="Aufdrehen im Vierfüßler Stand links",
        videoPath="assets/videos/AufdrehenVLinks.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenVLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Wu1OzuT5c-8"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Vierfüßler Stand rechts: Gehen Sie in den Vierfüßler Stand. Strecken Sie nun Ihr linkes Bein nach hinten aus. Drehen Sie Ihren rechten Arm nach außen und stützen Sie sich mit der linken Hand ab. Schauen Sie dem Arm hinterher. Führen Sie die Bewegung langsam aus. Tauchen Sie dann ab, indem Ihr rechter Arm unter Ihrem Körper hindurchgeht und Ihr Oberkörper sich leicht verknotet. Gehen Sie zurück in die Grundstellung und führen Sie diese Übung für 1 Minute aus.",
        name="Aufdrehen im Vierfüßler Stand rechts",
        videoPath="assets/videos/AufdrehenVRechts.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenVRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/ni7Ndtnyg8s"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Stehen: Stellen Sie sich hin. Beugen Sie sich nach vorne, sodass Oberkörper und Beine einen 90-Grad-Winkel bilden. Lassen Sie Ihre Arme baumeln und achten Sie auf einen geraden Rücken. Ihr linker Arm geht nun seitlich nach oben wie ein Flügelschlag, während der rechte Arm weiter locker nach unten hängt. Ihr Kopf schaut dem Arm, der gerade hoch geht, hinterher. Dann geht der Arm wieder zurück, und der rechte Arm ist derjenige, der hochgeht. Führen Sie das Ganze im gezeigten Tempo für etwa 1 Minute aus.",
        name="Aufdrehen im Stehen",
        videoPath="assets/videos/AufdrehenImStehen2.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/AGBMjoUHsPQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Drehung im Stehen: Verknoten Sie Ihre Arme vor dem Oberkörper, während Sie aufrecht stehen. Ihre Schultern sind tief und unten. Ihr Kopf ist gerade und schaut nach vorne. Drehen Sie sich ausatmend auf die eine Seite, dann einatmend zurück zur Ausgangsposition und dann ausatmend zur anderen Seite. Führen Sie diese Übung für ca. 1 Minute aus, sie kann auch im Sitzen ausgeführt werden. Ihr Bauch sollte leicht angespannt sein und ihre Beine in einer stabilen Stellung und die Knie sollten leicht gebeugt sein.",
        name="Drehung im Stehen",
        videoPath="assets/videos/DrehungImStehen.mp4",
        dauer=60,
        imagePath="assets/images/DrehungImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/XS96zl2e804"),
    UebungList(
        looping=True,
        timer=True,
        execution="Öffnen und schließen BWS: Stellen Sie sich etwas breitbeinig hin. Strecken Sie Ihre Arme nach oben, dannach lehnen Sie sich nach hinten und spreizen Ihre Finger auseinander. Die Daumen sollten nach hinten zeigen, und Sie sollten während dieser Bewegung einatmen. Atmen Sie aus und führen Sie Ihren ausgestreckten Armen eine Art Kreisbewegung aus, bei der Sie sie aus der Ausgangsposition wie eine Windmühle nach vorne drehen, bis es nicht weitergeht. Runden Sie dabei Ihren Rücken (wie der Ronaldo mit gekrümmtem Rücken). Gehen Sie wieder zurück zur Ausgangsposition.",
        name="Öffnen BWS",
        videoPath="assets/videos/OeffnenBWS.mp4",
        dauer=60,
        imagePath="assets/images/oeffnenBWS.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/4aDc9GLT1bo"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Mobilisierung Oberer Rücken: Stehen Sie breitbeinig und aufrecht. Strecken Sie beide Arme nach oben und fassen Sie sich selbst an den Händen, so als würden Sie sich selbst in die Länge ziehen. Beginnen Sie nun im stabilen Stand, Ihren Oberkörper in kreisartigen Bewegungen hin und her zu schwingen. Die Arme bleiben oben und der Rücken gerade, wobei sie versuchen die Drehung aus dem Rücken heraus zu machen und nicht aus der Hüfte heraus. Diese bewegt sich möglichst nicht. Brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Mobilisierung Oberer Rücken",
        videoPath="assets/videos/MORuecken.mp4",
        dauer=60,
        imagePath="assets/images/MobilisationObererRuecken.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/RoZ_XFUCQ6A"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Handgelenkflexion und -Extension links: Setzen Sie sich auf den Boden und legen Sie Ihren Unterarm auf einer Tischkante ab, sodass Ihr Handgelenk freischwebt. Sie können sich auch auf einen Stuhl setzen, allerdings brauchen Sie dann einen höheren Tisch. Beugen Sie das Handgelenk nach oben und halten Sie die Position für einige Sekunden. Beugen Sie das Handgelenk dann nach unten und halten Sie erneut. Achten Sie darauf, nicht zu stark zu dehnen.",
        name="Handgelenkflexion und -Extension links",
        videoPath="assets/videos/HandgelenkFlexionLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkFlexionLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/-zwuxR5K5pA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Rumpf unterer Rücken rechts: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Bein an und lassen Sie es nach rechts kippen. Drehen Sie Ihre Hüfte ebenfalls nach rechts. Ihre Schultern bleiben am Boden, sodass Sie sich verdrehen. Das rechte Bein bleibt ausgestreckt. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Rumpf unterer Rücken rechts",
        videoPath="assets/videos/DehnungRumpfUntererRueckenRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungRumpfUntererRueckenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/rz9ITNqHmOY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Rumpf unterer Rücken links: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Bein an und lassen Sie es nach rechts kippen. Drehen Sie Ihre Hüfte ebenfalls nach rechts. Ihre Schultern bleiben am Boden, sodass Sie sich verdrehen. Das rechte Bein bleibt ausgestreckt. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Rumpf unterer Rücken links",
        videoPath="assets/videos/DehnungRumpfUntererRueckenLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungRumpfUntererRueckenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/2C4r5b3OwFc"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Rumpfdehnung rechts: Stehen Sie aufrecht und strecken Sie die Arme über den Kopf. Beugen Sie Ihren Oberkörper sanft zur Seite, während Ihre Hände gestreckt über Ihnen sind und Sie sich in die Länge ziehen. Halten Sie die Dehnung für 15-20 Sekunden auf jeder Seite und wiederholen Sie sie mehrmals. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Rumpfdehnung rechts",
        videoPath="assets/videos/SeitlicheRumpfDehnugRechts.mp4",
        dauer=15,
        imagePath="assets/images/SeitlicheRumpfDehnugRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/UQx0DGGF78Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Rumpfdehnung links: Stehen Sie aufrecht und strecken Sie die Arme über den Kopf. Beugen Sie Ihren Oberkörper sanft zur Seite, während Ihre Hände gestreckt über Ihnen sind und Sie sich in die Länge ziehen. Halten Sie die Dehnung für 15-20 Sekunden auf jeder Seite und wiederholen Sie sie mehrmals. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Rumpfdehnung links",
        videoPath="assets/videos/SeitlicheRumpfDehnugLinks.mp4",
        dauer=15,
        imagePath="assets/images/SeitlicheRumpfdehnungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/9xNuqENu7MY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kobradehnung: Legen Sie sich mit Bauch auf eine Matte. Stützen Sie sich nun mit den Händen ab, als wären Sie eine Kobra. Halten Sie die Dehnung und übnerstrecken Sie den Kopf leicht. Sollten Sie Schmerzen/Schwindel spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Kobradehnung",
        videoPath="assets/videos/Kobradehnung.mp4",
        dauer=30,
        imagePath="assets/images/Kobradehnung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Z4DQUb6rLsQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Lendenwirbeldehnung links: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Knie an und lassen Sie es nach rechts fallen. Drehen Sie Ihre Hüfte, sodass ein 90-Grad-Winkel zwischen dem Boden und Ihrem Gesäß entsteht. Strecken Sie den linken Arm seitlich aus. Die rechte Hand liegt am linken Knie und zieht dieses leicht in Richtung Boden. Atmen Sie natürlich und schauen sie nach oben, wobei ihre Hüfte am Boden fixiert bleibt. Das linke Knie sollte mit ca. 90 Grad angewinkelt sein. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Lendenwirbeldehnung links",
        videoPath="assets/videos/LendernwirbeldehnungLinks.mp4",
        dauer=30,
        imagePath="assets/images/LendernwirbeldehnungLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/h2H-mFxIOd0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Lendenwirbeldehnung rechts: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr rechtes Knie an und lassen Sie es nach links fallen. Drehen Sie Ihre Hüfte, sodass ein 90-Grad-Winkel zwischen dem Boden und Ihrem Gesäß entsteht. Strecken Sie den rechten Arm seitlich aus. Die linke Hand liegt am rechtem Knie und zieht dieses leicht in Richtung Boden. Atmen Sie natürlich und schauen sie nach oben, wobei ihre Hüfte am Boden fixiert bleibt. Das rechte Knie sollte mit ca. 90 Grad angewinkelt sein. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Lendenwirbeldehnung rechts",
        videoPath="assets/videos/LendenwirbeldehnungRechts.mp4",
        dauer=30,
        imagePath="assets/images/LendenwirbeldehnungRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3FTm-Pv4M4E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Bauchpresse: Legen Sie sich mit dem Rücken auf eine Matte. Knie beugen, Arme nach oben strecken. Heben Sie den Oberkörper dann mit Hilfe der Bauchmuskeln vom Boden ab. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Bauchpresse",
        videoPath="assets/videos/Bauchpresse3.mp4",
        dauer=12,
        imagePath="assets/images/Bauchpresse.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/SpCWj5PBYJk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Russische Drehung: Setzen Sie sich auf eine Matte. Heben Sie Ihre Beine vom Boden ab und lehnen Sie Ihren Oberkörper nach hinten. Verschränken Sie Ihre Arme vor dem Oberkörper. Beginnen Sie sich abwechselnd nach rechts und dann nach links zu drehen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Russische Drehung",
        videoPath="assets/videos/RussischeDrehung.mp4",
        dauer=30,
        imagePath="assets/images/RussischeDrehung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/jGdCFO5Z3c0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Bergsteiger: Gehen Sie über eine Matte in die Liegestützposition. Halten Sie den Rücken gerade und tun Sie so, als würden Sie einen Berg hinauflaufen. Ihre Arme stützen Sie. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Bergsteiger",
        videoPath="assets/videos/Bergsteiger2.mp4",
        dauer=40,
        imagePath="assets/images/Bergsteiger.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/BYLJb8IXdoU"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Fersenaschlag: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihre Knie an. Heben Sie Ihren Oberkörper leicht vom Boden ab und halten Sie Ihren Hals in einer natürlichen Position. Ihre Arme sind nah am Körper. Berühren Sie nun abwechselnd mit Ihrer rechten Hand Ihre rechte Ferse und umgekehrt. Ihr Oberkörper bleibt oben. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Fersenaschlag",
        videoPath="assets/videos/Fersenanschlag2.mp4",
        dauer=30,
        imagePath="assets/images/Fersenanschlag.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/f7DbKiLrLHQ"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Beinhebung: Liegen Sie mit dem Rücken auf einer Matte. Ihre Hände sind nah am Körper und Ihre Beine sind gestreckt. Heben Sie Ihre Beine nun nach oben. Sie bleiben dabei gestreckt. Ihr Kopf schaut die ganze Zeit nach oben. Senken Sie die Beine und wiederholen Sie die Übung. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Beinhebung",
        videoPath="assets/videos/Beinhebung.mp4",
        dauer=15,
        imagePath="assets/images/Beinhebung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/vGZNPmdk1Ew"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Unterarmstütz: Führen Sie die Übung auf einer Matte aus. Der Rücken sollte gerade sein. Falls Ihnen die Übung zu schwer fällt, können Sie sich auf den Knien abstützen. Halten Sie diese Position. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Unterarmstütz",
        videoPath="assets/videos/Unteramstuetz.mp4",
        dauer=30,
        imagePath="assets/images/Unterarmstuetz.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/S7r-k1Wr2Ww"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Plank links: Liegen Sie auf einer Matte auf einer Seite und stützen Sie sich auf den linken Unterarm. Heben Sie Ihre Hüften, so dass Ihr Körper eine gerade Linie bildet. Halten Sie die Position, während Ihr freier Arm nah am Körper auf Ihrer Hüfte liegt. Sie können auch den rechten Fuß nach oben tun, wenn Ihnen die Übung zu leicht fällt. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Plank links",
        videoPath="assets/videos/SPlankLinks.mp4",
        dauer=30,
        imagePath="assets/images/SeitlichePlankLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/hzJvSYPNXhs"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Plank rechts: Liegen Sie auf einer Matte auf einer Seite und stützen Sie sich auf den rechten Unterarm. Heben Sie Ihre Hüften, so dass Ihr Körper eine gerade Linie bildet. Halten Sie die Position, während Ihr freier Arm nah am Körper auf Ihrer Hüfte liegt. Sie können auch den linken Fuß nach oben tun, wenn Ihnen die Übung zu leicht fällt. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Plank rechts",
        videoPath="assets/videos/SPlankRechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlichePlankRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/KZ2YCBsi_k0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sit-Ups: Legen Sie sich auf den Rücken auf eine Matte mit gebeugten Knien. Halten Sie die Hände hinter dem Kopf oder über der Brust gekreuzt. Spannen Sie die Bauchmuskeln an und heben Sie Ihren Oberkörper langsam und kontrolliert vom Boden ab, während Sie ausatmen. Senken Sie sich langsam und kontrolliert ab, während Sie einatmen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sit-Ups",
        videoPath="assets/videos/SitUps.mp4",
        dauer=15,
        imagePath="assets/images/SitUps.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/mS2zFc6X3TE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stärkung Bauchmuskeln: Legen Sie sich auf den Rücken auf eine Matte. Winkeln Sie Ihre Beine an, sodass ein rechter Winkel zwischen Waden und Unterschenkel entsteht. Drücken Sie Ihre Knie nun nach vorne und halten Sie mit den Bauchmuskeln/Beinen dagegen. Halten Sie die Position. Achten Sie darauf, kein Hohlkreuz zu machen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Stärkung Bauchmuskeln",
        videoPath="assets/videos/SBauchmuskeln.mp4",
        dauer=30,
        imagePath="assets/images/StaerkungBauchmuskeln.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/qlp47zcmgMo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="ISG-Dehnen rechts: Gehen Sie in den Kniestand auf einer Matte. Stellen Sie den linken Fuß nach vorne, sodass ein rechter Winkel zwischen Wade und Unterschenkel entsteht. Ihr Oberkörper ist kerzengerade. Die Blickrichtung ist gerade, und Sie fangen nun an, Ihren Oberkörper nach vorne zu schieben. Halten Sie diese Position für etwa eine Minute. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Dehnen rechts",
        videoPath="assets/videos/ISGRechts.mp4",
        dauer=60,
        imagePath="assets/images/ISGDehnenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/zEbejHx8UTo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="ISG-Dehnen links: Gehen Sie in den Kniestand auf einer Matte. Stellen Sie den rechten Fuß nach vorne, sodass ein rechter Winkel zwischen Wade und Unterschenkel entsteht. Ihr Oberkörper ist kerzengerade. Die Blickrichtung ist gerade, und Sie fangen nun an, Ihren Oberkörper nach vorne zu schieben. Halten Sie diese Position für etwa eine Minute. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Dehnen links",
        videoPath="assets/videos/ISGLinks.mp4",
        dauer=60,
        imagePath="assets/images/ISGDehnenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/jOSKrACCJlw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Hüftbeuger Dehnung rechts: Gehen Sie zunächst in den Kniestand auf einer Matte. Nehmen Sie den linken Fuß nach vorne, sodass Sie einen rechten Winkel im Knie haben. Fußgelenk und Knie sind in einer Linie. Nehmen Sie Ihre Hände nach oben und schieben Sie Ihre Hüfte nun mit geradem Rücken nach vorne. Ihre Füße bleiben am Boden. Halten Sie diese Position. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Hüftbeuger Dehnung rechts",
        videoPath="assets/videos/HueftbeugerRechts.mp4",
        dauer=30,
        imagePath="assets/images/HueftbeugerDehnenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/wiX7cNIQs_M"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Hüftbeuger Dehnung links: Gehen Sie zunächst in den Kniestand auf einer Matte. Nehmen Sie den linken Fuß nach vorne, sodass Sie einen rechten Winkel im Knie haben. Fußgelenk und Knie sind in einer Linie. Nehmen Sie Ihre Hände nach oben und schieben Sie Ihre Hüfte nun mit geradem Rücken nach vorne. Ihre Füße bleiben am Boden. Halten Sie diese Position. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Hüftbeuger Dehnung links",
        videoPath="assets/videos/HueftbeugerLinks.mp4",
        dauer=30,
        imagePath="assets/images/HueftbeugerDehnenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EbzpcQUSOtc"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Entlastung LWS/Unterer Rücken: Stellen Sie einen Stuhl an ein Ende der Matte oder positionieren Sie die Matte vor einem Sofa/niedrigem Tisch, auf dem Sie Ihre Füße ablegen können. Legen Sie sich dann mit dem Rücken auf die Matte und legen Sie Ihre Füße auf dem eben beschriebene Objekt ab. Es sollte ein rechter Winkel im Knie entstehen. Vermeiden Sie ein Hohlkreuz und entspannen Sie Ihren unteren Rücken. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Entlastung LWS/Unterer Rücken",
        videoPath="assets/videos/EntlastungLWS.mp4",
        dauer=60,
        imagePath="assets/images/EntlastungLWS.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/cwotOq8FSwU"#
        ###########################################################################################################
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Zusammenrollen: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie anschließend die Knie an und ziehen Sie sie in Richtung Kopf. Ihre Arme unterstützen das Knie zum Körper hinzuiehen, indem Sie auf die Kniee mit den Händen eine leichte Zugkraft ausüben. Ziehen Sie die Knie so nah zum Bauch, dass Sie Ihre Arme wie gezeigt zu einem Paket verschnüren können. Atmen Sie ganz ruhig und entspannt. Sollten bei dieser Übung Schmerzen entstehen, brechen Sie sie bitte sofort ab.",
        name="Zusammenrollen",
        videoPath="assets/videos/Zusammenrollen.mp4",
        dauer=30,
        imagePath="assets/images/Zusammenrollen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/_O0gn-U2hlk"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stärkung Unterer Rücken: Legen Sie sich in Bauchlage auf eine Matte. Strecken Sie Arme und Füße aus. Ihr Blick ist zum Boden gerichtet. Heben Sie abwechselnd den linken Arm, den rechten Fuß und den rechten Arm, den linken Fuß vom Boden ab. Legen Sie die Arme und die Beine während der Übung nicht ab, sondern versuchen Sie die Spannung zu halten. Achten Sie außerdem darauf, dass ihre Arme und Beine die ganze Zeit ausgestreckt sind. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Stärkung Unterer Rücken",
        videoPath="assets/videos/StaerkungURuecke.mp4",
        dauer=40,
        imagePath="assets/images/StaerkungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3B2Z01vr0N8"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kräftigung U. Rücken: Gehen Sie idealerweise auf einer Matte in den Vierfüßlerstand. Heben Sie Ihre Knie leicht vom Boden ab und stützen Sie ihr Gewicht auf den Zehenspitzen, wobei ihr Rücken gerade bleibt. Tippen Sie nun abwechselnd mit dem rechten Knie (Das Linke geht mit) auf die linke Seite, etwa auf Höhe Ihrer linken Hand und dann mit dem linken Knie (Das Rechte geht mit) etwa auf Höhe der Rechten Hand. Während dieser Bewegung sollte ein ca. 90 Grad großer Winkel Zwischen ihrem Bauch und den Oberschenkeln erhalten bleiben. Versuchen Sie, den oberen Rücken gerade zu halten, während sich Ihre Hüfte und Ihr unterer Rücken drehen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kräftigung U. Rücken",
        videoPath="assets/videos/StaerkungUNRuecken.mp4",
        dauer=60,
        imagePath="assets/images/StaerkungURuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Tt2VIMA0e6g"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung in Rückenlage: Legen Sie sich mit dem Rücken auf eine Matte. Setzen Sie Ihre Hände rechts und links neben dem Körper ab. Heben Sie nun Ihr Gesäß leicht vom Boden ab und stützen Sie sich mit den Händen oder legen Sie sie, wenn es von der Kraftanstrengung her geht am besten auf Ihrer Hüfte ab. Halten Sie diese Position für 45 Sekunden und atmen Sie ganz natürlich. Der Blick ist dabei zur Decke gerichtet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kräftigung in Rückenlage",
        videoPath="assets/videos/KraeRueckenlage.mp4",
        dauer=45,
        imagePath="assets/images/KraeftigunginRueckenlage.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/QB0LjdFCfHA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Po Brücke: Legen Sie sich mit dem Rücken auf eine Matte. Setzen Sie Ihre Hände rechts und links neben dem Körper ab. Ziehen Sie Ihre Füße an und stellen Sie sie auf dem Boden ab, sodass die Waden senkrecht zum Boden sind. Drücken Sie nun Ihren unteren Rücken nach oben, sodass nur der Schulterbereich und Ihre Füße den Boden berühren. Verschränken Sie Ihre Arme unter Ihrem Po, damit sie zusätzlich stützen können. Halten Sie die Position für etwa 40 Sekunden. Achten Sie darauf, dass Ihr Rücken und Ihr Bauch eine gerade sind und Ihr Gesäß nicht nach unten hängt, ansonsten erzielt die Übung nicht die gewünschte Wirkung. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Po Brücke",
        videoPath="assets/videos/Po-Bruecke.mp4",
        dauer=40,
        imagePath="assets/images/PoBruecke.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/pEK5XSs2qsY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kniebeugen: Stehen Sie aufrecht, die Füße schulterbreit auseinander. Strecken Sie ihre Arme zur Stabilisation gerade nach vorne aus und richten Sie ihren Blick ebenfalls nach vorne. Beugen Sie die Knie und senken Sie sich, als ob Sie sich setzen würden. Stellen Sie sicher, dass Ihre Knie nicht über Ihre Zehen hinausragen. Kehren Sie zur aufrechten Position zurück. Diese Übung stärkt den gesamten unteren Rücken sowie die Beinmuskulatur. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kniebeugen",
        videoPath="assets/videos/Kniebeugen.mp4",
        dauer=20,
        imagePath="assets/images/Kniebeugen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/qmHBoTsihoM"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Rückenstrecker auf dem Boden: Legen Sie sich auf den Bauch und strecken Sie die Arme vor den Kopf nach vorne aus. Heben Sie Arme und Beine gleichzeitig für ca. 5 Sekunden an und halten Sie diese Position. Senken Sie dann Arme und Beine ab, allerdings nur so, dass Sie den Boden nicht berühren und die Spannung erhalten bleibt. Heben Sie ihre Arme und Füße erneut an. Achten Sie darauf, dass ihr Blick in Richtung Boden ist und Arme, sowie Füße die ganze Zeit ausgestreckt sind. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Rückenstrecker auf dem Boden",
        videoPath="assets/videos/Rueckenstrecker.mp4",
        dauer=40,
        imagePath="assets/images/RueckenstreckerBoden.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/F9iyR-G_at8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Unterarmstütz: Führen Sie die Übung auf einer Matte aus. Gehen Sie nun in den Unterarmstütz, sodass sich ihr Gewicht auf die Unterarme und die Zehen verteilt. Beine, Becken und Oberkörper bilden eine Linie und der Rücken ist gerade. Wenn die Übung zu schwer fällt, können Sie sich auf den Knien abstützen aber heben Sie nicht ihr Gesäß, ansonsten verliert diese Übung ihre Wirkung. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Unterarmstütz (leichter)",
        videoPath="assets/videos/ErleichtertePlank.mp4",
        dauer=30,
        imagePath="assets/images/ErleichtertePlank.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/7-kXz-cVoDY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="ISG öffnen: Legen Sie ein eingerolltes Handtuch auf eine Matte. Legen Sie sich nun auf die Matte, sodass das Handtuch unter dem Hintern ist und mittig, zwischen den Pobacken liegt. Es sollte bis zum mittleren Rücken reichen. Halten Sie Ihren Rücken am Boden, während die Knie angewinkelt werden. Drücken Sie dann die Knie nach außen und schließen Sie sie wieder. Wiederholen Sie dies etwa 15-mal. Ihre Hände stützen seitlich ab. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="ISG öffnen",
        videoPath="assets/videos/ISG-oeffnen.mp4",
        dauer=15,
        imagePath="assets/images/ISGoefnnen.png",
        added=False,
        instruction="",
        required="Matte + Handtuch",
        onlineVidePath="https://youtu.be/Q1jS228pF5k"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="ISG-Mobilisieren: Legen Sie ein eingerolltes Handtuch auf eine Matte. Legen Sie sich nun auf die Matte, sodass das Handtuch unter dem Hintern ist und mittig zwischen den Pobacken liegt. Es sollte bis zum unteren Rücken reichen. Halten Sie Ihren Rücken am Boden. Die Knie gehen nach oben, sodass sich ein 90 Grad Winkel zwischen Wade und Unterschenkel bildet. Stellen Sie sich vor, Sie würden in der Luft ein Mini-Fahrrad fahren und bewegen Sie Ihre Füße in kurzer Sequenz vor und zurück. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Mobilisieren",
        videoPath="assets/videos/ISG-Mobilisieren.mp4",
        dauer=40,
        imagePath="assets/images/ISGMobilisieren.png",
        added=False,
        instruction="",
        required="Matte + Handtuch",
        onlineVidePath="https://youtu.be/_td9lk1GOUA"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Becken Kippen: Legen Sie sich mit dem Rücken auf eine Matte. Stellen Sie Ihre Füße so auf, dass sie Kontakt mit dem Boden haben. Legen Sie Ihre Hände auf das Becken. Spannen Sie Ihre Bauch- und Gesäßmuskeln an, sodass Ihre Lendenwirbelsäule gegen den Boden gedrückt wird, und atmen Sie dabei aus. Kommen Sie anschließend in ein leichtes Hohlkreuz und atmen Sie dabei ein. Wiederholen Sie die Bewegung. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Becken Kippen",
        videoPath="assets/videos/BeckenKippen.mp4",
        dauer=15,
        imagePath="assets/images/BeckenKippen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/LI2sTBCvLz4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisation Hüfte: Legen Sie sich mit dem Rücken auf eine Matte oder ein Bett. Ziehen Sie abwechselnd den linken und dann den rechten Fuß zum Körper, indem Sie Ihr Knie anwinkeln und Ihre Ferse dabei am Boden streifen. Achten Sie darauf, dass Ihr unterer Rücken am Boden fixiert bleibt. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Hüfte (leicht)",
        videoPath="assets/videos/MobilisationHuefteL.mp4",
        dauer=40,
        imagePath="assets/images/MobilisationHuefteLeicht.png",
        added=False,
        instruction="",
        required="Matte/Bett",
        onlineVidePath="https://youtu.be/jm6u63O9Ne0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisationsübung: Hüftkreisen Rechts: Stehen Sie auf einem Bein und halten Sie sich, wenn nötig, an einer Wand fest. Kreisen Sie das nicht am Boden stehende Bein langsam in einer großen Kreisbewegung nach vorne, dann zur Seite und dann nach hinten. Wiederholen Sie die Bewegung in die entgegengesetzte Richtung. Das kreisende Bein sollte ausgestreckt sein, und der Oberkörper möglichst gerade. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name=" Hüftkreisen Rechts",
        videoPath="assets/videos/HueftkreisenRechts.mp4",
        dauer=50,
        imagePath="assets/images/HueftkreisenRechts.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/BR8kgXuYAPk"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisationsübung: Hüftkreisen Links: Stehen Sie auf einem Bein und halten Sie sich, wenn nötig, an einer Wand fest. Kreisen Sie das nicht am Boden stehende Bein langsam in einer großen Kreisbewegung nach vorne, dann zur Seite und dann nach hinten. Wiederholen Sie die Bewegung in die entgegengesetzte Richtung. Das kreisende Bein sollte ausgestreckt sein, und der Oberkörper möglichst gerade. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Hüftkreisen Links",
        videoPath="assets/videos/HueftkreisenLinks.mp4",
        dauer=50,
        imagePath="assets/images/HueftkreisenLinks.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/s86j1yJg6PA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Leistendehnung Rechts im Liegen: Setzen Sie sich auf eine Matte. Nehmen Sie Ihren linken Fuß und richten Sie ihn so aus, dass das Schienbein parallel zur kurzen Mattenvorderseite ist und der Oberschenkel parallel zur langen Mattenseite ist. Nehmen Sie Ihren rechten Fuß nach hinten und stützen Sie sich mit einem Arm nach hinten ab. Lehnen Sie Ihren Oberkörper leicht auf die linke vordere Seite. Das hinteres Bein ist möglichst gerade, ebenso wie der Rücken. Legen Sie ihre freie Hand auf dem Knie des angewinkelten Fußes. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Leistendehnung Rechts im Liegen",
        videoPath="assets/videos/LeistendehnungR.mp4",
        dauer=110,
        imagePath="assets/images/LeistendehnungRechtsimLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/QrvfRHwwH4Q"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Leistendehnung Links im Liegen: Setzen Sie sich auf eine Matte. Nehmen Sie Ihren rechten Fuß und richten Sie ihn so aus, dass das Schienbein parallel zur kurzen Mattenvorderseite ist und der Oberschenkel parallel zur langen Mattenseite ist. Nehmen Sie Ihren linken Fuß nach hinten und stützen Sie sich mit einem Arm nach hinten ab. Lehnen Sie Ihren Oberkörper leicht auf die rechte vordere Seite. Das hinteres Bein ist möglichst gerade, ebenso wie der Rücken. Legen Sie ihre freie Hand auf dem Knie des angewinkelten Fußes. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Leistendehnung Links im Liegen",
        videoPath="assets/videos/LeistendehnungL.mp4",
        dauer=110,
        imagePath="assets/images/LeistendehnungLinksimLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/74859z3armM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Oberschenkeldehnung Links im Stehen: Stellen Sie sich an eine Wand. Stützen Sie sich ab und stellen Sie sich auf ein Bein. In diesem Fall sollten Sie auf dem rechten Bein stehen und Ihr linkes Bein anziehen. Nehmen Sie den linken Fuß in die Hand, sodass es im Oberschenkel zieht. Achten Sie darauf, dass die Kniee möglichst nah nebeneinander sind und der Rücken gerade ist. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Oberschenkeldehnung Links im Stehen",
        videoPath="assets/videos/OberschenkeldehnungL.mp4",
        dauer=50,
        imagePath="assets/images/OberschenkelL.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/zIkLYjww8Xo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Oberschenkeldehnung Rechts im Stehen: Stellen Sie sich an eine Wand. Stützen Sie sich ab und stellen Sie sich auf ein Bein. In diesem Fall sollten Sie auf dem linken Bein stehen und Ihr rechtes Bein anziehen. Nehmen Sie den rechten Fuß in die Hand, sodass es im Oberschenkel zieht. Achten Sie darauf, dass die Kniee möglichst nah nebeneinander sind und der Rücken gerade ist. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Oberschenkeldehnung Rechts im Stehen",
        videoPath="assets/videos/OberschenkeldehnungR.mp4",
        dauer=50,
        imagePath="assets/images/OberschenkelR.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/4ILbRparn4Q"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Unterschenkel links (Bei Meniskus): Legen Sie sich auf ein Bett oder eine Matte. Sie benötigen einen Gürtel. Winkeln Sie Ihr linkes Bein an und legen Sie den Gürtel so um den linken Fuß, dass Sie beide Enden in der Hand halten und den Fuß zu sich ziehen können. Heben Sie den linken Fuß nach oben, üben Sie leichten Zug über den Gürtel aus und versuchen Sie, das Knie durchzustrecken. Achten Sie darauf, dass der untere Rücken fixiert bleibt und sich kein Hohlkreuz bildet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Unterschenkel links (Bei Meniskus)",
        videoPath="assets/videos/UnterschenkelLinks.mp4",
        dauer=40,
        imagePath="assets/images/DehnungUnterschenkelLinks.png",
        added=False,
        instruction="",
        required="Gürtel +  Matte/Bett",
        onlineVidePath="https://youtu.be/_qmRLY-DSJ4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Unterschenkel rechts (Bei Meniskus): Legen Sie sich auf ein Bett oder eine Matte. Sie benötigen einen Gürtel. Winkeln Sie Ihr rechtes Bein an und legen Sie den Gürtel so um den rechten Fuß, dass Sie beide Enden in der Hand halten und den Fuß zu sich ziehen können. Heben Sie den rechten Fuß nach oben, üben Sie leichten Zug über den Gürtel aus und versuchen Sie, das Knie durchzustrecken. Achten Sie darauf, dass der untere Rücken fixiert bleibt und sich kein Hohlkreuz bildet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Unterschenkel rechts (Bei Meniskus)",
        videoPath="assets/videos/UnterschenkelRechts.mp4",
        dauer=40,
        imagePath="assets/images/DehnungUnterschenkelRechts.png",
        added=False,
        instruction="",
        required="Gürtel + Matte",
        onlineVidePath="https://youtu.be/pV3LgKXtP98"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnen: Wadenmuskulatur. Ausführung: Stehen Sie etwa einen Schritt von einer Wand entfernt. Legen Sie die Handflächen zum Stützen leicht über Kopfhöhe an die Wand. Platzieren Sie das linke Bein nach hinten und beugen Sie das vordere Bein. Drücken Sie die Ferse des hinteren Beins in Richtung Boden, um die Wade zu dehnen. Schieben Sie dann anschließend ihren Oberkörper in Richtung Wand. Achten Sie dabei auf einen geraden Rücken, ein gestrecktes hinteres Bein und darauf, dass die Verse am Boden bleibt. Halten Sie die Dehnung für 20-30 Sekunden auf beiden Seiten. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnen: Wadenmuskulatur rechts",
        videoPath="assets/videos/WadenmuskulaturRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehungWadenmuskulaturRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/ndPX0jiL-yM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnen: Wadenmuskulatur. Ausführung: Stehen Sie etwa einen Schritt von einer Wand entfernt. Legen Sie die Handflächen zum Stützen leicht über Kopfhöhe an die Wand. Platzieren Sie das rechte Bein nach hinten und beugen Sie das vordere Bein. Drücken Sie die Ferse des hinteren Beins in Richtung Boden, um die Wade zu dehnen. Schieben Sie dann anschließend ihren Oberkörper in Richtung Wand. Achten Sie dabei auf einen geraden Rücken, ein gestrecktes hinteres Bein und darauf, dass die Verse am Boden bleibt. Halten Sie die Dehnung für 20-30 Sekunden auf beiden Seiten. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnen: Wadenmuskulatur links",
        videoPath="assets/videos/WadenmuskulaturLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehungWadenmuskulaturLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/NrgkeAodF1o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Einbeinstand links: Stellen Sie sich auf Ihren linken Fuß. Achten Sie darauf, dass Ihr Knie etwas nach außen zeigt. Federn Sie Ihr linkes Bein leicht ein und versuchen Sie, nur auf dem linken Fuß zu stehen und sich auszubalancieren. Bewegen Sie Ihr freies Bein nach Möglichkeit ein wenig in alle Richtungen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Einbeinstand links",
        videoPath="assets/videos/EinbeinstandL.mp4",
        dauer=60,
        imagePath="assets/images/EinbeinstandLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/oFrGun0-R_o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kräftigung Wade: Nehmen Sie sich einen Stuhl mit Lehne. Stellen Sie sich davor und legen Sie Ihre Hände auf der Lehne ab. Gehen Sie auf die Zehenspitzen und halten Sie die Position kurz. Gehen Sie dann anschließend in die Hocke, nur soweit runter wie es geht, und halten Sie die Position. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kräftigung Waden",
        videoPath="assets/videos/KraeftigungWaden.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungWade.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/XRmHrfgaLkY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Beinheben: Legen Sie sich auf den Bauch. Heben Sie ein Bein nach oben, während Sie das Gesäß anspannen. Senken Sie das Bein langsam ab. Achten Sie darauf, dass das Bein, welches oben ist, ausgestreckt ist und so weit wie möglich nach oben geht. Der untere Rücken sollte fixiert am Boden bleiben und ein Hohlkreuz sollte vermieden werden. Führen Sie die Übung auf einer Matte aus. Führen sie insgesamt die angegebene Anzahl der Wiederholungen abwechselnd mit dem rechten und dem linken Oberschenkel aus. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Beinheben Bauchlage",
        videoPath="assets/videos/BeinhebenBauch.mp4",
        dauer=40,
        imagePath="assets/images/KraeftigungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/kn1NYZaZwo0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung: Quadrizeps Muskulatur links: Setzen Sie sich auf einen Stuhl mit aufrechtem Rücken. Heben Sie das linke gestreckte Bein an und halten Sie es für 5-10 Sekunden in der Luft. Senken Sie das Bein langsam ab. Wiederholen Sie diese Übung 10–15-mal. Stützen Sie sich bestenfalls mit ihren Händen an der Seite des Stuhles ab, um für Stabilität zu sorgen. Der Rücken, vor allem jedoch der untere Rücken sollte, falls vorhanden an der geraden Lehne des Stuhles fixiert bleiben. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Quadrizeps Muskulatur links",
        videoPath="assets/videos/QuadrizepsLinks.mp4",
        dauer=30,
        imagePath="assets/images/QuadrizeptsLinks.png",
        added=False,
        instruction="",
        required="Stuhl mit gerader Lehne",
        onlineVidePath="https://youtu.be/fKWBQrcdVkg"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung: Quadrizeps Muskulatur rechts: Setzen Sie sich auf einen Stuhl mit aufrechtem Rücken. Heben Sie das rechte gestreckte Bein an und halten Sie es für 5-10 Sekunden in der Luft. Senken Sie das Bein langsam ab. Wiederholen Sie diese Übung 10–15-mal. Stützen Sie sich bestenfalls mit ihren Händen an der Seite des Stuhles ab, um für Stabilität zu sorgen. Der Rücken, vor allem jedoch der untere Rücken sollte, falls vorhanden an der geraden Lehne des Stuhles fixiert bleiben. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Quadrizeps Muskulatur rechts",
        videoPath="assets/videos/QuadrizepsRechts.mp4",
        dauer=30,
        imagePath="assets/images/QuadrizeptsRechts.png",
        added=False,
        instruction="",
        required="Stuhl mit gerader Lehne",
        onlineVidePath="https://youtu.be/hTFWDHUh2Ps"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung Sprunggelenk rechts (Fußheben): Setzen Sie sich auf einen Stuhl. Machen Sie Ihren Rücken gerade und aufrecht und stellen Sie Ihre Füße auf dem Boden ab. Heben Sie nun Ihre rechte Fußspitze leicht an, wobei Ihre Ferse am Boden bleibt. Führen Sie die Übung langsam aus und achten Sie darauf, keine Schmerzen zu verursachen. Senken Sie Ihre Fußspitze wieder und beginnen Sie von vorne. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sprunggelenk rechts (Fußheben)",
        videoPath="assets/videos/SprunggelenkRechts.mp4",
        dauer=15,
        imagePath="assets/images/SprungelenkRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/UGN5LIz8C1A"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung Sprunggelenk links (Fußheben): Setzen Sie sich auf einen Stuhl. Machen Sie Ihren Rücken gerade und aufrecht und stellen Sie Ihre Füße auf dem Boden ab. Heben Sie nun Ihre linke Fußspitze leicht an, wobei Ihre Ferse am Boden bleibt. Führen Sie die Übung langsam aus und achten Sie darauf, keine Schmerzen zu verursachen. Senken Sie Ihre Fußspitze wieder und beginnen Sie von vorne. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sprunggelenk links (Fußheben)",
        videoPath="assets/videos/SprunggelenkLinks.mp4",
        dauer=15,
        imagePath="assets/images/SprungelenkLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/MvM0dd2occU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung Sprunggelenk links: Stellen Sie sich auf Ihr linkes Bein und legen sie gegebenenfalls ein Handtuch unter ihren Fuß. Versuchen Sie sich nicht abzustützen, da dies die Wirkung der Übung verringert. Strecken Sie Ihr rechtes Bein aus, sodass es in der Luft ist, einschließlich Ihrer Fußspitzen. Tippen Sie nun mit der Fußspitze vor sich auf den Boden und dann hinter sich. Versuchen Sie diese Bewegung auch seitwärts auszuführen, aber bleiben Sie dabei gerade und versuchen Sie, sich auszubalancieren. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab. Ist ihr Sprunggelenk aufgrund einer vor kurzem passierten Verletzung sehr instabil, stützen Sie sich bitte trotzdem ab, um ein umknicken zu vermeiden.",
        name="Kräftigung Sprunggelenk links",
        videoPath="assets/videos/KrSprunggelenkL.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungSprunggelenkLinks.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/69JU4-_mnlA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung Sprunggelenk rechts: Stellen Sie sich auf Ihr rechtes Bein und legen sie gegebenenfalls ein Handtuch unter ihren Fuß. Versuchen Sie sich nicht abzustützen, da dies die Wirkung der Übung verringert. Strecken Sie Ihr linkes Bein aus, sodass es in der Luft ist, einschließlich Ihrer Fußspitzen. Tippen Sie nun mit der Fußspitze vor sich auf den Boden und dann hinter sich. Versuchen Sie diese Bewegung auch seitwärts auszuführen, aber bleiben Sie dabei gerade und versuchen Sie, sich auszubalancieren. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab. Ist ihr Sprunggelenk aufgrund einer vor kurzem passierten Verletzung sehr instabil, stützen Sie sich bitte trotzdem ab, um ein umknicken zu vermeiden.",
        name="Kräftigung Sprunggelenk rechts",
        videoPath="assets/videos/KrSprunggelenkR.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungSprunggelenkRechts.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/kVFdDteho7I"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Knie vorne Hoch: Stellen Sie sich aufrecht hin. Schauen Sie nach vorne und ziehen Sie abwechselnd Ihr rechtes und dann Ihr linkes Knie nach oben. Das Knie sollte etwa auf Hüfthöhe gehen. Spannen Sie den Bauch dabei an. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Knie vorne Hoch",
        videoPath="assets/videos/KnieeVorneHoch.mp4",
        dauer=60,
        imagePath="assets/images/Knieevornehoch.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/1MaGukXPMiY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Nehmen Sie, wenn Ihr linkes Knie vorne ist, Ihren rechten Arm mit und umgekehrt. Führen Sie die Übung langsam aus. Beginnen Sie hiefür mit aufrechter Haltung und den Füßen schulterbreit auseinander. Machen Sie einen großen Schritt nach vorne, wobei Sie sicherstellen, dass das Knie des vorderen Beins im rechten Winkel über Ihrem Knöchel liegt. Das hintere Bein sollte ausgestreckt sein. Kehren Sie anschließend in die Ausgangsposition zurück und wiederholen Sie die Übung auf der anderen Seite. Das Knie darf nicht nach innen wegknicken, idealerweise bleibt es gerade ausgerichtet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Ausfallschritte",
        videoPath="assets/videos/Ausfallschritte.mp4",
        dauer=60,
        imagePath="assets/images/Ausfallschritte.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/rzGOuLXiFCk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kniebeugung mit Stuhl: Setzen Sie sich auf einen stabilen Stuhl. Strecken Sie Ihr linkes Bein langsam aus. Das Knie verändert seine Höhe nicht und bleibt auf seiner Ausgangsposition. Es sollte sich eine waagerechte Linie zwischen Oberschenkel und Schienbein bilden. Senken Sie den Fuß nun anschließend wieder ab. Wiederholen Sie diese Bewegung auf beiden Seiten. Insgesamt sollten sie auf die vorgeschriebene Wiederholungsanzahl kommen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kniebeugung mit Stuhl",
        videoPath="assets/videos/KniebeugungStuhl.mp4",
        dauer=30,
        imagePath="assets/images/KniebeugungmitStuhl.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/N2zp2n7fJI4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Einbeinstand links: Stellen Sie sich auf Ihren rechten Fuß. Achten Sie darauf, dass Ihr Knie etwas nach außen zeigt. Federn Sie Ihr rechtes Bein leicht ein und versuchen Sie, nur auf dem rechten Fuß zu stehen und sich auszubalancieren. Bewegen Sie Ihr freies Bein nach Möglichkeit ein wenig in alle Richtungen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Einbeinstand rechts",
        videoPath="assets/videos/EinbeinstandRechts.mp4",
        dauer=60,
        imagePath="assets/images/EinbeinstandRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/9tgYWwhyhqI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht und strecken Sie Ihren linken Arm aus, woraufhin der Arm leicht nach unten geht, sodass der Arm nun schräg nach unten zeigt. Die Handfläche zeigt nach vorne. Ihre rechte Hand geht nun unter dem linken Arm durch und greift den linken Daumen, um ihn sanft zum Körper zu ziehen. Achten Sie darauf, dass Sie nur eine leichte Dehnung spüren und den Daumen nicht zu stark zu sich ziehen.",
        name="Daumendehnung links",
        videoPath="assets/videos/DaumenDehnungLinks.mp4",
        dauer=30,
        imagePath="assets/images/DaumenDehnungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/jaheeVOXiXI"
    ),
     UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und halten Sie das Handtuch wie gezeigt vor sich. Drücken Sie nun Ihre Hände nach außen, um Spannung auf das Handtuch zu bekommen und halten Sie diese Position.",
        name="Außenrotation Schultern",
        videoPath="assets/videos/AusenrotSchultern.mp4",
        dauer=30,
        imagePath="assets/images/ausenrotSchultern.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/QcWreHBFxg4",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und greifen Sie das Handtuch wie gezeigt über sich. Drücken Sie nun Ihre Hände nach außen, um Spannung auf das Handtuch zu bekommen und lehnen Sie sich nach hinten.",
        name="Aufdehnen mit Handtuch",
        videoPath="assets/videos/AufdehnenHandtuch.mp4",
        dauer=30,
        imagePath="assets/images/aufdehnenmithandtuch.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/fPNmJ5lgqwI",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und im Ausfallschritt. Senken Sie nun das linke Knie in richtung Boden und achten Sie darauf, dass Ihr rechtes Knie sich nicht nach vorne bewegt und fixiert bleibt.",
        name="Einbeinkiebeuge rechts",
        videoPath="assets/videos/einbeinkniebeugeR.mp4",
        dauer=30,
        imagePath="assets/images/EinbeinkniebeugeR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/jOxyq5G_EYw",

    ),
     UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und im Ausfallschritt. Senken Sie nun das rechte Knie in richtung Boden und achten Sie darauf, dass Ihr linkes Knie sich nicht nach vorne bewegt und fixiert bleibt.",
        name="Einbeinkiebeuge links",
        videoPath="assets/videos/einbeinkniebeugeL.mp4",
        dauer=30,
        imagePath="assets/images/EinbeinkniebeugeL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/PYYvoqqwpws",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und nehmen Sie Ihre Hände so, als wollten Sie nach einer Stange in der Luft greifen. Ziehen Sie diese fiktive Stange aus der Luft nun mit geradem Rücken auf schulterhöhe nach unten.",
        name="Fiktive Klimmzüge",
        videoPath="assets/videos/fiktiveKlimzuege.mp4",
        dauer=30,
        imagePath="assets/images/fiktiveKlimmzuege.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Lp8ls2Wbc0o",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie die Hände wie gezeigt auf kopfhöhe überkreuz. Die Handrücken Ihrer Hände sind nach vorne gerichtet. Führen Sie anschließend eine Abwärtsbewegung mit den Händen durch, bei der sich Ihre Hände wie gezeigt drehen. ",
        name="Funktionelle Armkräftigung",
        videoPath="assets/videos/funktarmkraeftigung.mp4",
        dauer=30,
        imagePath="assets/images/funktarmkraeftigung.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/PEn-PzrGlGw",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den rechten Fuß wie gezeigt auf den linken Oberschenkel. Versuchen Sie Ihr rechtes Knie soweit wie möglich nach unten zu drücken.",
        name="Piriformisdehnung rechts",
        videoPath="assets/videos/priformisR.mp4",
        dauer=30,
        imagePath="assets/images/PiriformisR.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/n6F5P_gwv_s",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den linken Fuß wie gezeigt auf den rechten Oberschenkel. Versuchen Sie Ihr linkes Knie soweit wie möglich nach unten zu drücken.",
        name="Piriformisdehnung links",
        videoPath="assets/videos/pririformisL.mp4",
        dauer=30,
        imagePath="assets/images/PiriformisL.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/_S5BlGvFdF0",
    ),
]


uebungen_to_append00 = [1, 2, 3, 23, 48, 49, 174]
uebungen_to_append01 = [24, 25, 27, 28]
uebungen_to_append02 = [4, 5, 19, 20, 21, 22]
uebungen_to_append07 = [
    1,
    2,
    3,
    23,
    48,
    49,
    24,
    25,
    27,
    28,
    4,
    5,
    19,
    20,
    21,
    22,
    174
]

# Schultern

uebungen_to_append10 = [1, 29, 30, 31, 41, 43, 44, 45, 46, 47, 48, 49, 67, 182, 183, 190, 191, 192, 199, 201]
uebungen_to_append11 = [
    26,
    29,
    37,
    38,
    39,
    41,
    42,
    43,
    64,
    65,
    66,
    68,
    69,
    70,
    170,199
]
uebungen_to_append12 = [6, 7, 8, 9, 32, 33, 34, 35, 36, 171,]
uebungen_to_append17 = [
    6,
    7,
    8,
    9,
    32,
    33,
    34,
    35,
    36,
    26,
    29,
    37,
    38,
    39,
    41,
    42,
    43,
    64,
    65,
    66,
    68,
    69,
    70,
    1,
    29,
    30,
    31,
    41,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    67,
    170,
    171,
]

# mittlerer RÜcken
uebungen_to_append20 = [14, 117, 18, 105, 106, 107, 108, 109, 110, 179,
    180,
    181,
    182,
    183,
    184,
    186,
    187,
    188,
    189,
    190,
    191,
    194,
    195,]
uebungen_to_append21 = [38, 96, 10, 103, 196, 197, 198, 199, 200]
uebungen_to_append22 = [15, 16, 94, 95]
uebungen_to_append27 = [
    15,
    16,
    94,
    95,
    38,
    96,
    10,
    103,
    14,
    117,
    18,
    105,
    106,
    107,
    108,
    109,
    110,
]

# bauch
uebungen_to_append30 = [179, 184, 190, 191, 193]
uebungen_to_append31 = [
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
    196, 197, 199
]
uebungen_to_append32 = [
    92,
    93,
    94,
    95,
    96,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
]
uebungen_to_append37 = [
    92,
    93,
    94,
    95,
    96,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
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

# unterer Rücken
uebungen_to_append40 = [
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
    179,
    183,
    184,
    186,
    187,
    188,
    189,
    190,
    191,
    194,
    195,
]
uebungen_to_append41 = [
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
    166,198
]
uebungen_to_append42 = [
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
    149,185
]
uebungen_to_append47 = [
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

# Beine
uebungen_to_append50 = [40, 67, 104, 156, 158, 161, 162, 163, 164, 165]
uebungen_to_append51 = [
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
    172, 173
]
uebungen_to_append52 = [148, 149, 150, 151, 152, 153, 154, 155, 166, 168, 176, 177]
uebungen_to_append57 = [
    148,
    149,
    150,
    151,
    152,
    153,
    154,
    155,
    166,
    168,
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
    40,
    67,
    104,
    156,
    158,
    161,
    162,
    163,
    164,
    165,
    172,
    173, 176, 177
]

# Arme

uebungen_to_append60 = [
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
    183, 184
]

uebungen_to_append61 = [64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,175]
uebungen_to_append62 = [
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    62,
    63,
    169,
]
uebungen_to_append67 = [
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
    64,
    65,
    66,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    62,
    63,
    169,
    175

]


@receiver(post_save, sender=User)  # gets executed, if a new user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        if instance.is_superuser:
         for i in uebungen:
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
                    onlineVideoPath = i.onlineVidePath

                )
        inizialize_first_second()



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


def inizialize_first_second():
    for i in uebungen_to_append00:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 0))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append01:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 0))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append02:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 0))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append07:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append10:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 1))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append11:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 1))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append12:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 1))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append17:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 1))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append20:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 2))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append21:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 2))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append22:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 2))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append27:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 2))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append30:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 3))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append31:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 3))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append32:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 3))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append37:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 3))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append40:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 4))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append41:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 4))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append42:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 4))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append47:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 4))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append50:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 5))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append51:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 5))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append52:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 5))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append57:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 5))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
    for i in uebungen_to_append60:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 6))
        instance_exercise.second.add(models.Second.objects.create(second = 0))
        instance_exercise.save()
    for i in uebungen_to_append61:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 6))
        instance_exercise.second.add(models.Second.objects.create(second = 1))
        instance_exercise.save()
    for i in uebungen_to_append62:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 6))
        instance_exercise.second.add(models.Second.objects.create(second = 2))
        instance_exercise.save()
    for i in uebungen_to_append67:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first = 6))
        instance_exercise.second.add(models.Second.objects.create(second = 7))
        instance_exercise.save()
