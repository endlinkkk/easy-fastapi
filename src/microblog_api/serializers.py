from typing import List
from src.microblog_api.schemas import Tweet
from loguru import logger


def tweets_serializers(unserialized_tweets: List) -> List[Tweet]:
    serialized_tweets = []
    for tweet_obj in unserialized_tweets:
        print(tweet_obj.attachment)
        tweet = Tweet(
            id=tweet_obj.id,
            content=tweet_obj.content,
            attachments=[attachment.link for attachment in tweet_obj.attachment],
            author={"id": tweet_obj.author.id, "name": tweet_obj.author.name},
            likes=[
                {"user_id": like.author.id, "name": like.author.name}
                for like in tweet_obj.like
            ],
        )
        logger.info(
            f"Tweet image link - {[attachment for attachment in tweet.attachments]}"
        )
        serialized_tweets.append(tweet)
    return serialized_tweets
