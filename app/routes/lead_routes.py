from flask import Blueprint, request, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from ..utils.serializer import serialize_docs

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/', methods=['POST'])
def create_lead():
    try:
        data = request.get_json()
        value = data.get('value')
        data['createdAt'] = datetime.utcnow()
        from ..db import mongo
        
        existing = mongo.db.leads.find_one({"value": value})
        if existing:
            return jsonify({'success': False, 'message': 'Lead already exists'}), 400
            
        mongo.db.leads.insert_one(data)
        return jsonify({'success': True, 'message': 'Lead saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@leads_bp.route('/', methods=['GET'])
def get_all_leads():
    try:
        from ..db import mongo
        leads = list(mongo.db.leads.find().sort('createdAt', -1))
        return jsonify(serialize_docs(leads))
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@leads_bp.route('/<id>', methods=['PUT'])
def update_lead_status(id):
    try:
        data = request.get_json()
        status = data.get('status')
        from ..db import mongo
        mongo.db.leads.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@leads_bp.route('/<id>', methods=['DELETE'])
def delete_lead(id):
    try:
        from ..db import mongo
        mongo.db.leads.delete_one({"_id": ObjectId(id)})
        return jsonify({'success': True, 'message': 'Lead deleted'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@leads_bp.route('/count/all', methods=['GET'])
def get_leads_count():
    try:
        from ..db import mongo
        count = mongo.db.leads.count_documents({})
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
