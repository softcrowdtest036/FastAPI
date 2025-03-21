from bson import ObjectId
from app.core.database import mongodb
from app.schemas.online_order_link import OnlineOrderLinkCreate, OnlineOrderLinkUpdate

class OnlineOrderLinkService:

    @staticmethod
    async def get_all_links():
        db = mongodb.get_database()
        collection = db["online_order_links"]
        links = []
        cursor = collection.find()
        async for document in cursor:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
            links.append(document)
        return links

    @staticmethod
    async def create_link(link_data: OnlineOrderLinkCreate):
        db = mongodb.get_database()
        collection = db["online_order_links"]
        result = await collection.insert_one(link_data.dict())
        return str(result.inserted_id)

    @staticmethod
    async def get_link_by_id(link_id: str):
        db = mongodb.get_database()
        collection = db["online_order_links"]
        link = await collection.find_one({"_id": ObjectId(link_id)})
        if link:
            link["_id"] = str(link["_id"])
        return link

    @staticmethod
    async def update_link(link_id: str, update_data: OnlineOrderLinkUpdate):
        db = mongodb.get_database()
        collection = db["online_order_links"]
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        await collection.update_one(
            {"_id": ObjectId(link_id)},
            {"$set": update_dict}
        )

    @staticmethod
    async def delete_link(link_id: str):
        db = mongodb.get_database()
        collection = db["online_order_links"]
        await collection.delete_one({"_id": ObjectId(link_id)})
