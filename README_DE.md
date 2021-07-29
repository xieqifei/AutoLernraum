# AutoLernraum

Das Programm wird zur Buchung eines Lernraums an RWTH eingesetzt. 

## Anleitung zum Gebrauch

1. Installieren Python 3.x
2. Installieren Chrome Browser von aketueller Version
3. Herunterladen das Programm aus Github in Ihren Computer. Und dekomprimieren es
4. Edieren die Datei `test_selenium.py`, und verändern die folgenden Info.

```python
buchung = {'time': '08.00 - 16.30', 'kursnr': '08411027','info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Nunil', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}
```

> kursnr:Lernraum Nummer, welches Sie buchen möchten. Beispiel: 08411027 für Semi90.  Die Nummer finden Sie einfache in folgender Site. https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
>
> time: Zeitraum von Betrieb des Lernruams.  Dessen Form muss gleich wie 08.00 - 16.30 sein.
>
> email:email, in welche wird die Beschäftigung abgeschikt.
>
> sex: M für mannlich. W für Weiblich
>
> vorname:Vorname
>
> name:Name
>
> strasse:Strasse und Nummer
>
> ort:PLZ und Stadt. Beispiel:52076 Aachen
>
> matnr:sechsstellige matikelnummer
>
> telefon:Telefon Nummer
>
> Status, Ort von Lernraum und username bleiben Sie bitte wie vor. 

5. Speichern die Veränderung und führen `test_selenium.py` aus.  Zum Beispiel, ich will einen Lernraum in Bib 1 buchen, welcher um 8 Uhr öffnet, dann kann ich vor 7:59 das Programm ausführen.

## Zum Schluss

Wenn Sie an dem Programm interessieren, können Sie die Datei `/myclass/lernraum.py` lesen, wo  die kritische Code steht.  Das Programm wird irregulär erneuert werden. Falls es funktioniert nicht mehr, dann herunterladen das Neue.