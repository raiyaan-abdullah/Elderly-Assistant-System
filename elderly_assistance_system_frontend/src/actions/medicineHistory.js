import axios from 'axios'; //http client
import { createMessage} from './messages';
import {API_URL_2} from "./apiAddress";

import {GET_MEDICINE_HISTORY,  ADD_MEDICINE_HISTORY} from './types';

// GET MEDICINE
export const getMedicineHistory = () => dispatch => {
    axios.get(API_URL_2)
        .then ( res => {
            dispatch({
               type: GET_MEDICINE_HISTORY,
               payload: res.data
            });
        }).catch(err => console.log(err));
}


// ADD MEDICINE
export const addMedicineHistory = (medicine_history) => dispatch => {
    axios.post(API_URL_2, medicine_history)
        .then ( res => {
            dispatch(createMessage({ addMedicineHistory: "Medicine History Added"}));
            dispatch({
               type: ADD_MEDICINE_HISTORY,
               payload: res.data
            });
        }).catch(err => console.log(err));
}
