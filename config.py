import os
from dotenv import load_dotenv

print(f"Looking for .env at: {os.path.abspath('.env')}")
load_dotenv(override=True)

class Config:
    ETH_NODE_URL = "http://127.0.0.1:8545"  # Ganache URL
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    STUDENT_PRIVATE_KEY = os.getenv("STUDENT_PRIVATE_KEY")
    # print(f"Loaded CONTRACT_ADDRESS: {CONTRACT_ADDRESS}")
    # print(f"Loaded PRIVATE_KEY: {PRIVATE_KEY}")
    CONTRACT_ABI = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "badgeId",
          "type": "uint256"
        }
      ],
      "name": "BadgeEarned",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "challengeId",
          "type": "uint256"
        }
      ],
      "name": "ChallengeCompleted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "prompt",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "response",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "path",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "ChatMessage",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "lessons",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "score",
          "type": "uint256"
        }
      ],
      "name": "ProgressUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "SessionPaid",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "badges",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "balances",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "challengesCompleted",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "learningPath",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "sessionCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "sessionFee",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "studentProgress",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "studentScores",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "payForSession",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function",
      "payable": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "lessons",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "score",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "path",
          "type": "uint256"
        }
      ],
      "name": "updateProgress",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "challengeId",
          "type": "uint256"
        }
      ],
      "name": "completeChallenge",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "student",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "prompt",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "response",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "path",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "storeChatMessage",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "withdraw",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "student",
          "type": "address"
        }
      ],
      "name": "getStudentStats",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "lessons",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "score",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "sessions",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "balance",
          "type": "uint256"
        },
        {
          "internalType": "uint256[]",
          "name": "badgeIds",
          "type": "uint256[]"
        },
        {
          "internalType": "uint256",
          "name": "path",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "challenges",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]