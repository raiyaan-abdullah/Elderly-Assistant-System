import { GET_MEDICINE, DELETE_MEDICINE, ADD_MEDICINE, UPDATE_MEDICINE } from '../actions/types.js';

const initialState = {
    medicine: []
};

export default function(state=initialState, action) {
    switch(action.type) {
        case GET_MEDICINE:
            return {
                ...state,
                medicine: action.payload
            };

        case DELETE_MEDICINE:
            return {
                ...state,
                medicine: state.medicine.filter(medicine => medicine.id !== action.payload)
            };

        case ADD_MEDICINE:
            return {
                ...state,
                medicine: [ ...state.medicine,  action.payload]
            };
        case UPDATE_MEDICINE:
            return {
                ...state,
                medicine: [ ...state.medicine.filter(medicine => medicine.id !== action.payload.id ) ,  action.payload]
            };
        default:
            return state;
    }

}