import { useEffect } from "react";

export const useKafkaWebsocket = (onMessage: (msg: string) => void) => {
  useEffect(() => {
    const socket = new WebSocket(`ws://${import.meta.env.VITE_BE_IP}/ws`);

    socket.onopen = () => console.log("Connected to Kafka WebSocket");
    socket.onmessage = (event) => onMessage(event.data);
    socket.onclose = () => console.log("WebSocket disconnected");

    return () => {
      socket.close();
    };
  }, [onMessage]);
};
