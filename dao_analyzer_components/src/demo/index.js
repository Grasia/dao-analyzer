import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { DAOInfo } from '../lib';

class Demo extends Component {
    render() {
        return (
            <DAOInfo address='0x0123456789abcdef' network='mainnet' name='asdafgadafDAO'/>
        );
    }
}

ReactDOM.render(<Demo />, document.getElementById('root'));
