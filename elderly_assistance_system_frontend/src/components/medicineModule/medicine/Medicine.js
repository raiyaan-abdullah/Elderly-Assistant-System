import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import {getMedicine, deleteMedicine} from '../../../actions/medicine';

export class Medicine extends Component {
    static propTypes = {
        medicine: PropTypes.array.isRequired,
        getMedicine: PropTypes.func.isRequired,
        deleteMedicine: PropTypes.func.isRequired
    };

    componentDidMount() {
        this.props.getMedicine();
    }

    render() {
        return (
            <Fragment>
                <h2>List of Medicine</h2>
                <div className="table-responsive">
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Prescribed Time</th>
                                <th>Started</th>
                                <th>Drawer no.</th>
                                <th>Required Dosage</th>
                                <th>Current amount</th>
                                <th/>
                            </tr>
                        </thead>
                        <tbody>
                            { this.props.medicine.map( (medicine, index) => (
                                <tr key={index}>
                                    <td>{medicine.id}</td>
                                    <td>{medicine.name}</td>
                                    <td>{medicine.time}</td>
                                    <td>{medicine.started}</td>
                                    <td>{medicine.drawer}</td>
                                    <td></td>
                                    <td></td>
                                    <td><button onClick={this.props.deleteMedicine.bind(this, medicine.id)} className="btn red-background white">Delete</button></td>
                                </tr>
                            ))}


                            
                        </tbody>
                    </table>
                </div>
            </Fragment>
        )
    }
}

const mapStateToProps = state => ({
    medicine: state.medicine.medicine //here 'medicine' is the reducer in reducer/index.js, and 'medicine' is the passed parameter medicine.js file in same folder
})

export default connect(mapStateToProps, { getMedicine, deleteMedicine })(Medicine);


