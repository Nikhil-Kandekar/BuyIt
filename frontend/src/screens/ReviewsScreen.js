import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Row, Table } from 'react-bootstrap'

const ReviewsScreen = () => {
    const [products, setProducts] = useState()

    useEffect(()=>{
        let isMounted = true;
        axios.get(
                `/api/products?keyword=&pageNumber=1`
            ).then(({data})=>{
                if(isMounted){
                    setProducts(data.products)
                }                
            });
            return () => {
                isMounted = false;
            }; 
    }, [])
    console.log(products)

  return (        
    <>
    <Row>
        <Table striped bordered hover responsive className='table-sm'>
            <thead>
            <tr>
                <th>PRODUCT NAME</th>
                <th>USER</th>
                <th>RATING</th>
                <th>COMMENT</th>
                <th>FAKE?</th>
                <th></th>
            </tr>
            </thead>
            <tbody>
        {products && products.length!==0 && products.map((product) => (
            product.reviews.length>0 && product.reviews.map((review)=>(
            <tr key={review._id}>
                <td>{product.name}</td>
                <td>{review.name}</td>
                <td>{review.rating}</td>
                <td>{review.comment}</td>
                <td>{review.flag || "REAL"}</td>
                <td></td>
            </tr>))
        ))}
        </tbody>
        </Table>
    </Row>   
    </>
  )
}

export default ReviewsScreen


