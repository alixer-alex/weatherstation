import logo from './logo.svg';
import React,{useState, useEffect} from 'react';
import './App.css';

function App() {
  const [currentTemp, setCurrentTemp]= useState(0);
  useEffect(()=>{
    fetch('/weather').then(res=>res.json().then(data=>{
      setCurrentTemp(data.temp);
    }))
  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p> The current temperature at great neck new york is {currentTemp}</p>
      </header>
    </div>
  );
}

export default App;
