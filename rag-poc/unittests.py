import config
from rag import query


def testMonopoly():
    assert validate(
        question="How much total money does a player start with in Monopoly? (Answer with the number only)",
        expected="$1500",
    )


def testTicketToRide():
    assert validate(
        question="How many points does the longest continuous train get in Ticket to Ride? (Answer with the number only)",
        expected="10 points",
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
