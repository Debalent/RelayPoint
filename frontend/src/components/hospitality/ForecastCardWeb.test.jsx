import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import ForecastCardWeb from './ForecastCardWeb'

beforeEach(()=>{
  global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({ predictions: [ {date:'2025-12-20', predicted: 10, lower:8, upper:12} ] }) }))
})

test('renders forecast and allows override', async ()=>{
  render(<ForecastCardWeb propertyId={1} role={'housekeeping'} />)
  await waitFor(()=> expect(screen.getByText(/2025-12-20/)).toBeInTheDocument())
  expect(screen.getByText('10')).toBeInTheDocument()
  // Open override
  fireEvent.click(screen.getByText('Override'))
  fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '12' } })
  // Mock override POST
  global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({ id: 1, property_id: 1, role: 'housekeeping', date: '2025-12-20', override_value: 12 }) }))
  fireEvent.click(screen.getByText('Save Override'))
  await waitFor(()=> expect(screen.queryByText('Override for')).not.toBeInTheDocument())
})