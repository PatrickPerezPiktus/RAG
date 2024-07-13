from core.rag import query
import config
 

def test1():
    assert validate(
        question="Wie kann ich einen Vertrag kündigen?",
        expected="Sie können Ihren Vertrag bei beitragspflichtigen Versicherungen jederzeit zum Schluss der laufenden Versicherungsperiode kündigen. Bei beitragsfreien Versicherungen können Sie den Vertrag zu jedem Monatsende in Textform (z. B. Brief, Fax, E-Mail) kündigen. Eine Kündigung nach Rentenbeginn ist jedoch nicht möglich.",
    )


def validate(question: str, expected: str):
    response = query(question)
    prompt = config.testPrompt.format(
        expected=expected, actual=response
    )

    model = config.model
    result = model.invoke(prompt)
    result = result.strip().lower()

    print(prompt)

    if "true" in result:
        print("\033[92m" + f"Response: {result}" + "\033[0m")
        return True
    elif "false" in result:
        print("\033[91m" + f"Response: {result}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
