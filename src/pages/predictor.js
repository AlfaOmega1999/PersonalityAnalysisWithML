
import React, { useEffect, useState } from 'react';
import FastAPIClient from 'C:/Users/luisf/Escritorio/PersonalityAnalysisWithML/src/client.js';
import config from 'C:/Users/luisf/Escritorio/PersonalityAnalysisWithML/src/config.js';
//import Loader from '../../components/Loader';

const client = new FastAPIClient(config);

const Predictor = () => {
  //const [loading, setLoading] = useState(true)
  const [personality, setPersonality] = useState([])

  useEffect(() => {
  }, [])

  const Predict = (msg) => {
    client.getPrediction(msg).then((data) => {
      //setLoading(false)

      // SET THE RECIPIES DATA
      setPersonality(data?.results)
    });
  } 

  /*if (loading)
       return <Loader />*/
  return (
    <header id="home">
      <div>
        <br />
        <br />
        <br />

        <textarea placeholder="Escribe tu mensaje aquí..." id="text" name="text" rows="8"></textarea>  
        <br />
        <input id="button" type="submit" value="Predecir" onClick={() => Predict("hello this is a test msg")}></input>
        <h1>{personality}</h1> 

      </div>
    </header>
  );
};

export default Predictor;