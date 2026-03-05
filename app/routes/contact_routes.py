from flask import Blueprint, request, jsonify
from ..models import Contact
from bson.objectid import ObjectId
from ..utils.serializer import serialize_doc, serialize_docs

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        Contact.create(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@contact_bp.route('/', methods=['GET'])
def get_contacts():
    try:
        contacts = Contact.find_all()
        return jsonify(serialize_docs(contacts))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@contact_bp.route('/count/all', methods=['GET'])
def get_contact_count():
    try:
        from ..db import mongo
        count = mongo.db.contacts.count_documents({})
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@contact_bp.route('/status/<id>', methods=['PUT'])
def update_status(id):
    try:
        data = request.get_json()
        status = data.get('status')
        from ..db import mongo
        updated = mongo.db.contacts.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"status": status}},
            return_document=True
        )
        if updated:
            updated['_id'] = str(updated['_id'])
        return jsonify({'success': True, 'contact': serialize_doc(updated)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@contact_bp.route('/<id>', methods=['DELETE'])
def delete_contact(id):
    try:
        from ..db import mongo
        mongo.db.contacts.delete_one({"_id": ObjectId(id)})
        return jsonify({'success': True, 'message': 'Contact deleted'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
