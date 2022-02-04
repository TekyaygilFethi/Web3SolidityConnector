// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
pragma experimental ABIEncoderV2;
struct Hero {
    string name;
    string lightsaberColor;
    uint256 age;
}

contract SimpleStorage {
    mapping(string => uint256) nameToIndex;
    Hero[] heroes;

    function addHero(
        string memory _name,
        string memory _lightsaberColor,
        uint256 _age
    ) public {
        heroes.push(Hero(_name, _lightsaberColor, _age));
        uint256 idx = heroes.length - 1;
        nameToIndex[_name] = idx;
    }

    function getHero(string memory name) private view returns (Hero memory) {
        uint256 idx = nameToIndex[name];
        Hero memory hero = heroes[idx];

        return hero;
    }

    function getInfoByName(string memory name)
        public
        view
        returns (Hero memory)
    {
        uint256 idx = nameToIndex[name];
        return heroes[idx];
    }
}
