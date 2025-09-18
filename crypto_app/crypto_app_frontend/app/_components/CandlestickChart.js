import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Dimensions } from 'react-native';
import { CandlestickChart } from 'react-native-wagmi-charts';
import { MotiView } from 'moti';

const CandlestickChartComponent = ({ symbol, days }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://25.56.145.23:8000/api/v1/cryptocurrencies/history/by_symbol/${symbol}?dias=${days}`);
        const json = await response.json();

        if (response.ok) {
          // wagmi-charts usa `timestamp`, `open`, `high`, `low`, `close`
          const chartData = json.map(item => ({
            timestamp: new Date(item.timestamp).getTime(),
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
          }));
          setData(chartData);
        } else {
          throw new Error(json.detail || 'Failed to fetch data');
        }
      } catch (e) {
        setError(e.message);
        console.error("Error fetching data:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [symbol, days]);

  if (loading) {
    return <ActivityIndicator size="large" color="#00ffff" style={styles.loading} />;
  }

  if (error) {
    return <Text style={styles.errorText}>Error: {error}</Text>;
  }

  if (data.length === 0) {
    return <Text style={styles.noDataText}>No hay datos disponibles.</Text>;
  }

  return (
    <MotiView from={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ type: 'timing', duration: 300 }}>
      <CandlestickChart.Provider data={data}>
        <CandlestickChart width={Dimensions.get('window').width * 0.9} height={200}>
          <CandlestickChart.Candles />
          <CandlestickChart.Crosshair />
        </CandlestickChart>
      </CandlestickChart.Provider>
    </MotiView>
  );
};

const styles = StyleSheet.create({
  loading: {
    marginTop: 50,
  },
  errorText: {
    color: 'red',
    textAlign: 'center',
    marginTop: 20,
  },
  noDataText: {
    color: '#fff',
    textAlign: 'center',
    marginTop: 20,
  },
});

export default CandlestickChartComponent;