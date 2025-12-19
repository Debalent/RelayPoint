import React, {useEffect, useState} from 'react'

export default function CloudbedsMapping({propertyId=1}){
  const [rooms, setRooms] = useState([])
  const [mapping, setMapping] = useState({})

  useEffect(()=>{fetchRooms()}, [])
  async function fetchRooms(){
    // For PoC this will use a placeholder endpoint
    try{
      const res = await fetch(`/api/v1/integrations/cloudbeds/rooms?property_id=${propertyId}`)
      const data = await res.json()
      setRooms(data.rooms || [])
    }catch(e){console.warn(e)}
  }

  function saveMapping(cloudRoomId, propertyRoomId){
    setMapping(m => ({...m, [cloudRoomId]: propertyRoomId}))
    // TODO: POST mapping to API
  }

  return (
    <div style={{padding:12, background:'#fff', borderRadius:8}}>
      <h3>Cloudbeds Room Mapping (PoC)</h3>
      <table style={{width:'100%'}}>
        <thead><tr><th>Cloudbeds Room ID</th><th>Room Number</th><th>Map to Property Room</th></tr></thead>
        <tbody>
          {rooms.map(r => (
            <tr key={r.room_id}><td>{r.room_id}</td><td>{r.room_number}</td><td><input placeholder='Property Room ID' onBlur={e=>saveMapping(r.room_id,e.target.value)} /></td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}