# import redis-py package
import redis
import random

# import classes
from redinsgo_player_class import Redinsgo_Player
from redinsgo_cards_class import Redinsgo_Card

# Number of players
numPlayers = 50


# Function to create redingo database into redis 
def addInfo_redis(redisClient):
     
    # Get rid of any pre-existing keys (useful in the case of lists)
    redisClient.flushdb()

    # Insert a set with values from 1 to 99 into redis server
    # Will be utilized to create redinsgo cards
    redisClient.sadd('cardSet', *set([i+1 for i in range(99)]))
    
    # Insert users into redis server
    print('\n> Cadastrando jogadores ...', end = '')
    for userID in range(numPlayers):
        userID += 1
        if userID < 10:
            userID = '0' + str(userID)
        # Call class to add info into redis server
        Redinsgo_Player(userID, redisClient)
    # Print to indicate finished process
    print('  OK')
    
    # Insert random redinsgo cards for each user
    print('> Gerando cartelas ...', end = '')
    for userID in range(numPlayers):
        userID += 1
        if userID < 10:
            userID = '0' + str(userID)
        # Call class to add info into redis server
        Redinsgo_Card(userID, redisClient)
    # Prints to indicate finished processes
    print('  OK\n')
    print('> Nova base adicionada com sucesso!')


# Function to run redinsgo game
def new_redinsgoGame(redisClient):
    
    # Set all scores to zero before initializing the game
    for userID in range(numPlayers):
        userID += 1
        if userID < 10:
            userID = '0' + str(userID)
        scoreID = 'score:' + str(userID)
        redisClient.zadd(
            'scores', 
            {scoreID: 0}
        )
    
    # Generate random set for the game
    number_list = list(range(1,100))
    random.shuffle(number_list)

    print('\n> Números sorteados:', end = '')
    
    # Draw numbers, update scores and indicate winner
    for number in number_list:

        # Print out picked number
        print(' ' + str(number), sep = ' ', end = '', flush = True)


        # Update scores of each user
        for userID in range(numPlayers):
                
            # Retrieve user's card
            userID += 1
            if userID < 10:
                userID = '0' + str(userID)
            cardID = 'cartela:' + str(userID)
            card_numbers = redisClient.lrange(cardID, 0, -1)
                
            # Update score if number is in the card
            if str(number) in card_numbers:
                scoreID = 'score:' + str(userID)
                redisClient.zincrby('scores', 1, scoreID)
                
            # Check if any user reached 15 points
            user_with_15 = redisClient.zcount('scores', 15, 15) 
            if user_with_15 == 1:

                # Define hash to retrieve user data
                userHash = 'user:' + str(userID)

                # Print out info on winner
                print('\n\nTemos um vencedor!')
                print('\nJogador: ' + redisClient.hget(userHash, 'name'))
                print('Cartela: ' + redisClient.hget(userHash, 'card'))
                print('Cartela: ', card_numbers)
                break

        # Exit loop if there is already a winner
        if user_with_15 == 1:
            break


# Main function
def main():

    # Load redis client
    redisClient = redis.StrictRedis(
        'localhost',
        6379,
        charset = "utf-8",
        decode_responses = True
    )
    
    # Greet user
    print('\n\n> Bem-vindo ao Redinsgo!\n\n')
    
    # Loop to check if user wants to add new random player/card database
    while True:
        novaBase = input(
            '> Deseja cadastrar nova base de jogadores/cartelas? ([y]/n)  '
        ).lower()
        if novaBase == '' or novaBase == 'y':
            # Call function to generate new random player/card database
            addInfo_redis(redisClient)
            break
        elif novaBase == "n":
            # Check if players and card exists in redis server
            user_test = redisClient.exists('user:50')
            card_test = redisClient.exists('cartela:50')
            if user_test and card_test:
                break
            else:
                print('\n> Base inexistente. Gere nova base para jogar!\n')
        else:
            # Make sure user enters right input
            print('Pressione "ENTER" ou "y" para cadastrar nova base')
            print('ou "n" para não cadastrar')


    # Loop to check if user wants to play
    while True:
        novo_jogo = input(
            '\n> Deseja iniciar um novo jogo? ([y]/n)  '
        ).lower()
        if novo_jogo == '' or novo_jogo == 'y':
            # Call new game
            new_redinsgoGame(redisClient)
            continue
        elif novo_jogo == 'n':
            # Exit redinsgo if the user do not want to play anymore
            break
        else:
            # Make sure user enters right input
            print('Pressione "ENTER" ou "y" para iniciar novo jogo')
            print('ou "n" para sair do Redinsgo')
    
    
# Run program only when invoked with command-line
if __name__ == '__main__':
    main()
