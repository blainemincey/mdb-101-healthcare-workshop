#!/usr/bin/env python3
from pymongo import MongoClient

####
# Indicate start
####
print("============================")
print("  Starting my_python_app    ")
print("============================")
print('\n')


####
# Main start function
####
def main():
    # MongoDB Connection
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client[DATABASE]
    patients_collection = db[COLLECTION]

    # Define the query
    # Comment/uncomment one of the following query variables to either filter on one patient or return all patients
    query = {'patientId': 'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3'}
    # query = {}
    projection = {'_id': 0, 'patientId': 1, 'firstName': 1, 'lastName': 1, 'birthDate': 1}

    for doc in patients_collection.find(query, projection):
        print(doc)


####
# Aggregation Pipeline function
####
def aggregation():
    print('\n')
    print("== Executing Aggregation Pipeline ==")
    print('\n')

    # MongoDB Connection
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client[DATABASE]
    patients_collection = db[COLLECTION]

    pipeline = [
        {
            '$match': {
                'isDeceased': True,
                'conditions.conditionText': 'Suspected lung cancer (situation)'
            }
        },
        {
            '$group':
                {
                    '_id': '$city',
                    'yearOfDeath':
                        {
                            '$push':
                                {
                                    '$year': '$dateDeceased'
                                }
                        },
                    'count':
                        {
                            '$sum': 1
                        }
                    }
        },
        {
            '$sort':
                {
                    'count': -1
                }
        }]

    for doc in patients_collection.aggregate(pipeline):
        print(doc)


####
# Constants
####
MONGODB_URL = 'mongodb+srv://fhir:workshop@fhir-workshop-vautv.mongodb.net/test?retryWrites=true'
DATABASE = 'fhirDb'
COLLECTION = 'patients'


####
# Main
####
if __name__ == '__main__':
    main()
    # Uncomment below to run aggregation
    # aggregation()

####
# Indicate End
####
print('\n')
print("============================")
print("  Ending my_python_app      ")
print("============================")


