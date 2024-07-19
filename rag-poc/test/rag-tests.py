from core import rag
import config
 

def testVierGewinnt():
    assert validate(
        question="Wie gewinne ich vier gewinnt?",
        expected="Um bei Vier Gewinnt zu gewinnen, musst du als erster Spieler vier Spielchips in einer Reihe platzieren.",
    )
    
def testCatan():
    assert validate(
        question="Wie gewinne ich Catan?",
        expected="Um Catan zu gewinnen, musst du als erster Spieler 10 Siegpunkte erreichen. Du kannst Siegpunkte erhalten, indem du neue Straßen und Siedlungen baust und Siedlungen zu Städten erweiterst.",
    )


def testMonopolyGefängnis():
    assert validate(
        question="Wie komme ich bei Monopoly aus dem Gefängnis",
        expected="1. Du kannst am Anfang deines nächsten Zuges eine 'Du kommst aus dem Gefängnis frei'-Karte spielen, entweder indem du sie bereits besitzt oder indem du sie von einem anderen Spieler kaufst. Dann würfelst du und ziehst normal weiter. 2. Wenn du im nächsten Zug einen Pasch würfelst, kommst du sofort frei und ziehst aus dem Gefängnis heraus. Dein Zug ist dann beendet. 3. Du hast insgesamt drei Runden lang die Möglichkeit, einen Pasch zu würfeln und dich so freizukaufen. Wenn du nach drei Runden keinen Pasch würfelst, kannst du dich für 50 Einheiten freikaufen und mit deinem letzten Wurf aus dem Gefängnis herausziehen.",
    )

def testFalse():
    assert False == validate(
        question="Wie gewinne ich in Risiko",
        expected="Wenn du vier Spielchips in einer Reihe platzierst hast du gewonnen",
    )


def validate(question: str, expected: str):
    response = rag.querySimple(question, [])
    
    response = response['response']
    prompt = config.testPrompt.format(
        expected=expected, actual=response
    )

    model = config.getLLM()
    result = model.invoke(prompt)

    if "true" in result.content:
        return True
    elif "false" in result.content:
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false': {result}"
        )
