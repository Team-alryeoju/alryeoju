import React from 'react';
import { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState([{}])

  useEffect(() => 
    {fetch("/users").then(
      response => response.json()
    ).then(
      data => {
        setData(data);
      }
    ).catch((err) => console.log(err))
    }, [])

  return (
    <div className='App'>
      <h1>test 하는 중...</h1>
      <div>
        { (typeof data.users === 'undefined') ? (<p>loding...</p>) : (data.users.map((u) => <p key={u.id}>{u.name}</p>))}
      </div>
    </div>
  )
}

export default App;
