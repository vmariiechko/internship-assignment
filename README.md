
# Dokumentacja do rozwiązania zadania

![python]
![django]
![JWT]
[![license]][license-url]

## Spis Treści

- [Treść zadania](#treść-zadania)
- [Podjęte decyzje](#podjęte-decyzje)
- [Opis API](#opis-api)
    * [Tablica wszystkich URLi](#tablica-wszystkich-url)
    * [Uwierzytelnianie](#uwierzytelnianie)
    * [Widok wiadomości](#widok-wiadomości)
    * [Widok tworzenia wiadomości](#widok-tworzenia-wiadomości)
    * [Widok edycji wiadomości](#widok-edycji-wiadomości)
    * [Widok kasowania wiadomości](#widok-kasowania-wiadomości)
- [Testy jednostkowe](#testy-jednostkowe)
- [Rozmieszczenie aplikacji](#rozmieszczenie-aplikacji)

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
> w razie ręcznego wpisana linku, jako przedrostek musi być *link*. <br/>
> Aby się nie pomylić ze wpisywaniem linku, zachęcam do korzystania z hiperłączy poniżej,
> które domyślnie prowadzą na zapytanie GET w postaci graficznego interfejsu,
> który udostępnia DRF

#### Struktura opisu API

* Na początku jest podana tablica z ogólnym opisem URL
* Następnie jest opis każdego widoku

---

### Tablica wszystkich URL

| Punkt końcowy       |             GET             |            POST           |            PUT            |       DELETE       |
|---------------------|:---------------------------:|:-------------------------:|:-------------------------:|:------------------:|
| [/api/][/api/-url]  |    Dostać punkty końcowe    |            N/A            |            N/A            |         N/A        |
| /api/smses/         | Dostać wszystkie wiadomości |  Utworzyć nową wiadomość  |            N/A            |         N/A        |
| /api/smses/\<id>/   |   Znaleźć wiadomość po ID   |            N/A            | Nadpisać treść wiadomości | Skasować wiadomość |
| /api/token/         |             N/A             |    Uwierzytelnianie JWT   |            N/A            |         N/A        |
| /api/token/refresh/ |             N/A             | Dostać nowy token dostępu |            N/A            |         N/A        |
| /api-auth/          |             N/A             |   Uwierzytelnianie sesji  |            N/A            |         N/A        |


<p align="center">
  <img src="" />
</p>

---

### Uwierzytelnianie

Zaimplementowane rodzaje uwierzytelniania:

1. Oparte na sesji:
    * Dodane jako gotowe rozwiązanie w DRF
    * Pozwala na szybkie i wygodne logowanie się w interfejsie (zachęcana metoda do skorzystania z aplikacji)
    * URL: 
    * *Photo*

2. Oparte na tokenach (JWT)
    * Dodane jako dodatkowa funkcjonalność, 
      ponieważ dodanie uwierzytelniania przez sesję nie zajęło dużego wysiłku :)
    * Dla logowania się, aby dostać token dostępu i odświeżania należy wysłać zapytanie
      POST na /api/token/ z JSON-em:
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
      Należy zachować te klucze, zatem przy kolejnym zapytaniu, które wymaga uwierzytelniania,
      koniecznie trzeba umieścić token dostępu w nagłówku HTTP jako:
        ```
        Authorization: "Bearer <token dostępu>"
        ```
      Token dostępu ma dość krótki czas istnienia, zatem, aby dostać nowy token dostępu,
      należy wykorzystać token odświeżania, który ma znacznie dłuższy czas życia. 
    * Dla ponowienia tokena dostępu należy wysłać zapytanie POST na /api/token/refresh/
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
    * W wypadku wygaśnięcia tokena odświeżania należy ponownie zalogować się tak jak opisane
      powyżej, aby dostać nową parę tokenów.

---

### Widok wiadomości

Są dwa widoki dla wiadomości:
1. Widok dla przeglądu wszystkich wiadomości, zaimplementowano jako dodatkowa
   funkcjonalność dla kompletności rozwiązania. Należy wysłać zapytanie GET na /api/smses/. <br/>
   Odpowiedzią będzie JSON ze wszystkimi wiadomościami wraz z ich ID i autorem:
```json
[
    {
        "id": 1,
        "author": "Vadym",
        "message": "Nowa wiadomość",
        "views_count": 1
    },
    ...
]
```
Photo

2. Widok dla przeglądu specyficznej wiadomości. Należy wysłać zapytanie GET na /api/smses/\<id>/,
gdzie '\<id>' jest wartością ID dla specyficznej wiadomości. <br/>
Odpowiedzią będzie JSON z konkretną wiadomością razem z licznikiem wyświetleń:
```json
{
    "message": "Nowa wiadomość",
    "views_count": 2
}
```

---

### Widok tworzenia wiadomości

Aby utworzyć nową wiadomość, należy wysłać uwierzytelnione zapytanie POST na /api/smses/ z JSON-em:
```json
{
    "message": "Najnowsza wiadomość"
}
```
Jako odpowiedź dostaniemy status HTTP 201 CREATED

---

### Widok edycji wiadomości

Aby zmienić treść wiadomości, tylko autor może wysłać uwierzytelnione zapytanie PUT na /api/smses/\<id>/ z JSON-em:
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

---

### Widok kasowania wiadomości

Aby skasować wiadomość, tylko autor może wysłać uwierzytelnione zapytanie DELETE na /api/smses/\<id>/
Jako odpowiedź dostaniemy status HTTP 200 OK

---

### Testy jednostkowe

Napisałem 23 testy jednostkowe, pokrywające model wiadomości oraz wszystkie
punkty końcowe (przy użyciu pakietu coverage). Uwzględniłem testowanie uwierzytelniania oraz wyzerowanie licznika wyświetleń 
po nadpisaniu treści wiadomości, [kliknij, aby przejść do folderu z testami](*link do folderu z 
testami przez url jak w messendrze*)

---

### Rozmieszczenie aplikacji

> (deploy)

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
[/api/-url]: https://www.django-rest-framework.org/
[license-url]: https://github.com/vmariiechko/internship-assignment/blob/main/LICENSE


[api-root]: https://imgur.com/i0677Lt.png