import { useEffect } from "react";
import { useDispatch } from "react-redux";
import type { AppDispatch } from "../shared/store.ts";
import { updateGameProcessStatus } from "../shared";

export const useKafkaWebsocket = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    const socket = new WebSocket(`ws://${import.meta.env.VITE_BE_IP}/ws`);

    socket.onopen = () => console.log("Connected to Kafka WebSocket");
    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { gameId, type, status } = message;
        if (gameId && type && status) {
          dispatch(updateGameProcessStatus({ gameId, type, status }));
        } else {
          console.error("Invalid message format");
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    socket.onclose = () => console.log("WebSocket disconnected");

    return () => {
      socket.close();
    };
  }, [dispatch]);
};
