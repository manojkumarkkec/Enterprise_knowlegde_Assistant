class HallucinationEvaluator:


    def evaluate(
        self,
        answer:str,
        contexts:list[str],
    ):


        context_text = (
            " ".join(contexts)
            .lower()
        )


        answer_words = (
            answer
            .lower()
            .split()
        )


        unsupported = [
            word
            for word in answer_words
            if word not in context_text
        ]


        score = (
            len(unsupported)
            /
            len(answer_words)
        )


        return {

            "hallucination_score":
            round(score,3)

        }