import {useEffect, useState} from 'react'
import axios from 'axios'
import {format} from 'date-fns'

import './App.css';

const baseUrl = "http://localhost:5000"

function App() {
  const [description, setDescription] = useState("")
  const [eventsList, setEventsList] = useState([])
  
  const fetchEvents = async () => {
    const data = await axios.get(`${baseUrl}/events`)
    console.log(data)
    const { event } = data.data
    setEventsList(event)
  }
  
  const handleChange = e => setDescription(e.target.value)

  const handleDelete = async id => {
    try {
      await axios.delete(`${baseUrl}/events/${id}`)
      const updatedList = eventsList.filter(event => event.id !== id)
      setEventsList(updatedList)
    } catch (err) {
      console.error(err.message)
    }
  }

  const handleSubmit = e => {
    e.preventDefault()
    console.log(description)
  }

  useEffect(() => {
    fetchEvents()
  }, [])
  
  return (
    <div className="App">
      <section>
        <form onSubmit={handleSubmit}>
          <label htmlFor="description">Description</label>
          <input
            onChange={handleChange}
            type="text"
            name="description"
            id="description"
            value={description}
          />
          <button type="submit">Submit</button>
        </form>
      </section>
      <section>
        <ul>
          {eventsList.map(event => {
            return (
              <li style={{display: "flex"}} key={event.id}>
                {event.description}
                <button onClick={() => handleDelete(event.id)}>x</button>
              </li>
              )
            })}
        </ul>
      </section>
    </div>
  );
}

export default App;
