import os
import logging

os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GLOG_minloglevel"] = "2"

from google import genai

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Please set GEMINI_API_KEY environment variable")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def _finance_news_prompt(self, text: str) -> str:
        '''
        Builds a structured prompt for summarizing general or financial news.

        Prompt engineering principles applied:
        - Role assignment
        - Explicit tasks
        - Output formatting constraints
        - Few-shot guidance (example format)
        - Error handling instructions
        '''
        return f'''
                You are a highly skilled **Financial News Expert**.

                ### Objective
                Analyze the given news article and produce a **structured digest**.

                ### Tasks
                1. Summarize the news into **exactly 15 concise bullet points**.
                2. Provide the **overall sentiment** of the news (choose one: Positive, Negative, Neutral).
                3. List **strong stock recommendations** if explicitly supported by the article, otherwise return **"None"**.

                ### Output Requirements
                - Do not add explanations outside the required format.
                - Keep bullet points short and fact-focused.
                - Ensure there are **exactly 20 points** (no more, no less).
                - Use plain text only (no markdown beyond what is shown).
                - If information is missing, state "Not Mentioned" instead of inventing content.

                ### Example Format
                15-Point Digest:
                1. First key fact.
                2. Second key fact.
                ...
                15. Fifteenth key fact.

                Overall Sentiment: <Positive | Negative | Neutral>

                Stock Recommendations: <List of Stocks or "None">

                ### IMPORANT NOTE: PLEASE DONT HALLUCINATE!!

                ### News Text
                \"\"\"{text}\"\"\"
                '''

    def _general_news_prompt(self, text: str) -> str:
        
            '''
            Builds a structured prompt for summarizing general news.

            Prompt engineering principles applied:
            - Role assignment
            - Explicit tasks
            - Output formatting constraints
            - Few-shot guidance (example format)
            - Error handling instructions
            '''
            return f"""
                    You are a highly skilled **News Analyst**.
                    ### Objective
                    Analyze the given news article and produce a **structured digest**.

                    ### Tasks
                    1. Summarize the news into **exactly 15 concise bullet points**.
                    2. Provide the **overall sentiment** of the news (choose one: Positive, Negative, Neutral).
                    3. Identify the **main theme or category** of the news (choose one: Politics, Technology, Health, Entertainment, Science, Sports, Other).

                    ### Output Requirements
                    - Do not add explanations outside the required format.
                    - Keep bullet points short and fact-focused.
                    - Ensure there are **exactly 15 points** (no more, no less).
                    - Use plain text only (no markdown beyond what is shown).
                    - If information is missing, state "Not Mentioned" instead of inventing content.

                    ### Example Format
                    15-Point Digest:
                    1. First key fact.
                    2. Second key fact.
                    ...
                    15. Fifteenth key fact.

                    Overall Sentiment: <Positive | Negative | Neutral>

                    Main Theme: <Politics | Technology | Health | Entertainment | Science | Sports | Other>

                    ### IMPORANT NOTE: PLEASE DONT HALLUCINATE!!
                    
                    ### News Text
                    \"\"\"{text}\"\"\"
                    """
    
    def classify(self, text: str, financial: bool = False) -> str:
        prompt = self._finance_news_prompt(text) if financial else self._general_news_prompt(text)

        try:
            response = self.client.models.generate_content(model=self.model_name,
                                                           contents=prompt)
            category = response.text.strip()
            return category
        except Exception as e:
            logging.error(f"Classification failed: {e}")
            return "Error"


if __name__ == "__main__":
    classifer = GeminiClient()
    sample_text = "Apple shares surged after the company reported record quarterly earnings."
    print(classifer.classify(sample_text, financial=True))
