import { combineReducers } from "redux";
import medicine from "./medicine";
import medicineHistory from "./medicineHistory";
import messages from "./messages";

export default combineReducers({
  medicine,
  messages,
  medicineHistory
});
