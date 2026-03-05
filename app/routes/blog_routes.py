from flask import Blueprint, request, jsonify
import os
import json
import time
from slugify import slugify
from ..models import Blog
from ..middleware.auth import token_required
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from ..utils.serializer import serialize_doc, serialize_docs

blog_bp = Blueprint('blog', __name__)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@blog_bp.route('/', methods=['POST'])
def create_blog():
    try:
        # Handling multipart form data for file upload
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        blogCategory = request.form.get('blogCategory', '')
        sectionTitles = request.form.get('sectionTitles')
        content = request.form.get('content')
        
        blog_data = {
            'title': title,
            'category': category,
            'description': description,
            'blogCategory': blogCategory,
        }

        if 'blogImage' in request.files:
            file = request.files['blogImage']
            if file.filename != '':
                filename = secure_filename(f"{int(time.time())}-{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                blog_data['blogImage'] = filename
        else:
            blog_data['blogImage'] = ""

        if category == 'comprehensive':
            blog_data['slug'] = slugify(title)
            blog_data['sectionTitles'] = json.loads(sectionTitles) if sectionTitles else []
            blog_data['content'] = json.loads(content) if content else {}

        Blog.create(blog_data)
        
        return jsonify({'success': True, 'blog': str(blog_data.get('_id', ''))}) # Note: MongoDB adds _id during insert

    except Exception as e:
        print("BLOG CREATE ERROR:", e)
        return jsonify({'success': False, 'message': str(e)}), 500

@blog_bp.route('/', methods=['GET'])
def get_blogs():
    try:
        blogs = Blog.find_all()
        results = serialize_docs(blogs)
        # Normalize image field
        for blog in results:
            blog['blogImage'] = blog.get('blogImage') or blog.get('image') or ''
        return jsonify(results)
    except Exception as e:
        print('GET BLOGS ERROR:', e)
        return jsonify({'message': str(e)}), 500

@blog_bp.route('/<slug>', methods=['GET'])
def get_blog_by_slug(slug):
    try:
        blog = Blog.find_by_slug(slug)
        if not blog:
            return jsonify({'message': 'Blog not found'}), 404
        return jsonify(serialize_doc(blog))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@blog_bp.route('/<id>', methods=['DELETE'])
def delete_blog(id):
    try:
        # Note: Using find_by_id logic or direct delete
        from ..db import mongo
        mongo.db.blogs.delete_one({"_id": ObjectId(id)})
        return jsonify({'message': 'Deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@blog_bp.route('/count/all', methods=['GET'])
def get_blog_count():
    try:
        from ..db import mongo
        count = mongo.db.blogs.count_documents({})
        return jsonify({'count': count})
    except Exception as e:
        print("GET BLOG COUNT ERROR:", e)
        return jsonify({'message': str(e)}), 500
