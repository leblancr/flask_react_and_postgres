import {useEffect, useState} from 'react'
import axios from 'axios'
//import {format} from 'date-fns'
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import InputField from './InputField'; // Import your InputField component

const baseUrl = "http://localhost:5000"

function App() {
  const [description, setDescription] = useState("")
  const [editDescription, setEditDescription] = useState("")
  const [eventsList, setEventsList] = useState([])
  const [eventId, setEventId] = useState(null)
  
  const fetchEvents = async () => {
    const data = await axios.get(`${baseUrl}/events`)
    console.log(data)
    const { events } = data.data
    setEventsList(events)
  }
  
  const handleChange = (e, field) => {
    if (field === 'edit') {
      setEditDescription(e.target.value)
    }else{
      setDescription(e.target.value)
    }
  }

  const handleDelete = async id => {
    try {
      await axios.delete(`${baseUrl}/events/${id}`)
      const updatedList = eventsList.filter(event => event.id !== id)
      setEventsList(updatedList)
    } catch (err) {
      console.error(err.message)
    }
  }

  const toggleEdit = event => {
    setEventId(event.id)
    setEditDescription(event.description)
  }

  const handleSubmit = async e => {
    e.preventDefault()
    try {
      if (editDescription) {
        const data = await axios.put(`${baseUrl}/events/${eventId}`, {'description': editDescription})
        const updatedEvent = data.data.event
        const updatedList = eventsList.map(event => {
          if (event.id === eventId) {
            return event = updatedEvent
          }
          return event
        })
        setEventsList(updatedList)
      } else {
        const data = await axios.post(`${baseUrl}/events`, {description})
        setEventsList([...eventsList, data.data])
      }
      setDescription('')
      setEditDescription('')
      setEventId(null)
    }catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchEvents()
  }, [])
  
  return (
    <div className="App" style={{ backgroundColor: '#000', color: '#fff', minHeight: '100vh' }}>
      <section>
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <label htmlFor="description" style={{ marginBottom: '10px' }}>Description:</label>
          <div style={{ display: "flex", flexDirection: "row", alignItems: "center", marginBottom: '10px' }}>
            {/*<input*/}
            {/*  onChange={e => handleChange(e, 'description')}*/}
            {/*  type="text"*/}
            {/*  name="description"*/}
            {/*  id="description"*/}
            {/*  placeholder="Describe the task"*/}
            {/*  value={description}*/}
            {/*  style={{ flex: 1, padding: '8px', marginRight: '10px', fontSize: '14px' }}*/}
            {/*/>*/}
            <InputField
              value={description}
              onChange={(e) => handleChange(e, 'description')}
              placeholder="Describe the task"
            />
            <Button variant="outline-success" type="submit" style={{ minWidth: '80px' }}>Submit</Button>
          </div>
        </form>
      </section>
      <section>
        <ul>
          {eventsList.map(event => {
            if (eventId === event.id){
              return (
                <li>
                <form onSubmit={handleSubmit} key={event.id} style={{ display: "flex", alignItems: "center", flexDirection: "row"  }}>
                  <input
                    onChange={e => handleChange(e, 'edit')}
                    type="text"
                    name="editDescription"
                    id="editDescription"
                    value={editDescription}
                    style={{ flex: 1, marginRight: '10px' }}
                  />
                  <Button variant="outline-primary" type="submit">Submit</Button>
                </form>
                </li>
                )
            }else {
              return (
                <li className="listItem" key={event.id}>
                  {/*<button onClick={() => toggleEdit(event)}>Edit</button>*/}
                  {!editDescription && <Button variant="outline-primary" onClick={() => toggleEdit(event)}>Edit</Button>}
                  <span style={{ marginLeft: '20px' }}></span>
                  <Button variant="outline-danger" onClick={() => handleDelete(event.id)}>Delete</Button>
                  {/*{!eventsList && <Button onClick={() => handleDelete(event.id)}>Delete</Button>}*/}
                  <span style={{ marginLeft: '20px' }}></span>
                  <div className="description">
                    <p style={{ paddingLeft: 0,  paddingTop: '14px', margin: 0 }}>{event.description}</p>
                  </div>
                </li>
                )
            }
          })}
        </ul>
      </section>
    </div>
  );
}

export default App;
