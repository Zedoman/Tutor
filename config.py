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
  ]
