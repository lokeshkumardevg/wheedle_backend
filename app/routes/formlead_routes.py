from flask import Blueprint, request, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from ..utils.serializer import serialize_docs

formleads_bp = Blueprint('formleads', __name__)

@formleads_bp.route('/', methods=['POST'])
def create_form_lead():
    try:
        data = request.get_json()
        data['createdAt'] = datetime.utcnow()
        from ..db import mongo
        mongo.db.formleads.insert_one(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@formleads_bp.route('/', methods=['GET'])
def get_all_form_leads():
    try:
        from ..db import mongo
        leads = list(mongo.db.formleads.find().sort('createdAt', -1))
        return jsonify(serialize_docs(leads))
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@formleads_bp.route('/count/all', methods=['GET'])
def get_form_leads_count():
    try:
        from ..db import mongo
        count = mongo.db.formleads.count_documents({})
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@formleads_bp.route('/<id>', methods=['PUT'])
def update_form_lead_status(id):
    try:
        data = request.get_json()
        status = data.get('status')
        from ..db import mongo
        mongo.db.formleads.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@formleads_bp.route('/<id>', methods=['DELETE'])
def delete_form_lead(id):
    try:
        from ..db import mongo
        mongo.db.formleads.delete_one({"_id": ObjectId(id)})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
