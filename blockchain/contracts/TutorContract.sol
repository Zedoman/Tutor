// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TutorContract {
    address public owner;
    uint public sessionFee = 0.01 ether;
    mapping(address => uint) public studentProgress; // Lessons completed
    mapping(address => uint) public studentScores;   // Knowledge score
    mapping(address => uint) public balances;        // ETH paid by student
    mapping(address => uint) public sessionCount;    // Number of sessions
    mapping(address => uint[]) public badges;        // Array of badge IDs
    mapping(address => uint) public learningPath;    // 0: None, 1: Python, 2: Blockchain
    mapping(address => uint) public challengesCompleted; // Track challenge completions

    event SessionPaid(address indexed student, uint amount);
    event ProgressUpdated(address indexed student, uint lessons, uint score);
    event BadgeEarned(address indexed student, uint badgeId);
    event ChallengeCompleted(address indexed student, uint challengeId);
    event ChatMessage(
        address indexed student,
        string prompt,
        string response,
        uint path,
        uint timestamp
    ); // New event for chat history

    constructor() {
        owner = msg.sender;
    }

    function payForSession() external payable {
        require(msg.value >= sessionFee, "Insufficient payment");
        balances[msg.sender] += msg.value;
        sessionCount[msg.sender] += 1;
        emit SessionPaid(msg.sender, msg.value);
        _checkBadges(msg.sender);
    }

    function updateProgress(address student, uint lessons, uint score, uint path) external {
        require(msg.sender == owner, "Only owner can update progress");
        studentProgress[student] = lessons;
        studentScores[student] += score;
        if (path > 0 && path <= 2) learningPath[student] = path;
        emit ProgressUpdated(student, lessons, score);
        _checkBadges(student);
    }

    function completeChallenge(address student, uint challengeId) external {
        require(msg.sender == owner, "Only owner can complete challenges");
        challengesCompleted[student] += 1;
        if (challengesCompleted[student] % 3 == 0) {
            badges[student].push(3); // Badge ID 3: 3 Challenges
            emit BadgeEarned(student, 3);
        }
        emit ChallengeCompleted(student, challengeId);
    }

    function storeChatMessage(
        address student,
        string memory prompt,
        string memory response,
        uint path,
        uint timestamp
    ) external {
        require(msg.sender == owner, "Only owner can store chat messages");
        emit ChatMessage(student, prompt, response, path, timestamp);
    }

    function _checkBadges(address student) internal {
        if (studentProgress[student] >= 5 && badges[student].length == 0) {
            badges[student].push(1); // Badge ID 1: 5 Lessons
            emit BadgeEarned(student, 1);
        }
        if (balances[student] >= 0.1 ether && badges[student].length < 2) {
            badges[student].push(2); // Badge ID 2: 0.1 ETH Spent
            emit BadgeEarned(student, 2);
        }
    }

    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        uint balance = address(this).balance;
        payable(owner).transfer(balance);
    }

    function getStudentStats(address student) external view returns (uint lessons, uint score, uint sessions, uint balance, uint[] memory badgeIds, uint path, uint challenges) {
        return (studentProgress[student], studentScores[student], sessionCount[student], balances[student], badges[student], learningPath[student], challengesCompleted[student]);
    }
}