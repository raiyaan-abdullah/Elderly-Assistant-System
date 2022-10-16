import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { addMedicine} from '../../../actions/medicine';

export class Form extends Component {

    state = {
        name: '',
        time: '',
        start: '',
        drawer: ''
    }

    static propTypes = {
        addMedicine: PropTypes.func.isRequired
    }
    onChange = e => this.setState({ [e.target.name] : e.target.value});

    onSubmit = e => {
        e.preventDefault();
        const {name, time, started, drawer} = this.state;
        const medicine = {name, time, started, drawer};
        this.props.addMedicine(medicine);
        this.setState({
            name: "",
            time: "",
            //started not added because the next medicine might be started at the same time
            drawer: ""
        })
    }
    render() {
        const {name, time, started, drawer} = this.state;
        return (

            <div className="card card-body mb-5">
                <h2>Add Medicine</h2>
                <form onSubmit={this.onSubmit}>
                <div className="form-group">
                    <label>Name</label>
                    <input className="form-control" type="text" name="name" onChange={this.onChange} value={name}/>
                </div>
                <div className="form-group">
                    <label>Prescribed Time</label>
                    <input className="form-control" type="time" name="time" onChange={this.onChange} value={time}/>
                </div>
                <div className="form-group">
                    <label>Started</label>
                    <input className="form-control" type="datetime-local" name="started" onChange={this.onChange} value={started}/>
                </div>
                <div className="form-group">
                    <label>Drawer no.</label>
                    <input className="form-control" type="number" name="drawer" onChange={this.onChange} value={drawer}/>
                </div>
                <div className="form-group">
                    <label>Required dosage</label>
                    <input className="form-control" type="number" />
                </div>
                <div className="form-group">
                    <label>Current amount</label>
                    <input className="form-control" type="number" />
                </div>
                <div className="form-group">
                    <button type="submit" className="btn green-background white">Add</button>
                </div>
                </form>
            </div>

        )
    }
}

export default connect(null, {addMedicine})(Form);
