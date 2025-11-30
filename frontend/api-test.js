// Simple API test to verify connections
import api from './src/services/api';

async function testAPIConnections() {
  console.log('Testing API connections...');
  
  try {
    // Test public hospital search
    console.log('Testing public hospital search...');
    const searchResult = await api.public.searchHospitals({});
    console.log('Hospital search result:', searchResult.data);
    
    // Test getting all hospitals
    console.log('Testing get all hospitals...');
    const hospitalsResult = await api.hospital.getAllHospitals();
    console.log('Hospitals result:', hospitalsResult.data);
    
    // Test getting hospital levels
    console.log('Testing get hospital levels...');
    const levelsResult = await api.hospitalLevel.getAllLevels();
    console.log('Levels result:', levelsResult.data);
    
    // Test getting departments
    console.log('Testing get departments...');
    const departmentsResult = await api.department.getAllDepartments();
    console.log('Departments result:', departmentsResult.data);
    
    // Test getting all staff
    console.log('Testing get all staff...');
    const staffResult = await api.staff.getAllStaffs();
    console.log('Staff result:', staffResult.data);
    
    // Test getting all events
    console.log('Testing get all events...');
    const eventsResult = await api.event.getAllEvents();
    console.log('Events result:', eventsResult.data);
    
    console.log('All API tests completed successfully!');
  } catch (error) {
    console.error('API test error:', error.message);
    console.error('Error details:', error.response?.data || error);
  }
}

// Run the test
testAPIConnections();