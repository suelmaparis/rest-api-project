from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Opetrations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tag.all

@blp.arguments(TagSchema)
@blp.response(200, TagSchema)
def post(self, tag_data, store_id):

    tag = TagModel(**tag_data, store_id=store_id)

    try:
        db.session.add(tag)
        db.session.commit()
    except SQLAlchemyError as e:
        abort(
            500,
            message =str(e)
        )
    return tag

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
        
            db.session.add(item)
            db.session.commit
        except SQLAlchemyError:
            abort( 500, message="An error accured while insserting the tag.")
        
        return tag
    @blp.response(201, TagAndItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
        
            db.session.add(item)
            db.session.commit
        except SQLAlchemyError:
            abort( 500, message="An error accured while insserting the tag.")
        
        return {"message": "Item removed from tag", "item":item, "tag":tag}


@blp.route("/tag/<string:tag_id>")
class tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or404(tag_id)
        return tag
    
    @blp.response(202, description=" Delete a tag if no item is tagged")

    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more item. In this case , the tag  is not deleted "
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return{"message": "Tag deleted"}

    
