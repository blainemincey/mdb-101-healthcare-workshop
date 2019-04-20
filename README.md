# mdb-101-healthcare-workshop
This repository contains a guide on getting started with MongoDB.
Specifically, this is a step-by-step tutorial/workshop incorporating MongoDB Compass, MongoDB Atlas, and MongoDB Stitch.
The data utilized in this workshop is based on the health care domain.  The data was acquired by generating sample data 
in [FHIR](https://www.hl7.org/fhir/formats.html) format from the [Synthea](https://github.com/synthetichealth/synthea)
project.  In order to parse the files, this [FHIR Parser](https://github.com/blainemincey/fhir) was used.  The application
uses Spring Boot, Spring Data (MongoDB), Apache Camel, and the HAPI parser for HL7-FHIR.

# Introduction to MongoDB
## Hands-on Workshop

### Overview
This hands-on workshop is designed to get you familiar with all general aspects of MongoDB.  This includes using either
a local running version of MongoDB or MongoDB Atlas (database as a service).  This workshop will walk you through
importing data into your MongoDB instance/MongoDB Atlas cluster.  Using MongoDB Compass, this workshop will provide
guidance on how to query data (CRUD), introduce the user to the aggregation framework, and optimize queries (explain plans/
indexes).  Next, the user can see how queries can be written in Node and Python.  Finally, the user will be introduced 
to MongoDB Atlas as well as the serverless platform, MongoDB Stitch.

### Required Prerequisites
To successfully complete this workshop, the following software should be installed:

* [MongoDB Compass](https://www.mongodb.com/download-center/compass) - This is a GUI to MongoDB that will be used to 
write queries.

* Access to a MongoDB instance.  You can either download [MongoDB](https://www.mongodb.com/download-center/enterprise)
and set it up on a workstation/server.  Or, the *recommended* way to complete the workshop, is by using [MongoDB
Atlas](https://www.mongodb.com/cloud/atlas), the fully managed service from MongoDB.  To access, simply create an account
at [https://cloud.mongodb.com](https://cloud.mongodb.com) or login to an existing account you may have previously
created. More details are below.

### Optional Prerequisites
During the course of the workshop, code samples will be used with both Node.js and Python.  If you choose to edit/run
the provided source files, you will need to be sure to have the following installed:

* Node.js - If you would like to edit/run the Node.js source files

* Python - If you would like to edit/run the Python source files

* For the MongoDB Stitch section, the workshop will interface with a REST endpoint.  This will be a GET method and
can be easily done with your browser.  However, if you want to use something like cURL or 
[Postman](https://www.getpostman.com/), please be sure to have the tools installed.

### Advanced/Optional Prerequisites
In Lab 2, the workshop will guide the user to load data using MongoDB Compass.  If you are an advanced MongoDB
user and would prefer to use the terminal/command-line, be sure to have the MongoDB command-line tools
installed.  The workshop does *not* go into detail on the installation/use of these tools.

* Binary Import and Export Tools  
[mongorestore](https://docs.mongodb.com/manual/reference/program/mongorestore)  
[mongodump](https://docs.mongodb.com/manual/reference/program/mongodump)  

* Data Import and Export Tools  
[mongoimport](https://docs.mongodb.com/manual/reference/program/mongoimport)  
[mongoexport](https://docs.mongodb.com/manual/reference/program/mongoexport)  

### Note:
If you use MongoDB Atlas, you must be able to make outgoing requests from your computer to MongoDB Atlas services
which will be running on port 27017.  Please confirm that port 27017 is not blocked by checking with 
[PortQuiz](http://portquiz.net:27017).  If successful, you will see a page load that indicates you can make outgoing
requests on port 27017.  The page looks similar to the one below:

![](images/Outgoing_Port_Tester.jpg)


### Hands-on Labs
#### Lab 1 - Create the Cluster (Skip to Lab 2 if you have MongoDB installed locally)
#### Create a Free Tier Cluster
#### Click Build a Cluster

![](images/Clusters___Atlas__MongoDB_Atlas.jpg)

Be sure to select the Free Tier Option for your cluster.
Take a moment to browse the options (Provider & Region, Cluster Tier, Version, Backup, ...).  For this workshop,
select AWS as the Cloud Provider:

![](images/Create_Cluster___Atlas__MongoDB_Atlas.jpg)

Keep all of the defaults.  Be sure to name your Cluster Name to FHIR-Workshop (or anything you prefer) and then
click the green button to Create Cluster:

![](images/Name_Create_Cluster___Atlas__MongoDB_Atlas.jpg)

The cluster should complete provisioning within 5-7 minutes.

#### Install MongoDB Compass if you have not already
MongoDB Compass is the GUI for MongoDB.  Go to https://www.mongodb.com/download-center/compass to download and
install Compass for your platform.

#### After your MongoDB Atlas Cluster has been provisioned, setup Connection Security:
Return to the Atlas UI.  Your cluster should be provisioned.  Click the CONNECT button which will prompt you to setup
security:

![](images/Connect_Clusters___Atlas__MongoDB_Atlas.jpg)

After clicking the connect button, you should see the following:

![](images/ConnectionDialog__Clusters___Atlas__MongoDB_Atlas.jpg)

Add your current IP address and Create a MongoDB User.  This example assumes a Username of 'fhir' and password 'workshop'.

Click Choose a connection method and select Connect with MongoDB Compass.

Then select 'I am using Compass 1.12 or later' and COPY the connection string presented:

![](images/Security__Clusters___Atlas__MongoDB_Atlas.jpg)

#### Connect Compass
Start Compass and it should detect the connection string in your copy buffer:

![](images/connectstringdetect_MongoDB_Compass_-_Connect.jpg)

Select Yes.

Provide the password ('workshop') and before clicking CONNECT, CREATE A FAVORITE named FHIR-Workshop.  This will
allow us to quickly connect to the cluster in the future.

Click CONNECT.

If successful, you will see some internal databases used by MongoDB:

![](images/first_MongoDB_Compass_-_fhir-workshop-vautv_mongodb_net_27017.jpg)

#### Lab 2 - Load Data
We are now going to load data into MongoDB.  The data that will be used for this workshop
was parsed from file in FHIR format.  The data is in JSON format.

Download the dataset from Github. If you have the wget utility, you can get the dataset as follows:

wget https://raw.githubusercontent.com/blainemincey/mdb-101-healthcare-workshop/master/data/fhirDb-patients.json

Otherwise, just open the link in your browser and once the load completes, save the file (File > Save Page As in Chrome).

Or, it is also included as part of this GitHub repo in the data directory as fhirDb-patients.json.

The dataset is around 50 MB in size and contains around 600 patients (alive and deceased).

#### Create a Database and Collection  
Click the CREATE DATABASE button and create a 'fhirDb' database with a 'patients' collection:

![](images/createDatabase.jpg)  

Navigate to the patients collection and select Import Data from the menu.  
Then BROWSE to the fhirDb-patients.json file you downloaded:  

![](images/importFhir.jpg)  

#### Lab 3 - Browse the Documents
Notice how the patients documents have a variety of structures beyond a relational/tabular database
which is limited to rows and columns.  Many of the patient documents contain arrays of 
sub-documents.  Working with data in this way is much easier than having to flatten out multiple
tables into a single object.

#### Lab 4 - Analyze the Schema
Analyze the schema?  Wait, I thought MongoDB was a NoSQL database and was considered to be schema-less?
While that’s technically true, no dataset would be of any use without a schema. 
Although MongoDB does not enforce a schema, your collections of documents will still always have one. 
The key difference with MongoDB is that the schema can be flexible/polymorphic.

Within MongoDB Compass, select the Schema tab and select Analyze Schema. 
Compass will sample the documents in the collection to derive a schema. 
In addition to providing field names and types, Compass will also provide a summary 
of the data values. 
For example, for language, we can see that in our population, we have 79% that speak
English as their primary language:  

![](images/analyzeSchema.jpg)  

For fun, take a look at the address field which contains a GeoJSON point, i.e., a longitude
and latitude coordinate.  You can drill down on the map as it builds the query for you.  

![](images/geomap.jpg)

#### Lab 5 - Query Data with MongoDB Compass (CRUD Operations)  
Copy the code block and paste in the filter dialog in MongoDB Compass.

##### Find Operations  
* Simple filter (Single males)  
```
{maritalStatus:'S', gender: 'Male'}
```  

* Simple filter with query operators (Deceased with a date deceased of 2019)  
```
{isDeceased:true, dateDeceased : {$gte : ISODate('2019-01-01')}}  
```  

* Query sub-document/array  (Patients with 'Prediabetes' as a condition)  
```
{"conditions.conditionText":"Prediabetes"}
```  

* Query with AND as well as OR conditions (Deceased patients with either Sinusitis or has taken a medication starting with "Ace")  
```
{ isDeceased: true, $or: [ { "conditions.conditionText": "Sinusitis (disorder)" }, { "medicationRequests.display": /^Ace/ } ] }
```

* Query sub-document in array and project matched array element  
(Display Blood Pressure array element if the Systolic is greater than or = 140)  
Filter:  
```
{"observations.bloodPressure.display":"Systolic Blood Pressure", "observations.bloodPressure.value":{$gte:140}}
```  
Click Options and then in the Projection block:  
```
{patientId:1, "observations.$":1}
```

* Query using the $in (Display patients living in Memphis or Chattanooga)  
```
{city : {$in:["Memphis", "Chattanooga"]}}
```  

##### Update, Delete, Clone Operations  
Find a document and choose to update a field or fields.  In fact, add a field that
does not exist.  Next, clone a document.  Finally, delete the cloned document.
The MongoDB Compass interface provides all of the CRUD controls you need:  

![](images/copyclonedelete.jpg)  

#### Lab 6 - Create indexes to improve efficiency of queries  
Indexes support the efficient execution of queries in MongoDB. Without indexes, 
MongoDB must perform a *collection scan*, i.e. scan every document in a collection, 
to select those documents that match the query statement. 
If an appropriate index exists for a query, MongoDB can use the index to 
limit the number of documents it must inspect.  

In this lab, we will perform a search on a field, use the explain plan to determine if
it could be improved with an index, and create the index...all from within MongoDB Compass.  

Find a patientId to filter on.  For this example, we will use 'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3'.
Just make sure the patientId you use, exists within your dataset!

In the query box in Compass, enter the following:  
```
{patientId:'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3'}
```  

Then, click the Explain Plan tab as below:  

![](images/explainplanstart.jpg)  

Click the Execute Explain button in the middle of the GUI and review the output.  

![](images/explainresults.jpg)  

Considering this is a relatively small data size, an index may not immediately improve performance.
In our results, it indicates that a collection scan (bad!!) took place with our filter.  It also indicates
that the query took 0 milliseconds.  Again, if our data size was larger, this time would have been larger
as well.  We will now create an index on patientId and then run another explain plan.  

Click on the Indexes tab.  We will create an index on patientId.  Find the field in the
dropdown and select 'asc' as the index type.  Then, click the create button as below:  

![](images/createIdx.jpg)  

After creating the index, go back to your Explain Plan tab and Execute Explain once more.
This time, you should see that your index was hit and instead of a collection scan (bad!!),
an index scan occurred.  Your results should be similar to that below:  

![](images/afterIdxcreate.jpg)  


#### Lab 7 - Aggregation Framework  
MongoDB’s [aggregation framework](https://docs.mongodb.com/manual/core/aggregation-pipeline/) is modeled on the concept of data processing pipelines.
Documents enter a multi-stage pipeline that transforms the documents into an aggregated 
result.  

The most basic pipeline stages provide filters that operate like queries and document
transformations that modify the form of the output document.  

Other pipeline operations provide tools for grouping and sorting documents by specific
field or fields as well as tools for aggregating the contents of arrays, 
including arrays of documents. In addition, pipeline stages can use operators 
for tasks such as calculating the average or concatenating a string.  

The pipeline provides efficient data aggregation using native operations within 
MongoDB, and is the preferred method for data aggregation in MongoDB.

For this next series of exercises, we will use the aggregation pipeline builder in
MongoDB Compass to create our aggregation pipelines.

First, click on the Aggregations tab in MongoDB Compass.  Then, click the '...' next to the
'Save Pipeline' dialog and then, 'New Pipeline' as in the image below:  

![](images/aggregation.jpg)

For our first aggregation, we will determine the number of deaths in each city
from Lung Cancer.  This means, we will first need to use the $match operator to filter
our data for deceased patients with a condition of "Suspected lung cancer (situation)".
Also, enter a name for your aggregation to save.  For this example, we can use "LungCancerDeathsByCity".

Your first stage should resemble the image below:  

![](images/agg-step1.jpg)  

The next step is a bit tricky because we will incorporate a number of operators. Now that we
have filtered our data for deceased individuals with lung cancer, let's group the result
by city and then count the number of deaths per year.  You will Add Stage and then you
will select '$group' from the dropdown.  It will provide a template for this operator.
The text you should enter is below:  

```
{
  _id: "$city",  
  yearOfDeath : {$push: {$year:"$dateDeceased"}},  
  count: { $sum: 1}
}
```  
We are grouping by city.  Then, we are adding a field 'yearOfDeath'.  For this field,
we are "pushing" the year field from 'dateDeceased' into an Array.  Finally, we are
counting each element. Add an additional stage to sort by count decreasing.

The result should look similar to below:  

![](images/lungcancerresults.jpg)  

In our sample set of data, we can see that Knoxville had 3 total deaths suspected from
lung cancer in years 2014, 2004, and 1993.  

The completed aggregation pipeline (as text) is below:  
```
[
  {
    $match: { isDeceased:true,
              "conditions.conditionText":"Suspected lung cancer (situation)"}}, 
    {$group: {  _id: "$city", 
                yearOfDeath : {$push: {$year:"$dateDeceased"}},
                count: {$sum:1} }}, 
    {$sort: { "count": -1}
  }
]
```

Be sure to have named your Pipeline and saved it.  Again, click the '...' and select
to create a New Pipeline.  For our next aggregation, let's determine how many
deaths occurred per month for married men in our population.  First, we need to filter
for deceased males that were married.  In the first stage, select $match and the following:  

```
{
  isDeceased:true,
  maritalStatus:"M",
  gender:"Male"
}
```  

Add a Stage and select $group.  Enter the following:  
```
{
  _id: {$month:"$dateDeceased"},
  count : {$sum:1}
}
```

In the above, we will group by the month using the $month operator on the ISODate
dateDeceased.  Then, we will count each entry for each month.  

Next, add a stage and select $sort.  We will sort from highest to lowest.  

```
{
  "count": -1
}
```

If we wanted to 'limit' the result to either 1 or 2 results only, how would we do that?  

The final result is here:  

![](images/marrieddeathsbymonth.jpg)  


For our final aggregation, we will find the most common condition reported among
all residents (alive and deceased) in Chattanooga.  Below is the final aggregation as 
text but see if you can complete it on your own.  Before looking at the completed
aggregation, you will need to use $match, $unwind (i.e. unwind the condition array),
$group and perhaps $sort.  

Here is an image of the result and below that, the aggregation code:  

![](images/commonobs.jpg)  

```
[
    {
        $match: { city: "Chattanooga" }}, 
        {$unwind: { path: "$conditions"}}, 
        {$group: {  _id: "$conditions.conditionText",
                    count: { $sum : 1 } }}, 
        {$sort: { "count": -1}
    }
]
```  

#### Lab 8 - Code Examples
The next lab will focus on how to utilize the MongoDB Query Language while using
both the Node.js and Python drivers.  These are meant to strictly be high-level
examples of how to interface with MongoDB using two popular scripting/programming
languages.  

##### Node.js Example
First, let's take a look at an example in Node.js.  In the src/node directory of this
GitHub repo there is a Node.js src file that can be used to connect and query
our sample data.  The file is myNodeApp.js.  If you have cloned the Git repo, you
can go into the src/node directory and:  

```
npm install
```  

This will install the required files, i.e., the MongoDB driver.  If you are using MongoDB Atlas,
you will need to copy the connection URL from the Atlas Interface.
First, click the 'Connect' button within your cluster.  Then, click the "Connect to Application"
button on the window that pops up.  Then, select your driver (Node.js) and copy the
connection string as indicated below:  

![](images/nodeconnectapp.jpg)  

Open the myNodeApp.js src file and paste the url into the variable named dbUrl. Be sure
to edit your username/password as well. It should be similar to below:  
```
// Connection URL
const dbUrl = 'mongodb+srv://fhir:workshop@fhir-workshop-vautv.mongodb.net/test?retryWrites=true';
```  

Inspect the src file.  Be sure the patientId that is being filtered actually exists
within your dataset or you will not query for an existing document!  If you need
to edit the patientId, do so and then 'node myNodeApp.js'.  You should see output
similar to that below:  

```
$ node myNodeApp.js 
Connected successfully to MongoDB!
{ patientId: 'a7b1cd7b-8fa2-42ff-a491-9597d02368c7',
  firstName: 'Elanor679',
  lastName: 'Price929',
  birthDate: 1951-04-21T05:00:00.000Z }

```  

For fun, let's run one of the aggregation pipelines we created in Lab 7.  Find one
within MongoDB Compass and open it.  Click the '...' and select to Export to Language.
When the pop-up window opens, be sure to select 'Node' and then copy the block to the
right as indicated below:  

![](images/exportToLanguage.jpg)  

Find the function in the Node src file called myPipeline and paste your code
over the existing code.  In this example, we are running the aggregation we created
to find the most prevalent condition in Chattanooga.  

Your final function should look similar to that below:  


```
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
```  

Once your function is correct, be sure to go to the bottom of the src file and
comment out the find function and uncomment the myPipeline function.  It should
look similar to what is below:  

```
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
```  

Once you run the Node.js example again, your output should be similar to that below:  

```
$ node myNodeApp.js 
Connected successfully to MongoDB!
[ { _id: 'Viral sinusitis (disorder)', count: 54 },
  { _id: 'Acute viral pharyngitis (disorder)', count: 21 },
  { _id: 'Body mass index 30+ - obesity (finding)', count: 20 },
  { _id: 'Prediabetes', count: 18 },
  { _id: 'Anemia (disorder)', count: 16 },
  { _id: 'Acute bronchitis (disorder)', count: 16 },
  { _id: 'Chronic sinusitis (disorder)', count: 16 },
  { _id: 'Hypertension', count: 16 },
  { _id: 'Normal pregnancy', count: 15 },
  ......rest removed

```

#### Python Example
This example is written in Python3 and will follow the same format as the Node.js example
above.  First, be sure to have the Python MongoDB Driver installed, pymongo.  The most recent
version of the driver at this time is 3.7.2.  It is recommended to use pip to install pymongo on all platforms:  

```
python -m pip install pymongo
```  

##### Important Note  
Be sure to have dnspython installed as well to ensure the most recent url syntax can
be used.  The following will install dnspython:  

```
pip install dnspython
```

Next, make sure you have access to th Python example in the GitHub repo of this project.
The src is in src/python and is named my_python_app.py.  

If you are using MongoDB Atlas,
you will need to copy the connection URL from the Atlas Interface.
First, click the 'Connect' button within your cluster.  Then, click the "Connect to Application"
button on the window that pops up.  Then, select your driver (Python) and the version (3.6 or later) and copy the
connection string as indicated below:  

![](images/pythonUrl.jpg)  

Open the my_python_app.py src file and paste the url into the variable named MONGODB_URL
that is towards the bottom of the src file.  It should look similar to that below once
it has been pasted:  

```
####
# Constants
####
MONGODB_URL = 'mongodb+srv://fhir:workshop@fhir-workshop-vautv.mongodb.net/test?retryWrites=true'
DATABASE = 'fhirDb'
COLLECTION = 'patients'
```  

Once you have edited the Python src for the MONGODB_URL, you can either run the Python
script as is to filter on a single patientId or you can return all patients.  The
following variables can be easily commented/uncommented:  

```
# Define the query
# Comment/uncomment one of the following query variables to either filter on one patient or return all patients
# query = {'patientId': 'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3'}
query = {}
projection = {'_id': 0, 'patientId': 1, 'firstName': 1, 'lastName': 1, 'birthDate': 1}
```  

As indicated in the src above, filter on a patientId which exists within your dataset or
simply keep the empty filter to return all patients.  Take note that we are using projection
to limit the number of fields returned.  0 indicates we will NOT return the field and 1 indicates
the field will be returned.  Let's run the src where a single patient is returned.  Your
result should be similar to that below:  

```
$ python3 my_python_app.py 
============================
  Starting my_python_app    
============================

{'patientId': 'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3', 'firstName': 'Efren426', 'lastName': 'Casper496', 'birthDate': datetime.datetime(1938, 8, 1, 4, 0)}

============================
  Ending my_python_app      
============================

```

For fun, we will now edit our Python script to run one of our aggregation pipelines that we
created in Lab 7.  Find one within MongoDB Compass that we created and open it.
Click the '...' and select 'Export to Language'.  When the pop-up window opens, be sure to select
'Python' and then copy the block to the right as indicated below:  

![](images/pythonaggregation.jpg)  

Find the method definition called 'aggregation'.  There will be a variable named
pipeline.  You will paste your copied aggregation pipeline code from MongoDB Compass
into this variable.  In the example below, we are using the pipeline for determining
lung cancer deaths by City.  

Your final variable should look similar to the code below:  

```
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
```  

Once your variable is correctly formatted, be sure to go into the main definition towards
the bottom of the src file and uncomment the call to the 'aggregation' method.  It should
look similar to the Python src below:  

```
####
# Main
####
if __name__ == '__main__':
    main()
    # Uncomment below to run aggregation
    aggregation()
    
```  

When you run the Python script again, you should see output similar to that below:  

```
$ python3 my_python_app.py 
============================
  Starting my_python_app    
============================


{'patientId': 'b476d9e4-b3cf-417a-8fb4-3c2bccf08bf3', 'firstName': 'Efren426', 'lastName': 'Casper496', 'birthDate': datetime.datetime(1938, 8, 1, 4, 0)}


== Executing Aggregation Pipeline ==


{'_id': 'Knoxville', 'yearOfDeath': [2014, 2004, 1993], 'count': 3}
{'_id': 'Cleveland', 'yearOfDeath': [1996, 2001], 'count': 2}
{'_id': 'Chattanooga', 'yearOfDeath': [1979], 'count': 1}
{'_id': 'Brentwood', 'yearOfDeath': [1999], 'count': 1}


============================
  Ending my_python_app      
============================

```

#### MongoDB Atlas/MongoDB Stitch Labs  
The remaining labs in this workshop **do** require MongoDB Atlas and cannot be completed
using an on-premise or local version of MongoDB Enterprise Advanced.  If you have not already
created a MongoDB Atlas cluster, please refer back to Lab 1 at the beginning of this 
document to walk through the steps of setting it up. 

#### Lab 9 - Create a MongoDB Stitch Application  
MongoDB Stitch is a serverless platform that enables developers to quickly build 
applications without having to set up server infrastructure. Stitch is built on top 
of MongoDB Atlas, automatically integrating the connection to your database. 
You can connect to Stitch through the Stitch Client SDKs, which are available 
for many of the platforms that you develop for including JavaScript, iOS, 
and Android.  

After logging into MongoDB Atlas and selecting your project context, click the 'Stitch' link
in the left-hand navigation and then click the 'Create New Application' button in 
the center of the page as indicated in the image below:  

![](images/createStitch.jpg)  

Now, fill in the values on the pop-up window.  Enter an application name.  For example,
'MyFhirApp' and keep the remaining defaults.  Your page should look similar to that
below:  

![](images/createnewstitch.jpg)  

Once your Stitch application becomes enabled, the screen will indicate it is 
redirecting to your Stitch application.  Your page should look similar to that below:  

![](images/welcometostitch.jpg)  


#### Lab 10 - Expose data via REST-ful endpoint  
Now that we have created our Stitch application, let's expose our data through a
REST based endpoint using what is known as a Webhook.

First, click the Services menu in the left-hand navigation and then Add a Service.
Click on HTTP to create an HTTP service.  Provide a Service Name.  In this example,
we name our service 'getPatientByPatiendId'.  Click 'Add Service'.

![](images/createservice.jpg)  

After you add the service, you will then be directed to 'Add an Incoming Webhook'.  Click
that button and configure your settings to what is indicated below:  

![](images/createWebhook.jpg)  

To keep things simple for this introduction we’re running the webhook as the System user
and we’re skipping validation. Click Save, which will take us to the function editor
for the service.  

In the service function, we will capture the query argument and interface directly
with our data.  Use the following code below to paste into the Function Editor:  

```
// This function is the webhook's request handler.
exports = function(payload) {
  
  // We can indicate a message in our log.
  console.log("getPatientByPatientId webhook called.");

  // Grab the query param.  If does not exist, empty string
  var patientIdArg = payload.query.arg || '';
  
  // Reference our MongoDB Atlas database/collection
  var patientsCollection = context.services
    .get("mongodb-atlas")
    .db("fhirDb")
    .collection("patients");
  
  // Query for our patientId using the patientId arg.
  var patientDoc = patientsCollection.findOne({patientId: patientIdArg});
  
  return patientDoc;
};
```  

In the Console view below the editor, use the following code to actually test our
function we just created (Be sure the patientId exists in your dataset):  
```
exports({query: {arg: '705cc6d2-71a0-4f87-a976-8da866917ddd'}})
```  

![](images/testWebhook.jpg)  

Your editor/console should resemble that directly above.  Once your have made your
edits, click the 'Run' button and you should receive a result.  It will be a 
fairly large result as we did not edit any projections to limit the fields that are
returned.  

Now that we have created our Webhook and tested our function, how can we test it
using external tools like cURL or Postman?  

First, we will switch back to the 'Settings' for our Webhook and copy the Webhook
URL as indicated below:  

![](images/copywebhookurl.jpg)  

Also, notice that directly where we have our Webhook URL, there is an example of 
using the cURL command.  If you have cURL installed, simply copy this URL and run
your test being sure to pass your query argument.  Here is a complete example:  

```
curl https://webhooks.mongodb-stitch.com/api/client/v2.0/app/myfhirapp-xmbxe/service/getPatientByPatientId/incoming_webhook/getPatientWebhook?arg=705cc6d2-71a0-4f87-a976-8da866917ddd
```  

Again, if curl is installed, you should be able to run the command above (being sure to use
a patientId that exists in your dataset).  

If you have Postman available, see if you can invoke this endpoint using that tool.  


#### Lab 11 - Create a Stitch Trigger  
Stitch Triggers provide an easy way enable event processing in your applications. 
For example, for our patients collection, if a patient's record is updated to
indicate they are deceased, we could send a text via Twilio to someone that needs to
be immediately notified or we could send an email using AWS Simple Email Service (SES).  The
integration points are truly limitless.

For our example, if a person's isDeceased field is updated/replaced from false to true,
let's follow our field convention and create a dateDeceased field with today's date. 

To create our trigger, click the 'Triggers' link in the left-hand navigation.  There
are 3 types of triggers: Database, Authentication, and Scheduled.  We will be using the 
Database Triggers for this lab.  After clicking Triggers, you will have a screen similar
to that below.  Click 'Add a Database Trigger'.   

![](images/createdbtrigger.jpg)  

Be sure that Database Triggers is selected.  Name the Trigger.  In this example, we name
our trigger isDeceasedTrigger.  Keep the Enabled and Event Ordering enabled.  Select the
cluster, the database (fhirDb), and the collection (patients).  Now, click the Update
checkbox **and** the Replace checkbox, enable Full Document, and select 'New Function'.  Your page should look like
that below (other than the Replace option not checked):  

![](images/createdeceasedtrigger.jpg)  

After selecting 'New Function' towards the bottom, the Function Editor will open.  Name
the function 'myDeceasedFunction' and then click Save.  We will edit the function in the
next step.  Again, your screen should be similar to that below:  

![](images/mydeceasedfunction.jpg)  

Now, select 'Functions' from the side navigation and click on our newly created function
called myDeceasedFunction similar to that below:  

![](images/selectfunction.jpg)  

Paste the code below over what is in the function for our Database Trigger Function:  

```
exports = function(changeEvent) {
  
  console.log("Calling myDeceasedFunction from my database trigger.");
  
  if(changeEvent.operationType == 'update') {
    console.log("Update changeEvent.");
  }
  
  // When updating from MongoDB Compass, a 'replace' changeEvent occurs.
  if(changeEvent.operationType == 'replace') {
    console.log("Replace changeEvent.");
    
    var fullDocument = changeEvent.fullDocument;
    
    if(fullDocument.isDeceased === true) {
      var patientId = fullDocument.patientId;
      var dateDeceased = new Date();
      
      console.log(`Record updated to isDeceased for patientId: ${patientId}`);
      console.log(`Update dateDeceased to: ${dateDeceased}`);
      
      var query = {"patientId":patientId};
      var update = {$set : {"dateDeceased":dateDeceased}};
      var options = {multi:false};
      
      // Access the MongoDB Atlas service
      var patientsCollection = context.services
        .get("mongodb-atlas")
        .db("fhirDb")
        .collection("patients");
        
      patientsCollection.updateOne(query,update,options)
        .then(result => {
          const {matchedCount, modifiedCount} = result;
          if(matchedCount && modifiedCount) {
            console.log(`Successful update of patientId: ${patientId}`);
          }
        });
    }
  }
};

```

Once you have pasted the code into the function editor, be sure to click save.

Now, go over the MongoDB Compass and select a record where isDeceased is false.  Update
the field to true and click the Update button within MongoDB Compass.  Next, go into
your MongoDB Stitch console and click the Logs button on the left-hand navigation.  Expand
the entries that are indicated as being from the trigger and find the log statements.  You
should see something similar to what is below if your update was successful:  

![](images/runtrigger.jpg)  

Now, make note of the patientId that was updated.  Filter for that document in MongoDB
Compass and verify that the dateDeceased field was added and the value is today's datetime.
It is possible that the field is at the very bottom of the document so be sure to expand
the document to view all fields.  


#### Lab 12 - Query Anywhere with Stitch and Stitch Hosting  
MongoDB Stitch provides a multitude of capabilities.  One of those is Query Anywhere.
Query Anywhere gives you the capability to query data stored in MongoDB Atlas directly from
your client application code with the MongoDB query language.  Data access rules defined
on the Stitch server for each MongoDB collection let you securely filter results based on
the logged in user or the content of each document.  

Let's create a simple web page that will use Query Anywhere to interface with our data
stored in MongoDB Atlas.

#### Lab 13 - MongoDB Charts / Embedded Charts  

---  

**Congratulations!** You have completed the MongoDB 101 Healthcare Workshop!  

---  











