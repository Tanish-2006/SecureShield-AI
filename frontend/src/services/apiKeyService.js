import api from "../api/axios";

export const getApiKeys = async (projectId) => {
  const response = await api.get(`/api-keys/${projectId}`);
  return response.data;
};

export const createApiKey = async (data) => {
  const response = await api.post("/api-keys/", data);
  return response.data;
};