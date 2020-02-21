import random
from pprint import pprint

import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.business


def create_data():
    # Step 2: Create sample data
    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City', 'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich',
             'Lazy',
             'Fun']
    company_type = ['LLC', 'Inc', 'Company', 'Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    for x in range(1, 501):
        business = {
            'name': random.choice(names) + ' ' + random.choice(names) + ' ' + random.choice(company_type),
            'rating': random.randint(1, 5),
            'cuisine': random.choice(company_cuisine)
        }
        # Step 3: Insert business object directly into MongoDB via insert_one
        result = db.reviews.insert_one(business)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created {} of 500 as {}'.format(x, result.inserted_id))
    # Step 5: Tell us that you are done
    print('finished creating 500 business reviews')


def update_data():
    ASingleReview = db.reviews.find_one({})
    print('A sample document:')
    pprint(ASingleReview)

    result = db.reviews.update_one({'_id': ASingleReview.get('_id')}, {'$inc': {'likes': 1}})
    print('Number of documents modified : ' + str(result.modified_count))

    UpdatedDocument = db.reviews.find_one({'_id': ASingleReview.get('_id')})
    print('The updated document:')
    pprint(UpdatedDocument)


create_data()
# update_data()
