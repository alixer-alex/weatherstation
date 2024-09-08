
import React,{useState, useEffect} from 'react';
import './App.css';



function App() {
  const [currentTemp, setCurrentTemp]= useState(0);
  const [currentLoc, setCurrentLoc] = useState("Great Neck New York");
  const onChange=(e) => {
    e.preventDefault();
    setCurrentLoc(e.target.location.value);
  };
  useEffect(()=>{
    setCurrentTemp(0);
    fetch('/api/weather?location='+ currentLoc)
  .then(res=>res.json()
  .then(data=>{
    
    setCurrentTemp(data.temp);
  }))}
  ,[currentLoc])



  return (
    <>
    <a className="me" href="https://tenors-website.vercel.app/">Me</a>
    <div>
      <form className="input" onSubmit={(e)=>onChange(e)}> 
        <label htmlFor="Location">Location:</label><br/>
        <input type="text" name="location"/>
        <input className="butto" type="submit" value="Submit." />
      </form>

    </div>
    <div className="weather"> 
      <p> The highest temp in {currentLoc} in the next 24 hours is {currentTemp} F</p>
    </div>
    </>  
  );
}

export default App;
