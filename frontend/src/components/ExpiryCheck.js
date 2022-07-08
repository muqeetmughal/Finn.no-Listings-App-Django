
import jwt_decode from "jwt-decode";


export const isExpired = () => {
    
    var token = localStorage.getItem("access");
    if (token != null) {

        var decoded = jwt_decode(token);
        var dateNow = new Date();

        if (decoded.exp * 1000 < dateNow.getTime()) {
            return true
        } else {
            return false
        }
    }
    else{
        return true
    }
}

