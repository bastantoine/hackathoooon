import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const apiUrl = 'http://127.0.0.1:5000/covid';
  let data = "test";
  fetch(apiUrl)
      .then((response) => response.json())
      .then((response_data) => {
        console.log('nouvellesHospitalisations', response_data.nouvellesHospitalisations);
        data = response_data;
      });
    return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          <img src="https://i.kym-cdn.com/entries/icons/original/000/029/079/hellothere.jpg" alt="hello there!" />
          <br/>
          Hello there !
        </p>
        <div className="covid">
          <p className="covidH">{data}</p>
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
