const TutorContract = artifacts.require("TutorContract");

module.exports = function (deployer) {
  deployer.deploy(TutorContract);
};