
# Dokumentacja do rozwiązania zadania

![python]
![django]
![JWT]
[![license]][license-url]

## Spis Treści

- [Treść zadania](#treść-zadania)
- [Podjęte decyzje](#podjęte-decyzje)
- [Opis API](#opis-api)
    * [Tablica wszystkich URL](#tablica-wszystkich-url)
    * [Uwierzytelnianie](#uwierzytelnianie)
    * [Widok wiadomości](#widok-wiadomości)
    * [Widok tworzenia wiadomości](#widok-tworzenia-wiadomości)
    * [Widok edycji wiadomości](#widok-edycji-wiadomości)
    * [Widok kasowania wiadomości](#widok-kasowania-wiadomości)
- [Testy jednostkowe](#testy-jednostkowe)
- [Rozmieszczenie aplikacji](#rozmieszczenie-aplikacji)
- [Podziękowanie](#dziękuję-bardzo-za-uwagę-i-czekam-na-zwrotną-informację)

---

## Treść zadania

Zadaniem jest zaprojektowanie API i wykonanie aplikacji do zapisywania, zwracania
zapisanych oraz edycji krótkich tekstów (do 160 znaków).

---

## Podjęte decyzje

* Wybrany framework: [Django Rest Framework][drf-url] (dalej DRF)
* Zapisywanie wiadomości odbywa się w bazie danych SQLite (dalej BD) za pomocą Django ORM
* Odczytywanie wiadomości odbywa się za pomocą tzw. serializatorów, 
   które konwertują dane z BD do Python'owych typów i odwrotnie
* Licznik wyświetleń wiadomości jest zaimplementowany jako atrybut w BD.

---

## Opis API

> Uwaga: wszystkie punkty końcowe są wyświetlone w skróconym wariancie, 
> w razie ręcznego wpisana linku, jako przedrostek musi być [wiadomosci-api.herokuapp.com][deploy-url] <br/>
> Aby się nie pomylić ze wpisywaniem linku, zachęcam do korzystania z hiperłączy poniżej,
> które domyślnie prowadzą na zapytanie GET w postaci graficznego interfejsu,
> który udostępnia DRF.

#### Struktura opisu API

* Na początku jest podana tablica z ogólnym opisem URL.
* Następnie jest opis każdego widoku.

---

### Tablica wszystkich URL

| Punkt końcowy            |             GET             |            POST           |            PUT            |       DELETE       |
|--------------------------|:---------------------------:|:-------------------------:|:-------------------------:|:------------------:|
| [/api/][api-url]         |    Dostać punkty końcowe    |            N/A            |            N/A            |         N/A        |
| [/api/smses/][smses-url] | Dostać wszystkie wiadomości |  Utworzyć nową wiadomość  |            N/A            |         N/A        |
| [/api/smses/\<id>/][sms] |   Znaleźć wiadomość po ID   |            N/A            | Nadpisać treść wiadomości | Skasować wiadomość |
| [/api/token/][token]     |             N/A             |    Uwierzytelnianie JWT   |            N/A            |         N/A        |
| [/api/token/refresh/][r] |             N/A             | Dostać nowy token dostępu |            N/A            |         N/A        |
| [/api-auth/login][in]    |             N/A             |   Uwierzytelnianie sesji  |            N/A            |         N/A        |

---

### Uwierzytelnianie

> Do przetestowania aplikacji podaję do dyspozycji dwa konta: <br/>
> username: ```Jan``` password: ```nowakhaslo``` <br/>
> username: ```Zofia``` password: ```nowakhaslo```

Zaimplementowane rodzaje uwierzytelniania:

1. Oparte na sesji:
    * Dodane jako gotowe rozwiązanie w DRF
    * Pozwala na szybkie i wygodne logowanie się w interfejsie (zachęcana metoda do skorzystania z aplikacji)
    * URL logowania: [/api-auth/login][in]
    
<p align="center">
  <img src="https://imgur.com/9i5UKAH.png" />
</p>

2. Oparte na tokenach (JWT)
    * Dodane jako dodatkowa funkcjonalność, 
      ponieważ dodanie uwierzytelniania przez sesję nie zajęło dużego wysiłku :)
    * Dla logowania się, aby dostać token dostępu i odświeżania należy wysłać zapytanie
      POST na [/api/token/][token] z JSON-em:
        ```json
        {
            "username": "*username*",
            "password": "*password*"
        }
        ```
      zatem jako odpowiedź dostaniemy parę tokenów (kluczy):
        ```json
        {
            "refresh": "*długi napis, token odświeżania*",
            "access": "*długi napis, token dostępu*"
        }
        ```
      
      ![jwt-token1] ![jwt-token2]
      
      Należy zachować te klucze, zatem przy kolejnym zapytaniu, które wymaga uwierzytelniania,
      koniecznie trzeba umieścić token dostępu w nagłówku HTTP jako:
        ```
        Authorization: "Bearer <token dostępu>"
        ```
      Token dostępu ma dość krótki czas istnienia, zatem, aby dostać nowy token dostępu,
      należy wykorzystać token odświeżania, który ma znacznie dłuższy czas życia. 
    * Dla ponowienia tokena dostępu należy wysłać zapytanie POST na [/api/token/refresh/][r]
      z JSON-em:
        ```json
        {
            "refresh": "*długi napis, otrzymany wcześniej token odświeżania*"
        }
        ```
      w wyniku dostaniemy nowy token dostępu w postaci tego samego JSON-a:
        ```json
        {
            "access": "*długi napis, nowy token dostępu*"
        }
        ```
      ![refresh1] ![refresh2]
    * W wypadku wygaśnięcia tokena odświeżania należy ponownie zalogować się tak jak opisane
      powyżej, aby dostać nową parę tokenów.

---

### Widok wiadomości

Są dwa widoki dla wiadomości:
1. Widok dla przeglądu wszystkich wiadomości, zaimplementowano jako dodatkowa
   funkcjonalność dla kompletności rozwiązania. Należy wysłać zapytanie GET na [/api/smses/][smses-url] <br/>
   Odpowiedzią będzie JSON ze wszystkimi wiadomościami wraz z ich ID i autorem:
```json
[
    {
        "id": 1,
        "author": "Vadym",
        "message": "Nowa wiadomość",
        "views_count": 1
    },
    "..."
]
```
<p align="center">
  <img src="https://imgur.com/VPqAq0c.png" />
</p>

2. Widok dla przeglądu specyficznej wiadomości. Należy wysłać zapytanie GET na [/api/smses/\<id>/][sms],
gdzie '\<id>' jest wartością ID dla specyficznej wiadomości. <br/>
Odpowiedzią będzie JSON z konkretną wiadomością razem z licznikiem wyświetleń:
```json
{
    "message": "Nowa wiadomość",
    "views_count": 2
}
```
<p align="center">
  <img src="https://imgur.com/wnf1UkY.png" />
</p>

---

### Widok tworzenia wiadomości

Aby utworzyć nową wiadomość, należy być zalogowanym, aby zatem wysłać uwierzytelnione zapytanie POST na [/api/smses/][smses-url] z JSON-em:
```json
{
    "message": "Najnowsza wiadomość"
}
```
Jako odpowiedź dostaniemy status HTTP 201 CREATED.
![create1] ![create2]

---

### Widok edycji wiadomości

Aby zmienić treść wiadomości, tylko autor może wysłać uwierzytelnione zapytanie PUT na [/api/smses/\<id>/][sms] z JSON-em:
```json
{
    "message": "Edytowana wiadomość"
}
```
Jako odpowiedź dostaniemy JSON z nową wiadomością:
```json
{
    "message": "Edytowana wiadomość",
    "views_count": 0
}
```

![edit1] ![edit2]

---

### Widok kasowania wiadomości

Aby skasować wiadomość, tylko autor może wysłać uwierzytelnione zapytanie DELETE na [/api/smses/\<id>/][sms] <br/>
Jako odpowiedź dostaniemy status HTTP 200 OK

![delete]

---

### Testy jednostkowe

Napisałem 23 testy jednostkowe, pokrywające model wiadomości oraz wszystkie
punkty końcowe (przy użyciu pakietu coverage). Uwzględniłem testowanie uwierzytelniania oraz wyzerowanie licznika wyświetleń 
po nadpisaniu treści wiadomości.

[kliknij, aby przejść do folderu z testami][tests-url]

---

### Rozmieszczenie aplikacji

Jak można zrozumieć z URL, aplikacja była rozmieszczona na heroku. <br/>
Niestety czasami długo się ładuje strona, ale mam nadzieje, że to nie wpłynęło
na ogólne wrażenie rozwiązania zadania.

---

### Dziękuję bardzo za uwagę i czekam na zwrotną informację!

---

> Gmail [vmariiechko@gmail.com](mailto:vmariiechko@gmail.com) &nbsp;&middot;&nbsp;
> GitHub [@vmariiechko](https://github.com/vmariiechko) &nbsp;&middot;&nbsp;
> LinkedIn [@mariiechko](https://www.linkedin.com/in/mariiechko/)

<!-- Markdown links and images -->
[python]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[JWT]: https://img.shields.io/badge/JWT-%23d6d6d6?logo=JSON-Web-Tokens&logoColor=black&style=for-the-badge
[license]: https://img.shields.io/badge/license-MIT-%2341CD52.svg?&style=for-the-badge

[drf-url]: https://www.django-rest-framework.org/
[deploy-url]: https://wiadomosci-api.herokuapp.com/
[api-url]: https://wiadomosci-api.herokuapp.com/api/
[smses-url]: https://wiadomosci-api.herokuapp.com/api/smses/
[sms]: https://wiadomosci-api.herokuapp.com/api/smses/1/
[token]: https://wiadomosci-api.herokuapp.com/api/token/
[r]: https://wiadomosci-api.herokuapp.com/api/token/refresh/
[in]: https://wiadomosci-api.herokuapp.com/api-auth/login/
[tests-url]: https://github.com/vmariiechko/internship-assignment/tree/main/api/tests
[license-url]: https://github.com/vmariiechko/internship-assignment/blob/main/LICENSE

[drf-login]: https://imgur.com/9i5UKAH.png
[jwt-token1]: https://imgur.com/ft1xtM7.png
[jwt-token2]: https://imgur.com/eTOyIdx.png
[refresh1]: https://imgur.com/GtyTAk2.png
[refresh2]: https://imgur.com/BqyhdFN.png
[smses]: https://imgur.com/VPqAq0c.png
[sms]: https://imgur.com/wnf1UkY.png
[create1]: https://imgur.com/EeMs5XJ.png
[create2]: https://imgur.com/28X5lUV.png
[edit1]: https://imgur.com/DqJ8UGV.png
[edit2]: https://imgur.com/UvhVM6i.png
[delete]: https://imgur.com/sCREpre.png