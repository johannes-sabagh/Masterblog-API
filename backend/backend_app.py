from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        new_id = max((post['id'] for post in POSTS), default=0)+1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201

    return jsonify(POSTS), 200

@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def delete_post(post_id):
    global POSTS
    if request.method == 'DELETE':
        post_to_delete = next((post for post in POSTS if post['id'] == post_id))
        if post_to_delete:
            POSTS = [p for p in POSTS if p['id'] != post_id]
            return jsonify(post_to_delete)
        else:
            return 'not found'
    elif request.method == 'PUT':
        post_to_update = next((post for post in POSTS if post['id'] == post_id))
        if post_to_update:
            title = request.get_json()['title']
            content = request.get_json()['content']
            post_to_update['title'] = title
            post_to_update['content'] = content
            return jsonify(post_to_update)
        else:
            return 'not found'
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)
