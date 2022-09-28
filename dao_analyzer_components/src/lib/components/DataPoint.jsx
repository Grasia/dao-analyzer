import React, { Component } from 'react';
import PropTypes from 'prop-types';

/**
 * Used from each DataPoint on the right side of the second header
 */
export default class DataPoint extends Component {
    get_dp_icon(evolution) {
        if (isNaN(evolution)) {
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
        const round_evolution = Math.round(evolution)
        const round_evolution_rel = Math.round(evolution_rel * 100) / 100

        if (!isNaN(evolution) && !isNaN(evolution_rel)) {
            return `${round_evolution} (${Math.abs(round_evolution_rel)}%)`;
        } else if (!isNaN(evolution)) {
            return `${round_evolution}`;
        } else if (!isNaN(evolution_rel)) {
            return `${round_evolution_rel}%`;
        } else {
            return '';
        }
    }

    render() {
        const { id, title, number, evolution, evolution_rel } = this.props;
        let number_str = '?';
        // TODO: Move style to css

        if (typeof number === 'string') {
            number_str = number;
        } else if (!isNaN(number)) {
            number_str = Math.round(number);
        }

        const f_evolution = parseFloat(evolution);
        const f_evolution_rel = parseFloat(evolution_rel);

        return (<div id={id} className='dao-summary-datapoint'>
            <span className='dao-summary-datapoint-title'>{title}</span>
            <div className='dao-summary-datapoint-number'>{number_str}</div>
            { !isNaN(f_evolution) && 
                <>
                <div className='dao-summary-datapoint-lastmonth'>This Month</div>
                <div className='dao-summary-datapoint-evolution'>
                    {this.get_dp_icon(f_evolution)} {this.get_evolution_str(f_evolution, f_evolution_rel)}
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
