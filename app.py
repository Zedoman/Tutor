from flask import Flask, request, jsonify, send_from_directory
from GroqClient import GroqClient
from blockchain_client import BlockchainClient
from config import Config
import json
import datetime
import traceback

app = Flask(__name__, static_folder="./frontend", static_url_path="", )
groq_client = GroqClient()
blockchain = BlockchainClient()

# In-memory chat history storage (for demo, reset on restart)
chat_history = {}  # {student_address: {path: [messages]}}

# Serve index.html at the root URL
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index_new.html")

@app.route("/tutor", methods=["POST"])
def tutor_session():
    data = request.json
    print(f"Raw request data: {data}")

    try:
        student_address = data.get("student_address")
        prompt = data.get("prompt")
        eth_amount_raw = data.get("eth_amount", "0")
        eth_amount = int(eth_amount_raw) if eth_amount_raw else 0
        path = int(data.get("path", "0"))  # Default to "0" as string, then convert
        if path not in [0, 1, 2]:
            path = 0  # Default to No Path if invalid
        print(f"Parsed path: {path}")

        print(f"Parsed data - student_address: {student_address}, prompt: {prompt}, eth_amount: {eth_amount}, path: {path}")

        if not student_address or not prompt:
            return jsonify({"error": "Missing student address or prompt"}), 400

        stats = blockchain.get_stats(student_address)
        lessons, score, sessions, balance, badge_ids, current_path, challenges = stats
        print(f"Current stats: lessons={lessons}, score={score}, sessions={sessions}, balance={balance}, badges={badge_ids}, path={current_path}, challenges={challenges}")

        if eth_amount > 0:
            print(f"Attempting payment of {eth_amount} wei for {student_address}")
            student_private_key = Config.STUDENT_PRIVATE_KEY
            if not student_private_key:
                return jsonify({"error": "Student private key not configured in .env"}), 400

            tx = blockchain.pay_for_session(student_address, eth_amount)
            print(f"Transaction built: {tx}")
            signed_tx = blockchain.w3.eth.account.sign_transaction(tx, student_private_key)
            print(f"Transaction signed with student key")
            try:
                tx_hash = blockchain.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                receipt = blockchain.w3.eth.wait_for_transaction_receipt(tx_hash)
                print(f"Payment tx hash: {tx_hash.hex()}, Receipt: {receipt}")
            except Exception as e:
                print(f"Transaction failed: {str(e)}")
                return jsonify({"error": f"Payment failed: {str(e)}"}), 400

        # Get AI response with path context
        response = groq_client.get_tutoring_response(prompt, f"Lessons completed: {lessons}, Path: {'Python' if path == 1 else 'Blockchain' if path == 2 else 'None'}")
        question_complexity = min(len(prompt) // 10, 10)

        # Update progress with path
        blockchain.update_progress(student_address, lessons + 1, question_complexity, path)

        # Simulate a challenge (e.g., every 3rd lesson)
        if (lessons + 1) % 3 == 0:
            blockchain.complete_challenge(student_address, (lessons + 1) // 3)

        # Store chat history
        # if student_address not in chat_history:
        #     chat_history[student_address] = {}
        # if path not in chat_history[student_address]:
        #     chat_history[student_address][path] = []
        # chat_history[student_address][path].append({
        #     "prompt": prompt,
        #     "response": response,
        #     "timestamp": str(datetime.datetime.now()),
        #     "path": path
        # })
        # print(f"Storing chat for path: {path}")
        # print(f"Chat history for {student_address}, path {path}: {chat_history[student_address][path]}")

        # Store chat history on-chain
        timestamp = int(datetime.datetime.now().timestamp())
        # print(f"Before storing chat message: student={student_address}, prompt={prompt}, response={response}, path={path}, timestamp={timestamp}")
        # blockchain.store_chat_message(student_address, prompt, response, path, timestamp)
        # print(f"Chat message stored successfully for {student_address}, path {path}")
        print(f"Attempting to store chat message: student={student_address}, prompt={prompt}, response={response}, path={path}, timestamp={timestamp}")
        try:
            blockchain.store_chat_message(student_address, prompt, response, path, timestamp)
            print(f"Chat message stored successfully for {student_address}, path {path}")
        except Exception as e:
            print(f"Failed to store chat message: {str(e)}")
            return jsonify({"error": f"Failed to store chat message: {str(e)}"}), 500

        return jsonify({
            "response": response,
            "progress": lessons + 1,
            "score": score + question_complexity,
            "sessions": sessions + 1 if eth_amount > 0 else sessions,
            "balance": (balance + (eth_amount if eth_amount > 0 else 0)) / 10**18,
            "badges": badge_ids,
            "path": path,
            "challenges": challenges
            # "chat_history_all": chat_history.get(student_address, {})  # Send all paths for sidebar
        })

    except Exception as e:
        print(f"Unexpected error in /tutor: {str(e)}")
        print(traceback.format_exc())  # Print stack trace for debugging
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/stats/<student_address>", methods=["GET"])
def get_student_stats(student_address):
    try:
        lessons, score, sessions, balance, badge_ids, path, challenges = blockchain.get_stats(student_address)
        return jsonify({
            "lessons": lessons,
            "score": score,
            "sessions": sessions,
            "balance": balance / 10**18,
            "badges": badge_ids,
            "path": path,
            "challenges": challenges,
            "chat_history_all": chat_history.get(student_address, {})  # Send all paths
        })
    except Exception as e:
        print(f"Error getting stats: {str(e)}")
        return jsonify({"error": f"Stats error: {str(e)}"}), 500

@app.route("/chat-history/<student_address>/<int:path>", methods=["GET"])
def get_chat_history(student_address, path):
    try:
        print(f"Fetching chat history for {student_address}, path {path}")
        # Query the blockchain for ChatMessage events
        chat_events = blockchain.contract.events.ChatMessage.create_filter(
            fromBlock=0,
            argument_filters={"student": student_address}
        )
        # ).get_all_entries()
        print(f"Chat filter created: {chat_events}")
        chat_event = chat_events.get_all_entries()
        print(f"Chat events retrieved: {chat_event}")
        
        history = []
        for event in chat_event:
            event_path = event['args']['path']
            if event_path == path:
                history.append({
                    "prompt": event['args']['prompt'],
                    "response": event['args']['response'],
                    "timestamp": datetime.datetime.fromtimestamp(event['args']['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    "path": event_path
                })
        print(f"Chat history for {student_address}, path {path}: {history}")
        return jsonify({"chat_history": history})
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({"error": f"Error fetching chat history: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)