// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdvancedInteraction {
    uint256 public value;
    uint256[] public history;
    mapping(address => uint256) public userValues;

    event ValueChanged(uint256 newValue);
    event HistoryUpdated(uint256[] newHistory);

    // 1. Set value
    function setValue(uint256 _value) public {
        value = _value;
        emit ValueChanged(value);
    }

    // 2. Get value
    function getValue() public view returns (uint256) {
        return value;
    }

    // 3. Increment value
    function incrementValue() public {
        value += 1;
        emit ValueChanged(value);
    }

    // 4. Decrement value
    function decrementValue() public {
        require(value > 0, "Value cannot be negative");
        value -= 1;
        emit ValueChanged(value);
    }

    // 5. Reset value
    function resetValue() public {
        value = 0;
        emit ValueChanged(value);
    }

    // 6. Check if greater than
    function isGreaterThan(uint256 _number) public view returns (bool) {
        return value > _number;
    }

    // 7. Save to history
    function saveHistory() public {
        history.push(value);
        emit HistoryUpdated(history);
    }

    // 8. Get history
    function getHistory() public view returns (uint256[] memory) {
        return history;
    }

    // 9. Reset history
    function resetHistory() public {
        delete history;
        emit HistoryUpdated(history);
    }

    // 10. Get history count
    function historyCount() public view returns (uint256) {
        return history.length;
    }

    // 11. Multiply value
    function multiplyValue(uint256 _factor) public {
        value *= _factor;
        emit ValueChanged(value);
    }

    // 12. Divide value
    function divideValue(uint256 _divisor) public {
        require(_divisor > 0, "Divisor cannot be zero");
        value /= _divisor;
        emit ValueChanged(value);
    }

    // 13. Check if even
    function isEven() public view returns (bool) {
        return value % 2 == 0;
    }

    // 14. Check if odd
    function isOdd() public view returns (bool) {
        return value % 2 != 0;
    }

    // 15. Update history at index
    function updateHistory(uint256 index, uint256 newValue) public {
        require(index < history.length, "Index out of bounds");
        history[index] = newValue;
        emit HistoryUpdated(history);
    }

    // 16. Remove from history
    function removeHistory(uint256 index) public {
        require(index < history.length, "Index out of bounds");
        history[index] = history[history.length - 1];
        history.pop();
        emit HistoryUpdated(history);
    }

    // 17. Get max history value
    function getMaxHistoryValue() public view returns (uint256) {
        require(history.length > 0, "No history available");
        uint256 maxValue = history[0];
        for (uint256 i = 1; i < history.length; i++) {
            if (history[i] > maxValue) {
                maxValue = history[i];
            }
        }
        return maxValue;
    }

    // 18. Get min history value
    function getMinHistoryValue() public view returns (uint256) {
        require(history.length > 0, "No history available");
        uint256 minValue = history[0];
        for (uint256 i = 1; i < history.length; i++) {
            if (history[i] < minValue) {
                minValue = history[i];
            }
        }
        return minValue;
    }

    // 19. Get sum of history
    function getSumHistory() public view returns (uint256) {
        uint256 sum = 0;
        for (uint256 i = 0; i < history.length; i++) {
            sum += history[i];
        }
        return sum;
    }

    // 20. Get average of history
    function getAverageHistory() public view returns (uint256) {
        require(history.length > 0, "No history available");
        return getSumHistory() / history.length;
    }

    // 21. Set user value
    function setUserValue(uint256 _value) public {
        userValues[msg.sender] = _value;
    }

    // 22. Get user value
    function getUserValue(address _user) public view returns (uint256) {
        return userValues[_user];
    }

    // 23. Increment user value
    function incrementUserValue() public {
        userValues[msg.sender] += 1;
    }

    // 24. Decrement user value
    function decrementUserValue() public {
        require(userValues[msg.sender] > 0, "User value cannot be negative");
        userValues[msg.sender] -= 1;
    }

    // 25. Transfer user value
    function transferUserValue(address _to, uint256 _amount) public {
        require(userValues[msg.sender] >= _amount, "Insufficient user value");
        userValues[msg.sender] -= _amount;
        userValues[_to] += _amount;
    }

    // 26. Get contract balance
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // 27. Donate to contract
    function donate() public payable {
        // Funds are automatically added to contract balance
    }

    // 28. Withdraw from contract
    function withdraw(uint256 _amount) public {
        require(address(this).balance >= _amount, "Insufficient contract balance");
        payable(msg.sender).transfer(_amount);
    }

    // 29. Get timestamp
    function getTimestamp() public view returns (uint256) {
        return block.timestamp;
    }

    // 30. Get block number
    function getBlockNumber() public view returns (uint256) {
        return block.number;
    }
}
