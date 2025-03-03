# Decentralized EtherEd AI

A decentralized, AI-driven tutoring platform leveraging blockchain for secure payments and progress tracking, powered by Groq's LLAMA3 AI and built with Python Flask and Solidity.

## Overview
Decentralized EtherEd AI is an innovative educational platform that combines artificial intelligence with blockchain technology to deliver personalized tutoring. It adapts to a user's learning needs, handles payments via Ethereum smart contracts, and tracks progress on-chain for transparency and immutability.

https://github.com/user-attachments/assets/d18b2778-d64e-4658-8349-9e58454348a6

### Recent Enhancements
- **Path-Based Learning Tracks**
- **ChatGPT-Style Sidebar for Chat History**
- **Achievement Badges & Dynamic Avatar System**
- **Voice Input & Real-Time Leaderboard**
- **Celebratory Confetti Animations**
- **Futuristic Cyberpunk UI with Neon Effects**

---

## Key Features

### **Personalized Learning**
Uses Groq's LLAMA3 AI to provide tailored responses based on student queries and progress.

### **Path-Based Learning Tracks**
Supports five distinct learning paths with strict question restrictions:
1. **DSA Only:** For Data Structures and Algorithms (e.g., sorting, graphs, dynamic programming).
2. **Programming:** For coding-related questions (e.g., debugging, syntax, any language).
3. **BlockChain:** For blockchain-related questions (e.g., Ethereum, smart contracts, decentralization).
4. **Non-Tech Field:** For Aerospace, Mechanical, or Electrical questions (e.g., aerodynamics, circuits, robotics).
5. **Random:** For casual, non-study-related conversations (e.g., movies, hobbies, fun topics).

### **ChatGPT-Style Sidebar**
Organizes lifetime chat history by path, allowing users to revisit past conversations with a categorized interface.

### **Blockchain Integration**
- **Smart contracts** manage tutoring session payments (in ETH), store progress, award badges, and log chat history securely on Ethereum.
- **Lifetime Chat History** stored on-chain, tied to the user's Ethereum address, allowing indefinite access.

### **Futuristic Cyberpunk UI**
A neon-themed frontend with:
- Holographic effects
- Animated backgrounds
- Glowing buttons
- Smooth scrolling for a sci-fi aesthetic

### **Interactive Features**
- Dynamic Avatar System
- Voice Input
- Real-Time Leaderboard
- Achievement Badges
- Celebratory Confetti Animations
- Optional Text-to-Speech for Responses

### **Robust Error Handling**
Provides user-friendly messages (e.g., "Hey, this isn't a blockchain-related question!...") ensuring seamless learning.

---

## Why It Stands Out
- **Adaptive AI Tutoring**: Gamified, structured learning paths.
- **Blockchain-Powered Transparency**: Progress, payments, and achievements are immutable.
- **Modular & Scalable**: Flask backend, Ethereum integration, cyberpunk UI.
- **Visually Striking & Technically Advanced**: Cutting-edge AI with sci-fi design.

---

## Tech Stack
- **AI**: Groq LLAMA3
- **Backend**: Python Flask
- **Blockchain**: Solidity (Ethereum Smart Contracts), Web3.py, Truffle
- **Frontend**: HTML/CSS/JavaScript (Interactive UI)
- **Local Development**: Ganache (Local Ethereum Blockchain)

---

## Project Structure
```
Decentralized-EtherEd-AI/
├── blockchain/                  # Solidity smart contracts and deployment
│   ├── contracts/
│   │   └── AITutor.sol         # Main smart contract with badges
│   ├── migrations/
│   │   └── 1_deploy.js         # Truffle deployment script
│   └── truffle-config.js       # Truffle configuration                  
├── backend/                    # Flask backend
│   ├── app.py                  # Main Flask app with path restrictions
│   ├── gemini_client.py        # LLAMA3 AI integration
│   ├── blockchain_client.py    # Blockchain interaction
│   ├── config.py               # Configuration (API keys, ABI)
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Static frontend
│   └── index_new.html          # Cyberpunk UI with sidebar, avatars, badges, leaderboard
├── README.md                   # Project documentation
└── .env                        # Environment variables
```

---

## Prerequisites

### Install Node.js & npm
```
npm install -g truffle ganache-cli solc
brew tap ethereum/ethereum
brew install solidity
```

### Install Python 3.11 & Dependencies
```
pip install -r requirements.txt
```

### Install Ganache (Local Ethereum Blockchain)
```
npm install -g ganache-cli
```

### Install Truffle (Smart Contract Development Framework)
```
npm install -g truffle
```

---

## Setup Instructions

### **1. Clone the Repository**
```
git clone https://github.com/Zedoman/Tutor
cd Tutor
```

### **2. Install Dependencies**
#### Blockchain
```
cd blockchain
npm install
```
#### Backend
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
PRIVATE_KEY=0xYourGanachePrivateKeyHere
CONTRACT_ADDRESS=0xYourDeployedContractAddress
STUDENT_PRIVATE_KEY=0xYourStudentPrivateKeyHere
```

### **4. Deploy the Smart Contract**
Compile the contract:
```
truffle compile
```
Start Ganache:
```
ganache-cli
```
Deploy the contract:
```
cd blockchain
truffle migrate --network development
```
Update `.env` with `CONTRACT_ADDRESS` from the logs.

### **5. Update `config.py`**
Copy the ABI from `blockchain/build/contracts/AITutor.json` into `backend/config.py` under `CONTRACT_ABI`.

### **6. Run the Backend**
```
cd backend
python app.py
```
Flask runs on `http://127.0.0.1:5000/`.

---

## Usage

### **Access the Frontend**
Open `http://127.0.0.1:5000/` in your browser.

### **Interact with the Tutor**
1. **Enter Ethereum Address** (e.g., from Ganache)
2. **Select a Learning Path** (DSA Only, Programming, BlockChain, Non-Tech, Random)
3. **Ask a Question** (Type or use voice input)
4. **Select Payment** (ETH amount or "No Payment")
5. **Submit** (AI response, progress tracking, badges)

### **Access Chat History**
- Sidebar organizes history by path
- Click to view past conversations
- "Speak" button for text-to-speech

### **Check Progress**
```
curl -X GET http://127.0.0.1:5000/stats/0xYourEthereumAddress
```

---

## Future Enhancements
- **Token Rewards**: Introduce a custom ERC-20 token for students.
- **Multi-Tutor Support**: Extend the contract for multiple tutors.
- **Optimized Chat History Storage**: Off-chain indexing with The Graph.
- **Educational Partnerships**: Partner with MOOCs (Coursera, Udemy, Khan Academy) or universities for verified blockchain-backed certificates.
- **MetaMask Integration**: Real ETH transactions.
- **NFT-Based Tutoring Sessions:**: Issue exclusive NFTs granting access to premium AI tutors.
