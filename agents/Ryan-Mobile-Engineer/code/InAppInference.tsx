import React, {useEffect, useState} from 'react';
import {View, Text, Button, ActivityIndicator} from 'react-native';

// This is a skeleton POC for wiring native on-device inference calls.
// Native modules must be implemented per-platform (Android/iOS) to actually
// load the model and run inference. This RN component demonstrates flow,
// timing capture, and basic UI for measurements.

type InferenceResult = {
  output: any;
  latencyMs: number;
};

const InAppInference: React.FC = () => {
  const [running, setRunning] = useState(false);
  const [warmLatencies, setWarmLatencies] = useState<number[]>([]);
  const [coldLatency, setColdLatency] = useState<number | null>(null);
  const [lastResult, setLastResult] = useState<any>(null);

  // Placeholder native bridge API names. Platforms should implement
  // NativeModules.InferenceModule.loadModel() and .runInference(input)
  const InferenceModule: any = (global as any).InferenceModule;

  useEffect(() => {
    // attempt to load model on mount
    (async () => {
      try {
        if (InferenceModule && InferenceModule.loadModel) {
          await InferenceModule.loadModel();
        }
      } catch (e) {
        console.warn('Model load failed:', e);
      }
    })();
  }, []);

  const runCold = async () => {
    if (!InferenceModule || !InferenceModule.runInference) {
      alert('Native inference module not available');
      return;
    }
    setRunning(true);
    const input = { /* sample input */ };
    const start = Date.now();
    try {
      const res = await InferenceModule.runInference(input, true); // true = cold
      const latency = Date.now() - start;
      setColdLatency(latency);
      setLastResult(res);
    } catch (e) {
      console.warn('Inference failed', e);
    } finally {
      setRunning(false);
    }
  };

  const runWarmOnce = async () => {
    if (!InferenceModule || !InferenceModule.runInference) {
      alert('Native inference module not available');
      return;
    }
    const input = { /* sample input */ };
    const start = Date.now();
    const res = await InferenceModule.runInference(input, false);
    const latency = Date.now() - start;
    setWarmLatencies(prev => [...prev, latency].slice(-50));
    setLastResult(res);
  };

  const runWarmLoop = async (count = 10, delayMs = 200) => {
    setRunning(true);
    for (let i = 0; i < count; i++) {
      await runWarmOnce();
      await new Promise(r => setTimeout(r, delayMs));
    }
    setRunning(false);
  };

  const avg = (arr: number[]) => (arr.length ? Math.round(arr.reduce((a,b)=>a+b,0)/arr.length) : 0);

  return (
    <View style={{flex:1, padding:16}}>
      <Text style={{fontSize:18, fontWeight:'600'}}>On-Device Inference POC</Text>
      <View style={{height:12}} />
      <Button title="Run Cold Inference" onPress={runCold} disabled={running} />
      <View style={{height:8}} />
      <Button title="Run Warm Once" onPress={runWarmOnce} disabled={running} />
      <View style={{height:8}} />
      <Button title="Run Warm Loop (10x)" onPress={() => runWarmLoop(10, 200)} disabled={running} />
      <View style={{height:12}} />
      {running && <ActivityIndicator />}

      <View style={{height:12}} />
      <Text>Cold Latency: {coldLatency ?? '-'} ms</Text>
      <Text>Warm Avg Latency: {avg(warmLatencies)} ms (n={warmLatencies.length})</Text>
      <Text>Last Result: {lastResult ? JSON.stringify(lastResult).slice(0,200) : '-'}</Text>
    </View>
  );
};

export default InAppInference;
