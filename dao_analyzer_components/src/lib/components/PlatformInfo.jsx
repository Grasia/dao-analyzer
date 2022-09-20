import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ParticipationStat from './ParticipationStat.jsx';

/**
 * PlatformInfo is the component on the top left of the second header
 * It receives the DAO name, the network(s) and other data and displays it in a grid view.
 */
export default class PlatformInfo extends Component {
    render() {
        const props = this.props;

        return (
            <div className='dao-info-container'>
                <div className='dao-info-label'>Platform</div>
                <div className='dao-info-name'>{props.name}</div>
                <div className='dao-info-label'>Networks</div>
                <div className='dao-info-network'>{props.networks.join(', ')}</div>
                { props.creation_date &&
                    <>
                        <div className='dao-info-label'>Creation Date</div>
                        <div className='dao-info-date'>{props.creation_date}</div>
                    </>
                }
                { props.participation_stats &&
                    <>
                        <div className='dao-info-label'>Participation</div>
                        <div className='dao-info-stats'>
                            {props.participation_stats.map(ps => 
                                <ParticipationStat key={ps.text} text={ps.text} value={ps.value}/>
                            )}
                        </div>
                    </>
                }
            </div>
        );
    }
}

PlatformInfo.propTypes = {
    /**
     * The name of the platform
     */
    name: PropTypes.string,

    /**
     * The networks the platform is deployed in
     */
    networks: PropTypes.arrayOf(PropTypes.string),

    /**
     * The creation date of the organization
     */
    creation_date: PropTypes.string,

    /**
     * The array of participation_stats objects
     */
    participation_stats: PropTypes.arrayOf(PropTypes.object),

    /**
     * Dash-assigned callback that should be called to report property changes
     */
    setProps: PropTypes.func
}
