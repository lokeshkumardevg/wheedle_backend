from flask import Blueprint, request, jsonify
import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from ..utils.serializer import serialize_docs

testimonial_bp = Blueprint('testimonial', __name__)

UPLOAD_FOLDER = 'uploads/'

@testimonial_bp.route('/', methods=['POST'])
def create_testimonial():
    try:
        name = request.form.get('name')
        message = request.form.get('message')
        # ... additional fields if any
        
        data = {
            'name': name,
            'message': message,
            'createdAt': datetime.utcnow(),
        }

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data['image'] = filename

        from ..db import mongo
        mongo.db.testimonials.insert_one(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@testimonial_bp.route('/', methods=['GET'])
def get_testimonials():
    try:
        from ..db import mongo
        testimonials = list(mongo.db.testimonials.find().sort('createdAt', -1))
        return jsonify(serialize_docs(testimonials))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@testimonial_bp.route('/<id>', methods=['DELETE'])
def delete_testimonial(id):
    try:
        from ..db import mongo
        mongo.db.testimonials.delete_one({"_id": ObjectId(id)})
        return jsonify({'success': True, 'message': 'Deleted'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@testimonial_bp.route('/count/all', methods=['GET'])
def get_testimonial_count():
    try:
        from ..db import mongo
        count = mongo.db.testimonials.count_documents({})
        return jsonify({'count': count})
    except Exception:
        return jsonify({'count': 0}), 500
