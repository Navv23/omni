from omni.core.crawler import GoogleNewsCrawler
from omni.core.classifier import GeminiClient
from omni.io.mailer import Mailer
import logging

class OmniNewsService:
    def __init__(self, search: str, time_period: str, financial: bool, recipient: str):
        self.search = search
        self.time_period = time_period
        self.financial = financial
        self.recipient = recipient

        self.crawler = GoogleNewsCrawler()
        self.gemini = GeminiClient()
        self.mailer = Mailer()

    def run(self):
        # Step 1: Crawl news
        articles = self.crawler.run(search=self.search,
                                    time_period=self.time_period,
                                    financial_flag=self.financial)

        if not articles:
            print("No news articles found.")
            return False

        print(f"\nFetched {len(articles)} Articles")

        all_articles = []
        # Step 2: Classify
        for article, _ in articles:
            all_articles.append(article)
        
        if not all_articles:
            print("No news articles found.")
            return False

        articles_text = ' '.join(all_articles)

        if self.financial:
            prompt = self.gemini._finance_news_prompt(text=articles_text)
        else:
            prompt = self.gemini._general_news_prompt(text=articles_text)

        response = self.gemini.model.generate_content(prompt)
        summary = response.text if hasattr(response, 'text') else str(response)

        # Step 3: Prepare email body
        email_body = "=== News Digest ===\n\n"
        email_body += summary

        # Step 4: Send mail
        sent = self.mailer.send_mail(recipient=self.recipient, body=email_body)
        return sent
