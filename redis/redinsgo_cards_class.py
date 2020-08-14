# import the Redis client
import redis

class Redinsgo_Card():

    # Assigning instance parameters
    def __init__(self, cardNumberID, redisClient):
        self.redis_cardID = 'cartela:' + str(cardNumberID)  
        
        # Create a list of number for a redinsgo card
        card_list = redisClient.srandmember('cardSet', 15)
                
        # Adding info to Redis
        redisClient.lpush(
            self.redis_cardID,
            *card_list
        )