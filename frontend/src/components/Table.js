import { Link } from 'react-router-dom';
function Table({ data,onDelete }) {

    return (
        <div className="container">
            <table className="table table-hover">
                <thead >
                    <tr className="bg-info" style={{ height: "30%" }}>
                        <th>Code</th>
                        <th>Title</th>
                        <th>Model</th>
                        <th>Price</th>
                        <th>Engine</th>
                        <th>State</th>
                        <th>Location</th>
                        <th>Link</th>
                        <th>View</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {data && data.map(row => (
                        <tr key={row.finn_code}>
                            <td>{row.finn_code}</td>
                            <td>{row.title}</td>
                            <td>{row.Model}</td>
                            <td>{row.orignal_price}</td>
                            <td>{row.Engine_Included}</td>
                            <td>{row.State}</td>
                            <td>{row.Boat_location}</td>
                            <td><a href={row.url} target="_blank" rel="noreferrer"><i className="fas fa-link"></i></a></td>
                            <td><Link to={`/details/${row.finn_code}`}><i className="fa fa-eye" aria-hidden="true"></i></Link></td>

                            <td>{
                                row.status === "Active" ? <span className='badge bg-success'>{row.status}</span> :
                                    row.status === "Sold" ? <span className='badge bg-warning'>{row.status}</span> :
                                        <span className='badge bg-secondary'>{row.status}</span>} </td>
                            <td style={{cursor:"pointer"}} onClick={()=>{onDelete(row.finn_code)}}><i className="text-danger font-weight-bold text-center far fa-trash-alt"></i></td>

                        </tr>
                    ))}

                </tbody>
            </table>
        </div>
    )
}

export default Table;
