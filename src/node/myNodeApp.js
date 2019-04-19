const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

// Connection URL
const dbUrl = 'mongodb+srv://fhir:workshop@fhir-workshop-vautv.mongodb.net/test?retryWrites=true';

// Database Name
const databaseName = 'fhirDb';

// find documents
const findDocuments = function (db, callback) {
    const collection = db.collection('patients');

    let query = {patientId: 'a7b1cd7b-8fa2-42ff-a491-9597d02368c7'};
    let projection = {patientId: 1, firstName: 1, lastName: 1, birthDate: 1, _id: 0};

    let cursor = collection.find(query);
    cursor.project(projection);

    cursor.forEach(
        function (doc) {
            console.log(doc);
        }, function (err, result) {
            assert.equal(err, null);
            callback(result);
        }
    )

}

// run an aggregation
function myPipeline(db, callback) {
    const collection = db.collection('patients');

    collection.aggregate(
        [
            {
                '$match': {
                    'city': 'Chattanooga'
                }
            }, {
                '$unwind': {
                    'path': '$conditions'
                }
            }, {
                '$group': {
                    '_id': '$conditions.conditionText',
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    'count': -1
                }
            }
        ],
        function (err, cursor) {
            assert.equal(err, null);

            cursor.toArray(function (err, documents) {
                console.log(documents)
                callback(documents);
            });
        });
}

// Connect to the database
MongoClient.connect(dbUrl, {useNewUrlParser: true}, function (err, client) {
    assert.equal(null, err);
    console.log("Connected successfully to MongoDB!");

    const db = client.db(databaseName);

    /**
    findDocuments(db, function () {
        client.close();
    })
    */

    myPipeline(db, function () {
        client.close();
    })


});