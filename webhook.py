from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_chat():
    data = request.json
    # You could store this to DB or notify Slack/CRM
    print("Lead Info:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)