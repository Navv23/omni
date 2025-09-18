import argparse
from omni.jobs.service import OmniNewsService


def main():
    parser = argparse.ArgumentParser(description="Omni News Reporter CLI")
    parser.add_argument("--search", required=True, help="Search keyword(s) for news")
    parser.add_argument("--time", default="1d", help="Time period (e.g., 1d, 7d, 1y)")
    parser.add_argument("--financial", action="store_true", help="Flag: Only classify as financial news")
    parser.add_argument("--recipient", required=True, help="Recipient email address")

    args = parser.parse_args()

    job = OmniNewsService(search=args.search,
                          time_period=args.time,
                          financial=args.financial,
                          recipient=args.recipient)

    print("-- OMNI NEWS REPORTER --")
    if job.run():
        print(f"Email sent to {args.recipient}")
    else:
        print("Job failed or no articles found.")


if __name__ == "__main__":
    main()
