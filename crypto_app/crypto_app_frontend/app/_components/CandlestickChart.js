import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Dimensions } from 'react-native';
import { LineChart } from 'react-native-wagmi-charts';
import { MotiView } from 'moti';
import Constants from 'expo-constants';

const CandlestickChartComponent = ({ symbol, days }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = Constants.expoConfig.extra.API_URL;

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_URL}/api/v1/cryptocurrencies/history/by_symbol/${symbol}?dias=${days}`);
        const json = await response.json();

        if (response.ok) {
          // Adaptar los datos de tu API al formato requerido por la gráfica de líneas
          const chartData = json.map(item => ({
            timestamp: new Date(item.fecha).getTime(),
            value: item.valor,
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
    <MotiView
      from={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ type: 'timing', duration: 300 }}
    >
      <LineChart.Provider data={data}>
        <LineChart width={Dimensions.get('window').width * 0.9} height={200} backgroundColor="#000">
          <LineChart.Path color="#00ffff" />
          <LineChart.Cursor color="#00ffff">
            <LineChart.Tooltip textStyle={{ color: '#fff' }} />
          </LineChart.Cursor>
        </LineChart>
      </LineChart.Provider>
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