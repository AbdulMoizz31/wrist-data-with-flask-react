import { useState, useEffect } from "react";
import Plot from "react-plotly.js";

const ChartWithNotes = () => {
  const [selectedDate, setSelectedDate] = useState("2021-09-10");
  const [chartData, setChartData] = useState(null);
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    if (selectedDate) {
      fetch(`http://127.0.0.1:5000/data?date=${selectedDate}`)
        .then((response) => response.json())
        .then((data) => {
          //console.log(data);
          
          setChartData(data.chart);
          setNotes(data.notes);
        })
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, [selectedDate]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Wrist Wearable Data Monitor</h1>
      <label>
        Select Date:
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
        />
      </label>

      {chartData && (
        <Plot
          data={[
            {
              x: chartData.x,
              y: chartData.y,
              type: "scatter",
              mode: "lines",
              marker: { color: "blue" },
            },
          ]}
          layout={{
            title: "Heart Rate",
            // annotations: chartData.annotations.map((ann) => ({
            //   x: ann.time,
            //   y: 0,
            //   text: ann.emoji,
            //   showarrow: false,
            // })),
          }}
        />
      )}

      <ul>
        {notes.map((note, index) => (
          <li key={index}>
            <strong>{note.time}</strong>: {note.text} {note.emoji}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChartWithNotes;
