import React, {useEffect, useState} from 'react'

export default function ForecastAdmin(){
  const [models, setModels] = useState([])

  useEffect(()=>{ fetchModels() }, [])
  async function fetchModels(){
    try{
      const res = await fetch('/api/v1/admin/forecast/models')
      const data = await res.json()
      setModels(data.models || [])
    }catch(e){console.warn(e)}
  }

  return (
    <div style={{padding:12, background:'#fff', borderRadius:8}}>
      <h3>Forecast Models</h3>
      <table style={{width:'100%'}}>
        <thead><tr><th>ID</th><th>Property</th><th>Role</th><th>Type</th><th>Trained</th></tr></thead>
        <tbody>
          {models.map(m => (
            <tr key={m.id}><td>{m.id}</td><td>{m.property_id}</td><td>{m.role}</td><td>{m.model_type}</td><td>{m.created_at}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}