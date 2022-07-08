import React from "react";

function Content({ data }) {

    const prices_list = data.prices
    return (
        <div>
            <div className="row">
                <div className="col-md-6 col-sm-12 col-lg-4 fill">
                    <img
                        src={data.image}
                        width="300px"
                        height="300px"
                        alt={data.title}
                    />
                </div>

                <div className="col-md-6 col-sm-12 col-lg-8">
                    <div className="row">
                        <div className="col-md-3">
                            <label>
                                
                                    {data.Boat_location}
                               
                            </label>
                            <br />
                        </div>
                        <div className="col-md-3">
                            <label>
                                
                                    FIND CODE:
                               
                            </label>
                            <h6>
                                
                                     {data.finn_code}
                               
                            </h6>
                        </div>
                        <div className="col-md-6">
                            <label>
                                Last changed :
              </label>
                            <h6>
                                {data.last_changed}
                            </h6>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-3">
                            <label>
                                Contact Person:
              </label>
                            <h6>
                                {data.contact_name}
                            </h6>
                        </div>
                        <div className="col-md-3">
                            <label>
                                Phones:
              </label>
                            <h6>{data.phone_number}</h6>
                        </div>
                        <div className="col-md-6">
                            <label>
                                Address:
              </label>
                            <h6>{data.address}
                            </h6>
                        </div>
                        <div className="col-md-6">
                            <label>
                                
                                    Price:
                               
                            </label>
                            <h4>{data.orignal_price}
                            </h4>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-12">
                            <h4>{data.title}
                            </h4>
                        </div>
                    </div>
                </div>
            </div>



            <hr />
            <div className="row">
                <div dangerouslySetInnerHTML={{ __html: data.description }} className="col-md-6 col-sm-12" />
                <div className="col-md-6 col-sm-12">

                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th>
                                    #
                                </th>
                                <th>
                                    Changed Price
                                </th>
                                <th>
                                    Date Changed
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {prices_list.map(price => (
                                <tr>
                                    <td>
                                        {price.finn_code}
                                    </td>
                                    <td>
                                        {price.changed_price}
                                    </td>
                                    <td>
                                        {price.price_changed_date}
                                    </td>
                                </tr>
                            ))}


                        </tbody>
                    </table>


                </div>


            </div>
        </div >
    );
}

export default Content;
