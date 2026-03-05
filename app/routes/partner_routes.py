from flask import Blueprint, request, jsonify
import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

partner_bp = Blueprint('partner', __name__)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@partner_bp.route('/', methods=['POST'])
def create_partner():
    try:
        from ..db import mongo
        name = request.form.get('name', '')
        data = {
            'name': name,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
        }
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data['logo'] = filename
        elif 'logo' in request.files:
            file = request.files['logo']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data['logo'] = filename

        mongo.db.partners.insert_one(data)
        return jsonify({'success': True, 'message': 'created'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@partner_bp.route('/', methods=['GET'])
def get_partners():
    try:
        from ..db import mongo
        partners = list(mongo.db.partners.find().sort('createdAt', -1))
        for p in partners:
            p['_id'] = str(p['_id'])
            # Normalize date field
            if 'createdAt' in p:
                p['createdAt'] = p['createdAt'].isoformat() if hasattr(p['createdAt'], 'isoformat') else str(p['createdAt'])
            if 'updatedAt' in p:
                p['updatedAt'] = p['updatedAt'].isoformat() if hasattr(p['updatedAt'], 'isoformat') else str(p['updatedAt'])
        return jsonify(partners)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@partner_bp.route('/<id>', methods=['DELETE'])
def delete_partner(id):
    try:
        from ..db import mongo
        mongo.db.partners.delete_one({"_id": ObjectId(id)})
        return jsonify({'message': 'Deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
