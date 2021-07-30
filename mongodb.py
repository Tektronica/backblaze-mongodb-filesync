import pymongo
import settings

# python3 -m pip install --user pymongo
# The "dnspython" module must be installed to use mongodb+srv:// URIs. To fix this error install pymongo with the srv extra:/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install "pymongo[srv]"
# consider mongomock for mock access to mongo

USERNAME = settings.USERNAME # username
PASSWORD = settings.PASSWORD  # password
DATABASE = settings.DATABASE  # database

# this object represents a specific collection of documents contained in a MongoDB database
class Collection:
    def __init__(self, usr, pwd, db):
        self.myclient = pymongo.MongoClient(
            f"mongodb+srv://{usr}:{pwd}@cluster0.kvlzt.mongodb.net/{db}?retryWrites=true&w=majority")
        self.mydb = self.myclient["portfolio"]  # database
        self.mycol = self.mydb["test"]  # collection

    # Return all documents in the collection
    def findAll(self):
        allItems = []

        for x in self.mycol.find():
            allItems.append(x)

        return allItems

    # Return all documents in the collection
    def findAll(self):
        allDocs = []

        for x in self.mycol.find():
            allDocs.append(x)

        return allDocs

    # Insert one or many documents to collection
    def insert(self, doc):
        # doc can be a dictionary for a single document
        # doc can be a list of dictionaries representing multiple documents
        # one document
        if isinstance(doc, dict):
            x = self.mycol.insert_one(doc)

        # many documents
        elif isinstance(doc, list):
            x = self.mycol.insert_many(doc)

        # print list of the _id values of the inserted documents:
        return x.inserted_ids


# Example implementation
def main():
    # initialize collection object
    colObj = Collection(USERNAME, PASSWORD, DATABASE)
    print(colObj.findAll())


# Boilerplate to protect users from accidentally invoking the script
if __name__ == "__main__":
    main()
