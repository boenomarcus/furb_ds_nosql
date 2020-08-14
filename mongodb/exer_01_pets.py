# Import packages
import pymongo

# Creating a connection
mongoClient = pymongo.MongoClient()

# Accessing petshop database
db = mongoClient.petshop

# Deleting any pre-existing documents
db.pets.delete_many({})

# Inserting objects into "pets" collection of "petshop" database
db.pets.insert_one({'name':'Mike', 'species': 'Hamster'})
db.pets.insert_one({'name':'Dolly', 'species': 'Peixe'})
db.pets.insert_one({'name':'Kilha', 'species': 'Gato'})
db.pets.insert_one({'name':'Sally', 'species': 'Cachorro'})
db.pets.insert_one({'name':'Chuck', 'species': 'Gato'})

# Exercises

# Exercise 1.1
print('\n> Exercício 1.1')
peixe = {'species': 'Peixe'}
hamsterFrodo = {'name':'Frodo', 'species': 'Hamster'}
db.pets.insert_one(peixe)
db.pets.insert_one(hamsterFrodo)
print('> Pets inseridos no sistema:')
print(peixe)
print(hamsterFrodo)

# Exercise 1.2
print('\n> Exercício 1.2')
print(db.pets.count_documents({}))

# Exercise 1.3
print('\n> Exercício 1.3')
print(db.pets.find_one())

# Exercise 1.4
print('\n> Exercício 1.4')
cursor = list(db.pets.find({'name': 'Kilha', 'species': 'Gato'}))
print(cursor[0]['_id'])

# Exercise 1.5


# Exercise 1.6
print('\n> Exercício 1.6')
docs = db.pets.find({'species': 'Hamster'})
for doc in docs:
    print(doc)

# Exercise 1.7
print('\n> Exercício 1.7')
docs = db.pets.find({'name': 'Mike'})
for doc in docs:
    print(doc)

# Exercise 1.8
print('\n> Exercício 1.8')
docs = db.pets.find({'name': 'Mike', 'species': 'Cachorro'})
for doc in docs:
    print(doc)

print('')