// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;
pragma abicoder v2;

import "./ERC20.sol";

contract TokenPlace is ERC20("CryptoMonster", "CMON") {

    address owner;

    uint public Time_start;
    uint Time_dif;
    uint Time_now;
    uint Time_system;
    
    uint public PricePublicToken = 0.001 ether;
    uint SeedTokens       = 1000000;
    uint PublicTokens     = 6000000;
    uint PrivateTokens    = 3000000;

    enum Roles { Guest, User, PublicProvider, PrivateProvider, Owner }

    struct User {
        string  Name;       // Имя пользователя
        bytes32 Password;   // пароль пользователя
        Roles   Role;       // роль пользователя
        bool    WhiteList;  // переменная белого листа 
    }

    struct Request {
        string  name;        // Имя пользователя
        address account;     // Адрес аккаунта пользователя в сети ETH
        uint    id;
    }

    mapping (address => User) mapUser;          // данные о пользователях
    mapping (address => uint) mapSeedToken;     // данные об изначальных токенах
    mapping (address => uint) mapPublicToken;   // данные о публичных токенах
    mapping (address => uint) mapPrivateToken;  // данные о приватных токенах
    Request[] requests;                         // массив с запросами

    event Bought(address indexed account, uint amount); // Ивент покупки

    constructor() {
        Time_start  = block.timestamp;
        Time_system = block.timestamp;
        Time_dif    = 0;
        owner       = msg.sender;
        ERC20._mint(owner, 10000000);
 
        mapSeedToken[0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2] = 300000; // Investor1
        mapSeedToken[0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db] = 400000; // Investor2
        mapSeedToken[0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB] = 200000; // best friend
        mapUser[0x511cC355Ab72Ed3187Ed628E4C5ff36a934Ed006] = User("ere", keccak256(abi.encode("ere")), Roles.PrivateProvider, true);
        mapUser[0x747CDaE330AC4cfE8656aC1981a4EF4204f8D8af] = User("test", keccak256(abi.encode("test")), Roles.PublicProvider, true);
        // 0xB33909c36DeD414c5c4BeB7512300Ea69015714E 
        // 0x96af6CF5226aEFD698810E3514062287c444B963
        SeedTokens - 900000;
        mapPrivateToken[owner] = PrivateTokens;
        mapPublicToken[owner]  = PublicTokens;
        mapSeedToken[owner]    = SeedTokens;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not an owner!");
        _;
    }

    modifier onlyPrivetProvider() {
        require(mapUser[msg.sender].Role == Roles.PrivateProvider, "not a Private Provider!");
        _;
    }

    modifier onlyPublicProvider() {
        require(mapUser[msg.sender].Role == Roles.PublicProvider, "not a Public Provider!");
        _;
    }

    /**
    * @dev Функция таймера
    */
    function ReturnFaze() public view returns(uint) {
        uint _Time_now    = block.timestamp;
        uint _Time_system = _Time_now - Time_dif; 

        if ((_Time_system - Time_start)/60 < 5) {
            return 1;   // Подготовительная фаза
        } if ((_Time_system - Time_start)/60 < 10) {
            return 2;   // Приватная фаза
        } else {
            return 3;   // Публичная фаза
        }
    }

    function returnBalanceEther() public view returns(uint) {
        return msg.sender.balance;
    }

    function returnPublicTokenBalance() public view returns(uint) {
        return mapPublicToken[msg.sender];
    }

    function returnPrivateTokenBalance() public view returns(uint) {
        return mapPrivateToken[msg.sender];
    }

    function returnSeedTokenBalance() public view returns(uint) {
        return mapSeedToken[msg.sender];
    }

    /**
    * @dev Функция управления временем (доступна всем пользователям системы)
    */
    function addOneMinuteToTimeDiff() public returns (uint) {  
        Time_dif += 60;
        return Time_dif;
    }

    // Функция регистрации пользователей
    function Registration(string memory _name, string memory _password) external returns(User memory) {
        require(mapUser[msg.sender].Role != Roles.User, "You already an User!");
        mapUser[msg.sender] = User(_name, keccak256(abi.encode(_password)), Roles.User, false);
        return mapUser[msg.sender];
    }

    // авторизация для зарегистрированных пользователей
    function Authorization(string memory _name, string memory _password) external view returns(User memory) {
        require(mapUser[msg.sender].Role != Roles.Guest, "You are not registered!");
        require(keccak256(bytes(_name)) == keccak256(bytes(mapUser[msg.sender].Name)));
        require(keccak256(abi.encode(_password)) == keccak256(abi.encode(mapUser[msg.sender].Password)));
        return mapUser[msg.sender];
    }
    // Функция возврата данных о пользователе (для фронта)
    function ReturnUserInfo() external view returns(User memory) {
        return mapUser[msg.sender];
    }

    /**
    * @dev Функция покупки публичного токена
    */
    function BuyPublicToken(uint amount) public payable {
        // require(ReturnFaze() == 3, "Time is over!");    // Проверка периода покупки
        require(amount <= 5000, "Not enough tokens!");  // Проверка максимального количества покупки токенов
        
        // uint etherForTokens = amount * PricePublicToken;
        // uint refound = msg.value - etherForTokens;
        // Возврат пользователю разницы в эфире
        // if (refound != 0 ) {
        //     payable(msg.sender).transfer(refound);
        // }

        payable(owner).transfer(msg.value);
        ERC20._transfer(owner, msg.sender, amount);
        mapPublicToken[msg.sender] += amount;
        mapPublicToken[owner] -= amount;
        // Событие покупки
        emit Bought(msg.sender, amount);

    }

    /**
    * @dev Функция покупки приватного токена
    */ 
    function BuyPrivateToken(uint amount) public payable {
        require(ReturnFaze() == 2, "Time is over!");                              // Проверка периода покупки
        require(mapUser[msg.sender].WhiteList == true, "Free sale not started");  // Проверка на добавление в белый лист
        require(amount <= 100000, "Incorrect enough!");                           // Проверка количества покупаемых токенов

        uint price = 0.00075 ether;
        uint etherForTokens = amount * price;
        uint refound = msg.value - etherForTokens;
        // Возврат пользователю разницы в эфире
        if (refound != 0 ) {
            payable(msg.sender).transfer(refound);
        }

        payable(owner).transfer(etherForTokens);
        ERC20._transfer(owner, msg.sender, amount);
        mapPublicToken[msg.sender] += amount;
        mapPublicToken[owner] -= amount;
        // Событие покупки
        emit Bought(msg.sender, amount);
    }

    /**
    * @dev Перевод публичных токенов от пользователя пользователю
    */
    function TransferPublicTokenOnUser(address to, uint amount) public {
        require(mapUser[msg.sender].Role != Roles.Guest, "Not an user!");
    
        ERC20._transfer(msg.sender, to, amount);
        mapPublicToken[msg.sender] -= amount;
        mapPublicToken[to] += amount;
    }

    /**
    * @dev Перевод приватных токенов от пользователя пользователю
    */
    function TransferPrivateTokenOnUser(address to, uint amount) public {
        require(mapUser[msg.sender].Role != Roles.Guest, "Not an user!");

        ERC20._transfer(msg.sender, to, amount);
        mapPrivateToken[msg.sender] -= amount;
        mapPrivateToken[to] += amount;
    }

    /**
    * @dev Функция вознаграждения токенами 
    */
    function SendPublicTokens(uint amount, address account) external onlyPublicProvider {
        // require(ReturnFaze() == 3, "Time is over!");  // Проверка фазы

        ERC20._transfer(owner, msg.sender, amount);
        emit Bought(account, amount);
        mapPublicToken[owner] -= amount;
        mapPublicToken[account] += amount;
    }

    function ChangePriceForPublicTokens(uint newPrice) external onlyPublicProvider {
        PricePublicToken = newPrice;
    }

    /**
    * @dev Функция просмотра запросов
    */
    function ViewArrayRequests() public view onlyPrivetProvider returns(Request[] memory) {
        return requests;
    }

    /**
    * @dev Функция добавления запроса
    */
    function AddRequestInArray() public {
        require(mapUser[msg.sender].Role == Roles.User, "You are not registered");
        requests.push(Request(mapUser[msg.sender].Name, msg.sender, requests.length));
    }

    /**
    * @dev Функция удаления запроса
    */
    function RemoveRequestInArray(uint index) public onlyPrivetProvider {
        requests[index] = requests[requests.length-1];
        requests.pop();
    }
    
    /**
    * @dev Функция одобрения запроса
    */
    function AccessRequest(uint index) public onlyPrivetProvider {
        require(mapUser[requests[index].account].WhiteList == false, "You already in white list!");
        // require(ReturnFaze() == 1, "Time error!");
        mapUser[requests[index].account].WhiteList = true;
        requests[index] = requests[requests.length-1];
        requests.pop();
    }

    function returnBalance() public view returns(uint) {
        return mapPublicToken[msg.sender];
    }
}