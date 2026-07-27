class PromptInjectionDetector:


    PATTERNS = [

        "ignore previous instructions",

        "ignore all instructions",

        "system prompt",

        "developer message",

        "reveal your prompt",

        "show hidden instructions",

        "jailbreak",

        "bypass safety",

    ]


    def detect(
        self,
        text: str,
    ) -> bool:


        normalized = (
            text
            .lower()
        )


        for pattern in self.PATTERNS:

            if pattern in normalized:

                return True


        return False