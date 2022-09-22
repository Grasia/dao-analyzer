import React, { Component } from 'react';
import PropTypes from 'prop-types';

/**
 * Used from each DataPoint on the right side of the second header
 */
export default class DataPoint extends Component {
    get_dp_icon(evolution) {
        if (!evolution) {
            return (<></>);
        }

        let className = 'bi bi-dash-circle dp-icon-same';
        if (evolution < 0) {
            className = 'bi bi-arrow-down-circle-fill dp-icon-down';
        } else if (evolution > 0) {
            className = 'bi bi-arrow-up-circle-fill dp-icon-up';
        }

        return (<i className={className}></i>);
    }
    
    get_evolution_str(evolution, evolution_rel) {
        evolution = Math.round(evolution)
        evolution_rel = Math.round(evolution_rel * 100) / 100

        if (evolution && evolution_rel) {
            return `${evolution} (${Math.abs(evolution_rel)}%)`;
        } else if (evolution) {
            return `${evolution}`;
        } else if (evolution_rel) {
            return `${evolution_rel}%`;
        } else {
            return '';
        }
    }

    render() {
        const { id, title, number, evolution, evolution_rel } = this.props;
        let number_str = '?';
        // TODO: Move style to css

        // TODO: If number is int
        if (typeof number === 'string') {
            number_str = number;
        } else if (number) {
            number_str = Math.round(number);
        }

        return (<div id={id} className='dao-summary-datapoint'>
            <span className='dao-summary-datapoint-title'>{title}</span>
            <div className='dao-summary-datapoint-number'>{number_str}</div>
            { evolution && 
                <>
                <div className='dao-summary-datapoint-lastmonth'>This Month</div>
                <div className='dao-summary-datapoint-evolution'>
                    {this.get_dp_icon(evolution)} {this.get_evolution_str(evolution, evolution_rel)}
                </div>
                </>
            }
        </div>);
    }
}

DataPoint.propTypes = {
    /**
     * The css id to use
     */
    'id': PropTypes.string,

    /**
     * The title of the datapoint
     */
    'title': PropTypes.string.isRequired,

    /**
     * The big number to show
     */
    'number': PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * The absolute difference between this month and the last
     */
    'evolution': PropTypes.number,

    /**
     * The relative difference between this month and the last
     */
    'evolution_rel': PropTypes.number,
}

DataPoint.defaultProps = {
    'number': NaN,
}
