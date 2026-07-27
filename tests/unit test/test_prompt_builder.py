from app.knowledge.chat.prompt_builder import (
    PromptBuilder,
)



def test_prompt_contains_context():

    builder = PromptBuilder()


    contexts = [

        {
            "content": (
                "Company provides 20 leave days."
            ),

            "metadata": {
                "filename": "policy.pdf",
                "chunk_index": 1,
            },
        }

    ]


    messages = builder.build(

        question="How many leaves?",

        contexts=contexts,

        history=[],

    )


    system_content = str(
        messages[0].get(
            "content"
        )
    )


    assert (
        "Company provides 20 leave days."
        in system_content
    )


    assert (
        "policy.pdf"
        in system_content
    )



def test_prompt_contains_question():

    builder = PromptBuilder()


    messages = builder.build(

        question="What is security policy?",

        contexts=[],

        history=[],

    )


    user_message = messages[1]


    content = str(
        user_message.get(
            "content"
        )
    )


    assert (
        content
        ==
        "What is security policy?"
    )



def test_prompt_with_history():

    builder = PromptBuilder()


    history = [

        {
            "role": "user",
            "content": "Previous question",
        },

        {
            "role": "assistant",
            "content": "Previous answer",
        },

    ]


    messages = builder.build(

        question="New question",

        contexts=[],

        history=history,

    )


    system_content = str(
        messages[0].get(
            "content"
        )
    )


    assert (
        "Previous question"
        in system_content
    )


    assert (
        "Previous answer"
        in system_content
    )