import React, { Component } from 'react';
import PropTypes from 'prop-types';

/** 
 * This class will be used by DAOInfo and PlatformInfo
 */
export default class ParticipationStat extends Component {
    render () {
        const { text, value } = this.props;
        if (value) {
            return (<div><b>{value}</b> {text}</div>);
        } else {
            return (<div>{text}</div>);
        }
    }
}

ParticipationStat.propTypes = {
    /**
     * The text to show
     */
    text: PropTypes.string.isRequired,

    /**
     * The value to highlight, which will be appended to text
     */
    value: PropTypes.string,

    /**
     * The key used by React for optimization
     */
    key: PropTypes.string,
}
