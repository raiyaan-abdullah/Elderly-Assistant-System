import { GET_MEDICINE_HISTORY, ADD_MEDICINE_HISTORY } from '../actions/types.js';

const initialState = {
    medicine_history: []
};

export default function(state=initialState, action) {
    switch(action.type) {
        case GET_MEDICINE_HISTORY:
            return {
                ...state,
                medicine_history: action.payload
            };

        case ADD_MEDICINE_HISTORY:
            return {
                ...state,
                medicine_history: [ ...state.medicine_history,  action.payload]
            };
        default:
            return state;
    }

}