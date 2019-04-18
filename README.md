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







##### 

# Work In Progress...
Code Examples in Node.js and Python
Create Stitch application
Expose REST endpoint
Function/Trigger
Simple webpage w/ query anywhere/Stitch hosting
Charts/Embed charts








