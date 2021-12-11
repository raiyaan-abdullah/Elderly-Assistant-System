import React, { Component, Fragment } from 'react';
import { withAlert } from 'react-alert';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

export class Alerts extends Component {
  static propTypes = {

    message: PropTypes.object.isRequired,
  };

  componentDidUpdate(prevProps) {
    const {  alert, message } = this.props;


    if (message !== prevProps.message) {
      if (message.deleteMedicine) alert.success(message.deleteMedicine);
      if (message.addMedicine) alert.success(message.addMedicine);
      if (message.updateMedicine) alert.success(message.updateMedicine);
      if (message.passwordNotMatch) alert.error(message.passwordNotMatch);
    }
  }

  render() {
    return <Fragment />;
  }
}

const mapStateToProps = (state) => ({

  message: state.messages,
});

export default connect(mapStateToProps)(withAlert()(Alerts));