import axios, { type AxiosRequestConfig, type AxiosResponse } from "axios";

const axiosInstance = axios.create({
  baseURL: `http://${import.meta.env.VITE_BE_IP}`,
  timeout: 0,
  headers: {
    "Content-Type": "application/json",
  },
});

export const fetch = async <TRequest, TResponse>(
  endpoint: string,
  parameters: TRequest,
) => {
  const config: AxiosRequestConfig = {
    params: parameters,
  };
  const response = (await axiosInstance.get<TResponse>(
    endpoint,
    config,
  )) as AxiosResponse<TResponse>;

  return response.data;
};
