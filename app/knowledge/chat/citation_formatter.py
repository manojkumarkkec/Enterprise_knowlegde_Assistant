class CitationFormatter:


    def format(
        self,
        answer: str,
        sources: list[dict],
    ) -> str:


        citation_text = "\n\nSources:\n"


        for index, source in enumerate(
            sources,
            start=1,
        ):

            citation_text += (
                f"[{index}] "
                f"{source['filename']} "
                f"(chunk {source['chunk_index']})\n"
            )


        return answer + citation_text