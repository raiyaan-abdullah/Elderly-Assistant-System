import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getMedicine, updateMedicine} from '../../../actions/medicine';



export class FormUpdate extends Component {

    componentDidMount() {
        this.props.getMedicine();
    }

    state = {
        id:'',
        name: '',
        time: '',
        started: '',
        drawer: ''
    }

    static propTypes = {
        medicine: PropTypes.array.isRequired,
        updateMedicine: PropTypes.func.isRequired,
        getMedicine: PropTypes.func.isRequired,
    }


    onChange = e => this.setState({ [e.target.name] : e.target.value});


    onSelectChange = e => {



        this.setState({ 
            [e.target.name] : e.target.value, 
        });
        for (let list_index in this.props.medicine){ 
            if (this.props.medicine[list_index].id == e.target.value) {
                /* time includes seconds, but our input does not accept that */

                this.setState({ 
                    name: this.props.medicine[list_index].name,
                    time: this.props.medicine[list_index].time,
                    started: this.props.medicine[list_index].started.substring(0,16),
                    drawer: this.props.medicine[list_index].drawer
                });
            }
        }


        
    }



    onSubmit = e => {
        e.preventDefault();
        const {id, name, time, started, drawer} = this.state;
        const medicine = {id,name, time, started, drawer};
        this.props.updateMedicine(medicine);


    }
    render() {
        
        const {id,name, time, started, drawer} = this.state;

        return (
            
            <div className="card card-body mb-5">

                <h2>Update Medicine</h2>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>ID</label>
                        {/*
                        <input className="form-control" type="number" name="id" onChange={this.onSelectChange} value={id}/>
                        */}
                        <select className="form-control"  onChange={this.onSelectChange}  name="id" value={id}>
                            <option>Select a medicine ID</option>
                            { this.props.medicine.map( (medicine,index) => (
                                <option key={index} value={medicine.id}>
                                    {medicine.id}     
                                </option>
                            ))}                            
                        </select>
                            
                    </div>
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
                        <button type="submit" className="btn yellow-background">Update</button>
                    </div>
                </form>

            </div>



        )
    }
}

const mapStateToProps = state => ({
    medicine: state.medicine.medicine //here 'medicine' is the reducer in reducer/index.js, and 'medicine' is the passed parameter medicine.js file in same folder
})

export default connect(mapStateToProps, {getMedicine, updateMedicine})(FormUpdate);
