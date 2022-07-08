import React, { useState, useEffect } from "react";

import Table from "./Table";
import Spinner from './Spinner'
import { isExpired } from "./ExpiryCheck";

import { Redirect } from "react-router";
function Home() {


    const [data, setData] = useState({});
    const [pages, setPages] = useState({ "total_records": 0, "current_page": 1, "previous_page": 0, "next_page": 0, "total_pages": 0 });
    const [loading, setLoading] = useState(false);
    // const [access_token,setAccessToken] = useState(localStorage.getItem("access"))
    // const [is_expired, set_is_expired] = useState(isExpired())
    const [filters, setFilters] = useState(
        {
            'finn_code': '',
            'title': '',
            'brand': '',
            'color': '',
            'boat_location': '',
            'depth': '',
            'engine_included': '',
            'engine_manufacturer': '',
            'engine_type': '',
            'fuel': '',
            'length_cm': '',
            'length_feet': '',
            'material': '',
            'max_speed': '',
            'modelstr': '',
            'seating': '',
            'sleeps': '',
            'state': '',
            'type': '',
            'weight': '',
            'width': '',
            'description': '',
            'last_updated': '',
            'model': '',
            'model_year': '',
            'price': '',
            'status': '',
        }
    )

    const [url, setURL] = useState(`/api/listings/?page=${pages.current_page}&finn_code=${filters.finn_code}&title=${filters.title}&description=${filters.description}&Boat_location=${filters.boat_location}&State=${filters.state}&Type=${filters.type}&Brand=${filters.brand}&Model=${filters.model}&Model_Year=${filters.model_year}&Length_feet=${filters.length_feet}&Length_cm=${filters.length_cm}&Width=${filters.width}&Depth=${filters.depth}&Engine_Included=${filters.engine_included}&Engine_Manufacturer=${filters.engine_manufacturer}&Engine_Type=${filters.engine_type}&Motorstr=${filters.modelstr}&Max_Speed=${filters.max_speed}&Fuel=${filters.fuel}&Weight=${filters.weight}&Material=${filters.material}&Color=${filters.color}&Seating=${filters.seating}&Sleeps=${filters.sleeps}&orignal_price=${filters.price}&image=&last_updated=${filters.last_updated}&status=${filters.status}`);

    useEffect(() => {
        document.title = `Finn-Page:${pages.current_page}`
        getData();

    }, [url]);


    const getData = async () => {
        const requestOptions = {
            method: 'GET'
        };
        setLoading(false)
        const response = await fetch(url, requestOptions);
        const dataOutput = await response.json();
        setData(dataOutput.records);
        setPages({ "total_records": dataOutput.total_records, "current_page": dataOutput.current_page, "previous_page": dataOutput.previous_page, "next_page": dataOutput.next_page, "total_pages": dataOutput.total_pages })

        setLoading(true)
    };
    function handleChange(event) {
        const newValue = event.target.value;
        const inputValue = event.target.name;


        setFilters((prevValue) => {
            if (inputValue === "title") {
                return {
                    'finn_code': prevValue.finn_code,
                    'title': newValue,
                    'brand': prevValue.brand,
                    'color': prevValue.color,
                    'boat_location': prevValue.boat_location,
                    'depth': prevValue.depth,
                    'engine_included': prevValue.engine_included,
                    'engine_manufacturer': prevValue.engine_manufacturer,
                    'engine_type': prevValue.engine_type,
                    'fuel': prevValue.fuel,
                    'length_cm': prevValue.length_cm,
                    'length_feet': prevValue.length_feet,
                    'material': prevValue.material,
                    'max_speed': prevValue.max_speed,
                    'modelstr': prevValue.modelstr,
                    'seating': prevValue.seating,
                    'sleeps': prevValue.sleeps,
                    'state': prevValue.state,
                    'type': prevValue.type,
                    'weight': prevValue.weight,
                    'width': prevValue.width,
                    'description': prevValue.description,
                    'last_updated': prevValue.last_updated,
                    'model': prevValue.model,
                    'model_year': prevValue.model_year,
                    'price': prevValue.price,
                    'status': prevValue.status,
                }
            }
            else if (inputValue === "finn_code") {
                return {
                    'finn_code': newValue,
                    'title': prevValue.title,
                    'brand': prevValue.brand,
                    'color': prevValue.color,
                    'boat_location': prevValue.boat_location,
                    'depth': prevValue.depth,
                    'engine_included': prevValue.engine_included,
                    'engine_manufacturer': prevValue.engine_manufacturer,
                    'engine_type': prevValue.engine_type,
                    'fuel': prevValue.fuel,
                    'length_cm': prevValue.length_cm,
                    'length_feet': prevValue.length_feet,
                    'material': prevValue.material,
                    'max_speed': prevValue.max_speed,
                    'modelstr': prevValue.modelstr,
                    'seating': prevValue.seating,
                    'sleeps': prevValue.sleeps,
                    'state': prevValue.state,
                    'type': prevValue.type,
                    'weight': prevValue.weight,
                    'width': prevValue.width,
                    'description': prevValue.description,
                    'last_updated': prevValue.last_updated,
                    'model': prevValue.model,
                    'model_year': prevValue.model_year,
                    'price': prevValue.price,
                    'status': prevValue.status,
                }
            }
            else if (inputValue === "status") {
                return {
                    'finn_code': prevValue.finn_code,
                    'title': prevValue.title,
                    'brand': prevValue.brand,
                    'color': prevValue.color,
                    'boat_location': prevValue.boat_location,
                    'depth': prevValue.depth,
                    'engine_included': prevValue.engine_included,
                    'engine_manufacturer': prevValue.engine_manufacturer,
                    'engine_type': prevValue.engine_type,
                    'fuel': prevValue.fuel,
                    'length_cm': prevValue.length_cm,
                    'length_feet': prevValue.length_feet,
                    'material': prevValue.material,
                    'max_speed': prevValue.max_speed,
                    'modelstr': prevValue.modelstr,
                    'seating': prevValue.seating,
                    'sleeps': prevValue.sleeps,
                    'state': prevValue.state,
                    'type': prevValue.type,
                    'weight': prevValue.weight,
                    'width': prevValue.width,
                    'description': prevValue.description,
                    'last_updated': prevValue.last_updated,
                    'model': prevValue.model,
                    'model_year': prevValue.model_year,
                    'price': prevValue.price,
                    'status': newValue,
                }
            }
            else if (inputValue === "description") {
                return {
                    'finn_code': prevValue.finn_code,
                    'title': prevValue.title,
                    'brand': prevValue.brand,
                    'color': prevValue.color,
                    'boat_location': prevValue.boat_location,
                    'depth': prevValue.depth,
                    'engine_included': prevValue.engine_included,
                    'engine_manufacturer': prevValue.engine_manufacturer,
                    'engine_type': prevValue.engine_type,
                    'fuel': prevValue.fuel,
                    'length_cm': prevValue.length_cm,
                    'length_feet': prevValue.length_feet,
                    'material': prevValue.material,
                    'max_speed': prevValue.max_speed,
                    'modelstr': prevValue.modelstr,
                    'seating': prevValue.seating,
                    'sleeps': prevValue.sleeps,
                    'state': prevValue.state,
                    'type': prevValue.type,
                    'weight': prevValue.weight,
                    'width': prevValue.width,
                    'description': newValue,
                    'last_updated': prevValue.last_updated,
                    'model': prevValue.model,
                    'model_year': prevValue.model_year,
                    'price': prevValue.price,
                    'status': prevValue.status,
                }
            }

        })


    }
    function setURLfromFiltersState() {
        setURL(`/api/listings/?page=${pages.current_page}&finn_code=${filters.finn_code}&title=${filters.title}&description=${filters.description}&Boat_location=${filters.boat_location}&State=${filters.state}&Type=${filters.type}&Brand=${filters.brand}&Model=${filters.model}&Model_Year=${filters.model_year}&Length_feet=${filters.length_feet}&Length_cm=${filters.length_cm}&Width=${filters.width}&Depth=${filters.depth}&Engine_Included=${filters.engine_included}&Engine_Manufacturer=${filters.engine_manufacturer}&Engine_Type=${filters.engine_type}&Motorstr=${filters.modelstr}&Max_Speed=${filters.max_speed}&Fuel=${filters.fuel}&Weight=${filters.weight}&Material=${filters.material}&Color=${filters.color}&Seating=${filters.seating}&Sleeps=${filters.sleeps}&orignal_price=${filters.price}&image=&last_updated=${filters.last_updated}&status=${filters.status}`)
    }
    function nextPage() {
        setURL(`/api/listings/?page=${pages.next_page}&finn_code=${filters.finn_code}&title=${filters.title}&description=${filters.description}&Boat_location=${filters.boat_location}&State=${filters.state}&Type=${filters.type}&Brand=${filters.brand}&Model=${filters.model}&Model_Year=${filters.model_year}&Length_feet=${filters.length_feet}&Length_cm=${filters.length_cm}&Width=${filters.width}&Depth=${filters.depth}&Engine_Included=${filters.engine_included}&Engine_Manufacturer=${filters.engine_manufacturer}&Engine_Type=${filters.engine_type}&Motorstr=${filters.modelstr}&Max_Speed=${filters.max_speed}&Fuel=${filters.fuel}&Weight=${filters.weight}&Material=${filters.material}&Color=${filters.color}&Seating=${filters.seating}&Sleeps=${filters.sleeps}&orignal_price=${filters.price}&image=&last_updated=${filters.last_updated}&status=${filters.status}`)
    }

    function prevPage() {

        setURL(`/api/listings/?page=${pages.previous_page}&finn_code=${filters.finn_code}&title=${filters.title}&description=${filters.description}&Boat_location=${filters.boat_location}&State=${filters.state}&Type=${filters.type}&Brand=${filters.brand}&Model=${filters.model}&Model_Year=${filters.model_year}&Length_feet=${filters.length_feet}&Length_cm=${filters.length_cm}&Width=${filters.width}&Depth=${filters.depth}&Engine_Included=${filters.engine_included}&Engine_Manufacturer=${filters.engine_manufacturer}&Engine_Type=${filters.engine_type}&Motorstr=${filters.modelstr}&Max_Speed=${filters.max_speed}&Fuel=${filters.fuel}&Weight=${filters.weight}&Material=${filters.material}&Color=${filters.color}&Seating=${filters.seating}&Sleeps=${filters.sleeps}&orignal_price=${filters.price}&image=&last_updated=${filters.last_updated}&status=${filters.status}`)
    }
    const onDelete = async (finn_code) => {
        const requestOptions = {
            method: 'DELETE'
        };
        await fetch(`/api/delete/${finn_code}`,requestOptions);
        getData();

    }
    // if (is_expired) {
    //     return <Redirect to="/login" />
    // }

    

    return (
        <div className="Home">
            <header>
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    <div className="container-fluid">
                        <a className="navbar-brand" href="/">
                            <svg focusable="false" width="92" height="32" viewBox="0 0 184 64">
                                <title>FINN.NO</title>
                                <path fill="#06bffc" d="M179.8 58V6c0-1-.8-1.9-1.9-1.9H66c-1 0-1.9.8-1.9 1.9v53.8H178c1 0 1.8-.8 1.8-1.8">
                                </path>
                                <path fill="#0063fc" d="M22.5 4.2H6C5 4.2 4.2 5 4.2 6v52c0 1 .8 1.9 1.9 1.9H60V41.5C59.9 20.9 43.2 4.2 22.5 4.2"></path>
                                <path fill="#fff" d="M178 0H66c-3.3 0-6 2.7-6 6v17.4C53.2 9.6 38.9 0 22.5 0H6C2.7 0 0 2.7 0 6v52c0 3.3 2.7 6 6 6h172c3.3 0 6-2.7 6-6V6c0-3.3-2.7-6-6-6m1.8 58c0 1-.8 1.9-1.9 1.9H64.1V6c0-1 .8-1.9 1.9-1.9h112c1 0 1.9.8 1.9 1.9v52zM4.2 58V6C4.2 5 5 4.2 6 4.2h16.5c20.6 0 37.4 16.8 37.4 37.4v18.3H6c-1-.1-1.8-.9-1.8-1.9">
                                </path>
                                <path fill="#fff" d="M110.1 21.1h-4.2c-.7 0-1.2.5-1.2 1.2v19.3c0 .7.5 1.2 1.2 1.2h4.2c.7 0 1.2-.5 1.2-1.2V22.3c0-.6-.6-1.2-1.2-1.2m-12 0H83c-.7 0-1.2.5-1.2 1.2v19.3c0 .7.5 1.2 1.2 1.2h4.2c.7 0 1.2-.5 1.2-1.2v-4h7.7c.7 0 1.2-.5 1.2-1.2v-3.2c0-.7-.5-1.2-1.2-1.2h-7.7v-4.9h9.7c.7 0 1.2-.5 1.2-1.2v-3.7c0-.5-.6-1.1-1.2-1.1m62.8 0h-4.2c-.7 0-1.2.5-1.2 1.2v9.5l-6.6-10c-.3-.4-.8-.7-1.3-.7h-3.2c-.7 0-1.2.5-1.2 1.2v19.3c0 .7.5 1.2 1.2 1.2h4.2c.7 0 1.2-.5 1.2-1.2v-9.4l6.5 9.8c.3.4.8.7 1.3.7h3.4c.7 0 1.2-.5 1.2-1.2V22.3c-.1-.6-.6-1.2-1.3-1.2m-25.4 0h-4.2c-.7 0-1.2.5-1.2 1.2v9.5l-6.6-10c-.3-.4-.8-.7-1.3-.7H119c-.7 0-1.2.5-1.2 1.2v19.3c0 .7.5 1.2 1.2 1.2h4.2c.7 0 1.2-.5 1.2-1.2v-9.4l6.5 9.8c.3.4.8.7 1.3.7h3.4c.7 0 1.2-.5 1.2-1.2V22.3c-.1-.6-.6-1.2-1.3-1.2">
                                </path>
                            </svg>
                        </a>

                        <button
                            className="navbar-toggler"
                            type="button"
                            data-mdb-toggle="collapse"
                            data-mdb-target="#navbarSupportedContent"
                            aria-controls="navbarSupportedContent"
                            aria-expanded="false"
                            aria-label="Toggle navigation"
                        >
                            <i className="fas fa-bars"></i>
                        </button>

                        <div
                            className="collapse navbar-collapse"
                            id="navbarSupportedContent"
                        >
                            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                                <li className="nav-item">
                                    <a
                                        // onClick={downloadCsv}
                                        href="/api/export/"
                                        className="btn btn-success"
                                        tabIndex="-1"
                                        aria-disabled="true"
                                    >
                                        Export to Excel
                                    </a>
                                </li>
                                <li className="nav-item">
                                    <span
                                        className="nav-link disabled"
                                        tabIndex="-1"
                                        aria-disabled="true"
                                    >
                                        Current Page: {pages.current_page}
                                    </span>
                                </li>
                                <li className="nav-item">
                                    <span
                                        className="nav-link disabled"
                                        tabIndex="-1"
                                        aria-disabled="true"
                                    >
                                        Total: {pages.total_records}
                                    </span>
                                </li>
                            </ul>
                            <ul className="pagination pagination-circle">

                                <li className="page-item">
                                    <button
                                        onClick={prevPage}
                                        className="btn btn-danger"
                                        href="#"
                                        tabIndex="-1"
                                        aria-disabled="true"
                                    >
                                        <i className="fas fa-chevron-left"></i>
                                    </button>
                                </li>
                                <li className="page-item">
                                    <button onClick={nextPage} className="btn btn-primary">
                                        <i className="fas fa-chevron-right"></i>
                                    </button>
                                </li>

                                

                            </ul>

                            
                        </div>

                        
                    </div>
                </nav>
            </header>


            <div className="container mt-4 mb-4">
                <div className="d-flex input-group w-auto">
                    <input
                        type="text"
                        name="finn_code"
                        onChange={handleChange}
                        value={filters.finn_code}
                        className="form-control"
                        placeholder="Search Finn Code"
                        aria-label="Search"
                    />
                    <input
                        type="text"
                        name="title"
                        onChange={handleChange}
                        value={filters.title}
                        className="form-control"
                        placeholder="Search Title"
                        aria-label="Search"
                    />
                    <input
                        type="text"
                        name="description"
                        onChange={handleChange}
                        value={filters.description}
                        className="form-control"
                        placeholder="Search in Description"
                        aria-label="Search"
                    />
                    <input
                        type="text"
                        name="status"
                        onChange={handleChange}
                        value={filters.status}
                        className="form-control"
                        placeholder="Search Status"
                        aria-label="Search"
                    />
                    <button onClick={setURLfromFiltersState} className="btn btn-primary">
                        Search
                    </button>
                </div>
            </div>

            {loading ? <Table data={data} onDelete={onDelete} /> : <Spinner />}

        </div>
    );
}

export default Home;
