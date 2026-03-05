from flask import Blueprint, request, jsonify
import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from ..utils.serializer import serialize_docs

steps_bp = Blueprint('steps', __name__)

UPLOAD_FOLDER = 'uploads/'

@steps_bp.route('/', methods=['POST'])
def create_step():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        
        data = {
            'title': title,
            'description': description,
            'createdAt': datetime.utcnow(),
        }

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data['image'] = filename

        from ..db import mongo
        mongo.db.steps.insert_one(data)
        return jsonify(str(data.get('_id', ''))) 
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@steps_bp.route('/', methods=['GET'])
def get_steps():
    try:
        from ..db import mongo
        steps = list(mongo.db.steps.find().sort('createdAt', 1))
        return jsonify(serialize_docs(steps))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@steps_bp.route('/<id>', methods=['DELETE'])
def delete_step(id):
    try:
        from ..db import mongo
        mongo.db.steps.delete_one({"_id": ObjectId(id)})
        return jsonify("Deleted")
    except Exception as e:
        return jsonify({'message': str(e)}), 500
