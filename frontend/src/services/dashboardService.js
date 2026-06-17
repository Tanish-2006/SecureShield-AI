import api from "../api/axios";

export const getDashboard = async (projectId) => {
  const response = await api.get(`/dashboard/stats/${projectId}`);
  return response.data;
};