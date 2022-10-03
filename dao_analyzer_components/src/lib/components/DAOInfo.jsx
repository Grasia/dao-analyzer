import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ParticipationStat from './ParticipationStat.jsx';

/** 
 * DAOInfo is the component on the top left of the second header
 * It receives the DAO name, the network(s), the address, the creation date,
 * and the participation statistics and shows them in a grid view.
 */
export default class DAOInfo extends Component {
    render() {
        const { id, name, network, address, creation_date, first_activity, participation_stats } = this.props;

        return (
            <div className='dao-info-container'>
                <div className='dao-info-label'>DAO</div>
                <div className='dao-info-name'>{name || <i>No Name Given</i>}</div>
                <div className='dao-info-label'>Network</div>
                <div className='dao-info-network'>{network}</div>
                <div className='dao-info-label'>Address</div>
                <div className='dao-info-address'><span className='address'>{address}</span></div>
                { creation_date ? 
                    <>
                        <div className='dao-info-label'>Creation Date</div>
                        <div className='dao-info-date'>{creation_date}</div>
                    </>
                    /* else if */
                    : first_activity &&
                    <>
                        <div className='dao-info-label'>First Activity</div>
                        <div className='dao-info-date'>{first_activity}</div>
                    </>
                }
                { this.props.participation_stats &&
                    <>
                        <div className='dao-info-label'>Participation</div>
                        <div className='dao-info-stats'>
                            {this.props.participation_stats.map(ps => 
                                <ParticipationStat key={ps.text} text={ps.text} value={ps.value}/>
                            )}
                        </div>
                    </>
                }
            </div>
        );
    }
}

DAOInfo.propTypes = {
    /**
     * The ID used to identify the component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The organization (DAO) name
     */
    name: PropTypes.string,

    /**
     * The network the DAO is deployed on
     */
    network: PropTypes.string,

    /**
     * The address of the organization
     */
    address: PropTypes.string,

    /** 
     * The creation date of the organization
     */
    creation_date: PropTypes.string,

    /**
     * The date where the first activity was recorded
     */
    first_activity: PropTypes.string,

    /**
     * The array of participation_stats objects
     */
    participation_stats: PropTypes.arrayOf(PropTypes.object),

    /**
     * Dash-assigned callback that should be called to report property changes
     */
    setProps: PropTypes.func
};

DAOInfo.defaultProps = {
    id: 'dao-info',
    name: 'no name given'
};

