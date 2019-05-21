# Hangman API

Python implementation of Hangman API.

API specification and inspiration 'borrowed' from [despo](https://github.com/despo/hangman/)


### Create new hangman game

#### Request

```
POST /hangman
```

#### Response

```
{ hangman: hangman_string, token: game token }
```

### Guess a letter

#### Request

```
PUT /hangman { token: game token, letter: guess }
```

#### Response

```
{ hangman: hangman_string, token: game token, correct: true|false }
```

When the letter has already been used

```
status 304
```

### Get solution

#### Request

```
GET /hangman { token: game token }
```
#### Response
```
{ solution: game solution, token: game token }
```

