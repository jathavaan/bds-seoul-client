import axios, { type AxiosRequestConfig, type AxiosResponse } from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
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
