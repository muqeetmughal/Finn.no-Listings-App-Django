import React,{useState,useEffect} from 'react'
import Spinner from './Spinner'
import Content from './Content'
import {useHistory} from 'react-router-dom'
// import home_url from './Home'
function Details({ match }) {
    const history = useHistory();
    const finn_code = match.params.finn_code
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});
    const [access_token,setAccessToken] = useState(localStorage.getItem("access"))
    // const [url, setURL] = useState(`http://127.0.0.1:8000/api/detail/${finn_code}`);
    const url = `/api/detail/${finn_code}`

    // console.log(url)

    
    const getData = async () => {
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json',
                    'Authorization':`Bearer ${access_token}`},
        };
        setLoading(false)
        const response = await fetch(url, requestOptions);
        const data = await response.json();
        setData(data);
        console.log(data)
        setLoading(true)
    };

    useEffect(() => {
        document.title = `Finn-Details:${finn_code}`
        getData();
      }, [url]);
    return (
        
        <div className="container" style={{marginTop: 10}}>
            <button onClick={() => history.goBack()} className="btn btn-primary mb-4">Back</button>

            {loading ?<Content data={data} />: <Spinner />}
        </div>
    )
}

export default Details
