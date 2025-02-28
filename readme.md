# Decentralized EtherEd AI

A decentralized, AI-driven tutoring platform leveraging blockchain for secure payments and progress tracking, powered by Groq's LLAMA3 AI and built with Python Flask and Solidity.

## Overview
The Decentralized AI-Powered Tutor is an innovative educational tool that combines artificial intelligence with blockchain technology to deliver personalized tutoring. It adapts to a user's learning needs, handles payments via Ethereum smart contracts, and tracks progress on-chain for transparency and immutability. Recent enhancements include achievement badges, a dynamic avatar system, voice input, a real-time leaderboard, and celebratory confetti animations.

## Key Features
- **Personalized Learning:** Uses Groq's LLAMA3 AI to provide tailored responses based on student queries and progress.
- **Blockchain Integration:** Smart contracts manage tutoring session payments (in ETH), store progress, award badges, and log chat history securely on the Ethereum blockchain.
- **Lifetime Chat History:** Chat history is stored on-chain, tied to the user's Ethereum address, allowing users to access their conversations indefinitely.
- **Scalable Design:** Built with Python Flask for the backend, making it easy to extend or integrate with other systems.
- **Decentralized Trust:** No central authority; payments, progress, achievements, and chat history are verifiable on-chain.
- **Futuristic Cyberpunk UI:** Features a neon-themed, cyberpunk-inspired frontend with holographic effects, animated backgrounds, glowing buttons, and a dynamic sidebar—designed to impress with a sci-fi aesthetic.
- **Interactive Features:** Includes a dynamic avatar system, voice input, a real-time leaderboard, achievement badges, celebratory confetti animations, and a ChatGPT-style sidebar for path-based chat history.

## Why It Stands Out
- Addresses real-world education challenges with adaptive AI tutoring and gamification.
- Demonstrates practical blockchain use beyond finance (payments, data integrity, and achievements).
- Modular, professional codebase with a stunning, interactive UI, ready for hackathon demos or production scaling.

## Tech Stack
- **AI:** Groq LLAMA3
- **Backend:** Python Flask
- **Blockchain:** Solidity (smart contracts), Ethereum (via Web3.py), Truffle (deployment)
- **Frontend:** HTML/CSS/JavaScript with dynamic features (avatars, badges, confetti)
- **Local Development:** Ganache (local Ethereum blockchain)

## Project Structure
```
Decentralized-AI-Tutor/
├── blockchain/                  # Solidity smart contracts and deployment
│   ├── contracts/
│   │   └── TutorContract.sol   # Main smart contract with badges
│   ├── migrations/
│   │   └── 1_deploy.js         # Truffle deployment script
│   └── truffle-config.js       # Truffle configuration                  
├── backend/                    # Flask backend
│   ├── app.py                  # Main Flask app
│   ├── gemini_client.py        # LLAMA3 AI integration
│   ├── blockchain_client.py    # Blockchain interaction
│   ├── config.py               # Configuration (API keys, ABI)
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Static frontend
│   └── index.html             # Interactive UI with avatars, badges, voice, leaderboard, confetti
├── README.md                   # Project documentation
└── .env                        # Environment variables
```

## Prerequisites
- **Node.js & npm:** For Truffle, Ganache, and Solidity
  ```sh
  npm install -g truffle ganache-cli solc
  brew tap ethereum/ethereum
  brew install solidity
  ```
- **Python 3.11:** For Flask and Web3.py
  ```sh
  pip install -r requirements.txt
  ```
- **Ganache:** Local Ethereum blockchain
  ```sh
  npm install -g ganache-cli
  ```
- **Truffle:** Smart contract development framework
  ```sh
  npm install -g truffle
  ```

## Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/Zedoman/Tutor
cd Tutor
```
### 2. Install Dependencies
#### Blockchain
```sh
cd blockchain
npm install
```
#### Backend
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
PRIVATE_KEY=0xYourGanachePrivateKeyHere
CONTRACT_ADDRESS=0xYourDeployedContractAddress
STUDENT_PRIVATE_KEY=0xYourStudentPrivateKeyHere
```
### 4. Deploy the Smart Contract
Compile the contract:
```sh
truffle compile
```
Start Ganache:
```sh
ganache-cli
```
Deploy the contract:
```sh
cd blockchain
truffle migrate --network development
```
Update `.env` with `CONTRACT_ADDRESS` from the logs.

### 5. Update `config.py`
Copy the ABI from `blockchain/build/contracts/TutorContract.json` into `backend/config.py` under `CONTRACT_ABI`.

### 6. Run the Backend
```sh
cd backend
python app.py
```
Flask runs on `http://127.0.0.1:5000/`.

## Usage
### Access the Frontend
Open `http://127.0.0.1:5000/` in your browser.

### Interact with the Tutor
1. **Enter Ethereum Address:** Manually input a valid Ethereum address (e.g., from Ganache).
2. **Ask a Question:** Type or use voice input for an educational query (e.g., "What is Python?").
3. **Select Payment:** Choose an ETH amount (e.g., 0.01 ETH) or "No Payment".
4. **Submit:** Receive AI-generated responses, track progress, earn badges, and see updates on the dashboard.

### Check Progress
```sh
curl -X GET http://127.0.0.1:5000/stats/0xYourEthereumAddress
```

## How It Works
### Architecture
- **Frontend:** Sends POST requests to `/tutor` with Ethereum address, question, and payment amount.
- **Backend (Flask):**
  - Queries blockchain for the student’s progress, score, sessions, balance, and badges.
  - Calls Groq LLAMA3 with query and progress context.
  - Processes payments and updates progress on-chain via the smart contract.
  - Returns AI response and updated stats.
- **Blockchain:** `TutorContract.sol` handles ETH payments, progress tracking, scores, and badges.

### API Endpoints
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | Serves the interactive `index.html` | None |
| `/tutor` | POST | Processes a tutoring session | `student_address`, `prompt`, `eth_amount` (JSON) |
| `/stats/<address>` | GET | Retrieves student stats | `address` (path parameter) |

#### Example Request
```sh
curl -X POST http://127.0.0.1:5000/tutor \
-H "Content-Type: application/json" \
-d '{"student_address": "0xYourEthereumAddress", "prompt": "What is blockchain?", "eth_amount": "10000000000000000"}'
```
#### Example Response
```json
{
  "response": "Blockchain is a decentralized ledger technology...",
  "progress": 1,
  "score": 1,
  "sessions": 1,
  "balance": 0.01,
  "badges": [1]
}
```

## Future Enhancements
- **Token Rewards:** Introduce a custom ERC-20 token for rewarding students.
- **Multi-Tutor Support:** Extend the contract to support multiple tutors.
- **Chat History Optimization:** Implement batching or off-chain indexing (e.g., The Graph) to optimize lifetime chat history storage on mainnet.
- **Enhanced UI Interactions:** Add more interactive animations, 3D elements, and particle effects to further elevate the cyberpunk design.
- **UI Framework Upgrade:** Replace the frontend with a React/Vue app for a richer, more responsive experience.
- **Payment Integration:** Add MetaMask support for real ETH payments.
