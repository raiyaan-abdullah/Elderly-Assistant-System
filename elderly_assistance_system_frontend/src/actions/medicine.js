import axios from 'axios'; //http client
import { createMessage} from './messages';
import {API_URL} from "./apiAddress";

import {GET_MEDICINE, DELETE_MEDICINE, ADD_MEDICINE, UPDATE_MEDICINE} from './types';

// GET MEDICINE
export const getMedicine = () => dispatch => {
    axios.get(API_URL)
        .then ( res => {
            dispatch({
               type: GET_MEDICINE,
               payload: res.data
            });
        }).catch(err => console.log(err));
}

// DELETE MEDICINE
export const deleteMedicine = (id) => dispatch => {
    axios.delete(API_URL+`${id}/`)
        .then ( res => {
            dispatch(createMessage({ deleteMedicine: "Medicine Deleted"}));
            dispatch({
               type: DELETE_MEDICINE,
               payload: id
            });
        }).catch(err => console.log(err));
}

// ADD MEDICINE
export const addMedicine = (medicine) => dispatch => {
    axios.post(API_URL, medicine)
        .then ( res => {
            dispatch(createMessage({ addMedicine: "Medicine Added"}));
            dispatch({
               type: ADD_MEDICINE,
               payload: res.data
            });
        }).catch(err => console.log(err));
}

// UPDATE MEDICINE
export const updateMedicine = (medicine) => dispatch => {
    axios.put(API_URL+`${medicine.id}/`, medicine)
        .then ( res => {
            dispatch(createMessage({ updateMedicine: "Medicine Updated"}));
            dispatch({
               type: UPDATE_MEDICINE,
               payload: res.data
            });
        }).catch(err => console.log(err));
}
