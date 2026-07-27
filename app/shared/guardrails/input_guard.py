from app.shared.guardrails.injection_detector import (
    PromptInjectionDetector,
)


class InputGuard:


    def __init__(self):

        self.injection_detector = (
            PromptInjectionDetector()
        )



    def validate(
        self,
        question: str,
    ):


        if not question.strip():

            raise ValueError(
                "Question cannot be empty"
            )


        if len(question) > 4000:

            raise ValueError(
                "Question too long"
            )


        if self.injection_detector.detect(
            question
        ):

            raise ValueError(
                "Potential prompt injection detected"
            )


        return True