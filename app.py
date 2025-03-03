from flask import Flask, request, jsonify, send_from_directory
from GroqClient import GroqClient
from blockchain_client import BlockchainClient
from config import Config
import json
import datetime
import traceback

app = Flask(__name__, static_folder="./frontend", static_url_path="")
groq_client = GroqClient()
blockchain = BlockchainClient()

# In-memory chat history storage (for demo, reset on restart)
chat_history = {}  # {student_address: {path: [messages]}}

# Helper function to check if prompt matches the path
def validate_prompt_for_path(prompt, path):
    prompt_lower = prompt.lower()
    
    if path == 1:  # DSA only
        dsa_keywords = [
    "data structure", "algorithm", "binary search", "sorting", "graph", "tree", "linked list", 
    "stack", "queue", "hash", "hashing", "hashmap", "hashtable", "set", "map", "array", "matrix",
    "dp", "dynamic programming", "greedy", "divide and conquer", "backtracking", "recursion", 
    "iterative", "bfs", "dfs", "breadth first search", "depth first search", "topological sort", 
    "shortest path", "dijkstra", "bellman-ford", "floyd-warshall", "kruskal", "prim", "mst", 
    "minimum spanning tree", "union find", "disjoint set", "trie", "segment tree", "fenwick tree", 
    "binary indexed tree", "heap", "priority queue", "binary tree", "bst", "binary search tree", 
    "avl tree", "red-black tree", "b tree", "b+ tree", "suffix tree", "suffix array", "knapsack", 
    "lcs", "longest common subsequence", "lis", "longest increasing subsequence", "edit distance", 
    "string matching", "kmp", "knuth-morris-pratt", "rabin-karp", "two pointers", "sliding window", 
    "merge sort", "quick sort", "heap sort", "bubble sort", "insertion sort", "selection sort", 
    "radix sort", "bucket sort", "counting sort", "big o", "time complexity", "space complexity", 
    "asymptotic notation", "recurrence relation", "master theorem", "floyd cycle", "tortoise hare", 
    "kadane", "maximum subarray", "n queen", "sudoku", "permutation", "combination", "bit manipulation", 
    "bitmask", "xor", "and operation", "or operation", "bitwise", "graph traversal", "cycle detection", 
    "connected components", "strongly connected components", "tarjan", "kosaraju", "articulation point", 
    "bridge edge", "eulerian path", "hamiltonian path", "flow network", "max flow", "min cut", 
    "ford-fulkerson", "bipartite graph", "matching", "hungarian algorithm"
]
        if not any(keyword in prompt_lower for keyword in dsa_keywords):
            return False, "Please ask a DSA-related question (e.g., about sorting, graphs, or dynamic programming)."
    
    elif path == 2:  # Programming
        programming_keywords = [
    "code", "coding", "programming", "debug", "debugging", "syntax", "function", "variable", "loop", 
    "class", "object", "javascript", "java", "c++", "cpp", "ruby", "sql", "html", "css", "python", 
    "go", "golang", "rust", "typescript", "php", "swift", "kotlin", "scala", "perl", "r language", 
    "matlab", "shell", "bash", "powershell", "perl", "lua", "dart", "assembly", "asm", "c#", "csharp", 
    "vb", "visual basic", "f#", "erlang", "elixir", "haskell", "clojure", "lisp", "fortran", "cobol", 
    "pascal", "delphi", "ada", "ocaml", "prolog", "script", "program", "compile", "compiler", "interpret", 
    "interpreter", "runtime", "exception", "error handling", "try catch", "throw", "finally", "stack trace", 
    "memory leak", "pointer", "reference", "dereference", "memory management", "garbage collection", 
    "heap memory", "stack memory", "thread", "multithreading", "concurrency", "parallel", "async", 
    "asynchronous", "promise", "callback", "event loop", "closure", "scope", "lexical scope", "hoisting", 
    "inheritance", "polymorphism", "encapsulation", "abstraction", "interface", "abstract class", "method", 
    "constructor", "destructor", "getter", "setter", "property", "static method", "instance", "singleton", 
    "factory pattern", "observer pattern", "strategy pattern", "decorator pattern", "mvc", "model view controller", 
    "rest api", "graphql", "http request", "json", "xml", "yaml", "database", "query", "orm", "object relational mapping", 
    "crud", "create read update delete", "regex", "regular expression", "unit test", "testing", "tdd", 
    "test driven development", "mock", "stub", "framework", "library", "package", "module", "import", 
    "export", "dependency", "pip", "npm", "yarn", "maven", "gradle", "docker", "container", "virtual machine", 
    "devops", "ci cd", "continuous integration", "continuous deployment", "git", "version control", "commit", 
    "branch", "merge", "pull request", "repository", "frontend", "backend", "full stack", "web development", 
    "mobile development", "app development", "cross platform", "ide", "integrated development environment", 
    "vscode", "visual studio", "eclipse", "intellij", "pycharm", "sublime", "atom", "jupyter", "notebook"
]
        if not any(keyword in prompt_lower for keyword in programming_keywords):
            return False, "Please ask a programming-related question (e.g., about coding, debugging, or syntax)."
    
    elif path == 3:  # BlockChain
        blockchain_keywords = ["blockchain", "ethereum", "smart contract", "crypto", "bitcoin", "decentralized", "ledger", "token", "web3", "dapp"]
        if not any(keyword in prompt_lower for keyword in blockchain_keywords):
            return False, "Please ask a blockchain-related question (e.g., about Ethereum, smart contracts, or decentralization)."
    
    elif path == 4:  # Non Tech field (Aerospace, Mechanical, Electrical)
        non_tech_keywords = [
    "aerospace", "mechanical", "electrical", "aerodynamics", "thermodynamics", "robotics", "circuits", 
    "motors", "avionics", "engineering", "aeronautical", "astronautical", "flight dynamics", "lift", "drag", 
    "thrust", "propulsion", "jet engine", "turbine", "rocket", "spacecraft", "satellite", "orbit", "trajectory", 
    "reentry", "thermal protection", "guidance system", "navigation", "control system", "aerofoil", "wing", 
    "fuselage", "empennage", "stability", "control surface", "flaps", "ailerons", "rudder", "elevator", 
    "wind tunnel", "computational fluid dynamics", "cfd", "mach number", "supersonic", "hypersonic", 
    "transonic", "laminar flow", "turbulent flow", "boundary layer", "nozzle", "combustion", "fuel system", 
    "mechanical design", "cad", "computer aided design", "solidworks", "autodesk", "finite element analysis", 
    "fea", "stress analysis", "strain", "material science", "mechanics", "statics", "dynamics", "kinematics", 
    "vibration", "fatigue", "fracture mechanics", "manufacturing", "cnc", "machining", "3d printing", 
    "additive manufacturing", "welding", "fabrication", "assembly", "gear", "bearing", "shaft", "lever", 
    "pulley", "cam", "spring", "piston", "crankshaft", "flywheel", "hydraulics", "pneumatics", "pump", 
    "valve", "actuator", "sensor", "control engineering", "pid controller", "feedback loop", "servo", 
    "stepper motor", "dc motor", "ac motor", "induction motor", "synchronous motor", "transformer", 
    "capacitor", "resistor", "inductor", "diode", "transistor", "mosfet", "bjt", "op amp", "operational amplifier", 
    "circuit design", "pcb", "printed circuit board", "schematic", "breadboard", "multimeter", "oscilloscope", 
    "signal processing", "filter", "amplifier", "rectifier", "inverter", "converter", "power supply", "ac dc", 
    "dc ac", "voltage", "current", "resistance", "ohm's law", "kirchhoff's law", "thevenin", "norton", 
    "superposition", "maxwell's equations", "electromagnetism", "magnetic field", "electric field", "faraday's law", 
    "induction", "generator", "alternator", "battery", "solar panel", "renewable energy", "power electronics", 
    "microcontroller", "arduino", "raspberry pi", "embedded system", "iot", "internet of things", "automation", 
    "plc", "programmable logic controller", "scada", "supervisory control", "relay", "switchgear", "fuse", 
    "circuit breaker", "grounding", "earthing", "lightning protection", "hvac", "heating ventilation", "air conditioning"
]
        if not any(keyword in prompt_lower for keyword in non_tech_keywords):
            return False, "Please ask a question related to Aerospace, Mechanical, or Electrical fields (e.g., about aerodynamics, circuits, or robotics)."
    
    elif path == 5:  # Random (no studies/tech)
        study_tech_keywords = [
    "study", "learn", "code", "coding", "programming", "blockchain", "dsa", "data structure", "algorithm", 
    "python", "javascript", "ethereum", "java", "c++", "cpp", "ruby", "sql", "html", "css", "go", "golang", 
    "rust", "typescript", "php", "swift", "kotlin", "scala", "perl", "r language", "matlab", "shell", "bash", 
    "powershell", "lua", "dart", "assembly", "asm", "c#", "csharp", "vb", "visual basic", "f#", "erlang", 
    "elixir", "haskell", "clojure", "lisp", "fortran", "cobol", "pascal", "delphi", "ada", "ocaml", "prolog", 
    "script", "program", "compile", "compiler", "interpret", "interpreter", "runtime", "exception", 
    "error handling", "debug", "debugging", "syntax", "function", "variable", "loop", "class", "object", 
    "smart contract", "crypto", "cryptocurrency", "bitcoin", "decentralized", "ledger", "token", "web3", 
    "dapp", "solidity", "vyper", "truffle", "hardhat", "ganache", "metamask", "wallet", "private key", 
    "public key", "address", "transaction", "gas", "mining", "proof of work", "proof of stake", "consensus", 
    "aerospace", "mechanical", "electrical", "aerodynamics", "thermodynamics", "robotics", "circuits", 
    "motors", "avionics", "engineering", "aeronautical", "astronautical", "flight dynamics", "propulsion", 
    "jet engine", "rocket", "spacecraft", "satellite", "mechanical design", "cad", "finite element analysis", 
    "kinematics", "vibration", "manufacturing", "cnc", "hydraulics", "pneumatics", "transformer", "capacitor", 
    "resistor", "diode", "transistor", "circuit design", "power electronics", "microcontroller", "arduino", 
    "embedded system", "iot", "automation", "plc", "scada", "math", "mathematics", "algebra", "calculus", 
    "geometry", "trigonometry", "probability", "statistics", "linear algebra", "differential equations", 
    "physics", "chemistry", "biology", "science", "experiment", "research", "education", "school", "university", 
    "college", "exam", "test", "quiz", "homework", "assignment", "project", "lecture", "lesson", "course", 
    "curriculum", "syllabus", "teacher", "professor", "student", "learn", "learning", "knowledge", "academic", 
    "study material", "textbook", "paper", "thesis", "dissertation", "software", "hardware", "network", 
    "database", "server", "client", "api", "rest api", "graphql", "json", "xml", "yaml", "cloud", "aws", 
    "azure", "gcp", "docker", "kubernetes", "devops", "ci cd", "git", "version control", "machine learning", 
    "ai", "artificial intelligence", "deep learning", "neural network", "data science", "big data", "analytics", 
    "cybersecurity", "hacking", " penetration testing", "encryption", "security", "password", "authentication", 
    "authorization", "oauth", "jwt", "token", "frontend", "backend", "full stack", "web development", 
    "mobile development", "app development", "ide", "vscode", "visual studio", "eclipse", "intellij"
]
        if any(keyword in prompt_lower for keyword in study_tech_keywords):
            return False, "Please ask a casual, non-study-related question (e.g., about movies, hobbies, or fun topics)."
    
    return True, ""

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
        if path not in [1, 2, 3, 4, 5]:  # Updated path validation
            path = 1  # Default to No Path if invalid
        print(f"Parsed path: {path}")

        print(f"Parsed data - student_address: {student_address}, prompt: {prompt}, eth_amount: {eth_amount}, path: {path}")

        if not student_address or not prompt:
            return jsonify({"error": "Missing student address or prompt"}), 400
        
        # Validate prompt against path rules
        is_valid, error_message = validate_prompt_for_path(prompt, path)
        if not is_valid:
            return jsonify({"custom error": error_message}), 400

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
        # Define path-specific context
        path_context = {
            1: "DSA only - Answer questions strictly about Data Structures and Algorithms (e.g., sorting, graphs, dynamic programming). Refuse to answer non-DSA questions.",
            2: "Programming - Answer questions strictly about programming (e.g., coding, debugging, syntax, any language). Refuse to answer non-programming questions.",
            3: "BlockChain - Answer questions strictly about blockchain (e.g., Ethereum, smart contracts, decentralization). Refuse to answer non-blockchain questions.",
            4: "Non Tech field - Answer questions strictly about Aerospace, Mechanical, or Electrical fields (e.g., aerodynamics, circuits, robotics). Refuse to answer questions outside these fields.",
            5: "Random - Engage in casual conversation only (e.g., about movies, hobbies, fun topics). Refuse to answer any study-related or tech-related questions."
        }
        # Get AI response with path-specific context
        context = f"Lessons completed: {lessons}, Path: {path_context[path]}"
        response = groq_client.get_tutoring_response(prompt, context)
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