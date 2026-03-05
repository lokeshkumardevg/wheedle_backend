from flask import Blueprint, request, jsonify
import os
import time
from ..models import Job
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from ..utils.serializer import serialize_docs

job_bp = Blueprint('job', __name__)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@job_bp.route('/', methods=['POST'])
def create_job():
    try:
        title = request.form.get('title')
        jobType = request.form.get('jobType')
        description = request.form.get('description')
        
        job_data = {
            'title': title,
            'jobType': jobType,
            'description': description,
        }

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                job_data['image'] = filename
        else:
            job_data['image'] = ""

        Job.create(job_data)
        
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@job_bp.route('/', methods=['GET'])
def get_jobs():
    try:
        jobs = Job.find_all()
        return jsonify(serialize_docs(jobs))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@job_bp.route('/<id>', methods=['DELETE'])
def delete_job(id):
    try:
        from ..db import mongo
        mongo.db.jobs.delete_one({"_id": ObjectId(id)})
        return jsonify({'message': 'Job deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@job_bp.route('/count/all', methods=['GET'])
def get_job_count():
    try:
        from ..db import mongo
        count = mongo.db.jobs.count_documents({})
        return jsonify({'count': count})
    except Exception as e:
        print("GET JOB COUNT ERROR:", e)
        return jsonify({'message': str(e)}), 500
