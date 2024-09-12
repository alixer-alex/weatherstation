
import React,{useState, useEffect} from 'react';
import './App.css';



function App() {
  const [currentF, setCurrentF] = useState(true)
  const [currentTemp, setCurrentTemp]= useState(0);
  const [currentTempMin, setCurrentTempMin]= useState(0);
  const [currentTempC, setCurrentTempC]= useState(0);
  const [currentTempCMin, setCurrentTempCMin]= useState(0);
  const [currentLoc, setCurrentLoc] = useState("Great Neck New York");


  const onChange=(e) => {
    e.preventDefault();
    setCurrentLoc(e.target.location.value);
  };
  useEffect(()=>{
    setCurrentTemp(360);
    setCurrentTempMin(365);
    setCurrentTempC(360);
    setCurrentTempCMin(365);
    fetch('/api/weather?location='+ currentLoc)
  .then(res=>res.json()
  .then(data=>{
    
    setCurrentTemp(data.temp);
    setCurrentTempMin(data.temp2);
    setCurrentTempC(data.tempc);
    setCurrentTempCMin(data.tempc2);
  }))}
  ,[currentLoc])


  function WeatherType (){
    if(currentF == true) 
      {
        return <div className="weather"> 
          <p> the highest temp in {currentLoc} in the next 24 hours is {currentTemp} F</p>
          <p> the lowest temp in {currentLoc} in the next 24 hours is {currentTempMin} F</p>
        </div>
      }
    else {
      return <div className="weather"> 
      <p> the highest temp in {currentLoc} in the next 24 hours is {currentTempC} non-american units (C)</p>
      <p> the lowest temp in {currentLoc} in the next 24 hours is {currentTempCMin} non-american units (C)</p>
    </div>
    }
  }

  function ButtonChange(){
    if(currentF == true) 
      {
        return <button className="canada" type="button" onClick={()=>setCurrentF(false)}> c </button>;
      }
    else{
        return <button className="canada" type="button" onClick={()=>setCurrentF(true)}> f </button>;
    }
  }

  return (
    <>
    <a className="me" href="https://tenors-website.vercel.app/">me</a>

    <ButtonChange/>
    <div>
      <form className="input" onSubmit={(e)=>onChange(e)}> 
        <label htmlFor="location">location:</label><br/>
        <input type="text" name="location"/>
        <input className="butto" type="submit" value="submit." />
      </form>

    </div>
    <WeatherType/>
    <iframe className="brat" src="https://open.spotify.com/embed/album/2lIZef4lzdvZkiiCzvPKj7?utm_source=generator" width="50%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </>  
  );
}

export default App;
