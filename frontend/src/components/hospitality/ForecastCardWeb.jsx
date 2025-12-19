import React, {useEffect, useState} from 'react'

export default function ForecastCardWeb({propertyId=1, role='housekeeping'}){
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedDate, setSelectedDate] = useState(null)
  const [overrideValue, setOverrideValue] = useState('')

  useEffect(()=>{ fetchForecast() }, [])

  async function fetchForecast(){
    setLoading(true)
    const today = new Date().toISOString().slice(0,10)
    try{
      const res = await fetch(`/api/v1/forecast/forecast?property_id=${propertyId}&start_date=${today}&horizon=7&role=${role}`)
      const data = await res.json()
      setPredictions(data.predictions || [])
    }catch(e){ console.warn(e) }
    setLoading(false)
  }

  async function saveOverride(){
    if(!selectedDate) return
    const payload = { property_id: propertyId, role, date: selectedDate, override_value: Number(overrideValue) }
    try{
      const res = await fetch('/api/v1/forecast/override', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) })
      const json = await res.json()
      setPredictions(p => p.map(pt => pt.date === selectedDate ? {...pt, predicted: Number(overrideValue)} : pt))
      setSelectedDate(null)
      setOverrideValue('')
    }catch(e){ console.warn(e) }
  }

  return (
    <div style={{padding:12, background:'#fff', borderRadius:8}}>
      <h3>7-day staff forecast — {role}</h3>
      {loading && <div>Loading…</div>}
      <table style={{width:'100%'}}>
        <thead><tr><th>Date</th><th>Predicted</th><th>Range</th><th>Action</th></tr></thead>
        <tbody>
          {predictions.map(item => (
            <tr key={item.date}>
              <td>{item.date}</td>
              <td>{Math.round(item.predicted)}</td>
              <td>[{Math.round(item.lower)} - {Math.round(item.upper)}]</td>
              <td><button onClick={()=>{ setSelectedDate(item.date); setOverrideValue(Math.round(item.predicted)) }}>Override</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedDate && (
        <div style={{marginTop:12}}>
          <div>Override for {selectedDate}</div>
          <input type='number' value={overrideValue} onChange={e=>setOverrideValue(e.target.value)} />
          <button onClick={saveOverride}>Save Override</button>
        </div>
      )}
    </div>
  )
}