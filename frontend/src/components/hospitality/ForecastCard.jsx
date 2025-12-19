import React, {useEffect, useState} from 'react';
import { View, Text, Button, FlatList, TextInput, StyleSheet } from 'react-native';

export default function ForecastCard({propertyId, role='housekeeping'}){
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [overrideValue, setOverrideValue] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(()=>{
    fetchForecast();
  }, []);

  async function fetchForecast(){
    setLoading(true);
    const today = new Date().toISOString().slice(0,10);
    try{
      const res = await fetch(`/api/v1/forecast/forecast?property_id=${propertyId}&start_date=${today}&horizon=7&role=${role}`);
      const data = await res.json();
      setPredictions(data.predictions || []);
    }catch(e){
      console.warn('Failed to fetch forecast', e);
    }finally{setLoading(false)}
  }

  async function saveOverride(){
    if(!selectedDate || overrideValue==null) return;
    const payload = {property_id: propertyId, role, date: selectedDate, override_value: Number(overrideValue)};
    try{
      const res = await fetch('/api/v1/forecast/override', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)});
      const data = await res.json();
      // basic optimistic update
      setPredictions(p => p.map(pt=> pt.date===selectedDate ? {...pt, predicted: Number(overrideValue)} : pt));
      setOverrideValue(null);
      setSelectedDate(null);
    }catch(e){console.warn('Failed to save override', e)}
  }

  return (
    <View style={styles.card}>
      <Text style={styles.title}>7-day staff forecast — {role}</Text>
      {loading && <Text>Loading…</Text>}
      <FlatList
        data={predictions}
        keyExtractor={(item)=>item.date}
        renderItem={({item})=> (
          <View style={styles.row}>
            <Text style={styles.date}>{item.date}</Text>
            <Text style={styles.value}>{Math.round(item.predicted)}</Text>
            <Text style={styles.range}>[{Math.round(item.lower)} - {Math.round(item.upper)}]</Text>
            <Button title="Override" onPress={()=>{setSelectedDate(item.date); setOverrideValue(item.predicted)}} />
          </View>
        )}
      />

      {selectedDate && (
        <View style={styles.overrideBox}>
          <Text>Override for {selectedDate}</Text>
          <TextInput keyboardType='numeric' value={String(overrideValue)} onChangeText={t=>setOverrideValue(t)} style={styles.input} />
          <Button title="Save Override" onPress={saveOverride} />
        </View>
      )}

    </View>
  )
}

const styles = StyleSheet.create({
  card: { padding: 12, backgroundColor: '#fff', borderRadius: 8, shadowColor: '#000', shadowOpacity: 0.05 },
  title: { fontWeight: '700', marginBottom: 8 },
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 6 },
  date: { flex: 2 },
  value: { flex: 1, textAlign: 'center' },
  range: { flex: 2, textAlign: 'right' },
  overrideBox: { marginTop: 12 },
  input: { borderWidth: 1, padding: 8, marginVertical: 8 }
})