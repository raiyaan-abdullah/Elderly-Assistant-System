import React, { Component } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

class MyCalendar extends Component {



    render() {
        return (

            <Calendar
                localizer={localizer}
                defaultDate={new Date()}
                defaultView="month"
                events={this.props.MedicineRecords}  //MedicineRecords is received from parent
                style={{ height: "100vh" }}
                eventPropGetter={event => ({
                    style: {
                        backgroundColor: event.consumed ? "#3cbbb1": "#f45866",
                        color: event.consumed ? "#fff": "#fff"
                         
                    }
                })}
            />

        );
    }
}

export default MyCalendar;