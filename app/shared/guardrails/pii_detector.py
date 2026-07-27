import re


class PIIDetector:


    PATTERNS = {

        "email":
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",


        "phone":
        r"\b\d{10}\b",


        "aadhaar":
        r"\b\d{4}\s\d{4}\s\d{4}\b",

    }



    def detect(
        self,
        text: str,
    ) -> dict:


        findings = {}


        for name, pattern in self.PATTERNS.items():

            matches = re.findall(
                pattern,
                text,
            )


            if matches:

                findings[name] = matches


        return findings