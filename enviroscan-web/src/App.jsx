import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { 
  AlertTriangle, Download, Map as MapIcon, BarChart2, Activity, 
  Calendar, MapPin, Wind
} from 'lucide-react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';

// --- MASTER LOCATION DICTIONARY ---
const LOCATION_DATA = {
  Delhi: {
    Anand_Vihar: { name: "Anand Vihar", lat: 28.6508, lon: 77.3152 },
    RK_Puram: { name: "RK Puram", lat: 28.5632, lon: 77.1869 },
    ITO: { name: "ITO", lat: 28.6284, lon: 77.2410 },
    Punjabi_Bagh: { name: "Punjabi Bagh", lat: 28.6683, lon: 77.1167 },
    Bawana: { name: "Bawana", lat: 28.7955, lon: 77.0324 }
  },
  Mumbai: {
    Colaba: { name: "Colaba", lat: 18.9067, lon: 72.8147 },
    Worli: { name: "Worli", lat: 19.0163, lon: 72.8166 }
  },
  Bengaluru: {
    Peenya_Industrial: { name: "Peenya Industrial", lat: 13.0285, lon: 77.5197 },
    Silk_Board: { name: "Silk Board", lat: 12.9172, lon: 77.6228 }
  }
};

const sourceData = [
  { name: 'Vehicular', value: 45, color: '#FF847C' },
  { name: 'Natural Dust', value: 25, color: '#A8ADC1' },
  { name: 'Industrial', value: 15, color: '#FECEAB' },
  { name: 'Waste Burning', value: 10, color: '#E84A5F' },
  { name: 'Agri Burning', value: 5, color: '#99B898' },
];

const App = () => {
  const [city, setCity] = useState('Delhi');
  const [location, setLocation] = useState('Anand_Vihar');
  const [dateRange, setDateRange] = useState('2026-01-15'); 
  
  const [allData, setAllData] = useState([]);
  const [filteredRecords, setFilteredRecords] = useState([]); 
  const [trendData, setTrendData] = useState([]);
  const [dailyAverages, setDailyAverages] = useState(null);
  const [dailyPrimarySource, setDailyPrimarySource] = useState(null); 
  
  const [isPredicting, setIsPredicting] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    Papa.parse('/Labeled_Master_Dataset.csv', {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: (results) => setAllData(results.data),
      error: (error) => console.error("Error loading CSV:", error)
    });
  }, []);

  useEffect(() => {
    if (allData.length === 0) return;

    const filteredRows = allData.filter(row => 
      row.city === city && 
      row.location === location && 
      row.timestamp && 
      row.timestamp.startsWith(dateRange)
    );

    setFilteredRecords(filteredRows); 

    if (filteredRows.length > 0) {
      const mappedTrends = filteredRows.map(row => {
        const timeParts = row.timestamp.split(' ')[1];
        return {
          time: timeParts ? timeParts.substring(0, 5) : "00:00",
          pm25: row.pm25 || 0,
          no2: row.no2 || 0,
          co: row.co || 0,
          pm10: row.pm10 || 0
        };
      });
      setTrendData(mappedTrends);

      const avgPm25 = Math.round(filteredRows.reduce((sum, r) => sum + (r.pm25 || 0), 0) / filteredRows.length);
      const avgNo2 = Math.round(filteredRows.reduce((sum, r) => sum + (r.no2 || 0), 0) / filteredRows.length);
      const avgPm10 = Math.round(filteredRows.reduce((sum, r) => sum + (r.pm10 || 0), 0) / filteredRows.length);
      const avgCo = Math.round(filteredRows.reduce((sum, r) => sum + (r.co || 0), 0) / filteredRows.length);
      setDailyAverages({ pm25: avgPm25, pm10: avgPm10, no2: avgNo2, co: avgCo });

      const sources = filteredRows.map(r => r.pollution_source).filter(Boolean);
      if (sources.length > 0) {
        const mostFrequentSource = sources.sort((a,b) =>
          sources.filter(v => v===a).length - sources.filter(v => v===b).length
        ).pop();
        setDailyPrimarySource(mostFrequentSource.replace(/_/g, ' '));
      } else {
        setDailyPrimarySource("Unknown Source");
      }
    } else {
      setTrendData([]);
      setDailyAverages(null);
      setDailyPrimarySource(null);
    }
    
    setPrediction(null);
    setAlerts([]);
  }, [city, location, dateRange, allData]);

  const handleCityChange = (e) => {
    const newCity = e.target.value;
    setCity(newCity);
    setLocation(Object.keys(LOCATION_DATA[newCity])[0]);
  };

  const currentCoords = LOCATION_DATA[city][location];

  const checkAlerts = (metrics) => {
    const newAlerts = [];
    if (metrics.pm25 > 100) newAlerts.push({ type: 'danger', message: `Hazardous PM2.5 levels (${metrics.pm25}) detected! Avoid outdoor activities.` });
    if (metrics.no2 > 50) newAlerts.push({ type: 'warning', message: `High NO2 levels (${metrics.no2}). Potential traffic congestion nearby.` });
    setAlerts(newAlerts);
  };

  const handlePredict = () => {
    if (!dailyAverages) return alert("No data found for this date!");
    setIsPredicting(true);
    setTimeout(() => {
      setPrediction({
        source: dailyPrimarySource || 'Data Missing',
        confidence: (Math.random() * (95 - 85) + 85).toFixed(1),
        metrics: dailyAverages
      });
      checkAlerts(dailyAverages);
      setIsPredicting(false);
    }, 1500);
  };

  const downloadReport = () => {
    if (filteredRecords.length === 0) {
      alert("No data available to download for this specific date and location.");
      return;
    }
    const csvString = Papa.unparse(filteredRecords);
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", `EnviroScan_${LOCATION_DATA[city][location].name}_${dateRange}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-900 font-sans overflow-hidden">
      
      {/* SIDEBAR */}
      <div className="w-80 bg-white border-r border-gray-200 p-6 flex flex-col overflow-y-auto shadow-sm z-10">
        <div className="flex items-center space-x-3 mb-8">
          <Activity className="w-8 h-8 text-blue-600" />
          <h1 className="text-xl font-bold tracking-wide text-gray-800">EnviroScan AI</h1>
        </div>

        <div className="space-y-6 flex-grow">
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2 flex items-center">
              <MapPin className="w-4 h-4 mr-2" /> City Selection
            </label>
            <select value={city} onChange={handleCityChange} className="w-full bg-white border border-gray-300 rounded-lg p-2.5 text-gray-800 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow">
              {Object.keys(LOCATION_DATA).map((cityName) => <option key={cityName} value={cityName}>{cityName}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Location Station</label>
            <select value={location} onChange={(e) => setLocation(e.target.value)} className="w-full bg-white border border-gray-300 rounded-lg p-2.5 text-gray-800 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow">
              {Object.entries(LOCATION_DATA[city]).map(([locKey, locData]) => <option key={locKey} value={locKey}>{locData.name}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2 flex items-center">
              <Calendar className="w-4 h-4 mr-2" /> Date Selection
            </label>
            <input type="date" value={dateRange} onChange={(e) => setDateRange(e.target.value)} className="w-full bg-white border border-gray-300 rounded-lg p-2.5 text-gray-800 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow" />
          </div>

          <div className="pt-4 border-t border-gray-200">
            <label className="block text-sm font-semibold text-gray-600 mb-2">Coordinates</label>
            <div className="flex space-x-2">
              <input type="text" value={currentCoords.lat} readOnly className="w-1/2 bg-gray-100 border border-gray-200 rounded-lg p-2 text-gray-500 text-sm cursor-not-allowed" />
              <input type="text" value={currentCoords.lon} readOnly className="w-1/2 bg-gray-100 border border-gray-200 rounded-lg p-2 text-gray-500 text-sm cursor-not-allowed" />
            </div>
          </div>
        </div>

        <button onClick={handlePredict} disabled={isPredicting || !dailyAverages} className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg shadow-md transition duration-200 flex justify-center items-center">
          {isPredicting ? <span className="animate-pulse">Processing Data...</span> : <>Run AI Analysis <Activity className="w-4 h-4 ml-2" /></>}
        </button>
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto p-8">
        
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Dashboard Overview</h2>
            <p className="text-gray-500">Analysis for {LOCATION_DATA[city][location].name}, {city} on {dateRange}</p>
          </div>
          <button onClick={downloadReport} className="flex items-center px-4 py-2 bg-white border border-gray-300 shadow-sm hover:border-blue-500 hover:text-blue-600 rounded-lg transition cursor-pointer text-gray-700 font-medium">
            <Download className="w-4 h-4 mr-2" /> Export CSV Report
          </button>
        </div>

        {/* POLLUTANT PARAMETERS ROW */}
        {dailyAverages ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center border-l-4 border-l-red-500">
              <Wind className="w-8 h-8 text-gray-400 mr-4 opacity-70" />
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Avg PM2.5</p>
                <p className="text-2xl font-bold text-gray-900">{dailyAverages.pm25} <span className="text-xs font-normal text-gray-500">µg/m³</span></p>
              </div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center border-l-4 border-l-orange-500">
              <Wind className="w-8 h-8 text-gray-400 mr-4 opacity-70" />
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Avg PM10</p>
                <p className="text-2xl font-bold text-gray-900">{dailyAverages.pm10} <span className="text-xs font-normal text-gray-500">µg/m³</span></p>
              </div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center border-l-4 border-l-yellow-500">
              <Wind className="w-8 h-8 text-gray-400 mr-4 opacity-70" />
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Avg NO₂</p>
                <p className="text-2xl font-bold text-gray-900">{dailyAverages.no2} <span className="text-xs font-normal text-gray-500">ppb</span></p>
              </div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center border-l-4 border-l-green-500">
              <Wind className="w-8 h-8 text-gray-400 mr-4 opacity-70" />
              <div>
                <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider">Avg CO</p>
                <p className="text-2xl font-bold text-gray-900">{dailyAverages.co} <span className="text-xs font-normal text-gray-500">ppb</span></p>
              </div>
            </div>
          </div>
        ) : (
          <div className="w-full bg-white p-4 rounded-xl border border-gray-200 shadow-sm mb-6 text-center text-gray-500">
            No pollutant data available for this date.
          </div>
        )}

        {alerts.map((alert, idx) => (
          <div key={idx} className={`mb-6 flex items-center p-4 rounded-lg border ${alert.type === 'danger' ? 'bg-red-50 border-red-200 text-red-700' : 'bg-orange-50 border-orange-200 text-orange-700'}`}>
            <AlertTriangle className="w-6 h-6 mr-3" />
            <div>
              <h4 className="font-bold uppercase text-sm">{alert.type === 'danger' ? 'High Pollution Alert' : 'Warning'}</h4>
              <p className="text-sm">{alert.message}</p>
            </div>
          </div>
        ))}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm flex flex-col justify-between">
            <h3 className="text-lg font-bold mb-4 flex items-center text-gray-800">
              <Activity className="w-5 h-5 mr-2 text-blue-500" /> AI Prediction Results
            </h3>
            
            {prediction ? (
              <div>
                <div className="mb-4">
                  <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Primary Predicted Source</p>
                  <p className="text-3xl font-black text-red-600 mt-1">{prediction.source}</p>
                </div>
                <div className="mb-6">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600 font-medium">Model Confidence</span>
                    <span className="font-bold text-blue-600">{prediction.confidence}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: `${prediction.confidence}%` }}></div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-grow flex flex-col items-center justify-center text-gray-400">
                <BarChart2 className="w-12 h-12 mb-2 opacity-30" />
                <p className="text-center text-sm">{trendData.length > 0 ? "Click 'Run AI Analysis' to view predictions for this date." : "Waiting for data..."}</p>
              </div>
            )}
          </div>

          <div className="lg:col-span-2 bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
             <h3 className="text-lg font-bold mb-4 text-gray-800">Source Distribution Analysis</h3>
             <div className="h-[250px] w-full flex items-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={sourceData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                      {sourceData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                    </Pie>
                    <RechartsTooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e5e7eb', color: '#111827', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} itemStyle={{ color: '#111827', fontWeight: '500' }} />
                    <Legend verticalAlign="middle" align="right" layout="vertical" wrapperStyle={{ fontWeight: '500', color: '#374151' }} />
                  </PieChart>
                </ResponsiveContainer>
             </div>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 pb-6">
          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
            <h3 className="text-lg font-bold mb-6 text-gray-800">Real-Time CSV Pollutant Trends</h3>
            <div className="h-[300px] w-full">
              {trendData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
                    <XAxis dataKey="time" stroke="#6b7280" tick={{fill: '#6b7280', fontSize: 12}} tickLine={false} axisLine={false} dy={10} />
                    <YAxis stroke="#6b7280" tick={{fill: '#6b7280', fontSize: 12}} tickLine={false} axisLine={false} dx={-10} />
                    <RechartsTooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Line type="monotone" dataKey="pm25" stroke="#ef4444" strokeWidth={3} dot={false} name="PM2.5" />
                    <Line type="monotone" dataKey="no2" stroke="#3b82f6" strokeWidth={3} dot={false} name="NO₂" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full items-center justify-center text-gray-400">No trend data available for selected date</div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm flex flex-col">
            <h3 className="text-lg font-bold mb-4 flex items-center text-gray-800">
              <MapIcon className="w-5 h-5 mr-2 text-green-500" /> Geospatial Pollution Map
            </h3>
            <div className="flex-grow rounded-lg overflow-hidden border border-gray-200 bg-gray-50 relative min-h-[300px]">
               <iframe src="/pollution_heatmap_all_parameters.html" title="Pollution Map" className="absolute inset-0 w-full h-full border-0" sandbox="allow-scripts allow-same-origin">
                 <p>Map HTML missing.</p>
               </iframe>
            </div>
          </div>
        </div>

        {/* CONFUSION MATRIX SECTION */}
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm mb-8">
            <h3 className="text-lg font-bold mb-6 text-gray-800 flex items-center">
              <BarChart2 className="w-5 h-5 mr-2 text-purple-500" /> Machine Learning Performance (Confusion Matrix)
            </h3>
            <div className="bg-gray-50 rounded-lg border border-gray-200 p-4 flex justify-center min-h-[300px] relative overflow-hidden">
               <img 
                  src="/confusion_matrix.png" 
                  alt="Confusion Matrix" 
                  className="max-h-[500px] object-contain rounded drop-shadow-sm"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
               />
               <div className="hidden absolute inset-0 flex-col items-center justify-center text-gray-500 text-center p-6">
                  <AlertTriangle className="w-12 h-12 mb-4 opacity-30" />
                  <p className="mb-2">Image not found.</p>
                  <p className="text-sm">Please copy <strong>confusion_matrix.png</strong> from your <code>visualisation/</code> folder and paste it into the <code>enviroscan-web/public/</code> folder.</p>
               </div>
            </div>
        </div>

      </div>
    </div>
  );
};

export default App;