import re


class OutputGuard:


    def __init__(self):

        pass



    def sanitize(
        self,
        text: str,
    ) -> str:


        # Mask emails

        text = re.sub(

            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

            "[EMAIL_REMOVED]",

            text,

        )


        # Mask phone numbers

        text = re.sub(

            r"\b\d{10}\b",

            "[PHONE_REMOVED]",

            text,

        )


        return text