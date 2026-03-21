from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]



@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200



@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "title and content are required"}), 400

    new_id = max((post['id'] for post in POSTS), default=0) + 1
    new_post = {"title": data["title"], "content": data["content"], "id": new_id}
    POSTS.append(new_post)
    return jsonify(new_post), 201



@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS

    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_delete:
        POSTS = [p for p in POSTS if p['id'] != post_id]
        return jsonify(post_to_delete)
    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "title and content are required"}), 400

    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_update:

        post_to_update['title'] = data['title']
        post_to_update['content'] = data['content']
        return jsonify(post_to_update)
    else:
        return jsonify({"error": "Post not found"}), 404



@app.route('/api/posts/search')
def find_post():
    found_posts = []
    title = request.args.get('title', '')
    content = request.args.get('content', '')

    for post in POSTS:
        if (title and title in post['title']) or (content and content in post['content']):
            found_posts.append(post)

    return jsonify(found_posts)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)
