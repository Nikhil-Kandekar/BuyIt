import axios from 'axios';
import React, { useState } from 'react'
import { Form, FormControl } from 'react-bootstrap';
import Webcam from "react-webcam"

function WebcamScreen() {
    const [image, setImage] = useState('')
    const [imghide, setimghide] = useState("hidden")
    const [height, setHeight] = useState()
    const [measurements, setMeasurements] = useState({})

    const handleSubmit = async(e) =>{
        e.preventdefault()
        const blob = await fetch(image).then((res) => res.blob());
        const formData = new FormData();

        formData.append('file', blob)

        await axios.post('http://127.0.0.1:8002/getmeasurements?height=180', formData,{
          headers: {
              'content-type': 'multipart/form-data'
          },
          proxy: {
            host: 'localhost',
            port: 8002
          }
        }).then((res)=>{
            console.log(res)
        })
        
        // setMeasurements(response)
        // console.log(measurements)

    }

    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user"
      };


  return (
      <> 
        <Webcam
            audio={false}
            height="500"
            screenshotFormat="image/jpeg"
            width="100%"
            videoConstraints={videoConstraints}
        > 
        {({ getScreenshot }) => (
            <>
            <button
                className='btn btn-info'
                onClick={() => {
                    setTimeout(()=>{
                        const imageSrc = getScreenshot()
                        setImage(imageSrc)
                        setimghide("")
                    },5000);                    
                }}
            >
                Capture photo
            </button>
            
            </>
            )}
        </Webcam>
        <Form id="body-form" >
            <input type="number" placeholder='Enter your Height in cms' onChange={(e)=>{
                setHeight(e.target.value)
                console.log(height)
            }}/>
            <input type="file" name="inputfile" onChange={(e)=>{
                setImage(e.target.value)
            }}/>
            <button
                className='btn btn-success'
                onClick={handleSubmit}
                >
                Submit photo
            </button>
        </Form>
        
        <img 
            src={image} 
            alt="captured pic"
            hidden={imghide}/>            
      </>
    
  )
}

export default WebcamScreen