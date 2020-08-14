# import the Redis client
import redis

class Redinsgo_Player():

    # Assigning instance parameters
    def __init__(self, playerNumberID, redisClient):
        playerID = str(playerNumberID)
        self.playerName = 'user' + playerID
        self.redis_hashUsername = 'user:' + playerID  
        self.redinsgoCard = 'cartela:' + playerID
        self.redinsgoScore = 'score:' + playerID
    
        # Adding info to Redis
        redisClient.hmset(
            self.redis_hashUsername,
            {
                "name": self.playerName,
                "card": self.redinsgoCard,
                "score": self.redinsgoScore
            }
        )

