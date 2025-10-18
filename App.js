import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

function App() {
  const [prices, setPrices] = useState([]);
  const [formData, setFormData] = useState({ date: "", foodPrice: "", fuelPrice: "" });

  useEffect(() => {
    axios.get("http://localhost:5000/prices").then(res => setPrices(res.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post("http://localhost:5000/prices", formData);
    const updated = await axios.get("http://localhost:5000/prices");
    setPrices(updated.data);
    setFormData({ date: "", foodPrice: "", fuelPrice: "" });
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">📊 Food vs Fuel Price Tracker</h1>

      <form onSubmit={handleSubmit} className="mb-6 flex gap-2">
        <input
          type="date"
          className="border p-2 flex-1"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Food Price"
          className="border p-2 flex-1"
          value={formData.foodPrice}
          onChange={(e) => setFormData({ ...formData, foodPrice: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Fuel Price"
          className="border p-2 flex-1"
          value={formData.fuelPrice}
          onChange={(e) => setFormData({ ...formData, fuelPrice: e.target.value })}
          required
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">Add</button>
      </form>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={prices}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="foodPrice" stroke="#82ca9d" name="Food Price" />
          <Line type="monotone" dataKey="fuelPrice" stroke="#8884d8" name="Fuel Price" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;