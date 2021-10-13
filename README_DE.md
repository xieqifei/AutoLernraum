# AutoLernraum

Das Programm wird zur Buchung eines Lernraums an RWTH eingesetzt. 

## Anleitung zum Gebrauch

1. Installieren Python 3.x
2. Installieren Chrome Browser von aketueller Version
3. Herunterladen das Programm aus Github in Ihren Computer. Und dekomprimieren es
4. Edieren die Datei `random_test.py`, und verändern die folgenden Info.email,sex,vorname,name,strasse,ort,matnr,telefon.

```python
buchung = {'info': {'id': 0, 'username': 'suiyi', 'email': 'example@email.com', 'sex': 'M', 'vorname': 'Feieie', 'name': 'Xu', 'strasse': 'Ponttorstr.1','ort': '52074  Aachen', 'status': 'S-RWTH', 'matnr': '404093', 'telefon': '00491799860915'}, 
'id': 0, 'username': 'suiyi', 'ort': 'suiyi', 'kursnr': '08511007'}
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

5. switch = 1=>buchen. switch = 0 =>nicht buchen.

```python
lernraumList = [
    {'switch': 1, 'ort': 'Bib1', 'kursnr': "08511007", 'time': '08:00-14:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611004", 'time': '08:00-14:00'},

    {'switch': 0, 'ort': 'Bib1', 'kursnr': "08511008", 'time': '14:00-20:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611005", 'time': '14:00-20:00'}
]
```

5. Speichern die Veränderung und führen `random_test.py` aus.  

Test Enviroment: Windows

